"""The `sync` target of the Python pack's makefile, its place there and its project command in the
kit's full line."""

from collections.abc import Callable
from pathlib import Path

import pytest

from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from support.claude_stand_in import Step, read_calls
from support.shipped_agents import ROOT
from support.template_make_support import (
    KIT_MK,
    MAKEFILE,
    green_line,
    header_text,
    makefile_lines,
    run_make,
    stand_in_uv,
    template_project,
)

KIT = ROOT / "operator" / "kit"
PYTHON_SECTIONS = ROOT / "operator" / "packs" / "python" / "CLAUDE.sections.md"
FIRST_LINE = "the factory's four targets `check`, `lint`, `test` and `sync`"
FOURTH_LINE = (
    "`duplicates` is a report outside `check`; `mutants` is for a sweep by hand, never a stage."
)
FIFTH_LINE = "for a Python project with a src layout"
KIT_MK_FOUR = "defines `sync`, `lint`, `test` and `check`"


def _line_number(target: str) -> int:
    lines = makefile_lines()
    heads = [index for index, line in enumerate(lines) if line.startswith(f"{target}:")]
    assert len(heads) == 1
    return heads[0]


def _first_line_is_the_four_targets() -> None:
    assert header_text().count(FIRST_LINE) == 1


def _no_three_targets() -> None:
    for path in (MAKEFILE, KIT_MK):
        assert path.read_text(encoding="utf-8").count("three targets") == 0


def _lines_four_and_five_stay() -> None:
    assert FOURTH_LINE in header_text()
    assert FIFTH_LINE in header_text()


def _sync_lies_between_check_and_lint() -> None:
    assert _line_number("check") < _line_number("sync") < _line_number("lint")


def _rules_file_names_the_four() -> None:
    kit_mk = " ".join(KIT_MK.read_text(encoding="utf-8").replace("#", " ").split())
    assert kit_mk.count(KIT_MK_FOUR) == 1
    for path in (KIT / "CLAUDE.md", PYTHON_SECTIONS):
        assert path.read_text(encoding="utf-8").count("names `check`, `lint` and `test`") == 0


@pytest.mark.parametrize(
    "check",
    [
        pytest.param(_first_line_is_the_four_targets, id="first-line"),
        pytest.param(_no_three_targets, id="no-three-targets"),
        pytest.param(_lines_four_and_five_stay, id="lines-four-and-five"),
        pytest.param(_sync_lies_between_check_and_lint, id="sync-after-check-before-lint"),
        pytest.param(_rules_file_names_the_four, id="rules-file"),
    ],
)
def test_template_says_the_contract_is_four_targets(check: Callable[[], None]) -> None:
    check()


@pytest.mark.parametrize(("status", "exit_status"), [(0, 0), (1, 2)])
def test_sync_runs_uv_sync_frozen_once_and_says_green(
    tmp_path: Path, status: int, exit_status: int
) -> None:
    template_project(tmp_path)
    stand_in_uv(tmp_path, [Step(exit_status=status)] * 2)

    result = run_make(tmp_path, "sync")

    assert result.exit_status == exit_status, result.stdout
    assert [call.arguments for call in read_calls(tmp_path / "bin")] == [["sync", "--frozen"]]
    if status == 0:
        assert green_line("sync").match(result.stdout.splitlines()[-1]), result.stdout
    else:
        assert "green" not in result.stdout


def test_template_pipeline_definition_names_sync_and_no_stage_lists_it() -> None:
    text = (KIT / "factory" / "pipeline.full.yml").read_text(encoding="utf-8")

    definition = RuamelPipelineDefinitionReader().parse(text)

    assert list(definition.project_commands) == [
        *["check", "lint", "test", "sync"],
        *["facts-diff", "facts-changes", "facts-files"],
    ]
    sync = definition.project_commands["sync"]
    assert sync.time_limit == 5
    assert sync.not_read == []
    for stage in definition.stages.values():
        assert "sync" not in stage.checks
        assert "sync" not in stage.reports
