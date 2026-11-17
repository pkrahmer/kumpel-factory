"""The container stage environment syncs with the makefile its source names."""

from pathlib import Path

import pytest

from factory.hosting.domain.git import CommitId
from factory.machine.application.make_file import MakeFileSource
from factory.machine.application.stage_environment import ContainerEnvironment
from factory.pipeline.application.boundaries import Boundaries
from factory.shared.domain.paths import WORK_BRANCH
from support.container_support import FIVE_MINUTES, Dataset, push_main
from support.git_support import install_agents
from support.human_clone import HumanClone
from support.make_file_support import AnsweringSource

NAMED = "factory/Makefile"
ROOT_MARKER = ".root-synced"
NAMED_MARKER = ".named-synced"


@pytest.fixture
def main_commit(boundaries: Boundaries, human: HumanClone, agent_home: Path) -> CommitId:
    """Push a root `Makefile` and a `factory/Makefile`, each of whose `sync` leaves its marker."""
    commit = push_main(
        boundaries,
        human,
        {
            "Makefile": f".PHONY: sync\n\nsync:\n\t@touch {ROOT_MARKER}\n",
            NAMED: f".PHONY: sync\n\nsync:\n\t@touch {NAMED_MARKER}\n",
        },
    )
    install_agents(agent_home, ["tester"])
    return commit


@pytest.mark.parametrize(
    ("source", "marker"),
    [
        (AnsweringSource(NAMED), NAMED_MARKER),
        (None, ROOT_MARKER),
        (AnsweringSource(None), ROOT_MARKER),
    ],
    ids=["named", "no-source", "none"],
)
def test_the_sync_runs_the_makefile_the_source_names_as_an_argument(
    dataset: Dataset, main_commit: CommitId, source: MakeFileSource | None, marker: str
) -> None:
    environment = ContainerEnvironment(
        dataset.boundaries, dataset.snapshots, dataset.containers, make_file=source
    )

    environment.prepare(main_commit, WORK_BRANCH, sync_time_limit=FIVE_MINUTES)

    [call] = dataset.containers.calls
    script = call.command[2]
    assert NAMED not in script
    assert (NAMED in call.command[3:]) is (marker == NAMED_MARKER)
    synced = {path.name for path in (dataset.workspace / "checkout").iterdir()}
    assert {ROOT_MARKER, NAMED_MARKER} & synced == {marker}
