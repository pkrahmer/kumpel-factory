"""A Claude run's instructions file carries the checkout's root `CLAUDE.md` after the prompt."""

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from factory.agents.adapters.claude_runtime import SWITCHES, ClaudeCodeRuntime
from factory.agents.domain.prompts import SYSTEM_PROMPT
from factory.hosting.adapters.git_cli import GitCli
from factory.machine.adapters.fake_containers import FakeContainerRuns
from factory.shared.domain.errors import AgentRuntimeError
from factory.shared.domain.paths import REMOTE, WORK_BRANCH
from support.agent_run_support import run_request
from support.claude_resume_support import _budget_reply, _reply
from support.claude_stand_in import REPLY, StandInCall, Step, read_calls, write_stand_in
from support.container_runtime_support import container_environment
from support.git_support import CHECKOUT, commit_all, run_git, write_files
from support.opencode_stand_in import (
    REPLY_EVENTS,
    configuration_text,
    opencode_request,
    stand_in_runtime,
)

INTRODUCTION = (
    "The project's instructions, its CLAUDE.md, follow; obey them as you obey this system prompt."
)
# Without a closing newline, so the lines it holds are the same however the block is closed.
PROJECT_TEXT = "# A project\n\n- Everything is English.\n- Run `make check`."
BRANCH = "work-item/F0001-S0001"


def _with_project(text: str) -> list[str]:
    return [
        *SYSTEM_PROMPT.splitlines(),
        "",
        INTRODUCTION,
        "<project-instructions>",
        *text.splitlines(),
        "</project-instructions>",
    ]


def _runtime(tmp_path: Path, steps: list[Step]) -> ClaudeCodeRuntime:
    executable = write_stand_in(tmp_path / "bin", steps)
    return ClaudeCodeRuntime(str(executable), tmp_path / "state")


def _instructions(call: StandInCall) -> str:
    return call.files[call.arguments[call.arguments.index("--append-system-prompt-file") + 1]]


def _work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    work.mkdir(exist_ok=True)
    return work


def test_a_root_claude_md_follows_the_system_prompt_in_its_block(tmp_path: Path) -> None:
    work = _work(tmp_path)
    (work / "CLAUDE.md").write_text(PROJECT_TEXT, encoding="utf-8")

    _runtime(tmp_path, [Step(stdout=REPLY)]).run(run_request(work))

    [call] = read_calls(tmp_path / "bin")
    instructions = _instructions(call)
    assert instructions.startswith(SYSTEM_PROMPT)
    assert instructions.splitlines() == _with_project(PROJECT_TEXT)


def _no_file(_: Path) -> None:
    return None


def _a_directory(work: Path) -> None:
    (work / "CLAUDE.md").mkdir()
    (work / "CLAUDE.md" / "notes.md").write_text(PROJECT_TEXT, encoding="utf-8")


@pytest.mark.parametrize(
    "prepare",
    [
        pytest.param(_no_file, id="absent"),
        pytest.param(_a_directory, id="directory"),
    ],
)
def test_a_checkout_without_a_root_claude_md_file_gets_the_system_prompt_alone(
    tmp_path: Path, prepare: Callable[[Path], None]
) -> None:
    work = _work(tmp_path)
    prepare(work)

    _runtime(tmp_path, [Step(stdout=REPLY)]).run(run_request(work))

    [call] = read_calls(tmp_path / "bin")
    assert _instructions(call) == SYSTEM_PROMPT


def test_a_root_claude_md_that_is_not_utf8_text_is_an_error_naming_its_path(
    tmp_path: Path,
) -> None:
    work = _work(tmp_path)
    path = work / "CLAUDE.md"
    path.write_bytes(b"# A project\n\xff\xfe not UTF-8\n")

    with pytest.raises(AgentRuntimeError) as raised:
        _runtime(tmp_path, [Step(stdout=REPLY)]).run(run_request(work))

    assert str(path) in raised.value.detail


def _on_the_host(tmp_path: Path, _: FakeContainerRuns) -> dict[str, str]:
    work = _work(tmp_path)
    executable = write_stand_in(tmp_path / "bin", [Step(stdout=REPLY)])
    ClaudeCodeRuntime(str(executable), tmp_path / "state").run(run_request(work))
    [call] = read_calls(tmp_path / "bin")
    return call.environment


def _in_a_container(tmp_path: Path, fake: FakeContainerRuns) -> dict[str, str]:
    work = _work(tmp_path)
    executable = write_stand_in(tmp_path / "bin", [Step(stdout=REPLY)])
    runtime = ClaudeCodeRuntime(str(executable), tmp_path / "state", containers=fake)
    request = run_request(work).model_copy(
        update={"environment": container_environment(tmp_path / "bin")}
    )
    runtime.run(request)
    [call] = fake.calls
    return dict(call.environment)


@pytest.mark.parametrize(
    "environment_of",
    [
        pytest.param(_on_the_host, id="host"),
        pytest.param(_in_a_container, id="container"),
    ],
)
def test_every_claude_call_switches_off_claude_md_and_writes_five_minute_cache(
    tmp_path: Path,
    fake: FakeContainerRuns,
    environment_of: Callable[[Path, FakeContainerRuns], dict[str, str]],
) -> None:
    environment = environment_of(tmp_path, fake)

    assert SWITCHES["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] == "1"
    assert SWITCHES["CLAUDE_CODE_PROMPT_CACHE_TTL"] == "5m"
    assert environment["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] == "1"
    assert environment["CLAUDE_CODE_PROMPT_CACHE_TTL"] == "5m"


def test_a_resumed_call_gets_the_same_instructions_file(tmp_path: Path) -> None:
    work = _work(tmp_path)
    (work / "CLAUDE.md").write_text(PROJECT_TEXT, encoding="utf-8")
    runtime = _runtime(tmp_path, [Step(stdout=_budget_reply()), Step(stdout=_reply())])

    runtime.run(run_request(work))

    first, second = read_calls(tmp_path / "bin")
    flag = "--append-system-prompt-file"
    assert (
        second.arguments[second.arguments.index(flag) + 1]
        == (first.arguments[first.arguments.index(flag) + 1])
    )
    assert _instructions(second) == _instructions(first)
    assert _instructions(first).splitlines() == _with_project(PROJECT_TEXT)


def test_a_claude_md_changed_on_the_branch_reaches_the_next_run(
    tmp_path: Path, *, checkout: GitCli
) -> None:
    # The fixture clones the remote into the checkout the runs work in.
    del checkout
    directory = tmp_path / CHECKOUT
    run_git(directory, "checkout", "-q", "-B", BRANCH, f"{REMOTE}/{WORK_BRANCH}")
    write_files(directory, {"CLAUDE.md": PROJECT_TEXT})
    commit_all(directory, "first instructions")
    runtime = _runtime(tmp_path, [Step(stdout=REPLY), Step(stdout=REPLY)])
    runtime.run(run_request(directory))
    changed = "# A project\n\n- Everything is German now."
    write_files(directory, {"CLAUDE.md": changed})
    commit_all(directory, "changed instructions")

    runtime.run(run_request(directory))

    first, second = read_calls(tmp_path / "bin")
    assert _instructions(first).splitlines() == _with_project(PROJECT_TEXT)
    assert _instructions(second).splitlines() == _with_project(changed)


def test_an_opencode_agent_prompt_holds_no_project_instructions_block(tmp_path: Path) -> None:
    runtime = stand_in_runtime(tmp_path, [Step(stdout=REPLY_EVENTS)])
    request = opencode_request(tmp_path / "work")
    (tmp_path / "work" / "CLAUDE.md").write_text(PROJECT_TEXT, encoding="utf-8")

    runtime.run(request)

    [call] = read_calls(tmp_path / "bin")
    agents = json.loads(configuration_text(call))["agent"]
    for definition in agents.values():
        assert "<project-instructions>" not in str(definition.get("prompt", ""))
