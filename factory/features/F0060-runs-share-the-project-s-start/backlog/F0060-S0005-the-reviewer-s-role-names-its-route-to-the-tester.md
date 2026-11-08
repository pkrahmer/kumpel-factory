# The reviewer's role names its route to the tester

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

F0060-S0003 gave the reviewer a third way out, `tests`, in step 4 of its `## Stage`, but its `## Role` still says "Your recommendation is your decision: `docs` passes, `doing` sends the work item back", and the notes paragraph says a point on an acceptance criterion "sends it back with `doing`": the two sentences a reviewer reads first name only the old route, while step 4 says otherwise (noted by the reviewer and the coder of S0003, entries 22, 24, 28 and 30). After this story both `## Role` sentences name the route to the tester as step 4 states it, so that the reviewer's text says one thing; step 4 itself and the `### docs-review` subsection stay as they are. The operator guide describes the reviewer's ways out beside the smoke tester's, and the operator guide's sentence on the template's `review` says what the template holds once the human has added `tests` to it. Before it starts: the human's change after S0003 (`tests` as the third `next` of `review` in the three pipeline definitions) is on `develop`.

## Interface

- `agents/agents/reviewer.md`, `## Role`:
  - The recommendation sentence becomes: "Your recommendation is your decision: `docs` passes, `doing` sends the work item back, and `tests` sends it to the tester when step 4 of the Stage allows it." The sentence after it ("Never both, …") stays.
  - In the notes paragraph, "is still a finding and sends it back with `doing`" becomes "is still a finding and sends it back, with `doing` or, by step 4 of the Stage, with `tests`".
- The leave for earlier tests (to be given by the human when refining; proposed words): "`_RECOMMENDATION` and `_NOTES` of `tests/agent_files/test_claude_agent_texts_review_leave.py` take the new sentences; if F0060-S0004 is not merged first, the reviewer's `Role` checksum in `PARTS_BEFORE` of `tests/support/shared_rules_support.py` takes the new text's, and `test_the_rest_of_the_reviewer_body_is_unchanged` maps the new sentences back to the earlier ones by `.replace`; each test keeps its name and checks the same thing."
- Tests: `tests/agent_files/test_reviewer_role_route_to_tests.py` for the criteria below.

## Acceptance criteria

1. The reviewer's `## Role` holds the new recommendation sentence exactly once, and no longer holds "`doing` sends the work item back. Never both": rows of one parametrized test.
2. The reviewer's `## Role` holds "with `doing` or, by step 4 of the Stage, with `tests`" exactly once, and no longer holds "sends it back with `doing`.": rows of one parametrized test.
3. Step 4 of the reviewer's `## Stage` and its `### docs-review` subsection are unchanged: each still holds the sentence it held before this story.
4. `make check` stays green.
5. docs: the operator guide's `docs/operator-guide/agent-runtime.md`, where it lists the smoke tester's two ways out, also lists the reviewer's: `docs` to pass, `tests` when every finding needs only the story's own tests and `review`'s `next` offers it, `doing` otherwise, each counting as a round where it goes back; `docs/operator-guide/pipeline.md` (*More than one route*) says what the template's `review` lists as it now stands; `docs/decisions.md` records the route from review to the tester with its reason (58 of the 65 coder runs right after review findings in F0050 to F0059 only passed the work item on) and the rejected split of one review's findings across two stages (F0060, decision 5).

## Smoke test

```bash
grep -c '`tests` sends it to the tester when step 4 of the Stage allows it' agents/agents/reviewer.md
```
Expect: `1`

```bash
uv run pytest tests/agent_files/test_reviewer_role_route_to_tests.py tests/agent_files/test_claude_agent_texts_review_leave.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal
