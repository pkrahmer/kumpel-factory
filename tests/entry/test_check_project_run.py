"""The project check command with `--run`: the settings, the live points and their report."""

import os
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import pytest
from pydantic import BaseModel, ConfigDict

from factory.entry import check_project
from factory.entry.check_project import main
from factory.hosting.adapters.git_cli import GitCli
from factory.machine.adapters.fake_images import FakeImages
from factory.machine.application.images import ImageBuild
from factory.machine.application.project_run import ProjectRun
from factory.machine.domain.stage_layer import STAGE_FILE
from factory.pipeline.domain.project_check import POINT_NAMES
from factory.shared.domain.settings import InstanceSettings
from support.project_check_support import committed_repository, installed_home, ready_files
from support.project_run_support import (
    GREEN_CHECK,
    GREEN_SYNC,
    Outcome,
    ScriptedContainerRuns,
    result,
)
from support.settings_support import BASE, CONTAINER

STATIC_LINES = [f"{name}: ok" for name in POINT_NAMES]
STAGE_FILE_TEXT = "ARG FACTORY_BASE\nFROM ${FACTORY_BASE}\nRUN true\n"
RED_LAST = "make: *** [Makefile:2: check] Error 2"


@dataclass(frozen=True)
class Fakes:
    """The fakes the patched wiring hands to the use case."""

    runs: ScriptedContainerRuns
    images: FakeImages


class Layout(BaseModel):
    """The folders of one run: the repositories and the two agent homes."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    ready: Path
    staged: Path
    faulty: Path
    home: Path
    other_home: Path
    empty_home: Path


@pytest.fixture
def layout(tmp_path: Path) -> Layout:
    """Three repositories and three agent homes: installed, installed elsewhere, empty."""
    empty_home = tmp_path / "empty-home"
    empty_home.mkdir()
    return Layout(
        ready=committed_repository(tmp_path / "ready", ready_files()),
        staged=committed_repository(
            tmp_path / "staged", ready_files({STAGE_FILE: STAGE_FILE_TEXT})
        ),
        faulty=committed_repository(
            tmp_path / "faulty", ready_files({"factory/feature-form.md": None})
        ),
        home=installed_home(tmp_path / "agent-home"),
        other_home=installed_home(tmp_path / "other-home"),
        empty_home=empty_home,
    )


def _set_settings(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, agent_home: Path, *, complete: bool = True
) -> None:
    for name in os.environ:
        if name.startswith("FACTORY_"):
            monkeypatch.delenv(name)
    image_file = tmp_path / "image-id"
    image_file.write_text("sha256:" + "a" * 12 + "\n", encoding="utf-8")
    environment = {
        **BASE,
        **CONTAINER,
        "FACTORY_WORKSPACE": str(tmp_path / "workspace"),
        "FACTORY_CHECKOUT": str(tmp_path / "instance-checkout"),
        "FACTORY_STATE": str(tmp_path / "state"),
        "FACTORY_IMAGE_ID_FILE": str(image_file),
        "FACTORY_CLAUDE_HOME": str(agent_home),
    }
    if not complete:
        del environment["FACTORY_REPOSITORY_URL"]
    for name, value in environment.items():
        monkeypatch.setenv(name, value)


def _patch_wiring(
    monkeypatch: pytest.MonkeyPatch,
    outcomes: list[Outcome] | None = None,
    build: ImageBuild | None = None,
) -> Fakes:
    runs = ScriptedContainerRuns(
        [result(GREEN_SYNC), result(GREEN_CHECK)] if outcomes is None else outcomes
    )
    images = FakeImages() if build is None else FakeImages(build_result=build)

    def build_project_run(settings: InstanceSettings) -> ProjectRun:
        assert settings.stage_image is not None
        return ProjectRun(
            images,
            containers=runs.at,
            git=GitCli,
            stage_image=settings.stage_image,
        )

    monkeypatch.setattr(check_project, "build_project_run", build_project_run)
    return Fakes(runs=runs, images=images)


def test_incomplete_settings_end_before_anything_runs(
    layout: Layout,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _set_settings(monkeypatch, tmp_path, layout.home, complete=False)
    fakes = _patch_wiring(monkeypatch)

    status = main(["--run", str(layout.ready)])

    captured = capsys.readouterr()
    assert status == 2
    assert captured.out == ""
    assert captured.err.startswith("cannot run: ")
    assert fakes.runs.runs == []
    assert fakes.images.builds == []


def test_a_static_fault_prints_what_the_command_prints_without_run(
    layout: Layout,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _set_settings(monkeypatch, tmp_path, layout.home)
    fakes = _patch_wiring(monkeypatch)
    without_run = main([str(layout.faulty)])
    expected = capsys.readouterr().out

    status = main(["--run", str(layout.faulty)])

    assert (without_run, status) == (1, 1)
    assert capsys.readouterr().out == expected
    assert fakes.runs.runs == []
    assert fakes.runs.workspaces == []
    assert fakes.images.builds == []


@dataclass(frozen=True)
class Case:
    """One run of the report: the repository, the fakes' outcomes, the lines and the status."""

    repository: str
    outcomes: list[Outcome]
    build: ImageBuild | None
    live_lines: list[str]
    verdict: str
    status: int


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            Case(
                "ready",
                [result(GREEN_SYNC), result(GREEN_CHECK)],
                None,
                ["image: ok", "sync: ok", "check: ok"],
                "project: ready",
                0,
            ),
            id="green",
        ),
        pytest.param(
            Case(
                "ready",
                [result(GREEN_SYNC), result(f"sync: green (1.0 s)\n{RED_LAST}\n", 2)],
                None,
                ["image: ok", "sync: ok", f"check: FAIL: exit status 2: {RED_LAST}"],
                "project: not ready (1 fault)",
                1,
            ),
            id="red-check",
        ),
        pytest.param(
            Case(
                "staged",
                [result(GREEN_SYNC), result(GREEN_CHECK)],
                ImageBuild(
                    passed=False,
                    duration=timedelta(seconds=2),
                    output_tail="step 1\nError: no curl",
                ),
                ["image: FAIL: the image does not build: Error: no curl"],
                "project: not ready (1 fault)",
                1,
            ),
            id="red-build",
        ),
    ],
)
def test_the_report_holds_the_live_points_that_ran(
    layout: Layout,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    case: Case,
) -> None:
    _set_settings(monkeypatch, tmp_path, layout.home)
    _patch_wiring(monkeypatch, case.outcomes, case.build)
    folder: Path = getattr(layout, case.repository)

    status = main(["--run", str(folder)])

    assert capsys.readouterr().out.splitlines() == [*STATIC_LINES, *case.live_lines, case.verdict]
    assert status == case.status


@pytest.mark.parametrize(
    "given", [pytest.param(False, id="from-settings"), pytest.param(True, id="from-option")]
)
def test_the_agents_point_reads_the_agent_home_of_the_run(
    layout: Layout,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    given: bool,
) -> None:
    settings_home = layout.empty_home if given else layout.home
    _set_settings(monkeypatch, tmp_path, settings_home)
    fakes = _patch_wiring(monkeypatch)
    option = ["--agent-home", str(layout.other_home)] if given else []

    status = main([*option, "--run", str(layout.ready)])

    lines = capsys.readouterr().out.splitlines()
    assert "agents: ok" in lines
    assert status == 0
    homes = (layout.home, layout.other_home, layout.empty_home)
    assert len(fakes.runs.runs) == 2
    for run in fakes.runs.runs:
        for mount in run.mounts:
            assert not any(
                Path(mount.source) == home or home in Path(mount.source).parents for home in homes
            )
