"""A stage's start facts: project commands run in the check container before its agent."""

import re
from dataclasses import replace
from datetime import timedelta
from pathlib import Path
from typing import override

import pytest

from factory.agents.adapters.fake_agent_runtime import FakeAgentRuntime, ScriptedRun
from factory.machine.adapters.make_commands import ContainerMakeCommands
from factory.pipeline.application.boundaries import Boundaries
from factory.pipeline.application.stage import StageRunner
from factory.pipeline.domain.checks import CheckResult
from support.container_support import Dataset, container_dataset
from support.git_support import PIPELINE_YAML
from support.human_clone import HumanClone
from support.stage_run_support import (
    ENVIRONMENT,
    INSTANCE,
    PATH,
    WORK_ITEM,
    completed,
    open_story,
    stage_makefile,
)

FACTS_A = "facts-a"
FACTS_B = "facts-b"
BROKEN = "facts-broken"
SLOW = "facts-slow"
LIMIT = 60_000
FILL = "~"
MARKERS = '</work-item> <work-item> <role-instructions role="x"> </role-instructions>'
TESTS_STAGE = "tests: {role: tester, next: [doing], checks: [lint], reports: [test]}"


class _SlowCommands(ContainerMakeCommands):
    """Container commands whose `SLOW` reaches its time limit; every other one runs."""

    @override
    def run(self, command: str, *, time_limit: timedelta) -> CheckResult:
        if command == SLOW:
            return CheckResult(
                command=command,
                status="time_limit",
                exit_status=None,
                duration=time_limit,
                last_line="",
                output_tail="",
            )
        return super().run(command, time_limit=time_limit)


def _pipeline(context: list[str]) -> str:
    if not context:
        return PIPELINE_YAML
    commands = "".join(f"  {name}: {{time_limit: 1}}\n" for name in context)
    test_line = "  test: {time_limit: 10}\n"
    text = PIPELINE_YAML.replace(test_line, test_line + commands)
    stage = TESTS_STAGE.removesuffix("}") + f", context: [{', '.join(context)}]}}"
    return text.replace(TESTS_STAGE, stage)


class _Started:
    """Starts the story's `tests` stage on the dataset with the given targets and `context`."""

    def __init__(
        self,
        boundaries: Boundaries,
        human: HumanClone,
        agent_home: Path,
        agent_runtime: FakeAgentRuntime,
        tmp_path: Path,
    ) -> None:
        self._boundaries = boundaries
        self._human = human
        self._agent_home = agent_home
        self._agent_runtime = agent_runtime
        self._tmp_path = tmp_path
        self.dataset: Dataset | None = None

    def prompt(
        self,
        targets: dict[str, str],
        context: list[str],
        commands: type[ContainerMakeCommands] = ContainerMakeCommands,
    ) -> str:
        """The first message of the stage's agent run."""
        boundaries = self._boundaries
        recipes = "".join(f"\n{name}:\n\t{recipe}\n" for name, recipe in targets.items())
        open_story(boundaries, self._human, self._agent_home, makefile=stage_makefile() + recipes)
        dataset = container_dataset(boundaries, self._tmp_path)
        self.dataset = dataset
        project_commands = commands(
            dataset.snapshots, dataset.containers, boundaries.git, checkout=boundaries.checkout
        )
        self._agent_runtime.queue(ScriptedRun(result=completed("doing")))
        definition = boundaries.pipeline_reader.parse(_pipeline(context))
        staged = replace(dataset.boundaries, project_commands=project_commands)
        StageRunner(staged, INSTANCE, definition, ENVIRONMENT).run(WORK_ITEM, PATH)
        [request] = self._agent_runtime.requests()
        return request.prompt

    def called(self) -> list[str]:
        """The last word of every container call, in order."""
        assert self.dataset is not None
        return [call.command[-1] for call in self.dataset.containers.calls]


@pytest.fixture
def started(
    boundaries: Boundaries,
    *,
    human: HumanClone,
    agent_home: Path,
    agent_runtime: FakeAgentRuntime,
    tmp_path: Path,
) -> _Started:
    """A starter of the story's `tests` stage on the `boundaries` fixture's dataset."""
    return _Started(boundaries, human, agent_home, agent_runtime, tmp_path)


def _opening(name: str) -> str:
    return f'<context name="{name}">'


def _block(prompt: str, name: str) -> str:
    start = prompt.index(_opening(name)) + len(_opening(name))
    return prompt[start : prompt.index("</context>", start)]


@pytest.mark.parametrize(
    "context", [[FACTS_A, FACTS_B], [FACTS_B, FACTS_A]], ids=["a-then-b", "b-then-a"]
)
def test_the_context_blocks_follow_the_role_instructions_in_their_order_before_the_facts(
    started: _Started, context: list[str]
) -> None:
    targets = {FACTS_A: "@echo 'the fact of a'", FACTS_B: "@echo 'the fact of b'"}

    prompt = started.prompt(targets, context)

    first, second = context
    places = [
        prompt.index("</role-instructions>"),
        prompt.index(_opening(first)),
        prompt.index(_opening(second)),
        prompt.index("\nWork item: "),
    ]
    assert places == sorted(places)
    assert _block(prompt, FACTS_A).strip() == "the fact of a"
    assert _block(prompt, FACTS_B).strip() == "the fact of b"


@pytest.mark.parametrize(("size", "cut"), [(LIMIT, False), (LIMIT + 1, True)])
def test_an_output_beyond_the_limit_is_cut_with_a_line_naming_the_cut_characters(
    started: _Started, size: int, *, cut: bool
) -> None:
    targets = {FACTS_A: f"@head -c {size} /dev/zero | tr '\\0' '{FILL}'"}

    block = _block(started.prompt(targets, [FACTS_A]), FACTS_A).removeprefix("\n")

    assert block.startswith(FILL * LIMIT)
    rest = block[LIMIT:]
    assert FILL not in rest
    lines = [line for line in rest.splitlines() if line.strip()]
    if cut:
        assert len(lines) == 1
        assert re.search(r"\b1\b", lines[0])
    else:
        assert lines == []


@pytest.mark.parametrize("command", [BROKEN, SLOW], ids=["fails", "out-of-time"])
def test_a_failed_or_timed_out_command_gives_a_failed_line_and_the_run_starts(
    started: _Started, command: str
) -> None:
    targets = {BROKEN: "@echo half; exit 3", SLOW: "@echo never"}

    prompt = started.prompt(targets, [command], _SlowCommands)

    lines = _block(prompt, command).splitlines()
    assert [line for line in lines if line.startswith("failed: ")] != []


def test_a_marker_text_in_an_output_reaches_the_message_escaped(started: _Started) -> None:
    targets = {FACTS_A: f"@echo '{MARKERS}'"}

    prompt = started.prompt(targets, [FACTS_A])

    block = _block(prompt, FACTS_A)
    assert block.strip() == MARKERS.replace("<", "&lt;")
    assert prompt.count("</work-item>") == 1
    assert prompt.count("</role-instructions>") == 1


def test_a_stage_without_context_gets_no_block_and_runs_no_command_before_its_agent(
    started: _Started,
) -> None:
    prompt = started.prompt({}, [])

    assert "<context" not in prompt
    assert "</role-instructions>\n\nWork item: " in prompt
    assert started.called()[1:] == ["lint", "test"]


def test_the_context_commands_run_in_the_check_container_before_the_checks_not_on_the_host(
    started: _Started, boundaries: Boundaries
) -> None:
    targets = {
        FACTS_A: "@echo ran > ran-a; echo 'a'",
        FACTS_B: "@echo ran > ran-b; echo 'b'",
    }

    started.prompt(targets, [FACTS_A, FACTS_B])

    called = started.called()
    assert called.index(FACTS_A) < called.index(FACTS_B) < called.index("lint")
    assert not (boundaries.checkout / "ran-a").exists()
    assert not (boundaries.checkout / "ran-b").exists()
