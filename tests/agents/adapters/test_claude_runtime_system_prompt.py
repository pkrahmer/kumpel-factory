"""The system prompt a run gets when the runtime has no readable system-prompt file."""

from collections.abc import Callable
from pathlib import Path

import pytest

from factory.agents.adapters.claude_runtime import ClaudeCodeRuntime
from factory.agents.domain.prompts import SYSTEM_PROMPT
from factory.shared.domain.errors import AgentRuntimeError
from support.agent_run_support import run_request
from support.claude_stand_in import REPLY, Step, read_calls, write_stand_in
from support.shipped_agents import SYSTEM_PROMPT_FILE


def _no_file(_: Path) -> Path | None:
    return None


def _missing(tmp_path: Path) -> Path | None:
    return tmp_path / "home" / "system-prompt.md"


def _unreadable(tmp_path: Path) -> Path | None:
    # A folder at the file's path exists and cannot be read as text, whoever runs the test.
    folder = tmp_path / "home" / "system-prompt.md"
    folder.mkdir(parents=True)
    return folder


@pytest.mark.parametrize(
    ("system_prompt_file", "readable"),
    [
        pytest.param(_no_file, True, id="no-file"),
        pytest.param(_missing, True, id="missing-path"),
        pytest.param(_unreadable, False, id="unreadable-file"),
    ],
)
def test_a_run_without_a_readable_system_prompt_file_gets_the_built_in_one_or_an_error(
    tmp_path: Path,
    system_prompt_file: Callable[[Path], Path | None],
    readable: bool,
) -> None:
    path = system_prompt_file(tmp_path)
    work = tmp_path / "work"
    work.mkdir()
    executable = write_stand_in(tmp_path / "bin", [Step(stdout=REPLY)])
    runtime = ClaudeCodeRuntime(str(executable), tmp_path / "state", None, system_prompt_file=path)

    if not readable:
        with pytest.raises(AgentRuntimeError) as raised:
            runtime.run(run_request(work))
        assert str(path) in raised.value.detail
        return

    runtime.run(run_request(work))

    [call] = read_calls(tmp_path / "bin")
    instructions = call.files[
        call.arguments[call.arguments.index("--append-system-prompt-file") + 1]
    ]
    assert instructions == SYSTEM_PROMPT
    assert SYSTEM_PROMPT_FILE.read_text(encoding="utf-8") == SYSTEM_PROMPT
