"""The `claude -p` runtime gives every request the same decision tool and otherwise its own call."""

import json
from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from factory.agents.adapters.claude_runtime import ClaudeCodeRuntime
from factory.agents.domain.agent_runs import AgentDefinition, AgentRunRequest
from support.claude_stand_in import Step, read_calls, write_stand_in

REPLY = json.dumps(
    {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "num_turns": 1,
        "total_cost_usd": 0.25,
        "duration_ms": 1200,
        "usage": {"input_tokens": 10, "output_tokens": 5},
        "permission_denials": [],
        "structured_output": {"decision": "question", "entry": "Done."},
    }
)


def _arguments(tmp_path: Path, decisions: list[str]) -> list[str]:
    """The arguments of the one call the runtime makes for a request allowing `decisions`."""
    work = tmp_path / "work"
    work.mkdir()
    executable = write_stand_in(tmp_path / "bin", [Step(stdout=REPLY)])
    request = AgentRunRequest(
        agent=AgentDefinition(
            name="coder",
            model="opus",
            tools=["Read", "Grep", "Glob", "Edit", "Bash", "Write", "Skill"],
            effort="medium",
            budget_usd=Decimal("3"),
            instructions="Write the code.",
        ),
        prompt="Stage: doing",
        allowed_decisions=decisions,
        time_limit=timedelta(seconds=30),
        working_directory=work,
    )
    ClaudeCodeRuntime(str(executable), tmp_path / "state").run(request)
    (call,) = read_calls(tmp_path / "bin")
    return call.arguments


def _schema(arguments: list[str]) -> str:
    return arguments[arguments.index("--json-schema") + 1]


def test_requests_with_different_decisions_get_the_same_json_schema(tmp_path: Path) -> None:
    first = _arguments(tmp_path / "first", ["review", "tests", "question"])
    second = _arguments(tmp_path / "second", ["question"])

    assert _schema(first) == _schema(second)


def test_the_decision_is_any_string_described_as_named_in_the_message(tmp_path: Path) -> None:
    schema = json.loads(_schema(_arguments(tmp_path, ["doing", "question"])))
    decision = schema["properties"]["decision"]

    assert decision["type"] == "string"
    assert "enum" not in decision
    assert "message" in decision["description"]
    assert "allowed decisions" in decision["description"]


@pytest.mark.parametrize("decisions", [["review", "tests", "question"], ["question"]])
def test_the_other_launch_arguments_are_as_before(tmp_path: Path, decisions: list[str]) -> None:
    arguments = _arguments(tmp_path, decisions)
    session = arguments[arguments.index("--session-id") + 1]
    schema = arguments.index("--json-schema") + 1

    assert arguments[:schema] + arguments[schema + 1 :] == [
        "-p",
        "Stage: doing",
        "--model",
        "opus",
        "--effort",
        "medium",
        "--tools",
        "Read,Grep,Glob,Edit,Bash,Write,Skill",
        "--session-id",
        session,
        "--append-system-prompt-file",
        str(tmp_path / "state" / f"instructions-{session}.md"),
        "--permission-mode",
        "auto",
        "--permission-prompts",
        "none",
        "--strict-mcp-config",
        "--max-budget-usd",
        "3",
        "--output-format",
        "json",
        "--json-schema",
    ]
