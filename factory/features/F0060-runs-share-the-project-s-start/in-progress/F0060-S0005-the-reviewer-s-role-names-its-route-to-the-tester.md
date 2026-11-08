---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 682
comments_read: [6727864627]
handed_over: approval
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
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T22:14:16.468777Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T22:14:18.982510Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T22:14:39.832988Z'
  stage: intake
  run: 01c7ace9b15447a0b444657abce5bc03
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T22:14:45.353712Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T22:19:29.836597Z'
  stage: tests
  run: 0dd4e3ee161d44b5b760920f93abefa6
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T22:19:35.173410Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-08T22:22:05.332147Z'
  stage: doing
  run: 5c40ce28840d4a56a610ca62f4f7cf5d
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-08T22:22:10.661622Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-08T22:22:36.494619Z'
  stage: review
  run: f6ebcca8a47d4150991ea8d06f26bf70
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-08T22:22:41.650684Z'
  stage: docs
- number: 14
  speaker: documenter
  kind: result
  at: '2026-11-08T22:26:43.506961Z'
  stage: docs
  run: d81fcdc3f2794932af6e1511985f72a9
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-08T22:26:48.402929Z'
  stage: smoke-test
- number: 16
  speaker: smoke-tester
  kind: result
  at: '2026-11-08T22:29:07.377119Z'
  stage: smoke-test
  run: 547adf6589e541e4ab3aa75eb9d590ac
---

# The reviewer's role names its route to the tester

## Description

F0060-S0003 gave the reviewer a third way out, `tests`, in step 4 of its `## Stage`, but its `## Role` still says "Your recommendation is your decision: `docs` passes, `doing` sends the work item back", and the notes paragraph says a point on an acceptance criterion "sends it back with `doing`": the two sentences a reviewer reads first name only the old route, while step 4 says otherwise (noted by the reviewer and the coder of S0003, entries 22, 24, 28 and 30). After this story both `## Role` sentences name the route to the tester as step 4 states it, so that the reviewer's text says one thing; step 4 itself and the `### docs-review` subsection stay as they are. The operator guide describes the reviewer's ways out beside the smoke tester's, and the operator guide's sentence on the template's `review` says what the template holds once the human has added `tests` to it. Before it starts: the human's change after S0003 (`tests` as the third `next` of `review` in the three pipeline definitions) is on `develop`.

## Interface

- `agents/agents/reviewer.md`, `## Role`:
  - The recommendation sentence becomes: "Your recommendation is your decision: `docs` passes, `doing` sends the work item back, and `tests` sends it to the tester when step 4 of the Stage allows it." The sentence after it ("Never both, …") stays.
  - In the notes paragraph, "is still a finding and sends it back with `doing`" becomes "is still a finding and sends it back, with `doing` or, by step 4 of the Stage, with `tests`".
- The leave for earlier tests (the human, journal entry 4): `_RECOMMENDATION` and `_NOTES` of `tests/agent_files/test_claude_agent_texts_review_leave.py` take the new sentences; if F0060-S0004 is not merged first, the reviewer's `Role` checksum in `PARTS_BEFORE` of `tests/support/shared_rules_support.py` takes the new text's, and `test_the_rest_of_the_reviewer_body_is_unchanged` of `tests/agent_files/test_claude_agent_texts_review_groups.py` maps the new sentences back to the earlier ones by `.replace`; any other earlier test whose only failure is this story's change of the reviewer's `## Role` is updated the same way, and the tester's entry names it; each test keeps its name and checks the same thing.
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
4. 2026-11-08 human: (a). The proposed words are my leave, with `tests/agent_files/test_claude_agent_texts_review_groups.py` named as the file of `test_the_rest_of_the_reviewer_body_is_unchanged`; also any other earlier test whose only failure is this story's change of the reviewer's `## Role`, updated the same way and named in the entry. Carry it into the Interface and drop the proposal markers.
5. factory: started intake as vm.
6. intake: accepted

   - Human's answer carried in from journal entry 4: the Interface's leave line now holds the human's leave and no longer the proposed words. It names `tests/agent_files/test_claude_agent_texts_review_groups.py` as the file of `test_the_rest_of_the_reviewer_body_is_unchanged`. It also covers any other earlier test whose only failure is this story's change of the reviewer's `## Role`, and says the tester's entry must name each one. I removed the "proposed by feature acceptance; refine before starting" marker. The Description is unchanged because the meaning of the task did not change.
   - Interface: names `agents/agents/reviewer.md` `## Role` and quotes the exact old and new text of both sentences, which match the current file. It names the earlier tests the leave covers and the new test module `tests/agent_files/test_reviewer_role_route_to_tests.py`.
   - Criteria: 1 and 2 each test both sides, the new text present exactly once and the old text gone, as rows of one parametrized test. 3 pins step 4 and `### docs-review` as unchanged. 4 is `make check` and 5 is `docs:`, the last two. Each can be tested by one test function without further decisions.
   - Smoke test: the `grep -c` command can be run and expects `1`. The pytest command passes no `-q`, which is right because `addopts` already sets it, so the summary line can be checked.
   - Docs criterion: names what the reader must know: the reviewer's ways out in `agent-runtime.md`, the template's `review` in `pipeline.md`, and the decision and its rejected alternative in `docs/decisions.md`. It dictates no sentences.
   - Architecture: the story changes agent text and tests only, with the new test under `tests/agent_files/`. No code, contract or dependency changes.
   - Scope: within F0060 (the reviewer's route to the tester) and not in its Out of scope.
   - Route: `tests`, because `agents/agents/reviewer.md` is outside the documenter's write paths.
7. factory: started tests as vm.
8. tester: Wrote the tests for the reviewer's `## Role` route to the tester, and updated the earlier tests the human's leave in journal entry 4 covers.

   - criterion 1: tests/agent_files/test_reviewer_role_route_to_tests.py::test_reviewer_role_recommendation_names_the_route_to_the_tester. Two rows: the new sentence is in `## Role` exactly once, and "`doing` sends the work item back. Never both" is in it zero times.
   - criterion 2: tests/agent_files/test_reviewer_role_route_to_tests.py::test_reviewer_role_notes_name_the_route_to_the_tester. Two rows: "with `doing` or, by step 4 of the Stage, with `tests`" is in `## Role` exactly once, and "sends it back with `doing`." is in it zero times.
   - criterion 3: tests/agent_files/test_reviewer_role_route_to_tests.py::test_reviewer_stage_step_4_and_docs_review_are_unchanged. Two rows: `## Stage` still holds step 4 word for word, and the opening of `### docs-review` (its heading and first paragraph).
   - criterion 4 (`make check`) and criterion 5 (docs): no test of their own.

   Files created: tests/agent_files/test_reviewer_role_route_to_tests.py.

   Earlier test files changed under the human's leave (journal entry 4). Each test keeps its name and checks the same thing:
   - tests/agent_files/test_claude_agent_texts_review_leave.py: `_RECOMMENDATION` and `_NOTES` now hold the new sentences.
   - tests/agent_files/test_claude_agent_texts_review_groups.py: `test_the_rest_of_the_reviewer_body_is_unchanged` now maps the two new sentences back to the earlier ones by `.replace`, before the existing replacements.
   - tests/support/shared_rules_support.py: the reviewer's `Role` checksum in `PARTS_BEFORE` changed from 992493990 to 373419100, because F0060-S0004 is not merged. I computed the new value from the reviewer text with the Interface's two changes applied.

   To check this, I applied the two changes to a scratch edit of agents/agents/reviewer.md, outside my write paths, and restored the file afterwards. With the earlier tests unchanged, that edit made exactly these earlier tests fail:
   - tests/agent_files/test_shared_rules_system_prompt.py::test_every_agent_file_keeps_its_own_sections_word_for_word_in_order[reviewer], which reads `PARTS_BEFORE`
   - tests/agent_files/test_claude_agent_texts_review_groups.py
   - tests/agent_files/test_claude_agent_texts_review_leave.py

   No other earlier test failed. With my updates and the scratch edit, all of tests/agent_files passed.

   Red run (`make test`, on the unchanged reviewer.md), failing for the right reason (wrong result, the old text is still there):
   - the new test's rows `old-sentence-gone`, `new-route-once` and `old-route-gone` fail; `new-sentence-once` failed too, by the scratch check above (the new sentence is not in the file yet)
   - test_claude_agent_texts_review_leave.py fails on the old text
   - test_every_agent_file_keeps_its_own_sections_word_for_word_in_order[reviewer] fails on the old checksum

   Every module was imported; nothing failed to import. `make lint` is green.

   For the coder: change only agents/agents/reviewer.md `## Role`, using the two sentences exactly as the Interface quotes them.

   The factory left out changes outside the write paths: agents/agents/reviewer.md.

   `lint`: lint: green (0.1 s)
9. factory: started doing as vm.
10. coder: Changed the two sentences in `## Role` of `agents/agents/reviewer.md` to the exact wording the Interface quotes. No other file changed.

    - The recommendation sentence now reads "… `doing` sends the work item back, and `tests` sends it to the tester when step 4 of the Stage allows it." The "Never both, …" sentence after it is unchanged.
    - In the notes paragraph, "sends it back with `doing`." now reads "sends it back, with `doing` or, by step 4 of the Stage, with `tests`."

    Test results:
    - First run, before the change: the tester's new test file, `test_claude_agent_texts_review_leave.py` and `test_shared_rules_system_prompt.py[reviewer]` failed on the old text, as the tester's entry expected.
    - After the change: all of `tests/agent_files` passes, and `make check` is green (`check: green`).

    Main choice: I replaced the two strings word for word and checked first that each old string occurred exactly once. I rejected rewording or merging the paragraph around them, because the tests and the Interface fix the text word for word, and step 4 and `### docs-review` have to stay as they are.

    Refactor: there is nothing to refactor, since the diff is two lines of agent text.

    The journal changed no meaning of the task, so the Description stays as it is.

    Not touched: the docs criterion (`docs/operator-guide/agent-runtime.md`, `docs/operator-guide/pipeline.md`, `docs/decisions.md`). That is the documenter's work.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
11. factory: started review as vm.
12. reviewer: no findings

    - Group 1, acceptance criteria:
      - Criterion 1: `test_reviewer_role_recommendation_names_the_route_to_the_tester` has two rows. One checks that the new sentence appears exactly once in `## Role`, the other that "`doing` sends the work item back. Never both" is gone.
      - Criterion 2: `test_reviewer_role_notes_name_the_route_to_the_tester` has two rows. One checks the new route text appears exactly once, the other that "sends it back with `doing`." is gone.
      - Criterion 3: `test_reviewer_stage_step_4_and_docs_review_are_unchanged` has two rows. They pin step 4 word for word and the heading and first paragraph of `### docs-review`. Both match `agents/agents/reviewer.md` on the branch, and the diff does not touch `## Stage`.
      - Criterion 4: the coder's entry 10 reports `make check` green.
      - Criterion 5 is the documenter's.
      - I ran the new test file and the three earlier test files the change touches (`test_claude_agent_texts_review_leave.py`, `test_claude_agent_texts_review_groups.py`, `test_shared_rules_system_prompt.py`). All pass. The smoke test's `grep -c` gives `1`.
    - Group 2, architecture: only agent text and tests change, and no code under `src/`.
    - Group 3, security: no secrets and no markers that silence a check.
    - Group 4, quality:
      - `agents/agents/reviewer.md:35` and `:37` hold exactly the two sentences the Interface quotes. The sentence "Never both, …" is unchanged.
      - The new test reuses `section_text` and `agent_body`. It copies no helper.
      - The `.replace` lines added to the review-groups test come before `untested_side_is_a_note` and map back to the earlier text that test expects. The checksum test passes.
    - Group 5, work item hygiene: the Description matches what was built. The coder's entry names the main choice (a word-for-word replacement) and what it rejected (rewording the paragraph). The docs criterion still says what the documenter must write.

    Earlier tests changed:
    - tests/agent_files/test_claude_agent_texts_review_leave.py: the human's leave, journal entry 4, carried into the Interface. `_RECOMMENDATION` and `_NOTES` take the new sentences.
    - tests/agent_files/test_claude_agent_texts_review_groups.py: the human's leave, journal entry 4, which names this file. `test_the_rest_of_the_reviewer_body_is_unchanged` maps the new sentences back to the earlier text with `.replace`.
    - tests/support/shared_rules_support.py: the human's leave, journal entry 4. The reviewer's `Role` checksum in `PARTS_BEFORE` changed because F0060-S0004 has not been merged.
13. factory: started docs as vm.
14. documenter: Wrote the docs criterion. I changed only documents, so I did not run `make check`; the factory runs the stage's checks after this. `make documents` passed: `documents ok (61.8 s)`.

    Files changed:
    - `docs/operator-guide/agent-runtime.md`: after the smoke tester's two ways out, I added the reviewer's three:
      - `docs` when there are no findings.
      - `tests` when every finding needs only the story's own tests and `review`'s `next` lists `tests`.
      - `doing` otherwise.
      Both `tests` and `doing` count as rounds.
    - `docs/operator-guide/pipeline.md`:
      - *More than one route*: the sentence about the template's `review` said it lists only `[docs, doing]`. It now says the template already lists `tests` and quotes its line from `operator/template/factory/pipeline.yml:25`. A definition whose `review` lists only `[docs, doing]` still sends every finding to `doing`.
      - Start facts: the template excerpt quoted `review` with `next: [docs, doing]`. It now shows `[docs, doing, tests]` to match the template. This is a stale quote I found while cross-reading.
    - `docs/decisions.md`: new entry "The reviewer may send findings on the story's own tests to the tester" (F0060-S0003, F0060-S0005).
      - Decision: step 4 of `## Stage` and the two `## Role` sentences.
      - Why: 58 of the 65 coder runs right after review findings in F0050 to F0059 only passed the work item on.
      - Rejected: splitting one review's findings across two stages (F0060, decision 5).

    Checked against the diff and still correct:
    - The rest of `docs/operator-guide/pipeline.md`.
    - The rest of `docs/operator-guide/agent-runtime.md`.
    - The reviewer decisions in `docs/decisions.md` around lines 581–588, 710–713, 1333 and 1368. They describe rules that still hold.
    - A search of `README.md` and `docs/` for other text naming the reviewer's ways out as only `docs` and `doing` found nothing else.

    Stale text I did not touch: none found.

    `guides`: guides: green (9.8 s)
    `secrets`: secrets: green (1.7 s)
    `documents`: documents ok (66.4 s)
15. factory: started smoke-test as vm.
16. smoke-tester: I ran both smoke test commands from the repository root, exactly as written. Both met their `Expect:` lines, so there are no findings.

    1. `grep -c '`tests` sends it to the tester when step 4 of the Stage allows it' agents/agents/reviewer.md`
       ```
       1
       ```
       Met: expected `1`.

    2. `uv run pytest tests/agent_files/test_reviewer_role_route_to_tests.py tests/agent_files/test_claude_agent_texts_review_leave.py`
       ```
       ...............                                                          [100%]
       15 passed in 0.03s
       ```
       Met: the summary line shows only `passed`, with no `failed` or `error`.

    I then compared the smoke test with the acceptance criteria and found no contradictions:
    - Criteria 1 to 3 are covered by the new test file, which passed.
    - For criterion 5 (docs), I checked the three documents:
      - `docs/operator-guide/agent-runtime.md:393` lists the reviewer's three ways out.
      - `docs/operator-guide/pipeline.md:98` quotes the template's `review` as `[docs, doing, tests]`.
      - `docs/decisions.md:1713` records the 58-of-65 reason.
    - Criterion 4: I did not run `make check`. The factory runs it after this stage.

    Findings: none.

    `check`: check: green
