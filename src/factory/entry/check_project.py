# SPDX-License-Identifier: Apache-2.0
"""The project check command: whether the commit at `HEAD` of a repository is ready."""

import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from factory.entry.wiring import build_agent_definitions, build_pipeline_definition_reader
from factory.hosting.adapters.git_cli import GitCli
from factory.pipeline.application.project_check import ProjectCheck
from factory.pipeline.domain.project_check import is_ready, report_lines
from factory.shared.domain.errors import GitError
from factory.shared.domain.settings import AGENT_HOME_VARIABLE

_USAGE = "usage: factory-check-project [--agent-home <dir>] <folder>"
_AGENT_HOME_OPTION = "--agent-home"
_REF = "HEAD"
_READY = 0
_NOT_READY = 1
_FAILURE = 2


class _Arguments(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    folder: Path
    agent_home: Path


class _UsageError(Exception):
    pass


def _parse(argv: Sequence[str], environ: Mapping[str, str]) -> _Arguments:
    folders: list[str] = []
    agent_home = environ.get(AGENT_HOME_VARIABLE) or None
    remaining = list(argv)
    while remaining:
        argument = remaining.pop(0)
        if argument == _AGENT_HOME_OPTION:
            if not remaining:
                raise _UsageError
            agent_home = remaining.pop(0)
        else:
            folders.append(argument)
    if len(folders) != 1 or agent_home is None:
        raise _UsageError
    return _Arguments(folder=Path(folders[0]), agent_home=Path(agent_home))


def _unreadable_reason(git: GitCli) -> str | None:
    try:
        commit = git.resolve(_REF)
    except (GitError, OSError) as error:
        return str(error)
    return f"no commit at {_REF}" if commit is None else None


def main(argv: Sequence[str] | None = None) -> int:
    """Check the repository in the folder, print the report and return the exit status."""
    try:
        arguments = _parse(sys.argv[1:] if argv is None else argv, os.environ)
    except _UsageError:
        print(_USAGE, file=sys.stderr)
        return _FAILURE
    git = GitCli(arguments.folder)
    reason = _unreadable_reason(git)
    if reason is not None:
        print(f"cannot read {arguments.folder}: {reason}", file=sys.stderr)
        return _FAILURE
    agents = build_agent_definitions(git, arguments.agent_home, _REF)
    points = ProjectCheck(git, build_pipeline_definition_reader(), agents, _REF).run()
    for line in report_lines(points):
        print(line)
    return _READY if is_ready(points) else _NOT_READY


if __name__ == "__main__":
    sys.exit(main())
