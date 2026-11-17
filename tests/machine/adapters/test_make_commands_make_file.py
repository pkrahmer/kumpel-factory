"""The make class in a check container calls make with the makefile its source names."""

from datetime import timedelta
from pathlib import Path

import pytest

from factory.hosting.adapters.git_cli import GitCli
from factory.machine.adapters.fake_containers import FakeContainerRuns
from factory.machine.adapters.fake_snapshots import FakeSnapshots
from factory.machine.adapters.make_commands import ContainerMakeCommands
from factory.machine.application.make_file import MakeFileSource
from support.git_support import CHECKOUT, write_files
from support.make_file_support import AnsweringSource

LIMIT = timedelta(minutes=1)
NAMED = "factory/Makefile"
CHECK_LINE = "check: green (0.1 s)"
TODAYS_CHECK = [
    "/bin/sh",
    "-c",
    '"$1" sync && "$1" --no-print-directory "$2"',
    "factory-check",
    "make",
    "check",
]
TODAYS_START_FACT = [
    "/bin/sh",
    "-c",
    '"$1" --no-print-directory "$2"',
    "factory-check",
    "make",
    "check",
]
# The only makefile of the base: its `sync` leaves a marker, its `check` prints its last line.
NAMED_MAKEFILE = (
    ".PHONY: sync check\n\n"
    "sync:\n\t@touch .synced\n\n"
    f"check:\n\t@test -f .synced\n\t@echo '{CHECK_LINE}'\n"
)


class Dataset:
    """The dataset's fakes, whose base's only makefile is `factory/Makefile`."""

    def __init__(self, tmp_path: Path, checkout: GitCli) -> None:
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        base = tmp_path / "base"
        write_files(base / "checkout", {NAMED: NAMED_MAKEFILE})
        self.snapshots = FakeSnapshots(workspace, base)
        self.containers = FakeContainerRuns(workspace)
        self.checkout = checkout
        self.directory = tmp_path / CHECKOUT

    def commands(self, source: MakeFileSource | None) -> ContainerMakeCommands:
        """The class under test on the fakes, with `source`."""
        return ContainerMakeCommands(
            self.snapshots,
            self.containers,
            self.checkout,
            checkout=self.directory,
            make_file=source,
        )


@pytest.fixture
def dataset(tmp_path: Path, checkout: GitCli) -> Dataset:
    """The fakes on a dataset whose base holds only `factory/Makefile`."""
    return Dataset(tmp_path, checkout)


def _refers(words: list[str], arguments: list[str], word: str) -> bool:
    """Whether a segment's `words` hold `word`, as itself or as the argument that holds it."""
    return word in words or any(
        f'"${position}"' in words for position, each in enumerate(arguments) if each == word
    )


def _assert_named(command: list[str], *, with_sync: bool) -> None:
    script = command[2]
    arguments = command[3:]
    assert command[:2] == ["/bin/sh", "-c"]
    assert NAMED not in script
    assert NAMED in arguments
    assert "check" in arguments
    named = ["-f", f'"${arguments.index(NAMED)}"']
    segments = [segment.split() for segment in script.split("&&")]
    syncs = [words for words in segments if _refers(words, arguments, "sync")]
    runs = [words for words in segments if _refers(words, arguments, "check")]
    assert bool(syncs) is with_sync
    assert runs
    for words in syncs + runs:
        assert any(words[index : index + 2] == named for index in range(len(words))), words


@pytest.mark.parametrize(
    ("script", "passes"),
    [
        pytest.param(
            '"$1" -f "$3" sync && "$1" -f "$3" --no-print-directory "$2"', True, id="both"
        ),
        pytest.param('"$1" -f "$3" sync && "$1" --no-print-directory "$2"', False, id="only-sync"),
        pytest.param(
            '"$1" sync && "$1" -f "$3" --no-print-directory "$2"', False, id="only-command"
        ),
    ],
)
def test_the_named_makefile_must_reach_the_sync_and_the_command_each(
    script: str, *, passes: bool
) -> None:
    command = ["/bin/sh", "-c", script, "factory-check", "make", "check", NAMED]

    if passes:
        _assert_named(command, with_sync=True)
    else:
        with pytest.raises(AssertionError):
            _assert_named(command, with_sync=True)


@pytest.mark.parametrize(
    ("source", "start_fact", "expected"),
    [
        (AnsweringSource(NAMED), False, None),
        (AnsweringSource(NAMED), True, None),
        (None, False, TODAYS_CHECK),
        (None, True, TODAYS_START_FACT),
        (AnsweringSource(None), False, TODAYS_CHECK),
        (AnsweringSource(None), True, TODAYS_START_FACT),
    ],
    ids=[
        "named-check",
        "named-start-fact",
        "no-source-check",
        "no-source-start-fact",
        "none-check",
        "none-start-fact",
    ],
)
def test_the_container_command_names_the_makefile_as_an_argument_only_when_the_source_gives_one(
    dataset: Dataset,
    source: MakeFileSource | None,
    *,
    start_fact: bool,
    expected: list[str] | None,
) -> None:
    commands = dataset.commands(source)

    if start_fact:
        commands.start_fact("check", time_limit=LIMIT)
    else:
        commands.run("check", time_limit=LIMIT)

    [call] = dataset.containers.calls
    if expected is None:
        _assert_named(call.command, with_sync=not start_fact)
    else:
        assert call.command == expected


def test_the_source_is_asked_at_every_call(dataset: Dataset) -> None:
    commands = dataset.commands(AnsweringSource(None, NAMED))

    commands.run("check", time_limit=LIMIT)
    commands.run("check", time_limit=LIMIT)

    first, second = dataset.containers.calls
    assert first.command == TODAYS_CHECK
    _assert_named(second.command, with_sync=True)


@pytest.mark.parametrize(
    ("source", "status"),
    [(AnsweringSource(NAMED), "passed"), (None, "failed")],
    ids=["named", "without-source"],
)
def test_a_check_runs_the_named_makefile_s_sync_and_command(
    dataset: Dataset, source: MakeFileSource | None, status: str
) -> None:
    result = dataset.commands(source).run("check", time_limit=LIMIT)

    assert result.status == status
    if status == "passed":
        assert result.last_line == CHECK_LINE
