"""The working branch is named by its role: the stage file reader and the evaluation's facts."""

import importlib
from collections.abc import Callable

import pytest
from pydantic import BaseModel, ValidationError

from factory.pipeline.domain.evaluation import EvaluationInput
from support.evaluation_support import DEFINITION, MAIN


def _imports_the_new_reader() -> None:
    from factory.entry.wiring import stage_file_on_work_branch  # noqa: PLC0415

    assert callable(stage_file_on_work_branch)


def _the_old_reader_is_gone() -> None:
    assert not hasattr(importlib.import_module("factory.entry.wiring"), "stage_file_on_main")


def _input_holds_the_work_commit() -> None:
    facts = EvaluationInput(definition=DEFINITION, snapshots=[], work_commit=MAIN)

    assert facts.work_commit == MAIN


def _input_refuses_the_main_commit() -> None:
    model: type[BaseModel] = EvaluationInput

    with pytest.raises(ValidationError):
        model(definition=DEFINITION, snapshots=[], main_commit=MAIN)


@pytest.mark.parametrize(
    "check",
    [
        pytest.param(_imports_the_new_reader, id="new-reader"),
        pytest.param(_the_old_reader_is_gone, id="old-reader-gone"),
        pytest.param(_input_holds_the_work_commit, id="work-commit"),
        pytest.param(_input_refuses_the_main_commit, id="main-commit-refused"),
    ],
)
def test_the_working_branch_is_named_by_its_role(check: Callable[[], None]) -> None:
    check()
