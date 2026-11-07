"""A watch on a clone without an the working branch ends with the git error the operator reads."""

import io
from dataclasses import replace
from pathlib import Path

import pytest

from factory.entry.watch import run_watch
from factory.hosting.adapters.git_cli import GitCli
from factory.hosting.domain.git import GitOptions
from factory.pipeline.application.boundaries import Boundaries
from factory.pipeline.domain.pipeline_definition import PipelineDefinition
from factory.shared.domain.errors import GitError
from factory.shared.domain.paths import REMOTE, WORK_BRANCH
from factory.watching.application.watcher import Watcher
from support.git_support import TEST_IDENTITY, run_git

UNRESOLVED = (
    f"resolve {REMOTE}/{WORK_BRANCH} failed (no exit status): "
    f"{REMOTE}/{WORK_BRANCH} does not resolve"
)


@pytest.fixture
def empty_clone(boundaries: Boundaries, tmp_path: Path) -> Boundaries:
    """The boundaries on a clone of an empty bare remote."""
    run_git(tmp_path, "init", "-q", "--bare", f"--initial-branch={WORK_BRANCH}", "empty.git")
    run_git(tmp_path, "clone", "-q", str(tmp_path / "empty.git"), "empty-clone")
    git = GitCli(tmp_path / "empty-clone", GitOptions(identity=TEST_IDENTITY))
    return replace(boundaries, git=git)


@pytest.mark.parametrize("through", ["run_watch", "watcher"])
def test_an_unresolved_origin_main_raises_the_operators_git_error(
    empty_clone: Boundaries, definition: PipelineDefinition, through: str
) -> None:
    with pytest.raises(GitError) as raised:
        if through == "run_watch":
            run_watch(empty_clone, "factory-1", io.StringIO(), io.StringIO())
        else:
            Watcher(empty_clone, "factory-1").evaluate(definition)

    assert str(raised.value) == UNRESOLVED
