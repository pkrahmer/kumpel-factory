"""The conformance check reads the makefile the pipeline definition names."""

from pathlib import Path

import pytest

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from factory.agents.application.project_agents import ProjectAgentDefinitions
from factory.hosting.adapters.git_cli import GitCli
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.pipeline.application.project_check import ProjectCheck
from support.git_support import PIPELINE_YAML
from support.project_check_support import (
    READY_MAKEFILE,
    committed_repository,
    installed_home,
    ready_files,
)

NAMED = "factory/Makefile"
NAMING_DEFINITION = f"make_file: {NAMED}\n{PIPELINE_YAML}"
# The named makefile lacks `lint` and `sync`, which the included file brings.
INCLUDING_MAKEFILE = "include common.mk\n\ncheck:\n\t@:\ntest:\n\t@:\n"
COMMON_MK = "lint:\n\t@:\nsync:\n\t@:\n"


def _makefile_faults(tmp_path: Path, changes: dict[str, str | None]) -> list[str]:
    files = ready_files({"factory/pipeline.yml": NAMING_DEFINITION, **changes})
    repository = committed_repository(tmp_path / "project", files)
    home = installed_home(tmp_path / "agent-home")
    git = GitCli(repository)
    agents = ProjectAgentDefinitions(git, FrontmatterAgentDefinitionReader(home), ref="HEAD")
    points = ProjectCheck(git, RuamelPipelineDefinitionReader(), agents).run()
    [point] = [point for point in points if point.name == "makefile"]
    assert not point.skipped
    return point.faults


@pytest.mark.parametrize(
    ("changes", "faults"),
    [
        ({NAMED: READY_MAKEFILE, "Makefile": None}, []),
        ({"Makefile": READY_MAKEFILE}, [f"{NAMED} is missing"]),
    ],
    ids=["named-only", "root-only"],
)
def test_the_makefile_point_reads_the_named_makefile(
    tmp_path: Path, changes: dict[str, str | None], faults: list[str]
) -> None:
    assert _makefile_faults(tmp_path, changes) == faults


@pytest.mark.parametrize(
    ("common_path", "faults"),
    [
        ("common.mk", []),
        ("factory/common.mk", [f"{NAMED}: included file common.mk is missing"]),
    ],
    ids=["at-the-root", "beside-the-makefile"],
)
def test_the_named_makefile_s_includes_are_taken_from_the_root(
    tmp_path: Path, common_path: str, faults: list[str]
) -> None:
    changes: dict[str, str | None] = {
        NAMED: INCLUDING_MAKEFILE,
        common_path: COMMON_MK,
        "Makefile": None,
    }

    found = _makefile_faults(tmp_path, changes)

    # A missing include also leaves its targets missing; the include's own fault must be there.
    assert set(faults) <= set(found)
    assert bool(found) is bool(faults)
