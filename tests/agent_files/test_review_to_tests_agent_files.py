"""A review whose findings need only tests goes to the tester: the agent texts and the pipeline."""

import re
from collections.abc import Callable

import pytest

from factory.shared.domain.identifiers import WorkItemId
from factory.shared.domain.paths import WORK_BRANCH
from support.proof_support import World, posts, start_story
from support.shipped_agents import shared_rules, stage_section
from support.two_routes_support import EVERY_TARGET_MAKEFILE, TWO_ROUTES, decide

NEW_LIST = (
    "R12. Rework rounds (review → doing, review → tests, docs → doing, smoke-test → doing, "
    "smoke-test → docs, and the human's close at the approval) "
)
REVIEW_TO_TESTS = TWO_ROUTES.replace(
    "review: {role: reviewer, next: [docs, doing], round_cap: 2}",
    "review: {role: reviewer, next: [docs, doing, tests], round_cap: 2}",
)
_NEGATION = re.compile(r"\b(without|not|no)\b")


def _reviewer_code_route_stage() -> str:
    """The reviewer's `## Stage` before its `### docs-review` subsection."""
    return stage_section("reviewer").split("### docs-review", 1)[0]


def _lines_naming_tests(text: str) -> list[str]:
    return [line for line in text.splitlines() if "`tests`" in line]


_AFTER_REVIEW = "When the latest result before your run is the reviewer's"


def _tester_sentence_after_review() -> str:
    """The sentence of the tester's step 0 that starts with the case after the reviewer."""
    section = stage_section("tester")
    step_zero = section[section.index("0. ") :]
    start = step_zero.find(_AFTER_REVIEW)
    if start < 0:
        return ""
    end = step_zero.find(". ", start)
    return step_zero[start:end] if end >= 0 else step_zero[start:]


@pytest.mark.parametrize(
    "holds",
    [
        pytest.param(lambda line: "allowed decisions" in line, id="allowed-decisions"),
        pytest.param(lambda line: "own story" in line, id="own-story"),
        pytest.param(lambda line: "`doing`" in line, id="doing-otherwise"),
        pytest.param(lambda line: re.search(r"\ball\b", line) is not None, id="all-findings"),
    ],
)
def test_the_reviewer_sends_findings_that_need_only_tests_to_the_tester(
    holds: Callable[[str], bool],
) -> None:
    lines = _lines_naming_tests(_reviewer_code_route_stage())

    assert any(holds(line) for line in lines)


def test_the_reviewer_sends_findings_to_doing_without_tests_among_the_allowed_decisions() -> None:
    lines = _lines_naming_tests(_reviewer_code_route_stage())

    assert any(
        "allowed decisions" in line and "`doing`" in line and _NEGATION.search(line)
        for line in lines
    )


@pytest.mark.parametrize(
    "fragment",
    [
        pytest.param("latest result before your run is the reviewer's", id="after-review"),
        pytest.param("exactly", id="exactly"),
        pytest.param("own story", id="own-story"),
        pytest.param("standing leave", id="standing-leave"),
        pytest.param("once", id="once"),
        pytest.param("end with `doing`", id="ends-with-doing"),
        pytest.param("each finding", id="each-finding"),
    ],
)
def test_the_tester_answers_the_reviewers_test_findings_and_hands_to_the_coder(
    fragment: str,
) -> None:
    assert fragment in _tester_sentence_after_review()


@pytest.mark.parametrize(
    "holds",
    [
        pytest.param(lambda rules: rules.count(NEW_LIST) == 1, id="new-list"),
        pytest.param(lambda rules: rules.count("review → tests") == 1, id="once"),
    ],
)
def test_r12_lists_review_to_tests_right_after_review_to_doing(
    holds: Callable[[str], bool],
) -> None:
    assert holds(shared_rules())


@pytest.fixture
def review_to_tests(world: World) -> WorkItemId:
    """A story started in a world whose `review` may decide `tests`, waiting at `review`."""
    world.human.push_files(
        WORK_BRANCH, {"factory/pipeline.yml": REVIEW_TO_TESTS, "Makefile": EVERY_TARGET_MAKEFILE}
    )
    story = start_story(world)
    decide(world, story, "tests", "intake")
    decide(world, story, "doing", "tests")
    decide(world, story, "review", "doing")
    return story


@pytest.mark.parametrize(
    ("reworks", "stage", "round_number", "blocked"),
    [
        pytest.param(1, "tests", 1, None, id="first-to-tests"),
        pytest.param(3, "review", 3, "round_cap", id="third-past-the-cap"),
    ],
)
def test_a_review_decision_tests_moves_to_the_tester_and_counts_a_round(
    world: World,
    review_to_tests: WorkItemId,
    *,
    reworks: int,
    stage: str,
    round_number: int,
    blocked: str | None,
) -> None:
    story = review_to_tests
    state = decide(world, story, "tests", "review")
    for _ in range(1, reworks):
        decide(world, story, "doing", "tests")
        decide(world, story, "review", "doing")
        state = decide(world, story, "tests", "review")
    if blocked is not None:
        world.tick.run()

    assert (state.stage, state.round, state.blocked) == (stage, round_number, blocked)
    assert len(posts(world, story, "round_cap")) == (1 if blocked else 0)
