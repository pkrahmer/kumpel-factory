"""The conformance check over a committed repository: the six points and their faults."""

from pathlib import Path

import pytest

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from factory.agents.application.project_agents import ProjectAgentDefinitions
from factory.hosting.adapters.git_cli import GitCli
from factory.machine.domain.stage_layer import StageLayerRefused, stage_layer
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.pipeline.application.project_check import ProjectCheck
from factory.pipeline.domain.project_check import POINT_NAMES, ProjectPoint
from support.git_support import AGENT_FILE, PIPELINE_YAML, pipeline_outcome
from support.project_check_support import (
    ROLES,
    committed_repository,
    installed_home,
    ready_files,
)

REFUSED_DEFINITION = PIPELINE_YAML + "colour: red\n"
TWO_FROMS = "ARG FACTORY_BASE\nFROM ${FACTORY_BASE}\nFROM ${FACTORY_BASE}\n"
VALID_STAGE_FILE = "ARG FACTORY_BASE\nFROM ${FACTORY_BASE}\n"
WITHOUT_LINT = "check:\n\t@:\ntest:\n\t@:\nsync:\n\t@:\n"
WITHOUT_SYNC = "check:\n\t@:\nlint:\n\t@:\ntest:\n\t@:\n"
SKIPPED_WITHOUT_DEFINITION = {"makefile", "agents", "write paths"}


def _stage_reason(text: str) -> str:
    try:
        stage_layer(text, "base")
    except StageLayerRefused as error:
        return str(error)
    raise AssertionError("the stage file was accepted")


def _run(
    tmp_path: Path,
    changes: dict[str, str | None] | None = None,
    roles: tuple[str, ...] = ROLES,
) -> list[ProjectPoint]:
    repository = committed_repository(tmp_path / "project", ready_files(changes))
    home = installed_home(tmp_path / "agent-home", roles)
    git = GitCli(repository)
    agents = ProjectAgentDefinitions(git, FrontmatterAgentDefinitionReader(home), ref="HEAD")
    return ProjectCheck(git, RuamelPipelineDefinitionReader(), agents).run()


def _faults(points: list[ProjectPoint]) -> dict[str, list[str]]:
    return {point.name: point.faults for point in points}


def test_a_ready_repository_has_six_points_without_a_fault(tmp_path: Path) -> None:
    points = _run(tmp_path)

    assert [point.name for point in points] == list(POINT_NAMES)
    assert all(point.faults == [] and not point.skipped for point in points)


@pytest.mark.parametrize(
    ("changes", "roles", "point", "expected"),
    [
        pytest.param(
            {"factory/pipeline.yml": None},
            ROLES,
            "pipeline definition",
            ["factory/pipeline.yml is missing"],
            id="missing-definition",
        ),
        pytest.param(
            {"factory/pipeline.yml": REFUSED_DEFINITION},
            ROLES,
            "pipeline definition",
            [pipeline_outcome(REFUSED_DEFINITION)],
            id="refused-definition",
        ),
        pytest.param(
            {"Makefile": None}, ROLES, "makefile", ["Makefile is missing"], id="no-makefile"
        ),
        pytest.param(
            {"Makefile": WITHOUT_LINT}, ROLES, "makefile", ["no target lint"], id="no-lint"
        ),
        pytest.param(
            {"Makefile": WITHOUT_SYNC}, ROLES, "makefile", ["no target sync"], id="no-sync"
        ),
        pytest.param(
            {"factory/stage.Containerfile": TWO_FROMS},
            ROLES,
            "stage file",
            [_stage_reason(TWO_FROMS)],
            id="two-froms",
        ),
        pytest.param(
            {},
            tuple(role for role in ROLES if role != "reviewer"),
            "agents",
            ["role reviewer: no agent file"],
            id="role-without-agent",
        ),
        pytest.param(
            {"factory/agents/coder.md": "No front matter.\n"},
            ROLES,
            "agents",
            None,
            id="project-agent-without-front-matter",
        ),
        pytest.param(
            {"docs/d.md": None},
            ROLES,
            "write paths",
            ["role documenter: write path docs/* matches no tracked file"],
            id="write-path-matches-nothing",
        ),
        pytest.param(
            {"factory/feature-form.md": None},
            ROLES,
            "forms",
            ["factory/feature-form.md is missing"],
            id="no-feature-form",
        ),
        pytest.param(
            {"factory/stage.Containerfile": VALID_STAGE_FILE},
            ROLES,
            None,
            [],
            id="valid-stage-file",
        ),
    ],
)
def test_each_fault_turns_its_point_and_no_other(
    tmp_path: Path,
    changes: dict[str, str | None],
    roles: tuple[str, ...],
    point: str | None,
    expected: list[str] | None,
) -> None:
    faults = _faults(_run(tmp_path, changes, roles))

    for name in POINT_NAMES:
        if name != point:
            assert faults[name] == [], name
    if point is None:
        return
    if expected is None:
        # The reader's own words follow the role; the role and one fault are what counts.
        assert len(faults[point]) == 1
        assert faults[point][0].startswith("role coder: ")
        assert faults[point][0] != "role coder: no agent file"
    else:
        assert faults[point] == expected


@pytest.mark.parametrize(
    "changes",
    [
        pytest.param({"factory/pipeline.yml": None}, id="missing"),
        pytest.param({"factory/pipeline.yml": REFUSED_DEFINITION}, id="refused"),
    ],
)
def test_without_a_valid_definition_three_points_are_skipped_and_two_judged(
    tmp_path: Path, changes: dict[str, str | None]
) -> None:
    judged = {
        **changes,
        "factory/stage.Containerfile": TWO_FROMS,
        "factory/feature-form.md": None,
    }
    points = {point.name: point for point in _run(tmp_path, judged)}

    assert {name for name, point in points.items() if point.skipped} == SKIPPED_WITHOUT_DEFINITION
    for name in SKIPPED_WITHOUT_DEFINITION:
        assert points[name].faults == []
    assert points["stage file"].faults == [_stage_reason(TWO_FROMS)]
    assert points["forms"].faults == ["factory/feature-form.md is missing"]


@pytest.mark.parametrize(
    ("files", "expected"),
    [
        pytest.param(
            {"Makefile": "include factory/kit.mk\ncheck lint test:\n", "factory/kit.mk": "sync:\n"},
            [],
            id="target-in-included-file",
        ),
        pytest.param(
            {
                "Makefile": "include factory/kit.mk\ncheck lint:\n",
                "factory/kit.mk": "include factory/deep.mk\ntest:\n",
                "factory/deep.mk": "sync:\n",
            },
            [],
            id="target-two-levels-down",
        ),
        pytest.param(
            {"Makefile": "include factory/kit.mk\ncheck lint test sync:\n"},
            ["Makefile: included file factory/kit.mk is missing"],
            id="missing-include",
        ),
        pytest.param(
            {"Makefile": "-include factory/kit.mk\ncheck lint test sync:\n"},
            [],
            id="missing-optional-include",
        ),
        pytest.param(
            {
                "Makefile": "include factory/kit.mk\ncheck lint test sync:\n",
                "factory/kit.mk": "include factory/deep.mk\n",
            },
            ["factory/kit.mk: included file factory/deep.mk is missing"],
            id="missing-nested-include",
        ),
        pytest.param(
            {"Makefile": "include a.mk\ncheck lint test:\n", "a.mk": "include Makefile\nsync:\n"},
            [],
            id="include-cycle",
        ),
        pytest.param(
            {"Makefile": "include ../common.mk\ncheck lint test sync:\n"},
            ["Makefile: included file ../common.mk is missing"],
            id="include-outside-the-repository",
        ),
        pytest.param(
            {"Makefile": "-include ../common.mk\ncheck lint test sync:\n"},
            [],
            id="optional-include-outside-the-repository",
        ),
        pytest.param(
            {
                "Makefile": "include ./factory/kit.mk\ncheck lint test:\n",
                "factory/kit.mk": "sync:\n",
            },
            [],
            id="include-with-dot-slash",
        ),
    ],
)
def test_targets_count_through_included_files(
    tmp_path: Path, files: dict[str, str | None], expected: list[str]
) -> None:
    faults = _faults(_run(tmp_path, files))

    assert faults["makefile"] == expected


def test_a_project_agent_counts_only_when_committed(tmp_path: Path) -> None:
    without_coder = tuple(role for role in ROLES if role != "coder")
    committed = _faults(
        _run(tmp_path / "committed", {"factory/agents/coder.md": AGENT_FILE}, without_coder)
    )
    repository = committed_repository(tmp_path / "uncommitted" / "project", ready_files())
    (repository / "factory" / "agents").mkdir(parents=True)
    (repository / "factory" / "agents" / "coder.md").write_text(AGENT_FILE, encoding="utf-8")
    home = installed_home(tmp_path / "uncommitted" / "agent-home", without_coder)
    git = GitCli(repository)
    agents = ProjectAgentDefinitions(git, FrontmatterAgentDefinitionReader(home), ref="HEAD")
    uncommitted = _faults(ProjectCheck(git, RuamelPipelineDefinitionReader(), agents).run())

    assert committed["agents"] == []
    assert uncommitted["agents"] == ["role coder: no agent file"]
