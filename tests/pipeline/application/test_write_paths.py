"""The write paths of a stage come from the pipeline definition at the stage-start commit."""

from pathlib import Path

import pytest

from factory.agents.application.write_paths import WritePathService
from factory.agents.domain.agent_runs import WritePathSettings
from factory.agents.domain.write_paths import protected_paths
from factory.hosting.adapters.git_cli import GitCli
from factory.pipeline.application.boundaries import Boundaries
from factory.pipeline.application.claims import StageStart
from factory.pipeline.domain.stops import HealthStatus
from factory.shared.domain.errors import PipelineDefinitionInvalid
from support.git_support import PIPELINE_YAML
from support.human_clone import HumanClone
from support.write_path_support import PIPELINE_FILE, push_definition, stage_start

PATH = "factory/features/F0001-example/in-progress/F0001-S0001-first.md"
FEATURE = "factory/features/F0001-example"
WIDENED_YAML = PIPELINE_YAML.replace(
    'tester: {write_paths: ["tests/*"]}', 'tester: {write_paths: ["tests/*", "src/*"]}'
)
BROKEN_NEXT_YAML = PIPELINE_YAML.replace(
    "intake: {role: intake, next: [tests]}", "intake: {role: intake, next: [nowhere]}"
)
MAKE_FILE = "factory/Makefile"
MAKE_FILE_YAML = f"make_file: {MAKE_FILE}\n{PIPELINE_YAML}"
FOREIGN_PLACEHOLDER_YAML = PIPELINE_YAML.replace(
    'tester: {write_paths: ["tests/*"]}', 'tester: {write_paths: ["{stage}/*"]}'
)


def _expected(boundaries: Boundaries, write_paths: list[str]) -> WritePathSettings:
    return WritePathSettings(
        root=boundaries.checkout, write_paths=write_paths, protected_paths=protected_paths(None)
    )


@pytest.mark.parametrize(
    ("stage", "write_paths"),
    [("tests", ["tests/*"]), ("intake", [PATH])],
)
def test_at_returns_the_role_write_paths_with_the_work_item_expanded(
    boundaries: Boundaries, checkout: GitCli, stage: str, write_paths: list[str]
) -> None:
    settings = WritePathService(boundaries).at(stage_start(checkout, stage), PATH)

    assert settings == _expected(boundaries, write_paths)
    assert settings.root == boundaries.checkout
    assert settings.protected_paths == protected_paths(None)


def test_at_expands_the_feature_to_the_feature_path(
    boundaries: Boundaries, checkout: GitCli
) -> None:
    settings = WritePathService(boundaries).at(stage_start(checkout, "acceptance"), PATH)

    assert settings.write_paths == [PATH, f"{FEATURE}/backlog/*"]


def test_at_reads_the_definition_as_it_was_at_the_stage_start_commit(
    boundaries: Boundaries, checkout: GitCli, human: HumanClone
) -> None:
    service = WritePathService(boundaries)
    earlier = stage_start(checkout, "tests")
    push_definition(human, checkout, WIDENED_YAML)
    later = stage_start(checkout, "tests")

    assert later.commit != earlier.commit
    assert service.at(earlier, PATH).write_paths == ["tests/*"]
    assert service.at(later, PATH).write_paths == ["tests/*", "src/*"]


def test_at_ignores_the_work_tree_copy_of_the_definition(
    boundaries: Boundaries, checkout: GitCli
) -> None:
    service = WritePathService(boundaries)
    start = stage_start(checkout, "tests")
    original = service.at(start, PATH)
    work_tree_file = boundaries.checkout / PIPELINE_FILE

    work_tree_file.write_text(WIDENED_YAML.replace('"tests/*"', '"*"'), encoding="utf-8")
    widened = service.at(start, PATH)
    work_tree_file.write_text("stages: [unclosed\n  : :\n", encoding="utf-8")
    broken = service.at(start, PATH)
    work_tree_file.unlink()
    deleted = service.at(start, PATH)

    assert original == _expected(boundaries, ["tests/*"])
    assert widened == original
    assert broken == original
    assert deleted == original


def test_at_refuses_a_commit_without_the_definition(
    boundaries: Boundaries, checkout: GitCli
) -> None:
    claim = stage_start(checkout, "tests").claim
    (boundaries.checkout / PIPELINE_FILE).unlink()
    commit = checkout.commit("remove the pipeline definition")

    with pytest.raises(PipelineDefinitionInvalid, match=r"factory/pipeline\.yml"):
        WritePathService(boundaries).at(StageStart(commit=commit, claim=claim), PATH)


def test_at_refuses_an_invalid_definition_at_the_commit(
    boundaries: Boundaries, checkout: GitCli, human: HumanClone
) -> None:
    push_definition(human, checkout, BROKEN_NEXT_YAML)

    with pytest.raises(PipelineDefinitionInvalid):
        WritePathService(boundaries).at(stage_start(checkout, "tests"), PATH)


@pytest.mark.parametrize("stage", ["unknown", "approval"])
def test_at_refuses_a_stage_that_is_missing_or_has_no_role(
    boundaries: Boundaries, checkout: GitCli, stage: str
) -> None:
    with pytest.raises(PipelineDefinitionInvalid, match=stage):
        WritePathService(boundaries).at(stage_start(checkout, stage), PATH)


@pytest.mark.parametrize(
    "path",
    [
        "docs/a.md",
        "factory/features/F0004-x/other/a.md",
        "factory/features/F0004-x/in-progress/a.md",
    ],
)
def test_at_refuses_a_path_that_is_no_work_item_path(
    boundaries: Boundaries, checkout: GitCli, path: str
) -> None:
    with pytest.raises(ValueError):
        WritePathService(boundaries).at(stage_start(checkout, "tests"), path)


def test_at_needs_no_installed_agent_file_and_raises_no_stop(
    boundaries: Boundaries, checkout: GitCli, agent_home: Path
) -> None:
    assert not (agent_home / "agents").exists()

    settings = WritePathService(boundaries).at(stage_start(checkout, "tests"), PATH)

    assert settings == _expected(boundaries, ["tests/*"])
    assert boundaries.health.read() == HealthStatus()


def test_at_refuses_a_foreign_placeholder_in_the_role_write_paths(
    boundaries: Boundaries, checkout: GitCli, human: HumanClone
) -> None:
    push_definition(human, checkout, FOREIGN_PLACEHOLDER_YAML)

    with pytest.raises(PipelineDefinitionInvalid, match=r"\{stage\}"):
        WritePathService(boundaries).at(stage_start(checkout, "tests"), PATH)


@pytest.mark.parametrize(
    ("committed", "work_tree", "expected"),
    [
        pytest.param(MAKE_FILE_YAML, None, protected_paths(MAKE_FILE), id="committed"),
        pytest.param(PIPELINE_YAML, MAKE_FILE_YAML, protected_paths(None), id="work-tree-only"),
        pytest.param(PIPELINE_YAML, None, protected_paths(None), id="without-the-key"),
    ],
)
def test_at_protects_the_makefile_the_definition_at_the_commit_names(
    boundaries: Boundaries,
    checkout: GitCli,
    human: HumanClone,
    *,
    committed: str,
    work_tree: str | None,
    expected: list[str],
) -> None:
    if committed != PIPELINE_YAML:
        push_definition(human, checkout, committed)
    start = stage_start(checkout, "tests")
    if work_tree is not None:
        (boundaries.checkout / PIPELINE_FILE).write_text(work_tree, encoding="utf-8")

    settings = WritePathService(boundaries).at(start, PATH)

    assert settings.protected_paths == expected
    assert (MAKE_FILE in settings.protected_paths) is (committed == MAKE_FILE_YAML)
