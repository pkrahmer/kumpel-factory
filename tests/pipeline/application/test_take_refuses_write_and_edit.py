"""The roles that write only their work item keep that limit, whichever tool wrote a file."""

from pathlib import Path

import pytest

from factory.agents.domain.agent_runs import WritePathSettings
from factory.agents.domain.write_paths import PROTECTED_PATHS, expand_write_paths
from factory.pipeline.application.take import is_refused
from support.shipped_agents import template_definition

FEATURE = "factory/features/F0001-demo"
WORK_ITEM = f"{FEATURE}/in-progress/F0001-S0001-demo.md"
# `Write` makes a file that was not there; `Edit` changes one that was.
WRITTEN = {"Write": "notes/new-file.md", "Edit": "README.md"}


@pytest.mark.parametrize("role", ["intake", "reviewer", "smoke-tester"])
@pytest.mark.parametrize(("tool", "path"), sorted(WRITTEN.items()))
def test_a_file_written_outside_the_work_item_is_refused(role: str, tool: str, path: str) -> None:
    patterns = template_definition().roles[role].write_paths
    settings = WritePathSettings(
        root=Path("/work"),
        write_paths=expand_write_paths(patterns, work_item_path=WORK_ITEM, feature_path=FEATURE),
        protected_paths=list(PROTECTED_PATHS),
    )

    assert is_refused(path, settings, WORK_ITEM), tool
    assert not is_refused(WORK_ITEM, settings, WORK_ITEM)
