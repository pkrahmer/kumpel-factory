"""The rule on write paths that every shipped agent carries explains what becomes of a write."""

import pytest

from support.shipped_agents import SHIPPED_NAMES, WRITE_PATHS_RULE, agent_body, shared_rules

_OLD_ENDING = (
    "the kernel refuses every other write, by any tool and any command you run, and the factory "
    "undoes any other write after the stage."
)


def test_rules_hold_the_write_paths_rule_as_one_line() -> None:
    assert WRITE_PATHS_RULE in shared_rules().splitlines()


@pytest.mark.parametrize("name", SHIPPED_NAMES)
def test_old_ending_of_the_write_paths_rule_is_gone(name: str) -> None:
    assert _OLD_ENDING not in agent_body(name)


def test_write_paths_rule_appears_once() -> None:
    lines = [line for line in shared_rules().splitlines() if line.startswith("R14. ")]

    assert len(lines) == 1
