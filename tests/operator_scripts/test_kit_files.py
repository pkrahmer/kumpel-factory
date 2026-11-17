"""The kit's files, and a project assembled from them judged by the project check."""

import re
from pathlib import Path

import pytest

from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.work.domain.story_form import check_story_form
from factory.work.domain.work_item import WorkItemDocument
from support.kit_support import (
    KIT,
    KIT_FILES,
    LINES,
    WRITTEN_FILES,
    Line,
    kit_pipeline_text,
    kit_project_files,
)
from support.project_check_support import ROLES, project_faults
from support.shipped_agents import ROOT

STACK_WORDS = re.compile(r"\b(uv|gradle|pytest|cmake)\b", re.IGNORECASE)
TEMPLATE_FILES = ("CLAUDE.md", "Makefile", "factory/pipeline.yml")
KIT_PROJECT_MAKEFILE = (
    "include factory/kit.mk\n"
    "sync:\n\t$(start)\n\t$(green)\n"
    "lint:\n\t$(start)\n\t$(green)\n"
    "test:\n\t$(start)\n\t$(green)\n"
    'check: lint test\n\techo "check: green"\n'
)
UNMATCHED_WRITE_PATHS: dict[Line, list[tuple[str, str]]] = {
    "thin": [
        ("builder", "src/*"),
        ("builder", "tests/*"),
        ("builder", "docs/*"),
        ("builder", "README.md"),
    ],
    "full": [
        ("tester", "tests/*"),
        ("coder", "src/*"),
        ("documenter", "README.md"),
        ("documenter", "docs/*"),
    ],
}
NO_FAULT_POINTS = ("pipeline definition", "stage file", "agents", "forms")

CRITERIA = "1. It works.\n2. `make check` stays green.\n3. docs: none."
SMOKE = "```bash\ntrue\n```\nExpect: nothing."
SECTIONS = (
    ("Description", "What it builds."),
    ("Interface", "None."),
    ("Acceptance criteria", CRITERIA),
    ("Smoke test", SMOKE),
    ("Journal", ""),
)


def _story(left_out: str | None) -> str:
    parts = ["# A story", ""]
    for heading, content in SECTIONS:
        if heading == left_out:
            continue
        parts += [f"## {heading}", ""]
        if content:
            parts += [content, ""]
    return "\n".join(parts) + "\n"


@pytest.mark.parametrize(
    ("line", "roles", "stages", "has_acceptance"),
    [
        pytest.param(
            "thin",
            {"builder", "reviewer"},
            ["doing", "review", "approval", "done"],
            False,
            id="thin",
        ),
        pytest.param("full", set(ROLES), None, True, id="full"),
    ],
)
def test_each_kit_pipeline_definition_loads_through_the_reader(
    line: Line, roles: set[str], stages: list[str] | None, has_acceptance: bool
) -> None:
    text = kit_pipeline_text(line)

    definition = RuamelPipelineDefinitionReader().parse(text)

    assert set(definition.roles) == roles
    if stages is not None:
        assert list(definition.stages) == stages
    assert (definition.acceptance_stage is not None) == has_acceptance
    assert definition.contract == "1.2"
    assert definition.make_file is None
    assert "# make_file: factory/Makefile" in text.splitlines()


@pytest.mark.parametrize("line", LINES)
def test_a_project_from_the_kit_alone_lacks_only_the_makefile_and_written_files(
    tmp_path: Path, line: Line
) -> None:
    faults = project_faults(tmp_path, kit_project_files(line))

    assert {name: faults[name] for name in NO_FAULT_POINTS} == {
        name: [] for name in NO_FAULT_POINTS
    }
    assert faults["makefile"] == ["Makefile is missing"]
    assert sorted(faults["write paths"]) == sorted(
        f"role {role}: write path {pattern} matches no tracked file"
        for role, pattern in UNMATCHED_WRITE_PATHS[line]
    )


@pytest.mark.parametrize("line", LINES)
def test_a_kit_project_with_its_makefile_and_written_files_is_ready(
    tmp_path: Path, line: Line
) -> None:
    files = {**kit_project_files(line), "Makefile": KIT_PROJECT_MAKEFILE, **WRITTEN_FILES}

    faults = project_faults(tmp_path, files)

    assert faults == {name: [] for name in faults}


@pytest.mark.parametrize(
    ("left_out", "passes"),
    [
        pytest.param(None, True, id="five-sections"),
        pytest.param("Interface", False, id="without-interface"),
    ],
)
def test_a_story_passes_the_kit_story_form_only_with_its_five_sections(
    left_out: str | None, passes: bool
) -> None:
    form = (KIT / "factory" / "story-form.md").read_text(encoding="utf-8")
    document = WorkItemDocument(state=None, body=_story(left_out), ignored_keys=[])

    findings = check_story_form(document, form, folder="backlog")

    assert (findings == []) == passes


@pytest.mark.parametrize("relative", KIT_FILES)
def test_each_kit_file_is_there_and_names_no_stack(relative: str) -> None:
    text = (KIT / relative).read_text(encoding="utf-8")

    assert text
    assert text.endswith("\n")
    assert STACK_WORDS.findall(text) == []


def test_the_template_stays_with_its_three_files() -> None:
    template = ROOT / "operator" / "template"

    assert all((template / relative).is_file() for relative in TEMPLATE_FILES)
