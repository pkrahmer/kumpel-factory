# SPDX-License-Identifier: Apache-2.0
"""The live part of the conformance check: the project's image, its sync and its check."""

import math
import shutil
import tempfile
from collections.abc import Callable, Mapping
from datetime import timedelta
from pathlib import Path

from factory.hosting.application.git import Git
from factory.machine.application.containers import ContainerRuns
from factory.machine.application.images import IMAGE_BUILD_TIME_LIMIT, Images
from factory.machine.application.project_commands import (
    CHECK_ENVIRONMENT,
    CHECK_SCRIPT,
    CHECK_SCRIPT_NAME,
    NAMED_CHECK_SCRIPT,
)
from factory.machine.application.stage_environment import (
    NAMED_SYNC_MAKE,
    SHELL,
    SYNC_ENVIRONMENT,
    SYNC_MAKE,
)
from factory.machine.domain.containers import (
    WORK,
    WORK_CHECKOUT,
    ContainerResult,
    bundle_mounts,
)
from factory.machine.domain.stage_layer import STAGE_FILE, StageLayerRefused, stage_layer
from factory.pipeline.application.project_check import ANY_BASE
from factory.pipeline.application.take import MOUNTED_CHECKOUT
from factory.pipeline.domain.checks import target_times
from factory.pipeline.domain.pipeline_definition import PipelineDefinition, command_time_limit
from factory.pipeline.domain.project_check import ProjectPoint
from factory.shared.domain.errors import ContainerError
from factory.shared.domain.printed_lines import printed_lines

HOME_FOLDER = "home"
CHECK_TAG_SUFFIX = "-check"

_REF = "HEAD"
_SYNC = "sync"
_CHECK = "check"
_CHECK_GREEN = "check: green"
# The stage's sync runs in the checkout its preparation has filled; here the clone is that
# checkout, so only the change into it comes before the make part.
_LIVE_SYNC_PREPARATION = 'set -eu\ncd "$1"\nshift\n'
_SYNC_SCRIPT_NAME = "factory-sync"


def check_image_tag(stage_image: str) -> str:
    """The tag the live check builds a project's stage file under, apart from the instance's."""
    return f"{stage_image}{CHECK_TAG_SUFFIX}"


def checkout_has_stage_file(workspace: Path) -> bool:
    """Whether the checkout in the work folder `workspace` holds a stage file."""
    return (workspace / MOUNTED_CHECKOUT / STAGE_FILE).is_file()


class ProjectRun:
    """Builds a repository's image and runs its sync and its check as a stage does."""

    def __init__(
        self,
        images: Images,
        *,
        containers: Callable[[Path], ContainerRuns],
        git: Callable[[Path], Git],
        stage_image: str,
        extra_environment: Mapping[str, str] = {},
        ca_bundle: Path | None = None,
    ) -> None:
        """Build through `images`; run in the containers `containers` gives for a work folder.

        `git` gives the git of a folder. The containers get `extra_environment` below their
        own names and `ca_bundle` mounted read-only at its own path.
        """
        self._images = images
        self._containers = containers
        self._git = git
        self._stage_image = stage_image
        self._extra_environment = dict(extra_environment)
        self._mounts = bundle_mounts(ca_bundle)

    def run(self, folder: Path, definition: PipelineDefinition) -> list[ProjectPoint]:
        """The points `image`, `sync` and `check` of the commit at `HEAD` of `folder`.

        The points stop after the first with a fault. The work folder is removed at the end.
        """
        workspace = Path(tempfile.mkdtemp(prefix="factory-check-project-"))
        try:
            return self._run_in(workspace, folder, definition)
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

    def _run_in(
        self, workspace: Path, folder: Path, definition: PipelineDefinition
    ) -> list[ProjectPoint]:
        checkout = workspace / MOUNTED_CHECKOUT
        self._clone(folder, checkout)
        (workspace / HOME_FOLDER).mkdir()
        image, image_point = self._image(checkout)
        if image_point.faults:
            return [image_point]
        containers = self._containers(workspace)
        try:
            path = self._images.path(image)
        except ContainerError as error:
            # The image the sync would run in cannot be read: the sync cannot start.
            return [image_point, _not_started(_SYNC, error)]
        sync_point = self._sync(containers, path, definition)
        if sync_point.faults:
            return [image_point, sync_point]
        return [image_point, sync_point, self._check(containers, path, definition)]

    def _clone(self, folder: Path, checkout: Path) -> None:
        commit = self._git(folder).resolve(_REF)
        clone = self._git(checkout)
        clone.clone(str(folder.resolve()))
        if commit is not None:
            clone.reset_to(commit)

    def _image(self, checkout: Path) -> tuple[str, ProjectPoint]:
        text = self._git(checkout).show_file(_REF, STAGE_FILE)
        if text is None:
            return self._stage_image, ProjectPoint(name="image")
        tag = check_image_tag(self._stage_image)
        try:
            layer = stage_layer(text, ANY_BASE)
        except StageLayerRefused as refusal:
            return tag, ProjectPoint(name="image", faults=[f"the image does not build: {refusal}"])
        build = self._images.build(layer, self._stage_image, tag, IMAGE_BUILD_TIME_LIMIT)
        if build.passed:
            return tag, ProjectPoint(name="image")
        fault = f"the image does not build: {_last_line(build.output_tail)}"
        return tag, ProjectPoint(name="image", faults=[fault])

    def _sync(
        self, containers: ContainerRuns, path: str, definition: PipelineDefinition
    ) -> ProjectPoint:
        if definition.make_file is None:
            script, arguments = SYNC_MAKE, [WORK_CHECKOUT]
        else:
            script, arguments = NAMED_SYNC_MAKE, [WORK_CHECKOUT, definition.make_file]
        command = [SHELL, "-c", _LIVE_SYNC_PREPARATION + script, _SYNC_SCRIPT_NAME, *arguments]
        environment = {**self._extra_environment, **SYNC_ENVIRONMENT, "PATH": path}
        time_limit = command_time_limit(definition, _SYNC)
        return _point(
            _SYNC,
            lambda: self._run(containers, command, environment, time_limit, WORK),
            time_limit,
            _sync_green_fault,
        )

    def _check(
        self, containers: ContainerRuns, path: str, definition: PipelineDefinition
    ) -> ProjectPoint:
        if definition.make_file is None:
            script, arguments = CHECK_SCRIPT, [_CHECK]
        else:
            script, arguments = NAMED_CHECK_SCRIPT, [_CHECK, definition.make_file]
        command = [SHELL, "-c", script, CHECK_SCRIPT_NAME, "make", *arguments]
        environment = {**self._extra_environment, **CHECK_ENVIRONMENT, "PATH": path}
        time_limit = command_time_limit(definition, _CHECK)
        return _point(
            _CHECK,
            lambda: self._run(containers, command, environment, time_limit, WORK_CHECKOUT),
            time_limit,
            _check_green_fault,
        )

    def _run(
        self,
        containers: ContainerRuns,
        command: list[str],
        environment: dict[str, str],
        time_limit: timedelta,
        working_directory: str,
    ) -> ContainerResult:
        return containers.run(
            command,
            mounts=self._mounts,
            environment=environment,
            time_limit=time_limit,
            working_directory=working_directory,
        )


def _point(
    name: str,
    run: Callable[[], ContainerResult],
    time_limit: timedelta,
    green_fault: Callable[[str], str | None],
) -> ProjectPoint:
    try:
        result = run()
    except ContainerError as error:
        return _not_started(name, error)
    fault = _run_fault(result, time_limit, green_fault)
    return ProjectPoint(name=name, faults=[] if fault is None else [fault])


def _not_started(name: str, error: ContainerError) -> ProjectPoint:
    return ProjectPoint(name=name, faults=[f"could not start: {error}"])


def _run_fault(
    result: ContainerResult, time_limit: timedelta, green_fault: Callable[[str], str | None]
) -> str | None:
    if result.timed_out:
        minutes = math.ceil(time_limit.total_seconds() / 60)
        return f"timed out after {minutes} min"
    if result.exit_status != 0:
        return f"exit status {result.exit_status}: {_last_line(result.output)}"
    return green_fault(result.output)


def _sync_green_fault(output: str) -> str | None:
    if any(time.target == _SYNC for time in target_times(output)):
        return None
    return 'no line "sync: green (<seconds> s)"'


def _check_green_fault(output: str) -> str | None:
    last = _last_line(output)
    if last == _CHECK_GREEN:
        return None
    return f'the last line is not "{_CHECK_GREEN}": {last}'


def _last_line(output: str) -> str:
    # Unlike a check's summary, make's own messages count: they say why a run is red.
    lines = printed_lines(output)
    return lines[-1] if lines else ""
