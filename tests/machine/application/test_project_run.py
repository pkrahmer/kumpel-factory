"""The live part of the conformance check: the image, the sync and the check in containers."""

from datetime import timedelta
from pathlib import Path

import pytest

from factory.hosting.adapters.git_cli import GitCli
from factory.machine.adapters.fake_images import FakeImages
from factory.machine.application.images import IMAGE_BUILD_TIME_LIMIT, ImageBuild
from factory.machine.application.project_run import ProjectRun
from factory.machine.domain.containers import (
    CA_BUNDLE_NAMES,
    WORK,
    WORK_CHECKOUT,
    WORK_HOME,
    extra_environment,
    read_only_at_own_path,
)
from factory.machine.domain.stage_layer import STAGE_FILE
from factory.pipeline.domain.pipeline_definition import PipelineDefinition
from factory.pipeline.domain.project_check import LIVE_POINT_NAMES, ProjectPoint
from factory.shared.domain.errors import ContainerError
from factory.shared.domain.settings import read_settings
from support.git_support import write_files
from support.project_check_support import committed_repository, ready_files
from support.project_run_support import (
    CHECK_MINUTES,
    GREEN_CHECK,
    GREEN_SYNC,
    NAMED_MAKEFILE,
    SYNC_MINUTES,
    Outcome,
    ScriptedContainerRuns,
    definition,
    result,
)
from support.settings_support import BASE, CONTAINER

STAGE_IMAGE = CONTAINER["FACTORY_STAGE_IMAGE"]
IMAGE_PATH = "/opt/tools/bin:/usr/bin:/bin"
STAGE_FILE_TEXT = "ARG FACTORY_BASE\nFROM ${FACTORY_BASE}\nRUN true\n"
FAILED_BUILD = ImageBuild(
    passed=False, duration=timedelta(seconds=3), output_tail="step 1\nError: no such package"
)


def _live(
    folder: Path,
    runs: ScriptedContainerRuns,
    images: FakeImages,
    pipeline: PipelineDefinition | None = None,
    *,
    environment: dict[str, str] | None = None,
    ca_bundle: Path | None = None,
) -> list[ProjectPoint]:
    project_run = ProjectRun(
        images,
        containers=runs.at,
        git=GitCli,
        stage_image=STAGE_IMAGE,
        extra_environment=environment or {},
        ca_bundle=ca_bundle,
    )
    return project_run.run(folder, pipeline or definition())


@pytest.fixture
def ready(tmp_path: Path) -> Path:
    """A ready repository without a stage file."""
    return committed_repository(tmp_path / "ready", ready_files())


@pytest.fixture
def staged(tmp_path: Path) -> Path:
    """A ready repository with a stage file."""
    return committed_repository(tmp_path / "staged", ready_files({STAGE_FILE: STAGE_FILE_TEXT}))


def test_live_points_of_a_ready_repository_without_a_stage_file(ready: Path) -> None:
    runs = ScriptedContainerRuns([result(GREEN_SYNC), result(GREEN_CHECK)])
    images = FakeImages(paths={STAGE_IMAGE: IMAGE_PATH})

    points = _live(ready, runs, images)

    assert LIVE_POINT_NAMES == ("image", "sync", "check")
    assert points == [ProjectPoint(name=name) for name in LIVE_POINT_NAMES]
    assert images.builds == []
    assert len(runs.runs) == 2
    assert all(run.environment["PATH"] == IMAGE_PATH for run in runs.runs)


@pytest.mark.parametrize("passed", [pytest.param(True, id="built"), pytest.param(False, id="red")])
def test_a_stage_file_is_built_under_the_check_tag(staged: Path, passed: bool) -> None:
    check_tag = f"{STAGE_IMAGE}-check"
    runs = ScriptedContainerRuns([result(GREEN_SYNC), result(GREEN_CHECK)])
    images = FakeImages(
        paths={check_tag: IMAGE_PATH},
        build_result=ImageBuild(passed=True, duration=timedelta(0), output_tail="")
        if passed
        else FAILED_BUILD,
    )

    points = _live(staged, runs, images)

    assert len(images.builds) == 1
    build = images.builds[0]
    assert (build.base, build.tag, build.time_limit) == (
        STAGE_IMAGE,
        check_tag,
        IMAGE_BUILD_TIME_LIMIT,
    )
    assert build.layer.text == STAGE_FILE_TEXT
    if passed:
        assert points == [ProjectPoint(name=name) for name in LIVE_POINT_NAMES]
        assert len(runs.runs) == 2
        assert all(run.environment["PATH"] == IMAGE_PATH for run in runs.runs)
    else:
        assert points == [
            ProjectPoint(name="image", faults=["the image does not build: Error: no such package"])
        ]
        assert runs.runs == []


@pytest.mark.parametrize(
    "make_file", [pytest.param(None, id="default"), pytest.param(NAMED_MAKEFILE, id="named")]
)
def test_the_sync_and_the_check_run_as_a_stage_runs_them(
    ready: Path, make_file: str | None
) -> None:
    runs = ScriptedContainerRuns([result(GREEN_SYNC), result(GREEN_CHECK)])

    _live(ready, runs, FakeImages(), definition(make_file=make_file))

    sync, check = runs.runs
    sync_words = " ".join(sync.command)
    check_words = " ".join(check.command)
    assert sync.working_directory == WORK
    assert WORK_CHECKOUT in sync_words
    assert "make" in sync_words
    assert "sync" in sync_words
    assert sync.time_limit == timedelta(minutes=SYNC_MINUTES)
    assert check.working_directory == WORK_CHECKOUT
    assert "make" in check.command
    assert "sync" in check_words
    assert "check" in check.command
    assert check.time_limit == timedelta(minutes=CHECK_MINUTES)
    for words in (sync_words, check_words):
        assert ("-f" in words and NAMED_MAKEFILE in words) is (make_file is not None)


_SYNC_LAST = "make: *** [Makefile:8: sync] Error 2"
_CHECK_LAST = "make: *** [Makefile:2: check] Error 2"


@pytest.mark.parametrize(
    ("outcomes", "point", "expected"),
    [
        pytest.param(
            [ContainerError("podman", "no such image")],
            "sync",
            "could not start: ",
            id="sync-not-started",
        ),
        pytest.param(
            [result("Resolved\n", None, timed_out=True)],
            "sync",
            f"timed out after {SYNC_MINUTES} min",
            id="sync-timed-out",
        ),
        pytest.param(
            [result(f"Resolved\n{_SYNC_LAST}\n", 2)],
            "sync",
            f"exit status 2: {_SYNC_LAST}",
            id="sync-red",
        ),
        pytest.param(
            [result("Resolved 3 packages\n")],
            "sync",
            'no line "sync: green (<seconds> s)"',
            id="sync-without-green-line",
        ),
        pytest.param(
            [result(GREEN_SYNC), ContainerError("podman", "no such image")],
            "check",
            "could not start: ",
            id="check-not-started",
        ),
        pytest.param(
            [result(GREEN_SYNC), result("lint: green (0.5 s)\n", None, timed_out=True)],
            "check",
            f"timed out after {CHECK_MINUTES} min",
            id="check-timed-out",
        ),
        pytest.param(
            [result(GREEN_SYNC), result(f"sync: green (1.0 s)\n{_CHECK_LAST}\n", 2)],
            "check",
            f"exit status 2: {_CHECK_LAST}",
            id="check-red",
        ),
        pytest.param(
            [result(GREEN_SYNC), result("sync: green (1.0 s)\nall done\n")],
            "check",
            'the last line is not "check: green": all done',
            id="check-without-green-line",
        ),
    ],
)
def test_faults_of_the_sync_and_the_check(
    ready: Path, outcomes: list[Outcome], point: str, expected: str
) -> None:
    runs = ScriptedContainerRuns(outcomes)

    points = _live(ready, runs, FakeImages())

    names = [each.name for each in points]
    assert names == list(LIVE_POINT_NAMES[: LIVE_POINT_NAMES.index(point) + 1])
    assert all(not each.faults for each in points[:-1])
    (fault,) = points[-1].faults
    if expected.endswith(": "):
        assert fault.startswith(expected)
        assert "no such image" in fault
    else:
        assert fault == expected
    assert len(runs.runs) == len(outcomes)


@pytest.mark.parametrize(
    "outcomes",
    [
        pytest.param([result(GREEN_SYNC), result(GREEN_CHECK)], id="green"),
        pytest.param([result(f"{_SYNC_LAST}\n", 2)], id="fault"),
        pytest.param([RuntimeError("the container broke")], id="exception"),
    ],
)
def test_the_work_folder_holds_the_commit_and_is_removed(
    tmp_path: Path, outcomes: list[Outcome]
) -> None:
    folder = committed_repository(tmp_path / "ready", ready_files())
    write_files(folder, {"README.md": "# Uncommitted\n", "src/new.py": "x = 1\n"})
    runs = ScriptedContainerRuns(outcomes)

    if isinstance(outcomes[-1], Exception):
        with pytest.raises(RuntimeError):
            _live(folder, runs, FakeImages())
    else:
        _live(folder, runs, FakeImages())

    first = runs.runs[0]
    assert first.files["README.md"] == "# R\n"
    assert "src/new.py" not in first.files
    assert first.files["Makefile"] == ready_files()["Makefile"]
    assert not first.workspace.exists()


def test_the_containers_get_the_site_variables_and_the_bundle(ready: Path, tmp_path: Path) -> None:
    bundle = tmp_path / "bundle.pem"
    bundle.write_text("certificate\n", encoding="utf-8")
    settings = read_settings(
        {
            **BASE,
            **CONTAINER,
            "FACTORY_CONTAINER_ENV": "HTTP_PROXY",
            "FACTORY_CA_BUNDLE": str(bundle),
        }
    )
    extras = extra_environment(
        settings, {"HTTP_PROXY": "http://proxy.invalid:3128", "OTHER": "left out"}
    )
    runs = ScriptedContainerRuns([result(GREEN_SYNC), result(GREEN_CHECK)])

    _live(ready, runs, FakeImages(), environment=extras, ca_bundle=bundle)

    assert len(runs.runs) == 2
    for run in runs.runs:
        assert run.environment["HTTP_PROXY"] == "http://proxy.invalid:3128"
        assert "OTHER" not in run.environment
        assert all(run.environment[name] == str(bundle) for name in CA_BUNDLE_NAMES)
        assert run.environment["HOME"] == WORK_HOME
        assert read_only_at_own_path(bundle) in run.mounts
