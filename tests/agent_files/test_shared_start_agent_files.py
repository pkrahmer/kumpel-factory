"""Every shipped agent file has the same tools, and five roles share one model and one effort."""

import pytest

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from support.shipped_agents import AGENT_HOME

SAME_TOOLS = ["Read", "Grep", "Glob", "Edit", "Bash", "Write", "Skill"]
SHIPPED = sorted(path.stem for path in (AGENT_HOME / "agents").glob("*.md"))
EFFORTS = {
    "intake": "medium",
    "tester": "medium",
    "coder": "medium",
    "documenter": "medium",
    "smoke-tester": "medium",
    "reviewer": "high",
    "acceptance-reviewer": "high",
}


def test_the_shipped_agents_are_the_seven_with_an_effort() -> None:
    assert sorted(EFFORTS) == SHIPPED


@pytest.mark.parametrize("name", SHIPPED)
def test_every_agent_file_has_the_same_tools_in_the_same_order(name: str) -> None:
    agent = FrontmatterAgentDefinitionReader(AGENT_HOME).read(name)

    assert agent.tools == SAME_TOOLS


@pytest.mark.parametrize(("name", "effort"), sorted(EFFORTS.items()))
def test_every_agent_file_runs_on_opus_at_its_roles_effort(name: str, effort: str) -> None:
    agent = FrontmatterAgentDefinitionReader(AGENT_HOME).read(name)

    assert (agent.model, agent.effort) == ("opus", effort)
