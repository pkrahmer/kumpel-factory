# SPDX-License-Identifier: Apache-2.0
"""The conformance check of a repository: six points judged on the files of one commit."""

import posixpath

from factory.agents.application.agent_runtime import AgentDefinitionReader
from factory.hosting.application.git import Git
from factory.machine.domain.stage_layer import STAGE_FILE, StageLayerRefused, stage_layer
from factory.pipeline.domain.pipeline_definition import PipelineDefinition, is_inside_checkout
from factory.pipeline.domain.project_check import (
    MAKEFILE,
    POINT_NAMES,
    SYNC_COMMAND,
    ProjectPoint,
    makefile_includes,
    makefile_targets,
    target_faults,
    write_path_faults,
)
from factory.shared.application.files import PipelineDefinitionReader
from factory.shared.domain.errors import (
    AgentDefinitionError,
    AgentDefinitionMissing,
    PipelineDefinitionInvalid,
)
from factory.shared.domain.paths import (
    FEATURE_FORM_FILE,
    PIPELINE_DEFINITION_FILE,
    STORY_FORM_FILE,
)

_PIPELINE, _MAKEFILE, _STAGE_FILE, _AGENTS, _WRITE_PATHS, _FORMS = POINT_NAMES
_ALL_FILES = ""
# The rule of a stage file does not depend on the base it is built on.
_ANY_BASE = "base"


class _Makefiles:
    """The targets of a makefile and of every file it includes, and the includes that miss."""

    def __init__(self, git: Git, ref: str) -> None:
        self._git = git
        self._ref = ref
        self.targets: set[str] = set()
        self.faults: list[str] = []

    def read(self, root_text: str) -> None:
        seen = {MAKEFILE}
        pending = [(MAKEFILE, root_text)]
        while pending:
            path, text = pending.pop(0)
            self.targets.update(makefile_targets(text))
            for include in makefile_includes(text):
                relative = posixpath.normpath(include.path)
                if relative in seen:
                    continue
                seen.add(relative)
                included = self._committed(relative)
                if included is not None:
                    pending.append((relative, included))
                elif not include.optional:
                    self.faults.append(f"{path}: included file {include.path} is missing")

    def _committed(self, relative: str) -> str | None:
        # A file outside the repository is not in the commit, and git refuses to look it up.
        if not is_inside_checkout(relative):
            return None
        return self._git.show_file(self._ref, relative)


class ProjectCheck:
    """Judges whether the repository behind `git` is ready for the factory, at `ref`."""

    def __init__(
        self,
        git: Git,
        pipeline_reader: PipelineDefinitionReader,
        agents: AgentDefinitionReader,
        ref: str = "HEAD",
    ) -> None:
        """Read every file through `git` at `ref`, the agents of the roles through `agents`."""
        self._git = git
        self._pipeline_reader = pipeline_reader
        self._agents = agents
        self._ref = ref

    def run(self) -> list[ProjectPoint]:
        """The six points in the order of `POINT_NAMES`."""
        definition, pipeline_point = self._pipeline_point()
        stage_point = self._stage_point()
        forms_point = self._forms_point()
        if definition is None:
            makefile, agents, write_paths = (
                ProjectPoint(name=name, skipped=True) for name in (_MAKEFILE, _AGENTS, _WRITE_PATHS)
            )
        else:
            makefile = self._makefile_point(definition)
            agents = self._agents_point(definition)
            write_paths = self._write_paths_point(definition)
        return [pipeline_point, makefile, stage_point, agents, write_paths, forms_point]

    def _show(self, path: str) -> str | None:
        return self._git.show_file(self._ref, path)

    def _pipeline_point(self) -> tuple[PipelineDefinition | None, ProjectPoint]:
        text = self._show(PIPELINE_DEFINITION_FILE)
        if text is None:
            fault = f"{PIPELINE_DEFINITION_FILE} is missing"
            return None, ProjectPoint(name=_PIPELINE, faults=[fault])
        try:
            definition = self._pipeline_reader.parse(text)
        except PipelineDefinitionInvalid as error:
            return None, ProjectPoint(name=_PIPELINE, faults=[error.fault])
        return definition, ProjectPoint(name=_PIPELINE)

    def _makefile_point(self, definition: PipelineDefinition) -> ProjectPoint:
        text = self._show(MAKEFILE)
        if text is None:
            return ProjectPoint(name=_MAKEFILE, faults=[f"{MAKEFILE} is missing"])
        makefiles = _Makefiles(self._git, self._ref)
        makefiles.read(text)
        commands = list(definition.project_commands)
        if SYNC_COMMAND not in commands:
            commands.append(SYNC_COMMAND)
        faults = [*makefiles.faults, *target_faults(commands, makefiles.targets)]
        return ProjectPoint(name=_MAKEFILE, faults=faults)

    def _stage_point(self) -> ProjectPoint:
        text = self._show(STAGE_FILE)
        if text is None:
            return ProjectPoint(name=_STAGE_FILE)
        try:
            stage_layer(text, _ANY_BASE)
        except StageLayerRefused as error:
            return ProjectPoint(name=_STAGE_FILE, faults=[str(error)])
        return ProjectPoint(name=_STAGE_FILE)

    def _agents_point(self, definition: PipelineDefinition) -> ProjectPoint:
        faults = []
        for role in definition.roles:
            try:
                self._agents.read(role)
            except AgentDefinitionMissing:
                faults.append(f"role {role}: no agent file")
            except AgentDefinitionError as error:
                faults.append(f"role {role}: {error.fault}")
        return ProjectPoint(name=_AGENTS, faults=faults)

    def _write_paths_point(self, definition: PipelineDefinition) -> ProjectPoint:
        tracked = self._git.list_files(self._ref, _ALL_FILES)
        return ProjectPoint(name=_WRITE_PATHS, faults=write_path_faults(definition, tracked))

    def _forms_point(self) -> ProjectPoint:
        faults = [
            f"{path} is missing"
            for path in (STORY_FORM_FILE, FEATURE_FORM_FILE)
            if self._show(path) is None
        ]
        return ProjectPoint(name=_FORMS, faults=faults)
