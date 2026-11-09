"""The smoke tester's rule for a run after a `check_red` stall: where the failure goes."""

import re
from collections.abc import Callable

import pytest

from support.shipped_agents import SHIPPED_NAMES, agent_body, shared_rules, stage_section

_MARK = "check_red"


def _rule_block() -> str:
    """The paragraph of the smoke tester's Stage section (consecutive lines) naming the stall."""
    blocks = re.split(r"\n\s*\n", stage_section("smoke-tester"))
    found = [block for block in blocks if _MARK in block]
    return "\n".join(found)


def _sentences() -> list[str]:
    """The rule's sentences: split at line ends and at a full stop followed by a space."""
    parts = re.split(r"\n|(?<=\.)\s+", _rule_block())
    return [part.strip() for part in parts if part.strip()]


def _some_sentence(*words: str) -> bool:
    return any(all(word.lower() in sentence.lower() for word in words) for sentence in _sentences())


def _no_rerun(sentence: str) -> bool:
    lowered = sentence.lower()
    return (
        "smoke test" in lowered
        and "again" in lowered
        and re.search(r"\b(not|never|no)\b", lowered) is not None
    )


def _commands_are_only_make_check(block: str) -> bool:
    targets = re.findall(r"\bmake\s+([\w-]+)", block)
    return all(target == "check" for target in targets) and "uv run" not in block


@pytest.mark.parametrize(
    "holds",
    [
        pytest.param(lambda: _MARK in _rule_block(), id="names-the-stall"),
        pytest.param(lambda: any(_no_rerun(s) for s in _sentences()), id="no-rerun"),
        pytest.param(lambda: _some_sentence("failing lines"), id="reads-failing-lines"),
        pytest.param(lambda: _some_sentence("`doing`", "test"), id="doing-test"),
        pytest.param(lambda: _some_sentence("`doing`", "type"), id="doing-type"),
        pytest.param(lambda: _some_sentence("`doing`", "lint"), id="doing-lint"),
        pytest.param(lambda: _some_sentence("`doing`", "layer"), id="doing-layer"),
        pytest.param(lambda: _some_sentence("`doing`", "security"), id="doing-security"),
        pytest.param(lambda: _some_sentence("`doing`", "licence"), id="doing-licence"),
        pytest.param(lambda: _some_sentence("`doing`", "cannot place"), id="doing-unplaced"),
        pytest.param(lambda: _some_sentence("`docs`", "documenter"), id="docs-documenter"),
        pytest.param(lambda: _some_sentence("`docs`", "README"), id="docs-readme"),
        pytest.param(lambda: _some_sentence("`docs`", "guide"), id="docs-guide"),
        pytest.param(lambda: _some_sentence("`docs`", "document check"), id="docs-document-check"),
        pytest.param(lambda: _some_sentence("`docs`", "secrets"), id="docs-secrets"),
        pytest.param(lambda: _some_sentence("entry", "name", "file"), id="entry-names-failures"),
        pytest.param(lambda: _commands_are_only_make_check(_rule_block()), id="only-make-check"),
    ],
)
def test_the_smoke_tester_routes_a_red_check_without_running_the_smoke_test_again(
    holds: Callable[[], bool],
) -> None:
    assert holds()


@pytest.mark.parametrize("name", SHIPPED_NAMES)
def test_the_red_check_rule_sits_in_the_smoke_testers_stage_and_in_no_shared_rule(
    name: str,
) -> None:
    body = agent_body(name)
    assert _MARK not in shared_rules()
    if name == "smoke-tester":
        assert _MARK in stage_section(name)
        assert body.count(_MARK) == stage_section(name).count(_MARK)
    else:
        assert _MARK not in body
