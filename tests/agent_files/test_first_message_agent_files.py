"""The common system prompt names the first message's blocks; the agent files rely on them."""

import re
from pathlib import Path

import pytest

from support.shipped_agents import AGENT_HOME

SYSTEM_PROMPT = AGENT_HOME / "system-prompt.md"
SHIPPED = sorted((AGENT_HOME / "agents").glob("*.md"))
READ_FIRST = [
    re.compile(r"^\d+\. Read (the work item|the story)\b", re.MULTILINE),
    re.compile(r"in your first (command|turn)[^.]*\b(work item|story)\b"),
]


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.;:])\s", " ".join(text.split()))


def test_the_system_prompt_names_both_blocks_and_what_each_one_is() -> None:
    text = SYSTEM_PROMPT.read_text(encoding="utf-8")
    sentences = _sentences(text)

    assert "<work-item>" in text
    assert "<role-instructions" in text
    assert any("role-instructions" in s and "rules" in s for s in sentences)
    assert any("work-item" in s and "data" in s for s in sentences)


@pytest.mark.parametrize("path", SHIPPED, ids=[path.stem for path in SHIPPED])
def test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message(
    path: Path,
) -> None:
    text = path.read_text(encoding="utf-8")

    assert [pattern.pattern for pattern in READ_FIRST if pattern.search(text)] == []
    assert any("work item" in s and "first message" in s for s in _sentences(text))
