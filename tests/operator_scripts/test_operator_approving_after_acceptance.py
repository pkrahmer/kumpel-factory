"""Kumpel's steps after a feature's acceptance name the waits the scripts impose."""

import re

import pytest

from support.operator_skill_support import SKILL

APPROVING = SKILL / "references" / "approving.md"
SECTION = "## After a feature's acceptance"
STEP = re.compile(r"(\d+)\. ")


def section_steps() -> dict[str, str]:
    """The numbered steps under the section, each with its continuation lines, by number."""
    lines = APPROVING.read_text(encoding="utf-8").splitlines()
    rest = lines[lines.index(SECTION) + 1 :]
    end = next((i for i, line in enumerate(rest) if line.startswith("## ")), len(rest))
    steps: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in rest[:end]:
        match = STEP.match(line)
        if match:
            current = steps.setdefault(match.group(1), [])
        if current is not None:
            current.append(line)
    return {number: "\n".join(text) for number, text in steps.items()}


@pytest.mark.parametrize(
    ("step", "phrase"),
    [
        pytest.param("1", "is in backlog/", id="archive-refusal-for-proposed-stories"),
        pytest.param("1", "next accepted acceptance", id="archive-waits-for-next-acceptance"),
        pytest.param("2", "promotion open: #", id="promotion-reuses-open-pull-request"),
    ],
)
def test_steps_after_an_acceptance_name_the_waits_of_the_scripts(step: str, phrase: str) -> None:
    assert phrase in section_steps()[step]
