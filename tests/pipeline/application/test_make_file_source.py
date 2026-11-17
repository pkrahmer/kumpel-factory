"""The makefile source built on git reads `make_file` from the definition at the working ref."""

from collections.abc import Callable

import pytest

from factory.hosting.adapters.git_cli import GitCli
from factory.machine.application.make_file import MakeFileSource
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.shared.domain.paths import PIPELINE_DEFINITION_FILE, WORK_BRANCH
from support.git_support import PIPELINE_YAML
from support.human_clone import HumanClone
from support.make_file_support import git_make_file_source_class

NAMED = "factory/Makefile"
MOVED = "build/factory.mk"


def _source(checkout: GitCli) -> MakeFileSource:
    source_class: Callable[..., MakeFileSource] = git_make_file_source_class()
    return source_class(checkout, RuamelPipelineDefinitionReader())


def _push_definition(human: HumanClone, checkout: GitCli, text: str) -> None:
    human.push_file(WORK_BRANCH, PIPELINE_DEFINITION_FILE, text)
    checkout.fetch()


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (f"make_file: {NAMED}\n{PIPELINE_YAML}", NAMED),
        (f"make_file: {NAMED}\n{PIPELINE_YAML}colour: red\n", None),
        (f'make_file: "  "\n{PIPELINE_YAML}', None),
        (f"{PIPELINE_YAML}# without the key\n", None),
    ],
    ids=["named", "invalid", "invalid-make-file", "without-the-key"],
)
def test_the_source_returns_the_make_file_of_the_definition_at_the_working_ref(
    human: HumanClone, checkout: GitCli, text: str, expected: str | None
) -> None:
    _push_definition(human, checkout, text)

    assert _source(checkout).make_file() == expected


def test_the_source_returns_none_for_a_missing_definition(
    human: HumanClone, checkout: GitCli
) -> None:
    human.remove_file(WORK_BRANCH, PIPELINE_DEFINITION_FILE)
    checkout.fetch()

    assert _source(checkout).make_file() is None


def test_the_source_reads_the_new_value_after_the_branch_moved(
    human: HumanClone, checkout: GitCli
) -> None:
    _push_definition(human, checkout, f"make_file: {NAMED}\n{PIPELINE_YAML}")
    source = _source(checkout)
    first = source.make_file()

    _push_definition(human, checkout, f"make_file: {MOVED}\n{PIPELINE_YAML}")

    assert (first, source.make_file()) == (NAMED, MOVED)
