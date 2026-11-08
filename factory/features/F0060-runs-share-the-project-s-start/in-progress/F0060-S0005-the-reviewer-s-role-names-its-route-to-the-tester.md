---
stage: intake
blocked: question
round: 0
attempts: 0
crashes: 0
pull_request: 682
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T22:12:53.881329Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T22:12:53.889053Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T22:13:28.773270Z'
  stage: intake
  run: f6509fec2afe435c91f4944f2eab0a34
  blocked: question
---

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

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Intake stopped on one point: the human has not yet given leave to change tests written by earlier stories. Everything else checks out.

   1. **The leave for earlier tests is still only proposed.** The Interface introduces the leave as "to be given by the human when refining; proposed words". The story still carries the marker "proposed by feature acceptance of 2026-11-08; refine before starting", and the journal has only "human: created". CLAUDE.md lists changing a test you did not write, beyond the standing leave to move shared helpers, under "Not without asking". This change needs that leave because it rewrites two sentences that earlier tests pin word for word:
      - `_RECOMMENDATION` and `_NOTES` in `tests/agent_files/test_claude_agent_texts_review_leave.py`.
      - The `untested_side_is_a_note` text in `test_the_rest_of_the_reviewer_body_is_unchanged`, in `tests/agent_files/test_claude_agent_texts_review_groups.py`. The proposed words name the test function but not this file.
      - The reviewer's `Role` checksum in `PARTS_BEFORE` of `tests/support/shared_rules_support.py`. F0060-S0004 is still in `backlog/`, so the "if S0004 is not merged first" condition applies.

      Options:
      - (a) Confirm the proposed words as your leave, with `tests/agent_files/test_claude_agent_texts_review_groups.py` named as the file of `test_the_rest_of_the_reviewer_body_is_unchanged`. I would carry that wording into the Interface and drop the "proposed" and "refine before starting" lines. **This is the one I would choose.**
      - (b) Merge F0060-S0004 first and narrow the leave to the two test files.
      - (c) Reword the leave yourself.

   **Already checked, for when you answer:**
   - **Format check:** passed.
   - **Before-it-starts condition:** met. `review` lists `next: [docs, doing, tests]` in `factory/pipeline.yml`.
   - **Interface:** names the file, the section and the exact old and new sentences. The current `agents/agents/reviewer.md:35` and `:37` hold the old sentences as quoted.
   - **Criteria:** 1 and 2 each check both sides (new text present exactly once, old text gone), each one parametrized test. Criterion 3 is a single unchanged check. All are testable without further decisions.
   - **Smoke test:** both commands are runnable and both `Expect:` lines can be checked. The pytest command passes no `-q`, which is right because `pyproject.toml`'s `addopts` already sets it.
   - **Docs criterion:** names what the reader must know and dictates no sentences.
   - **Architecture:** agent text and tests only, with the new test under `tests/agent_files/`. No code change.
   - **Scope:** within F0060 and not in its Out of scope.
   - **Route:** once you answer, it would be `tests`, because `agents/agents/reviewer.md` is outside the documenter's paths.
