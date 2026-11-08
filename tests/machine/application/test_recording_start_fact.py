"""The recording project commands record a start fact's run as they record a check's."""

from datetime import timedelta
from pathlib import Path
from typing import override

from factory.hosting.adapters.git_cli import GitCli
from factory.machine.application.project_commands import (
    ProjectCommands,
    RecordingProjectCommands,
)
from factory.machine.domain.command_records import CommandRecord
from factory.pipeline.domain.checks import CheckResult, CommandOutput
from factory.shared.adapters.clock import ManualClock
from factory.watching.adapters.factory_log import TimestampedFactoryLog
from factory.watching.adapters.record_log_jsonl import JsonLinesRecordLog

TIME_LIMIT = timedelta(minutes=3)
OUTPUT = "the first line of the fact\nthe second line of the fact\n"


class _StartFactCommands(ProjectCommands):
    """Answers every start fact with one whole output; a check is never asked."""

    def __init__(self) -> None:
        self.start_facts: list[tuple[str, timedelta]] = []

    @override
    def run(self, command: str, *, time_limit: timedelta) -> CheckResult:
        raise AssertionError(f"a start fact ran as a check: {command}")

    @override
    def start_fact(self, command: str, *, time_limit: timedelta) -> CommandOutput:
        self.start_facts.append((command, time_limit))
        return CommandOutput(
            command=command,
            status="passed",
            exit_status=0,
            duration=timedelta(seconds=2.5),
            last_line="the second line of the fact",
            output_tail="the second line of the fact",
            output=OUTPUT,
        )


def test_a_start_fact_reaches_the_inner_commands_and_is_recorded(
    checkout: GitCli, clock: ManualClock, tmp_path: Path
) -> None:
    records = JsonLinesRecordLog(tmp_path / "records" / "project-commands.jsonl", CommandRecord)
    inner = _StartFactCommands()
    log = TimestampedFactoryLog(tmp_path / "state" / "factory.log", clock)
    recorder = RecordingProjectCommands(inner, checkout, records, clock, log)

    returned = recorder.start_fact("facts", time_limit=TIME_LIMIT)

    assert inner.start_facts == [("facts", TIME_LIMIT)]
    assert returned.output == OUTPUT
    assert records.read() == [
        CommandRecord(
            command="facts",
            commit=checkout.resolve("HEAD"),
            started_at=clock.now(),
            duration_seconds=2.5,
            status="passed",
            exit_status=0,
            targets=[],
        )
    ]
