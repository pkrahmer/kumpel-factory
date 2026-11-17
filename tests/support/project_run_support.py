"""Container runs that play scripted outcomes and keep what the work folder held at each run."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from factory.machine.adapters.fake_images import FakeImages
from factory.machine.application.containers import ContainerRuns
from factory.machine.domain.containers import (
    ContainerLaunch,
    ContainerResult,
    Mount,
    check_container_call,
)
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.pipeline.domain.pipeline_definition import PipelineDefinition
from factory.shared.domain.errors import ContainerError
from support.git_support import PIPELINE_YAML

GREEN_SYNC = "Resolved 3 packages\nsync: green (1.0 s)\n"
GREEN_CHECK = "sync: green (1.0 s)\nlint: green (0.5 s)\ncheck: green\n"
SYNC_MINUTES = 7
CHECK_MINUTES = 9
NAMED_MAKEFILE = "factory/Makefile"

Outcome = ContainerResult | Exception


def result(output: str, exit_status: int | None = 0, *, timed_out: bool = False) -> ContainerResult:
    """A container run that ended with `exit_status` and printed `output`."""
    return ContainerResult(
        exit_status=exit_status, output=output, timed_out=timed_out, duration=timedelta(seconds=1)
    )


def definition(*, make_file: str | None = None) -> PipelineDefinition:
    """The tests' pipeline definition with a `sync` and a `check` time limit of their own."""
    text = PIPELINE_YAML.replace(
        "  check: {time_limit: 10}\n",
        f"  check: {{time_limit: {CHECK_MINUTES}}}\n  sync: {{time_limit: {SYNC_MINUTES}}}\n",
    )
    if make_file is not None:
        text = text.replace('contract: "1.0"', 'contract: "1.2"') + f"make_file: {make_file}\n"
    return RuamelPipelineDefinitionReader().parse(text)


@dataclass(frozen=True)
class SeenRun:
    """One call of `run`, and the files the checkout of the work folder held at that moment."""

    command: list[str]
    mounts: list[Mount]
    environment: dict[str, str]
    time_limit: timedelta
    working_directory: str
    workspace: Path
    image: str
    files: dict[str, str]


class ScriptedContainerRuns(ContainerRuns):
    """Runs nothing: each `run` takes the next outcome, a result to return or an error to raise."""

    def __init__(self, outcomes: Sequence[Outcome]) -> None:
        """Play `outcomes` in order; `at` names the folder mounted at `/work` and the image."""
        self._outcomes = list(outcomes)
        self.workspaces: list[Path] = []
        self.images: list[str] = []
        self.runs: list[SeenRun] = []

    def at(self, workspace: Path, image: str) -> ContainerRuns:
        """These runs, with `workspace` as the folder mounted at `/work`, in `image`."""
        self.workspaces.append(workspace)
        self.images.append(image)
        return self

    def launch(
        self,
        command: Sequence[str],
        *,
        mounts: Sequence[Mount],
        environment: Mapping[str, str],
        time_limit: timedelta,
        working_directory: str,
    ) -> ContainerLaunch:
        """The command's own words; nothing is recorded."""
        del working_directory
        check_container_call(command, mounts)
        return ContainerLaunch(argv=list(command), env=dict(environment), time_limit=time_limit)

    def run(
        self,
        command: Sequence[str],
        *,
        mounts: Sequence[Mount],
        environment: Mapping[str, str],
        time_limit: timedelta,
        working_directory: str,
    ) -> ContainerResult:
        """Record the call and the checkout's files, then return or raise the next outcome."""
        check_container_call(command, mounts)
        workspace = self.workspaces[-1]
        self.runs.append(
            SeenRun(
                command=list(command),
                mounts=list(mounts),
                environment=dict(environment),
                time_limit=time_limit,
                working_directory=working_directory,
                workspace=workspace,
                image=self.images[-1],
                files=_checkout_files(workspace / "checkout"),
            )
        )
        outcome = self._outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class UninspectableImages(FakeImages):
    """Fake images whose `PATH` cannot be read: `path` raises a `ContainerError`."""

    def path(self, image: str) -> str:
        """Raise as `podman image inspect` does for a missing image."""
        raise ContainerError("podman", f"no such image: {image}")


def _checkout_files(checkout: Path) -> dict[str, str]:
    if not checkout.is_dir():
        return {}
    return {
        path.relative_to(checkout).as_posix(): path.read_text(encoding="utf-8", errors="replace")
        for path in sorted(checkout.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(checkout).parts
    }
