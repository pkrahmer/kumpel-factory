# SPDX-License-Identifier: Apache-2.0
"""The rules of the conformance check: makefile targets and includes, faults, the report."""

import re
from collections.abc import Collection, Sequence

from pydantic import BaseModel, ConfigDict

from factory.agents.domain.write_paths import matches_any
from factory.pipeline.domain.pipeline_definition import PipelineDefinition

POINT_NAMES: tuple[str, ...] = (
    "pipeline definition",
    "makefile",
    "stage file",
    "agents",
    "write paths",
    "forms",
)
# The points of the live part, which runs the repository in containers after the static part.
LIVE_POINT_NAMES: tuple[str, ...] = ("image", "sync", "check")
MAKEFILE = "Makefile"
SYNC_COMMAND = "sync"

_NAME = r"[A-Za-z0-9_.\-]+"
# The colon must not start an assignment (`:=`, `::=`), so neither colon may be followed by
# another colon or `=` once the match is made.
_RULE_LINE = re.compile(rf"^(?P<names>{_NAME}(?:[ \t]+{_NAME})*)[ \t]*(?:::|:)(?![:=])")
_INCLUDE_LINE = re.compile(r"^(?P<keyword>include|-include|sinclude)[ \t]+(?P<paths>.*)$")
_OPTIONAL_KEYWORDS = ("-include", "sinclude")
_COMMENT = "#"
_VARIABLE = "$"
_PLACEHOLDER_START = "{"
_SKIPPED = "skipped: no valid pipeline definition"


class ProjectPoint(BaseModel):
    """One point of the check: its name, its faults, and whether it was not judged."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    faults: list[str] = []
    skipped: bool = False


class MakefileInclude(BaseModel):
    """One path a makefile includes, and whether a missing file is no error."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    path: str
    optional: bool


def makefile_targets(text: str) -> frozenset[str]:
    """The names before the colon of every rule line of the makefile `text`."""
    targets: set[str] = set()
    for line in text.splitlines():
        match = _RULE_LINE.match(line)
        if match is not None:
            targets.update(match.group("names").split())
    return frozenset(targets)


def makefile_includes(text: str) -> list[MakefileInclude]:
    """The paths of every include line of the makefile `text`, those with a variable left out."""
    includes: list[MakefileInclude] = []
    for line in text.splitlines():
        match = _INCLUDE_LINE.match(line)
        if match is None:
            continue
        optional = match.group("keyword") in _OPTIONAL_KEYWORDS
        paths = match.group("paths").split(_COMMENT, 1)[0].split()
        includes.extend(
            MakefileInclude(path=path, optional=optional) for path in paths if _VARIABLE not in path
        )
    return includes


def target_faults(commands: Sequence[str], targets: Collection[str]) -> list[str]:
    """`no target <name>` for every command without a target, in the order of `commands`."""
    return [f"no target {command}" for command in commands if command not in targets]


def write_path_faults(definition: PipelineDefinition, tracked: Sequence[str]) -> list[str]:
    """A fault for every write path of every role that matches no path of `tracked`."""
    faults: list[str] = []
    for role, role_definition in definition.roles.items():
        for pattern in role_definition.write_paths:
            # A placeholder is filled per work item, so no committed file need match it.
            if _PLACEHOLDER_START in pattern:
                continue
            if not any(matches_any(path, [pattern]) for path in tracked):
                faults.append(f"role {role}: write path {pattern} matches no tracked file")
    return faults


def _point_line(point: ProjectPoint) -> str:
    if point.skipped:
        return f"{point.name}: {_SKIPPED}"
    if point.faults:
        return f"{point.name}: FAIL: {'; '.join(point.faults)}"
    return f"{point.name}: ok"


def _verdict(points: Sequence[ProjectPoint]) -> str:
    count = sum(len(point.faults) for point in points)
    if count == 0:
        return "project: ready"
    noun = "fault" if count == 1 else "faults"
    return f"project: not ready ({count} {noun})"


def report_lines(points: Sequence[ProjectPoint]) -> list[str]:
    """One line per point in the given order, then the verdict."""
    return [*(_point_line(point) for point in points), _verdict(points)]


def is_ready(points: Sequence[ProjectPoint]) -> bool:
    """Whether no point has a fault."""
    return all(not point.faults for point in points)
