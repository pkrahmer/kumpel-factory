"""The installed builder serves the thin line; the installed reviewer checks a project's points."""

import dataclasses
import re
from decimal import Decimal
from pathlib import Path

import pytest

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from factory.agents.application.project_agents import ProjectAgentDefinitions
from factory.hosting.adapters.git_cli import GitCli
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.pipeline.application.boundaries import Boundaries
from factory.pipeline.application.pipeline_loading import PipelineLoader
from factory.pipeline.application.project_check import ProjectCheck
from factory.shared.domain.paths import WORK_BRANCH
from factory.shared.domain.sections import section_text
from support.git_support import AGENT_FILE
from support.human_clone import HumanClone
from support.project_check_support import committed_repository, ready_files
from support.shipped_agents import (
    AGENT_HOME,
    THIN_LINE_PIPELINE,
    agent_body,
    headings,
    stage_section,
    thin_line_definition,
)

BUILDER_TOOLS = ["Read", "Grep", "Glob", "Edit", "Bash", "Write", "Skill"]
PROJECT_BUILDER = "factory/agents/builder.md"


def _installed() -> FrontmatterAgentDefinitionReader:
    return FrontmatterAgentDefinitionReader(AGENT_HOME)


def test_the_installed_agents_name_and_read_the_builder() -> None:
    reader = _installed()

    builder = reader.read("builder")

    assert "builder" in reader.names()
    assert (builder.model, builder.effort, builder.budget_usd) == ("opus", "medium", Decimal(6))
    assert builder.tools == BUILDER_TOOLS


def test_the_builder_has_role_stage_and_lessons_and_ends_its_stage_with_review() -> None:
    body = agent_body("builder")

    assert headings(body) == ["## Role", "## Stage", "## Lessons"]
    assert "End with `review`" in stage_section("builder")


@pytest.mark.parametrize("word", ["gradle", "pytest", "cmake"])
def test_the_builder_names_no_stack(word: str) -> None:
    assert re.search(word, agent_body("builder"), re.IGNORECASE) is None


def test_the_installed_reviewer_checks_the_projects_review_points() -> None:
    body = agent_body("reviewer")
    points = section_text(body, "Stage") or ""

    assert "\n### The project's review points\n" in f"\n{points}\n"
    assert "`## Review`" in points
    assert "`CLAUDE.md`" in points.split("### The project's review points", 1)[1]


def test_the_thin_line_loads_with_the_installed_agents_alone(
    boundaries: Boundaries, human: HumanClone
) -> None:
    human.push_file(WORK_BRANCH, "factory/pipeline.yml", THIN_LINE_PIPELINE)
    boundaries.git.fetch()
    installed = dataclasses.replace(
        boundaries, agent_definitions=ProjectAgentDefinitions(boundaries.git, _installed())
    )

    assert PipelineLoader(installed).load() == thin_line_definition()


def test_the_thin_line_without_agent_files_passes_the_agents_point(tmp_path: Path) -> None:
    files = ready_files({"factory/pipeline.yml": THIN_LINE_PIPELINE})
    repository = committed_repository(tmp_path / "project", files)
    git = GitCli(repository)
    agents = ProjectAgentDefinitions(git, _installed(), ref="HEAD")

    points = ProjectCheck(git, RuamelPipelineDefinitionReader(), agents).run()

    assert not (repository / "factory" / "agents").exists()
    assert [point.faults for point in points if point.name == "agents"] == [[]]


@pytest.mark.parametrize(
    ("project_file", "instructions"),
    [
        pytest.param(AGENT_FILE, "Do the work.", id="project-builder"),
        pytest.param(None, None, id="installed-builder"),
    ],
)
def test_a_projects_builder_wins_over_the_installed_one(
    tmp_path: Path, project_file: str | None, instructions: str | None
) -> None:
    files = ready_files({"factory/pipeline.yml": THIN_LINE_PIPELINE, PROJECT_BUILDER: project_file})
    git = GitCli(committed_repository(tmp_path / "project", files))

    builder = ProjectAgentDefinitions(git, _installed(), ref="HEAD").read("builder")

    expected = instructions or _installed().read("builder").instructions
    assert builder.instructions.strip() == expected.strip()
