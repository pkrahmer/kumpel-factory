"""Each key of each shipped agent file shows in the call `ClaudeCodeRuntime` makes."""

import json
import re
from datetime import timedelta
from decimal import Decimal

import pytest

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from factory.agents.adapters.claude_runtime import ClaudeCodeRuntime
from factory.agents.domain.agent_runs import AgentRunRequest
from factory.agents.domain.prompts import PromptFacts, compose_prompt
from support.claude_stand_in import StandInCall, Step, read_calls, write_stand_in
from support.shipped_agents import (
    AGENT_HOME,
    SHIPPED_AGENTS,
    SHIPPED_NAMES,
    SYSTEM_PROMPT_FILE,
    ShippedAgent,
    front_matter_and_body,
)

REPLY = json.dumps(
    {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "num_turns": 1,
        "total_cost_usd": 0.25,
        "duration_ms": 1200,
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
        },
        "permission_denials": [],
        "structured_output": {"decision": "doing", "entry": "Done."},
    }
)


@pytest.fixture(scope="module")
def calls(tmp_path_factory: pytest.TempPathFactory) -> dict[str, StandInCall]:
    """The one call the runtime makes for each shipped agent, read from its file."""
    reader = FrontmatterAgentDefinitionReader(AGENT_HOME)
    made: dict[str, StandInCall] = {}
    for name in SHIPPED_NAMES:
        root = tmp_path_factory.mktemp(name)
        work = root / "work"
        work.mkdir()
        executable = write_stand_in(root / "bin", [Step(stdout=REPLY)])
        runtime = ClaudeCodeRuntime(
            str(executable), root / "state", None, system_prompt_file=SYSTEM_PROMPT_FILE
        )
        _, body = front_matter_and_body(name)
        runtime.run(
            AgentRunRequest(
                agent=reader.read(name),
                prompt=compose_prompt(
                    PromptFacts(
                        work_item="F0001-S0001",
                        path="factory/features/F0001-a/in-progress/F0001-S0001-a.md",
                        stage="doing",
                        allowed_decisions=["doing", "question"],
                        branch="work-item/F0001-S0001",
                        pull_request=1,
                        round=0,
                        body="# A story\n",
                        role=name,
                        role_instructions=body,
                    )
                ),
                allowed_decisions=["doing", "question"],
                time_limit=timedelta(seconds=30),
                working_directory=work,
            )
        )
        recorded = read_calls(root / "bin")
        assert len(recorded) == 1
        made[name] = recorded[0]
    return made


def _after(call: StandInCall, flag: str) -> str:
    return call.arguments[call.arguments.index(flag) + 1]


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_call_passes_the_agent_model(calls: dict[str, StandInCall], agent: ShippedAgent) -> None:
    assert _after(calls[agent.name], "--model") == agent.model


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_call_passes_the_agent_effort(calls: dict[str, StandInCall], agent: ShippedAgent) -> None:
    assert _after(calls[agent.name], "--effort") == agent.effort


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_call_passes_exactly_the_agent_tools(
    calls: dict[str, StandInCall], agent: ShippedAgent
) -> None:
    passed = {tool for tool in re.split(r"[,\s]+", _after(calls[agent.name], "--tools")) if tool}

    assert passed == set(agent.tools)


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_call_passes_the_agent_budget(calls: dict[str, StandInCall], agent: ShippedAgent) -> None:
    assert Decimal(_after(calls[agent.name], "--max-budget-usd")) == agent.budget_usd


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_instructions_file_holds_the_agent_body(
    calls: dict[str, StandInCall], agent: ShippedAgent
) -> None:
    call = calls[agent.name]
    instructions = call.files[_after(call, "--append-system-prompt-file")]
    message = _after(call, "-p")

    _, body = front_matter_and_body(agent.name)
    role_block = message.split(f'<role-instructions role="{agent.name}">\n', 1)[1]

    assert instructions == SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    assert body not in instructions
    assert role_block.startswith(body)
