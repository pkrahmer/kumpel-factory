"""The reviewer's Role names its route to the tester as step 4 of its Stage states it."""

import pytest

from factory.shared.domain.sections import section_text
from support.shipped_agents import agent_body

_RECOMMENDATION = (
    "Your recommendation is your decision: `docs` passes, `doing` sends the work item back, and "
    "`tests` sends it to the tester when step 4 of the Stage allows it."
)
_NOTES_ROUTE = "with `doing` or, by step 4 of the Stage, with `tests`"
_STEP_4 = (
    "4. When `tests` is among the allowed decisions and every finding needs only a change to the "
    "tests of the work item's own story, end with `tests` instead of `doing`: the tester answers "
    "them, and the coder runs once after it. When any finding needs a change outside those "
    "tests, all findings go to `doing`. When `tests` is not among the allowed decisions, "
    "findings go to `doing` as before. The entry with the findings is the same either way."
)
_DOCS_REVIEW = (
    "### docs-review\n\n"
    "On the docs route the documenter wrote the whole change; you review documents, not code. In "
    "the stage `docs-review`, this subsection replaces the Role's scope, its checklist (groups 1 "
    "to 6) and its decisions, and steps 1 to 4 above."
)


def _role() -> str:
    return section_text(agent_body("reviewer"), "Role") or ""


@pytest.mark.parametrize(
    ("text", "count"),
    [
        pytest.param(_RECOMMENDATION, 1, id="new-sentence-once"),
        pytest.param("`doing` sends the work item back. Never both", 0, id="old-sentence-gone"),
    ],
)
def test_reviewer_role_recommendation_names_the_route_to_the_tester(text: str, count: int) -> None:
    assert _role().count(text) == count


@pytest.mark.parametrize(
    ("text", "count"),
    [
        pytest.param(_NOTES_ROUTE, 1, id="new-route-once"),
        pytest.param("sends it back with `doing`.", 0, id="old-route-gone"),
    ],
)
def test_reviewer_role_notes_name_the_route_to_the_tester(text: str, count: int) -> None:
    assert _role().count(text) == count


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(_STEP_4, id="step-4"),
        pytest.param(_DOCS_REVIEW, id="docs-review"),
    ],
)
def test_reviewer_stage_step_4_and_docs_review_are_unchanged(text: str) -> None:
    assert text in (section_text(agent_body("reviewer"), "Stage") or "")
