"""The allowed decisions and the prompt composed from a stage's facts."""

from typing import Any

import pytest
from pydantic import ValidationError

from factory.agents.domain.prompts import END_LINE, PromptFacts, allowed_decisions, compose_prompt
from factory.work.domain.story_form import FormFinding

PATH = "factory/features/F0001-demo/in-progress/F0001-S0003-demo.md"
BODY = """\
# Demo

## Description

Text with <angle> brackets, a `<div>` and ümlauts.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
"""
INSTRUCTIONS = "You write code.\n\n## Stage\n\n1. Do the work.\n"
WORK_ITEM_CLOSE = "</work-item>"
ROLE_CLOSE = "</role-instructions>"
MARKERS = ["<work-item", "</work-item>", "<role-instructions", "</role-instructions>"]
MODE_LINE = "Mode: a test change the human approved; the coder's journal entry 4 names it."
VALID: dict[str, Any] = {
    "work_item": "F0001-S0003",
    "path": PATH,
    "stage": "doing",
    "allowed_decisions": ["review", "tests", "question"],
    "branch": "work-item/F0001-S0003",
    "pull_request": 7,
    "round": 1,
    "body": BODY,
    "role": "coder",
    "role_instructions": INSTRUCTIONS,
}
FACT_LINES = [
    f"Work item: {PATH}",
    "Id: F0001-S0003",
    "Stage: doing",
    "Allowed decisions: review, tests, question",
    "Branch: work-item/F0001-S0003",
    "Pull request: 7",
]


def _facts(**changes: Any) -> PromptFacts:
    return PromptFacts.model_validate({**VALID, **changes})


def _lines(**changes: Any) -> list[str]:
    return _facts_part(compose_prompt(_facts(**changes))).split("\n")


def _facts_part(message: str) -> str:
    return message.split(f"{ROLE_CLOSE}\n\n", 1)[1]


def _work_item_part(message: str) -> str:
    return message[: message.index(WORK_ITEM_CLOSE)]


@pytest.mark.parametrize(
    "decisions",
    [["question"], ["doing", "question"], ["review", "tests", "question"]],
)
def test_the_message_names_each_allowed_decision(decisions: list[str]) -> None:
    (line,) = [
        line
        for line in _lines(allowed_decisions=decisions)
        if line.startswith("Allowed decisions:")
    ]
    named = [name.strip() for name in line.split(":", 1)[1].split(",")]

    assert all(decision in named for decision in decisions)


def test_allowed_decisions_are_the_next_stages_in_order_then_question() -> None:
    assert allowed_decisions(["review", "doing"]) == ["review", "doing", "question"]


def test_question_is_allowed_at_a_stage_without_next() -> None:
    assert allowed_decisions([]) == ["question"]


def test_the_prompt_holds_the_facts_line_by_line_and_ends_with_the_end_line() -> None:
    prompt = compose_prompt(_facts())

    assert _facts_part(prompt).split("\n") == [*FACT_LINES, "Round: 1", END_LINE]
    assert not prompt.endswith("\n")


def test_the_end_line_says_what_the_factory_does_after_the_agent() -> None:
    assert END_LINE == (
        "End with your decision and your journal entry; "
        "the factory commits, pushes and moves the work item."
    )


def test_no_findings_give_a_passed_format_check_after_the_round() -> None:
    lines = _lines(findings=[])

    assert lines[6:] == ["Round: 1", "Format check: passed", END_LINE]


def test_findings_are_numbered_on_one_format_check_line() -> None:
    findings = [FormFinding(line=None, message="a"), FormFinding(line=3, message="b")]

    lines = _lines(findings=findings)

    assert lines[6:] == ["Round: 1", "Format check found: 1. a 2. b", END_LINE]


def test_without_findings_the_prompt_has_no_format_check_line() -> None:
    lines = _lines(findings=None)

    assert not [line for line in lines if line.startswith("Format check")]


def test_a_test_change_adds_the_mode_line_between_round_and_format_check() -> None:
    lines = _lines(test_change_entry=4, findings=[])

    assert lines[6:] == ["Round: 1", MODE_LINE, "Format check: passed", END_LINE]


def test_without_a_test_change_the_prompt_has_no_mode_line() -> None:
    lines = _lines(test_change_entry=None, findings=[])

    assert not [line for line in lines if line.startswith("Mode:")]


@pytest.mark.parametrize(
    ("field", "value", "accepted"),
    [
        ("round", 0, True),
        ("round", -1, False),
        ("pull_request", 1, True),
        ("pull_request", 0, False),
        ("test_change_entry", 1, True),
        ("test_change_entry", 0, False),
        ("round_cap", 1, True),
        ("round_cap", 0, False),
    ],
)
def test_prompt_facts_hold_their_limits_on_both_sides(
    field: str, value: int, accepted: bool
) -> None:
    if accepted:
        assert getattr(_facts(**{field: value}), field) == value
    else:
        with pytest.raises(ValidationError):
            _facts(**{field: value})


@pytest.mark.parametrize("role", ["tester", "reviewer", "documenter"])
def test_runs_of_different_roles_share_the_message_up_to_the_end_of_the_work_item(
    role: str,
) -> None:
    coder = compose_prompt(_facts())
    other = compose_prompt(_facts(role=role, role_instructions=f"You are the {role}.\n"))

    end = coder.index(WORK_ITEM_CLOSE) + len(WORK_ITEM_CLOSE)
    assert other[:end] == coder[:end]
    assert coder != other


def test_a_new_journal_entry_keeps_the_earlier_work_item_part_as_a_prefix() -> None:
    before = compose_prompt(_facts())
    after = compose_prompt(_facts(body=f"{BODY}3. intake: accepted.\n"))

    assert after.startswith(_work_item_part(before))


def test_the_message_holds_the_work_item_then_the_role_then_the_facts_one_blank_line_apart() -> (
    None
):
    message = compose_prompt(_facts())

    assert message.startswith("<work-item>")
    opening = len("<work-item>")
    body_at = message.index(BODY)
    assert message[opening:body_at].strip() == ""
    after_body = message[body_at + len(BODY) :]
    role_open = '<role-instructions role="coder">'
    assert after_body.lstrip(" \n").startswith(f"{WORK_ITEM_CLOSE}\n\n{role_open}")
    role_at = message.index(role_open) + len(role_open)
    instructions_at = message.index(INSTRUCTIONS, role_at)
    assert message[role_at:instructions_at].strip() == ""
    after_instructions = message[instructions_at + len(INSTRUCTIONS) :]
    facts = "\n".join([*FACT_LINES, "Round: 1", END_LINE])
    assert after_instructions.lstrip(" \n") == f"{ROLE_CLOSE}\n\n{facts}"


@pytest.mark.parametrize("marker", MARKERS)
def test_a_marker_text_in_the_body_is_escaped_and_opens_no_block(marker: str) -> None:
    body = BODY.replace("Text with", f"Text with {marker} and")

    message = compose_prompt(_facts(body=body))

    assert message.count("<work-item") == 1
    assert message.count(WORK_ITEM_CLOSE) == 1
    assert message.count("<role-instructions") == 1
    assert message.count(ROLE_CLOSE) == 1
    assert f"Text with &lt;{marker[1:]} and" in message


def test_a_body_without_a_marker_text_reaches_the_message_byte_for_byte() -> None:
    message = compose_prompt(_facts())

    assert BODY in message
    assert _work_item_part(message).removeprefix("<work-item>").strip() == BODY.strip()


@pytest.mark.parametrize(
    ("round_", "cap", "line"),
    [
        (
            0,
            2,
            "Round: 0 of 2; a rework decision after round 2 makes the factory ask the human.",
        ),
        (
            1,
            2,
            "Round: 1 of 2; a rework decision after round 2 makes the factory ask the human.",
        ),
        (
            2,
            2,
            "Round: 2 of 2; a rework decision after round 2 makes the factory ask the human.",
        ),
        (0, None, "Round: 0"),
        (2, None, "Round: 2"),
    ],
)
def test_the_round_line_names_the_stages_cap_when_it_has_one(
    round_: int, cap: int | None, line: str
) -> None:
    lines = _lines(round=round_, round_cap=cap)

    assert lines == [*FACT_LINES, line, END_LINE]
