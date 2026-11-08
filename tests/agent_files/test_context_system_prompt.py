"""The common system prompt names the `<context>` blocks as start facts the agent has already."""

import re

import pytest

from factory.agents.domain.prompts import SYSTEM_PROMPT
from support.shipped_agents import SYSTEM_PROMPT_FILE


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.;:])\s", " ".join(text.split()))


@pytest.mark.parametrize(
    "text",
    [SYSTEM_PROMPT_FILE.read_text(encoding="utf-8"), SYSTEM_PROMPT],
    ids=["shipped", "fallback"],
)
def test_the_system_prompt_names_the_context_blocks_as_facts_not_to_gather_again(
    text: str,
) -> None:
    sentences = [sentence for sentence in _sentences(text) if "<context>" in sentence]

    assert any("start" in sentence and "again" in sentence for sentence in sentences)
