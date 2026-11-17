"""The project check command: its arguments, the agent home, its output and exit status."""

from collections.abc import Callable
from pathlib import Path

import pytest
from pydantic import BaseModel, ConfigDict

from factory.entry.check_project import main
from support.git_support import run_git
from support.project_check_support import committed_repository, installed_home, ready_files

USAGE = "factory-check-project [--agent-home <dir>] <folder>"
HOME_VARIABLE = "FACTORY_CLAUDE_HOME"


class Layout(BaseModel):
    """The folders one run of the command may name."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    ready: Path
    faulty: Path
    plain: Path
    empty_repository: Path
    home: Path
    empty_home: Path


@pytest.fixture
def layout(tmp_path: Path) -> Layout:
    """A ready and a faulty repository, a plain folder, a repository without a commit, two homes."""
    plain = tmp_path / "plain"
    plain.mkdir()
    empty_repository = tmp_path / "empty-repository"
    empty_repository.mkdir()
    run_git(empty_repository, "init", "-q")
    empty_home = tmp_path / "empty-home"
    empty_home.mkdir()
    return Layout(
        ready=committed_repository(tmp_path / "ready", ready_files()),
        faulty=committed_repository(
            tmp_path / "faulty", ready_files({"factory/feature-form.md": None})
        ),
        plain=plain,
        empty_repository=empty_repository,
        home=installed_home(tmp_path / "agent-home"),
        empty_home=empty_home,
    )


Arguments = Callable[[Layout], list[str]]
Environment = Callable[[Layout], str | None]


def _no_home(_: Layout) -> str | None:
    return None


@pytest.mark.parametrize(
    ("arguments", "environment", "status", "last_line", "error"),
    [
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home), str(paths.ready)],
            _no_home,
            0,
            "project: ready",
            None,
            id="ready",
        ),
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home), str(paths.faulty)],
            _no_home,
            1,
            "project: not ready (1 fault)",
            None,
            id="not-ready",
        ),
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home)],
            _no_home,
            2,
            None,
            USAGE,
            id="no-folder",
        ),
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home), str(paths.ready), str(paths.faulty)],
            _no_home,
            2,
            None,
            USAGE,
            id="two-folders",
        ),
        pytest.param(
            lambda paths: [str(paths.ready)], _no_home, 2, None, USAGE, id="no-agent-home"
        ),
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home), str(paths.plain)],
            _no_home,
            2,
            None,
            "cannot read {plain}: ",
            id="no-git-repository",
        ),
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home), str(paths.empty_repository)],
            _no_home,
            2,
            None,
            "cannot read {empty_repository}: ",
            id="no-commit",
        ),
        pytest.param(
            lambda paths: [str(paths.ready)],
            lambda paths: str(paths.home),
            0,
            "project: ready",
            None,
            id="home-from-environment",
        ),
        pytest.param(
            lambda paths: ["--agent-home", str(paths.home), str(paths.ready)],
            lambda paths: str(paths.empty_home),
            0,
            "project: ready",
            None,
            id="option-beats-environment",
        ),
    ],
)
def test_main_prints_the_report_or_one_error_and_returns_its_status(
    layout: Layout,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *,
    arguments: Arguments,
    environment: Environment,
    status: int,
    last_line: str | None,
    error: str | None,
) -> None:
    home = environment(layout)
    if home is None:
        monkeypatch.delenv(HOME_VARIABLE, raising=False)
    else:
        monkeypatch.setenv(HOME_VARIABLE, home)

    returned = main(arguments(layout))
    captured = capsys.readouterr()

    assert returned == status
    if last_line is not None:
        lines = captured.out.splitlines()
        assert len(lines) == 7
        assert lines[-1] == last_line
    if error is not None:
        expected = error.format(plain=layout.plain, empty_repository=layout.empty_repository)
        error_lines = captured.err.splitlines()
        assert len(error_lines) == 1
        if expected == USAGE:
            assert USAGE in error_lines[0]
        else:
            assert error_lines[0].startswith(expected)
