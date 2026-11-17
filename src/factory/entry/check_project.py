# SPDX-License-Identifier: Apache-2.0
"""The project check command: whether the commit at `HEAD` of a repository is ready."""

import os
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from factory.entry.wiring import (
    build_agent_definitions,
    build_images,
    build_pipeline_definition_reader,
    read_environment_settings,
)
from factory.hosting.adapters.git_cli import GitCli
from factory.machine.adapters.podman_runs import PodmanRuns
from factory.machine.application.containers import ContainerRuns
from factory.machine.application.project_run import (
    ProjectRun,
    check_image_tag,
    checkout_has_stage_file,
)
from factory.machine.domain.containers import extra_environment
from factory.pipeline.application.project_check import ProjectCheck
from factory.pipeline.domain.project_check import ProjectPoint, is_ready, report_lines
from factory.shared.domain.errors import GitError, SettingsInvalid
from factory.shared.domain.paths import PIPELINE_DEFINITION_FILE
from factory.shared.domain.settings import (
    AGENT_HOME_VARIABLE,
    STAGE_IMAGE_VARIABLE,
    InstanceSettings,
)

_USAGE = "usage: factory-check-project [--agent-home <dir>] [--run] <folder>"
_AGENT_HOME_OPTION = "--agent-home"
_RUN_OPTION = "--run"
_REF = "HEAD"
_READY = 0
_NOT_READY = 1
_FAILURE = 2


class _Arguments(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    folder: Path
    agent_home: Path | None
    run: bool


class _UsageError(Exception):
    pass


def _parse(argv: Sequence[str]) -> _Arguments:
    folders: list[str] = []
    agent_home: str | None = None
    run = False
    remaining = list(argv)
    while remaining:
        argument = remaining.pop(0)
        if argument == _AGENT_HOME_OPTION:
            if not remaining:
                raise _UsageError
            agent_home = remaining.pop(0)
        elif argument == _RUN_OPTION:
            run = True
        else:
            folders.append(argument)
    if len(folders) != 1:
        raise _UsageError
    return _Arguments(
        folder=Path(folders[0]),
        agent_home=None if agent_home is None else Path(agent_home),
        run=run,
    )


def build_project_run(settings: InstanceSettings) -> ProjectRun:
    """The live part of the check on the instance's podman, stage image and container extras.

    `SettingsInvalid` when the settings name no stage image.
    """
    stage_image = settings.stage_image
    if stage_image is None:
        raise SettingsInvalid(STAGE_IMAGE_VARIABLE, "missing")

    def containers(workspace: Path) -> ContainerRuns:
        # The use case builds the stage file of the clone under the check's tag, so the
        # containers run in that image exactly when the clone holds one.
        image = check_image_tag(stage_image) if checkout_has_stage_file(workspace) else stage_image
        return PodmanRuns(
            settings.podman_executable,
            image,
            workspace,
            instance=settings.instance,
            profile=settings.container_profile,
        )

    return ProjectRun(
        build_images(settings),
        containers=containers,
        git=GitCli,
        stage_image=stage_image,
        extra_environment=extra_environment(settings, os.environ),
        ca_bundle=settings.ca_bundle,
    )


def _live_points(project_run: ProjectRun, git: GitCli, folder: Path) -> list[ProjectPoint]:
    # The static part has just read the definition at the same commit, so it is there and valid.
    text = git.show_file(_REF, PIPELINE_DEFINITION_FILE) or ""
    definition = build_pipeline_definition_reader().parse(text)
    return project_run.run(folder, definition)


def _unreadable_reason(git: GitCli) -> str | None:
    try:
        commit = git.resolve(_REF)
    except (GitError, OSError) as error:
        return str(error)
    return f"no commit at {_REF}" if commit is None else None


def main(argv: Sequence[str] | None = None) -> int:
    """Check the repository in the folder, print the report and return the exit status.

    With `--run`, a ready repository is then built and run in containers, as a stage does.
    """
    try:
        arguments = _parse(sys.argv[1:] if argv is None else argv)
    except _UsageError:
        print(_USAGE, file=sys.stderr)
        return _FAILURE
    agent_home = arguments.agent_home
    project_run: ProjectRun | None = None
    if arguments.run:
        try:
            settings = read_environment_settings(os.environ)
            project_run = build_project_run(settings)
        except SettingsInvalid as error:
            print(f"cannot run: {error}", file=sys.stderr)
            return _FAILURE
        agent_home = agent_home or settings.agent_home
    agent_home = agent_home or _environment_agent_home()
    if agent_home is None:
        print(_USAGE, file=sys.stderr)
        return _FAILURE
    git = GitCli(arguments.folder)
    reason = _unreadable_reason(git)
    if reason is not None:
        print(f"cannot read {arguments.folder}: {reason}", file=sys.stderr)
        return _FAILURE
    agents = build_agent_definitions(git, agent_home, _REF)
    points = ProjectCheck(git, build_pipeline_definition_reader(), agents, _REF).run()
    if project_run is not None and is_ready(points):
        points = [*points, *_live_points(project_run, git, arguments.folder)]
    for line in report_lines(points):
        print(line)
    return _READY if is_ready(points) else _NOT_READY


def _environment_agent_home() -> Path | None:
    value = os.environ.get(AGENT_HOME_VARIABLE)
    return Path(value) if value else None


if __name__ == "__main__":
    sys.exit(main())
