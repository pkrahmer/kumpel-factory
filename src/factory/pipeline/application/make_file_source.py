# SPDX-License-Identifier: Apache-2.0
"""The makefile the pipeline definition on the working branch names, read through git."""

from typing import override

from factory.hosting.application.git import Git
from factory.machine.application.make_file import MakeFileSource
from factory.pipeline.application.pipeline_loading import PIPELINE_REF
from factory.shared.application.files import PipelineDefinitionReader
from factory.shared.domain.errors import GitError, PipelineDefinitionInvalid
from factory.shared.domain.paths import PIPELINE_DEFINITION_FILE


class GitMakeFileSource(MakeFileSource):
    """Reads `make_file` from the pipeline definition at `PIPELINE_REF` at every call."""

    def __init__(self, git: Git, pipeline_reader: PipelineDefinitionReader) -> None:
        """Read the definition through `git` and parse it with `pipeline_reader`."""
        self._git = git
        self._pipeline_reader = pipeline_reader

    @override
    def make_file(self) -> str | None:
        """The definition's `make_file`; `None` when the definition is missing or not valid.

        The tick stops for a missing or invalid definition on its own; make's default is then
        as good as any.
        """
        try:
            text = self._git.show_file(PIPELINE_REF, PIPELINE_DEFINITION_FILE)
        except GitError:
            return None
        if text is None:
            return None
        try:
            return self._pipeline_reader.parse(text).make_file
        except PipelineDefinitionInvalid:
            return None
