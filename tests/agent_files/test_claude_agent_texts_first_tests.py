"""The coder starts from the tester's named test files and still ends with `make check`."""

import re
from collections.abc import Callable

import pytest

from factory.shared.domain.sections import section_text
from support.shipped_agents import agent_body

NAMED_FILES = "test files the tester's latest entry names"
SINGLE_FILES = "`CLAUDE.md`"
TARGETS_TODAY = frozenset({"check", "lint", "test"})


def _role() -> str:
    return section_text(agent_body("coder"), "Role") or ""


def _step_one() -> str:
    stage = section_text(agent_body("coder"), "Stage") or ""
    return next((line for line in stage.splitlines() if line.startswith("1. ")), "")


@pytest.mark.parametrize("part", [_role, _step_one], ids=["role", "step-one"])
def test_the_coder_starts_with_only_the_tester_s_named_test_files(part: Callable[[], str]) -> None:
    text = part()

    assert NAMED_FILES in text
    assert "only" in text
    assert SINGLE_FILES in text


def test_the_coder_no_longer_starts_with_the_whole_suite() -> None:
    assert "Start by running `make test`" not in _role()


def test_the_coder_still_finishes_with_make_check_green() -> None:
    assert "Finish with `make check` green." in _role()


def test_the_coder_file_names_no_new_make_target_and_no_pytest_option() -> None:
    body = agent_body("coder")

    assert set(re.findall(r"`make ([a-z-]+)", body)) <= TARGETS_TODAY
    assert "pytest" not in body
