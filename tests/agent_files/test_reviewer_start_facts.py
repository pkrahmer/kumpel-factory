"""The reviewer reads the diff from its start facts and runs the command only as a fallback."""

import re

import pytest

from support.shipped_agents import stage_section

_STEP = re.compile(r"^\d+\. ")


def _first_step(after_heading: str | None) -> str:
    lines = stage_section("reviewer").splitlines()
    if after_heading is not None:
        lines = lines[lines.index(after_heading) + 1 :]
    start = next(index for index, line in enumerate(lines) if line.startswith("1. "))
    step = [lines[start]]
    for line in lines[start + 1 :]:
        if not line.strip() or line.startswith("#") or _STEP.match(line):
            break
        step.append(line)
    return "\n".join(step)


@pytest.mark.parametrize(
    ("heading", "command"),
    [
        pytest.param(None, "`git diff develop...HEAD -- . ':!factory'`", id="review"),
        pytest.param(
            "### docs-review",
            "`git diff develop...HEAD -- README.md docs operator/README.md`",
            id="docs-review",
        ),
    ],
)
def test_the_reviewer_reads_the_diff_from_its_context_block_and_runs_it_only_as_fallback(
    heading: str | None, command: str
) -> None:
    step = _first_step(heading)

    assert "<context>" in step
    assert "failed:" in step
    assert "cut" in step
    assert "in your first command" not in step
    assert command in step
    assert "facts-" not in step
