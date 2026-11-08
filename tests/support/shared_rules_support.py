"""The texts of the shipped agent files as they stood before the shared rules moved."""

import zlib

from factory.shared.domain.sections import section_text

# The paragraphs of the shipped coder's `## Rules` section: the opening paragraphs, then R1 to R15.
RULES_BEFORE = (
    (
        "These rules apply to every agent in every stage. Stage-specific instructions are "
        "under `Stage` below; role-specific instructions under `Role`. A work item is a user "
        "story, `factory/features/<F0001-slug>/in-progress/<F0001-S0003-slug>.md`, or a "
        "feature's acceptance report beside them; its id is the file stem without the slug, "
        "`F0001-S0003`."
    ),
    (
        "Everything around your work is the factory's: it checks out the branch, opens the "
        "pull request, writes the work item's front matter and journal, commits, pushes, "
        "changes the stage and talks to the hosting service. You do the stage's work and end "
        "with a decision."
    ),
    (
        "R1. Git is the only truth. A stage starts from the committed state and carries "
        "nothing over from earlier runs."
    ),
    (
        "R2. Every stage ends with a decision and a journal entry. The decision is one of the"
        " `Allowed decisions` your prompt lists, which always include `question` (R8); when "
        "you cannot finish, that is a `question` too, and your entry says where you stopped. "
        "The entry is the text of your journal entry, without a number: what you did, why, "
        "what you rejected, what is open. The factory appends the entry, commits everything "
        "you left in the working tree, pushes and moves the work item."
    ),
    (
        "R3. One work item at a time. You work on exactly the work item named in your prompt."
        " You do not touch other work items, and you do not touch the feature's `feature.md`."
    ),
    (
        "R4. The work item is the memory. Everything the next stage needs is in the work "
        "item, through your entry: what you did, why, what you rejected, what is open. Code "
        "is not pasted into the work item; paths and commit hashes are. The reverse holds "
        "too: work items and criteria are not named in code or tests. Git links code to work "
        "items through the commit subject; a lasting reason is cited from "
        "`docs/decisions.md`."
    ),
    (
        "R5. Work item structure: the front matter and the `## Journal` section are the "
        "factory's; you never edit them, and an edit there is dropped. The `## Description` "
        "is the current meaning of the task and is rewritten when the journal changes it; a "
        "criterion the human's answer adds goes before the two closing ones (`make check` "
        "stays green, `docs:`), which stay last. No clock time in the work item: git has it. "
        "The folder is the lifecycle: `backlog/` is the human's, `in-progress/` is the "
        "pipeline's, `done/` the archive; you never move a work item."
    ),
    (
        "R6. Your prompt names the facts you need: the work item, the stage, the allowed "
        "decisions, the branch, the pull request, the round, and whatever your stage section "
        "says the factory tells you. Take them from the prompt; do not work them out from git"
        " or the hosting service. The work item itself, from its title to the end of its "
        "journal, is in your first message, in the `<work-item>` block, so you do not read it"
        " before you start; read its file again only for text you changed during the run."
    ),
    (
        "R7. The stage changes by your decision and nothing else. The factory checks it "
        "against the stage's `next` in the pipeline definition (`factory/pipeline.yml`). A "
        "forward decision waits for the stage's checks, which the factory runs itself after "
        "you (the project commands the stage lists under `checks`, such as `make check`, or "
        "`make lint` for the tests stage): red holds the work item at your stage and counts "
        "as a stall."
    ),
    (
        "R8. To ask the human, end with `question` and the question as your entry: precise, "
        "with the options you see and the one you would choose. The factory posts it on the "
        "pull request; the answer comes back as a journal entry and the stage runs again. Do "
        'not guess on anything listed under "Not without asking" in `CLAUDE.md`.'
    ),
    (
        "R9. Tests are written by the tester stage from the acceptance criteria. The coder "
        "never edits tests. A wrong test is a question (R8), not a fix; when the human's "
        "answer calls for a test change, the coder ends with `tests` and names the test and "
        "the change, and the tester makes exactly that change."
    ),
    (
        "R10. One branch per work item, checked out for you. The factory commits, pushes and "
        "moves the work item. You never push, check out, switch, merge, pull or call `gh`. "
        "You do not commit either: leave your changes in the working tree for the factory's "
        "commit. A work item's work reaches `develop` only through the human's merge of its "
        "pull request."
    ),
    (
        "R11. `make check` must be green before you hand forward; run it yourself while you "
        "work. `make check` means that command: if `make` or one of its tools is missing, end"
        " with `question` and say which; running the Makefile's commands by hand is not the "
        "check, and installing tools is not the stage's business. The factory checks the "
        "machine before it starts."
    ),
    (
        "R12. Rework rounds (review → doing, review → tests, docs → doing, "
        "smoke-test → doing, smoke-test → docs, and the human's close at the approval) "
        "share the work item's `round`, capped by the stage's `round_cap` in the "
        "pipeline definition. Your prompt names the round; on a rework round the latest "
        "entries name the findings. When the cap is passed, the factory asks the human "
        "instead of looping."
    ),
    (
        "R13. Nothing is started without the human: no story enters `in-progress/` but by "
        "their hand, no new features, no scope beyond the description. The feature's "
        "acceptance reviewer may propose stories as files in the feature's `backlog/`, on its"
        " own branch, which reach `backlog/` only when the human merges; nobody else writes "
        "there. If the description is wrong, ask."
    ),
    (
        "R14. The pipeline's own files — `factory/pipeline.yml`, `factory/story-form.md`, "
        "every feature's `feature.md`, `backlog/`, `done/` and `.claude/` — change only with "
        "the human's commit or on their explicit instruction. You write only within your "
        "write paths in the pipeline definition (`{work_item}` there is your own work item, "
        "outside its front matter and journal), nothing else: after the stage the factory "
        "takes only the changed paths your role may write and leaves every other change out, "
        "whatever tool or command made it, so a write elsewhere is lost. When the work needs "
        "a path outside your write paths, end with `question` and name it. Make temporary "
        "files with `mktemp` or `tempfile`; they are lost with the stage."
    ),
    (
        "R15. A project may bring its own skills under `.claude/skills/` and its own agents "
        "under `factory/agents/`; both are the human's files, like `CLAUDE.md`, and you never"
        " write them. When your tools include `Skill`, load a project skill whose description"
        " fits your work. Where a skill contradicts these instructions (it runs `make check` "
        "in the background, commits, pushes, or writes outside your write paths), these "
        "instructions win: follow them, and name in your entry the skill and the step you set"
        " aside."
    ),
)
OLD_PLACE_SENTENCE = (
    "Stage-specific instructions are under `Stage` below; role-specific instructions under `Role`."
)


def text_checksum(text: str) -> int:
    """A checksum of this text, so that a test pins a long text by a short number."""
    return zlib.crc32(text.encode("utf-8"))


def opening_text(body: str) -> str:
    """The text of an agent file's body before its first section, blank edges trimmed."""
    return body.split("\n## ", 1)[0].strip()


def own_parts(body: str) -> dict[str, int]:
    """The checksum of each part an agent file keeps: its opening and its own sections."""
    parts = {"opening": text_checksum(opening_text(body))}
    for heading in ("Role", "Stage", "Lessons"):
        text = section_text(body, heading)
        if text is not None:
            parts[heading] = text_checksum(text)
    return parts


# The checksums of each shipped agent file's own parts before the shared rules moved.
PARTS_BEFORE: dict[str, dict[str, int]] = {
    "intake": {"opening": 4094730114, "Stage": 2642281601, "Lessons": 2432462968},
    "tester": {
        "opening": 3972991499,
        "Role": 126951652,
        "Stage": 1483730218,
        "Lessons": 1459710826,
    },
    "coder": {"opening": 2541228184, "Role": 536293745, "Stage": 3093711021, "Lessons": 974268139},
    "reviewer": {
        "opening": 715436559,
        "Role": 992493990,
        "Stage": 1905995793,
        "Lessons": 1263948714,
    },
    "documenter": {
        "opening": 271755649,
        "Role": 4222941419,
        "Stage": 802983054,
        "Lessons": 3170124113,
    },
    "smoke-tester": {"opening": 2579831006, "Stage": 748053419, "Lessons": 1142280369},
    "acceptance-reviewer": {
        "opening": 1692244354,
        "Role": 1910490742,
        "Stage": 424571643,
        "Lessons": 780313483,
    },
}
