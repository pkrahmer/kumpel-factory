"""The factory's working branch is named by one constant of the paths module."""

from factory.shared.domain import paths
from factory.shared.domain.paths import WORK_BRANCH


def test_the_working_branch_is_one_constant_named_work_branch() -> None:
    assert WORK_BRANCH == "main"
    assert not hasattr(paths, "MAIN_BRANCH")
