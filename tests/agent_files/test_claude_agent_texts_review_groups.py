"""The reviewer's checklist goes through all five groups in every review."""

import re
import zlib

import pytest

from support.shipped_agents import SHIPPED_NAMES, agent_body

_ALL_GROUPS = (
    "Checklist, in this order. Go through all of groups 1 to 5 in every review, also when an "
    "earlier group fails, and report every finding of every group in this one entry; do not "
    "pad the report. Item 6 is part of every review."
)

_STOP_AT_THE_FIRST = (
    "Checklist, in this order. Stop at the first failing group of 1 to 5 and report it; do not "
    "pad the report. Item 6 is part of every review, whichever group failed."
)

# The CRC-32 of the reviewer's body on `main` before the checklist sentence changed.
_EARLIER_BODY_CRC32 = 3903663111

# The docs route's subsection, from its heading to the next heading, which a later story added.
_DOCS_REVIEW_SUBSECTION = re.compile(r"^### docs-review\n(?:(?!#).*\n|\n)*", re.MULTILINE)

# The checklist's documents item, from its heading to the paragraph after the checklist, which a
# later story added.
_DOCUMENTS_ITEM = re.compile(
    r"^### Documents\n(?:(?!#|Write findings as a numbered list).*\n|\n)*", re.MULTILINE
)


def test_the_checklist_sentence_asks_for_all_five_groups_right_before_item_one() -> None:
    assert f"\n{_ALL_GROUPS}\n\n1. **Acceptance criteria**" in agent_body("reviewer")


def test_the_reviewer_no_longer_says_stop_at_the_first_failing_group() -> None:
    assert "Stop at the first failing group" not in agent_body("reviewer")


@pytest.mark.parametrize("name", [name for name in SHIPPED_NAMES if name != "reviewer"])
def test_no_other_agent_asks_for_all_five_groups(name: str) -> None:
    assert "Go through all of groups 1 to 5" not in agent_body(name)


def test_the_rest_of_the_reviewer_body_is_unchanged() -> None:
    body = _DOCUMENTS_ITEM.sub("", _DOCS_REVIEW_SUBSECTION.sub("", agent_body("reviewer")))
    assert body.count(_ALL_GROUPS) == 1

    untested_side_is_a_note = (
        "A point on an acceptance criterion, the architecture, security or anything under "
        "`src/` is still a finding and sends it back with `doing`. One exception holds from "
        "round 0: a side of a stated limit that has no test is a note, not a finding, when you "
        "have read the code and it handles that side as the Interface says; the note names the "
        "side, the code's location and the missing row. A side the code does not handle, or "
        "handles otherwise, is a finding."
    )
    untested_side_is_a_finding = (
        "A point on an acceptance criterion (an untested side of a stated limit among them), "
        "the architecture, security or anything under `src/` is still a finding and sends it "
        "back with `doing`."
    )
    # A later story put the work item in the first message, so the reviewer no longer reads it.
    work_item_in_the_first_message = (
        " The work item itself, from its title to the end of its journal, is in your first "
        "message, in the `<work-item>` block, so you do not read it before you start; read its "
        "file again only for text you changed during the run."
    )
    # A later story let the reviewer read the diff from its start facts: the whole of step 1
    # before its Makefile sentence goes back to the earlier text.
    review_reads_the_diff = re.compile(r"(?m)^1\. Review .*? (?=Do not read the Makefile)")
    review_reads_both = (
        "1. Review `git diff develop...HEAD -- . ':!factory'` as the role section describes; the "
        "work item is the only other input. Read both in your first command: the work item, the "
        "diff's `--stat`, and the diff without the generated files `CLAUDE.md` names and lock "
        "files (add `':!<path>'` for each; the stat still lists them). "
    )
    docs_review_reads_the_diff = (
        "1. Read `git diff develop...HEAD -- README.md docs operator/README.md` in your first "
        "command. The work item is in your first message. Nothing else is under review."
    )
    docs_review_reads_both = (
        "1. Read the work item and `git diff develop...HEAD -- README.md docs "
        "operator/README.md` in your first command. Nothing else is under review."
    )
    # The earlier body named the working branch `main`, before it became `develop`.
    earlier = (
        review_reads_the_diff.sub(lambda _: review_reads_both, body, count=1)
        .replace(_ALL_GROUPS, _STOP_AT_THE_FIRST)
        .replace(untested_side_is_a_note, untested_side_is_a_finding)
        .replace(work_item_in_the_first_message, "")
        .replace(docs_review_reads_the_diff, docs_review_reads_both)
        .replace("develop", "main")
    )

    assert zlib.crc32(earlier.encode()) == _EARLIER_BODY_CRC32
