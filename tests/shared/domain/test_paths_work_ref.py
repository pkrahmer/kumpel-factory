"""The working branch's remote ref is one constant, and the two public refs are equal to it."""

import pytest

from factory.pipeline.application import pipeline_loading, task
from factory.shared.domain import paths


@pytest.mark.parametrize(
    "ref",
    [
        pytest.param(lambda: paths.WORK_REF, id="work-ref"),
        pytest.param(lambda: pipeline_loading.PIPELINE_REF, id="pipeline-ref"),
        pytest.param(lambda: task.FORM_REF, id="form-ref"),
    ],
)
def test_the_working_branch_s_remote_ref_is_origin_develop(ref: object) -> None:
    assert callable(ref)
    assert ref() == "origin/develop"
