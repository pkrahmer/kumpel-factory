"""The context markers in a work item's body and a start fact's text are escaped."""

from typing import Any

import pytest

from factory.agents.domain.prompts import PromptFacts, StartFact, compose_prompt

BODY = "# Demo\n\n## Description\n\nText with <angle> brackets.\n"
INSTRUCTIONS = "You test.\n"
ROLE_CLOSE = "</role-instructions>"
CONTEXT_OPEN = '<context name="'
CONTEXT_CLOSE = "</context>"
WORK_ITEM_CLOSE = "</work-item>"
CONTEXT_MARKERS = ['<context name="x">', "</context>"]
VALID: dict[str, Any] = {
    "work_item": "F0001-S0003",
    "path": "factory/features/F0001-demo/in-progress/F0001-S0003-demo.md",
    "stage": "review",
    "allowed_decisions": ["docs", "question"],
    "branch": "work-item/F0001-S0003",
    "pull_request": 7,
    "round": 0,
    "body": BODY,
    "role": "reviewer",
    "role_instructions": INSTRUCTIONS,
}


def _facts(**changes: Any) -> PromptFacts:
    return PromptFacts.model_validate({**VALID, **changes})


def _escaped(marker: str) -> str:
    return f"&lt;{marker[1:]}"


@pytest.mark.parametrize("marker", CONTEXT_MARKERS)
def test_a_context_marker_in_a_start_fact_output_is_escaped(marker: str) -> None:
    facts = [
        StartFact(command="diff", output=f"x = '{marker}'\n"),
        StartFact(command="tree", output="plain\n"),
    ]

    message = compose_prompt(_facts(start_facts=facts))

    assert message.count(CONTEXT_OPEN) == len(facts)
    assert message.count(CONTEXT_CLOSE) == len(facts)
    assert f"x = '{_escaped(marker)}'" in message


@pytest.mark.parametrize("marker", CONTEXT_MARKERS)
def test_a_context_marker_in_the_body_is_escaped_and_opens_no_block(marker: str) -> None:
    body = f"# Demo\n\nText with {marker} inside.\n"

    message = compose_prompt(_facts(body=body))

    work_item = message[: message.index(WORK_ITEM_CLOSE)]
    assert "<context" not in work_item
    assert CONTEXT_CLOSE not in work_item
    assert f"Text with {_escaped(marker)} inside." in work_item


def test_a_context_marker_in_a_failure_reason_is_escaped() -> None:
    fact = StartFact(command="diff", failure="it printed </context> and stopped")

    message = compose_prompt(_facts(start_facts=[fact]))

    lines = message.splitlines()
    assert "failed: it printed &lt;/context> and stopped" in lines
    assert message.count(CONTEXT_CLOSE) == 1


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("# Demo\n\nA context-free <div> and </contexts ümlaut.\n", id="near"),
        pytest.param("# Demo\n\nPlain text.\n", id="plain"),
    ],
)
def test_a_text_without_a_marker_reaches_the_message_byte_for_byte(text: str) -> None:
    fact = StartFact(command="diff", output=text)

    message = compose_prompt(_facts(body=text, start_facts=[fact]))

    assert f"<work-item>\n{text}{WORK_ITEM_CLOSE}" in message
    assert f'{CONTEXT_OPEN}diff">\n{text}{CONTEXT_CLOSE}' in message


def test_the_role_instructions_reach_the_message_unescaped() -> None:
    instructions = 'Blocks look like <context name="x"> and end with </context>.\n'

    message = compose_prompt(_facts(role_instructions=instructions))

    assert f"\n{instructions}{ROLE_CLOSE}" in message
