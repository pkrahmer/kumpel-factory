"""The conformance check's rules: makefile targets and includes, faults, the report."""

from collections.abc import Collection, Sequence

import pytest

from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.pipeline.domain.project_check import (
    POINT_NAMES,
    MakefileInclude,
    ProjectPoint,
    is_ready,
    makefile_includes,
    makefile_targets,
    report_lines,
    target_faults,
    write_path_faults,
)
from support.git_support import PIPELINE_YAML

ALL_TRACKED = ["src/a.py", "tests/t.py", "docs/d.md", "README.md"]


@pytest.mark.parametrize(
    ("text", "targets"),
    [
        pytest.param("check: lint\n", {"check"}, id="one-name"),
        pytest.param("a b: c\n", {"a", "b"}, id="two-names"),
        pytest.param("a\tb: c\n", {"a", "b"}, id="tab-between-names"),
        pytest.param("check : lint\n", {"check"}, id="space-before-colon"),
        pytest.param("x::\n", {"x"}, id="double-colon"),
        pytest.param("X := 1\n", set(), id="simple-assignment"),
        pytest.param("X ::= 1\n", set(), id="posix-assignment"),
        pytest.param("  y: z\n", set(), id="indented"),
        pytest.param("# c: d\n", set(), id="comment"),
        pytest.param("%.o: %.c\n", set(), id="pattern"),
        pytest.param("$(T): u\n", set(), id="variable"),
        pytest.param("src/a.o: x\n", set(), id="slash-in-name"),
    ],
)
def test_makefile_targets_are_the_names_of_rule_lines(text: str, targets: set[str]) -> None:
    assert makefile_targets(text) == frozenset(targets)


@pytest.mark.parametrize(
    ("text", "includes"),
    [
        pytest.param(
            "include a.mk b.mk\n",
            [
                MakefileInclude(path="a.mk", optional=False),
                MakefileInclude(path="b.mk", optional=False),
            ],
            id="two-paths",
        ),
        pytest.param("-include c.mk\n", [MakefileInclude(path="c.mk", optional=True)], id="dash"),
        pytest.param(
            "sinclude d.mk\n", [MakefileInclude(path="d.mk", optional=True)], id="sinclude"
        ),
        pytest.param(
            "include\te.mk\n",
            [MakefileInclude(path="e.mk", optional=False)],
            id="tab-after-keyword",
        ),
        pytest.param(
            "include a.mk # b.mk\n",
            [MakefileInclude(path="a.mk", optional=False)],
            id="comment-after-path",
        ),
        pytest.param("include $(X).mk\n", [], id="variable-path"),
        pytest.param("  include e.mk\n", [], id="indented"),
        pytest.param("included: f\n", [], id="rule-named-included"),
    ],
)
def test_makefile_includes_are_the_paths_of_include_lines(
    text: str, includes: list[MakefileInclude]
) -> None:
    assert makefile_includes(text) == includes


@pytest.mark.parametrize(
    ("commands", "targets", "faults"),
    [
        pytest.param(["check", "lint"], {"check"}, ["no target lint"], id="one-missing"),
        pytest.param(["check", "lint"], {"check", "lint"}, [], id="both-there"),
    ],
)
def test_target_faults_name_each_command_without_a_target(
    commands: Sequence[str], targets: Collection[str], faults: list[str]
) -> None:
    assert target_faults(commands, targets) == faults


@pytest.mark.parametrize(
    ("tracked", "faults"),
    [
        pytest.param(ALL_TRACKED, [], id="every-path-matches"),
        pytest.param(
            ["src/a.py", "tests/t.py", "README.md"],
            ["role documenter: write path docs/* matches no tracked file"],
            id="docs-matches-nothing",
        ),
    ],
)
def test_write_path_faults_name_write_paths_that_match_no_tracked_file(
    tracked: list[str], faults: list[str]
) -> None:
    # The definition's roles also hold {work_item} and {feature}/backlog/*, which no
    # tracked file matches and which are never judged.
    definition = RuamelPipelineDefinitionReader().parse(PIPELINE_YAML)

    assert write_path_faults(definition, tracked) == faults


def _points(**changes: ProjectPoint) -> list[ProjectPoint]:
    return [changes.get(name.replace(" ", "_"), ProjectPoint(name=name)) for name in POINT_NAMES]


@pytest.mark.parametrize(
    ("points", "lines", "ready"),
    [
        pytest.param(
            _points(),
            [*(f"{name}: ok" for name in POINT_NAMES), "project: ready"],
            True,
            id="ready",
        ),
        pytest.param(
            _points(makefile=ProjectPoint(name="makefile", faults=["no target lint"])),
            [
                "pipeline definition: ok",
                "makefile: FAIL: no target lint",
                "stage file: ok",
                "agents: ok",
                "write paths: ok",
                "forms: ok",
                "project: not ready (1 fault)",
            ],
            False,
            id="one-fault",
        ),
        pytest.param(
            _points(
                pipeline_definition=ProjectPoint(name="pipeline definition", faults=["bad"]),
                makefile=ProjectPoint(name="makefile", skipped=True),
                agents=ProjectPoint(name="agents", skipped=True),
                write_paths=ProjectPoint(name="write paths", skipped=True),
                forms=ProjectPoint(name="forms", faults=["one is missing", "two is missing"]),
            ),
            [
                "pipeline definition: FAIL: bad",
                "makefile: skipped: no valid pipeline definition",
                "stage file: ok",
                "agents: skipped: no valid pipeline definition",
                "write paths: skipped: no valid pipeline definition",
                "forms: FAIL: one is missing; two is missing",
                "project: not ready (3 faults)",
            ],
            False,
            id="three-faults-and-skipped",
        ),
    ],
)
def test_report_lines_name_each_point_and_end_with_the_verdict(
    points: list[ProjectPoint], lines: list[str], ready: bool
) -> None:
    assert report_lines(points) == lines
    assert is_ready(points) is ready
