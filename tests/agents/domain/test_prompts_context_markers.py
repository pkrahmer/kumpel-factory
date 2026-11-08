"""The context markers in a work item's body and a start fact's text are escaped."""

import pytest

from factory.agents.domain.prompts import CONTEXT_LIMIT, PromptFacts, StartFact, compose_prompt
from support.first_message_support import CODER_FACTS

ROLE_CLOSE = "</role-instructions>"
CONTEXT_OPEN = '<context name="'
CONTEXT_CLOSE = "</context>"
WORK_ITEM_CLOSE = "</work-item>"
CONTEXT_MARKERS = ['<context name="x">', "</context>"]


def _facts(
    body: str | None = None,
    start_facts: list[StartFact] | None = None,
    role_instructions: str | None = None,
) -> PromptFacts:
    update: dict[str, object] = {}
    if body is not None:
        update["body"] = body
    if start_facts is not None:
        update["start_facts"] = start_facts
    if role_instructions is not None:
        update["role_instructions"] = role_instructions
    return CODER_FACTS.model_copy(update=update)


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


def test_a_context_marker_before_the_cut_is_escaped() -> None:
    extra = 5
    kept = "x = '</context>'\n"
    output = kept + "a" * (CONTEXT_LIMIT - len(kept) + extra)
    fact = StartFact(command="diff", output=output)

    message = compose_prompt(_facts(start_facts=[fact]))

    assert "x = '&lt;/context>'" in message
    cut_line = f"[{extra} more characters cut here"
    assert any(line.startswith(cut_line) for line in message.splitlines())
    assert message.count(CONTEXT_CLOSE) == 1
