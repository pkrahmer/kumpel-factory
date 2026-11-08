---
stage: doing
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 680
comments_read: [6727432579, 6727512748, 6727549619]
handed_over: null
claim:
  instance: vm
  stage: doing
  started_at: '2026-11-08T21:52:04.393259Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T21:33:18.426284Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T21:33:18.434591Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T21:33:55.543632Z'
  stage: intake
  run: 97603a93ed974bf0b6abea542a55d12c
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T21:34:40.478403Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T21:34:45.259023Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T21:35:08.115134Z'
  stage: intake
  run: d2507eff746449e19223e935164122a4
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T21:35:13.137995Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T21:37:34.392381Z'
  stage: tests
  run: df24a412196847469eb123f9488ab5d4
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T21:37:39.400730Z'
  stage: doing
- number: 10
  speaker: coder
  kind: question
  at: '2026-11-08T21:41:19.948548Z'
  stage: doing
  run: bbbe62e25d374eac87289953e5339280
  blocked: question
- number: 11
  speaker: human
  kind: comment
  at: '2026-11-08T21:43:09.824921Z'
  stage: doing
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T21:43:12.243461Z'
  stage: doing
- number: 13
  speaker: coder
  kind: result
  at: '2026-11-08T21:43:28.206691Z'
  stage: doing
  run: d9f3517b57f4404b9318547f217f248f
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-08T21:43:33.103723Z'
  stage: tests
- number: 15
  speaker: tester
  kind: question
  at: '2026-11-08T21:44:40.279304Z'
  stage: tests
  run: 6978cd659a804a55939073b7a0bb3a3d
  blocked: question
- number: 16
  speaker: human
  kind: comment
  at: '2026-11-08T21:46:30.485852Z'
  stage: tests
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-08T21:46:32.943978Z'
  stage: tests
- number: 18
  speaker: tester
  kind: result
  at: '2026-11-08T21:47:01.555317Z'
  stage: tests
  run: 4828c96f0b9d429ea27e55629a0699cc
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-08T21:47:06.755052Z'
  stage: doing
- number: 20
  speaker: coder
  kind: result
  at: '2026-11-08T21:49:44.353205Z'
  stage: doing
  run: 641f81bf68d84b27bca5112156962ca2
- number: 21
  speaker: factory
  kind: started
  at: '2026-11-08T21:49:49.496761Z'
  stage: review
- number: 22
  speaker: reviewer
  kind: result
  at: '2026-11-08T21:50:36.749550Z'
  stage: review
  run: 8c95de3a25df443fb0990706b3294c7b
- number: 23
  speaker: factory
  kind: started
  at: '2026-11-08T21:50:41.871754Z'
  stage: doing
- number: 24
  speaker: coder
  kind: result
  at: '2026-11-08T21:51:16.821590Z'
  stage: doing
  run: 4996f868724d44dd81a56559382d9794
- number: 25
  speaker: factory
  kind: started
  at: '2026-11-08T21:51:21.940446Z'
  stage: tests
- number: 26
  speaker: tester
  kind: result
  at: '2026-11-08T21:51:59.159093Z'
  stage: tests
  run: 84700a7eee6046fbbd212702f2815765
- number: 27
  speaker: factory
  kind: started
  at: '2026-11-08T21:52:04.393259Z'
  stage: doing
---

# A review whose findings need only tests goes to the tester

## Description

Most review findings are missing tests: an untested side of a rule, a criterion without its test. The reviewer can send them only to `doing`, so the coder reads them, changes nothing and passes the work item to the tester. In F0050 to F0059, 58 of the 65 coder runs right after review findings did only that. After this story the reviewer decides `tests` when `tests` is among its allowed decisions and every finding needs only a change to the tests of the work item's own story; any finding that needs a change elsewhere sends all findings to `doing`, as today. The tester, when the latest result before its run is the reviewer's, writes or changes exactly the tests those findings name and ends with `doing`, so the coder runs once, after the tester, before the next review. The rule R12 names the new rework route. Whether the review stage offers `tests` is the pipeline definition's: the human adds it to `review`'s `next` after this story, and until then, or in a project that does not add it, the reviewer keeps deciding `doing`. The coder's handling of test findings in a mixed review stays as it is.

## Interface

- `agents/agents/reviewer.md`, `## Stage`: the choice between `tests` and `doing`, as the Description says; the entry with the findings is the same in both cases.
- `agents/agents/tester.md`, `## Stage`, step 0: the case where the latest result before the tester's run is the reviewer's: the tester writes or changes exactly the tests the reviewer's findings name, only in the tests of its own story (or under the standing leave of `CLAUDE.md`), runs those test files once, and ends with `doing`; its entry names each finding and the test that answers it.
- `agents/system-prompt.md` and `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`: R12's list of rework rounds gains `review → tests`, right after `review → doing`: "Rework rounds (review → doing, review → tests, docs → doing, smoke-test → doing, smoke-test → docs, and the human's close at the approval) …"; both texts stay equal.
- Tests from earlier stories that pin R12's text (the human's leave, journal entry 4): the tester updates R12's text in `REWORK_RULE` of `tests/agent_files/test_claude_agent_texts_docs_slip.py` and in the R12 entry of `tests/support/shared_rules_support.py` to the new list; each keeps checking the same thing.
- No code of the factory changes: a decision other than the first of a stage's `next` already counts as a rework round against the stage's `round_cap`.
- Tests: `tests/agent_files/test_review_to_tests_agent_files.py` for the criteria below.

## Acceptance criteria

1. The reviewer's `## Stage` says to decide `tests` when `tests` is among the allowed decisions and every finding needs only a change to the tests of the work item's own story, and to decide `doing` with all findings when any finding needs a change outside them.
2. The reviewer's `## Stage` says that without `tests` among the allowed decisions, findings go to `doing` as before.
3. The tester's step 0 says that when the latest result before its run is the reviewer's, it writes or changes exactly the tests the findings name, only in its own story's tests or under the standing leave, runs those test files once and ends with `doing`, naming each finding and its test in the entry.
4. R12 in `agents/system-prompt.md` lists `review → tests` among the rework rounds, right after `review → doing`, and `SYSTEM_PROMPT` equals the file.
5. A pipeline definition whose `review` stage has `next: [docs, doing, tests]` and `round_cap: 2` moves a work item from `review` to `tests` on the decision `tests` and counts one round; a third rework from `review` is held at `round_cap`: rows of one parametrized test.
6. `make check` stays green.
7. docs: the operator guide (`docs/operator-guide/pipeline.md`, the stages and their routes) says that the review stage may send a work item to the tester when its findings need only tests, that this needs `tests` in `review`'s `next`, and that it counts as a rework round.

## Smoke test

```bash
grep -c 'review → tests' agents/system-prompt.md
```
Expect: `1`

```bash
uv run pytest tests/agent_files/test_review_to_tests_agent_files.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Intake: the format check passed. I checked the rest of the story (Interface, criteria 1 to 5, smoke test, docs criterion, architecture, scope against F0060's feature.md and its decision 5). All of it is buildable except one point: the story changes R12, and tests from earlier stories pin R12's exact wording. Under `CLAUDE.md` ("Not without asking": a change to a test you did not write), that needs your leave.

   1. Criterion 4 adds `review → tests` to R12 in `agents/system-prompt.md` and `SYSTEM_PROMPT`. Two places from earlier stories hold R12's current text word for word:
      - `tests/agent_files/test_claude_agent_texts_docs_slip.py`: the constant `REWORK_RULE` (line 9), and the assertion `rules.count(REWORK_RULE) == 1` (line 67).
      - `tests/support/shared_rules_support.py`: the R12 entry of the rules table (line 98), which `tests/agent_files/test_shared_rules_system_prompt.py` checks against the system prompt.
      With the new R12 both fail, so `make check` (criterion 6) cannot be green unless they change. The story names neither, and the standing leave to move shared helpers does not cover changing their text. Options:
      (a) Give leave for the tester to update R12's text in those two places to the new list (`review → doing, review → tests, docs → doing, …`, or wherever you want `review → tests` in the list), each still checking the same thing. Add this to the story as an Interface line, and say where in R12's list `review → tests` goes.
      (b) Have this story leave R12 alone, and make the R12 change in a separate story.
      I would choose (a). Please also say where in the list the new route goes, so the coder and the tester read it the same way. The `grep -c 'review → tests'` smoke test does not pin that.
   2. Not for this story, but related: `test_the_template_lets_the_smoke_test_hand_a_slip_to_docs_and_keeps_every_other_next` in `test_claude_agent_texts_docs_slip.py` asserts that `operator/template/factory/pipeline.yml`'s `review` has `next == ["docs", "doing"]`. The change you plan to make by hand after this story (`next: [docs, doing, tests]` in the template) will break it on `develop`. Should this story also get leave to update that expectation now? Options: (a) yes, but only once the template changes, which means the test changes together with your commit; (b) you change the test yourself together with the template. I would choose (b), since this story must not change the template (R14).

   Everything else is ready for the `tests` route once the answer is in:
   - Interface: names the agent files, their sections, and `SYSTEM_PROMPT` in `prompts.py`, and says that no factory code changes. The pipeline already counts a decision other than a stage's first `next` as a rework round.
   - Criteria: each can be tested by one function. Criterion 1 covers both sides of the choice and criterion 2 the case without `tests`. Criterion 5's two rows are one parametrized test.
   - Smoke test: both commands can run. `addopts` already sets `-q` and the pytest command passes none, so the summary line prints.
   - Docs criterion: names what the operator must know and dictates no sentences.
   - Architecture and scope: agent files and the shipped prompt only. This is S0003 as the feature's Scope lists it.
4. 2026-11-08 human: 1. (a). Leave granted: the tester updates R12's text in `REWORK_RULE` of `tests/agent_files/test_claude_agent_texts_docs_slip.py` and in the R12 entry of `tests/support/shared_rules_support.py` to the new list; each keeps checking the same thing. `review → tests` goes right after `review → doing`: "Rework rounds (review → doing, review → tests, docs → doing, smoke-test → doing, smoke-test → docs, and the human's close at the approval) …". Please write this into the Interface.
   2. (b). I change `test_the_template_lets_the_smoke_test_hand_a_slip_to_docs_and_keeps_every_other_next` myself, in the same commit as the template's pipeline change after this story.
5. factory: started intake as vm.
6. intake: accepted

   Carried in from journal entry 4 (the human's answer): the R12 Interface line now gives where `review → tests` goes (right after `review → doing`) and quotes the new list. A new Interface line gives the tester leave to update R12's text in `REWORK_RULE` of `tests/agent_files/test_claude_agent_texts_docs_slip.py` and in the R12 entry of `tests/support/shared_rules_support.py`, with each still checking the same thing. Criterion 4 now also says "right after `review → doing`", so the order the answer sets has a criterion. Point 2 of that answer needs nothing from this story: the human changes the template's `next` test in their own commit.

   - Interface: names `agents/agents/reviewer.md` `## Stage`, `agents/agents/tester.md` step 0, `agents/system-prompt.md` with `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py` (R12's exact new text), the two earlier tests the human gave leave to change, and the new test file. No factory code changes, because a decision other than a stage's first `next` already counts as a rework round.
   - Criteria: each can be tested by one function. Criterion 1 covers both sides of the reviewer's choice (`tests` when every finding needs only test changes, `doing` with all findings otherwise). Criterion 2 covers `tests` missing from the allowed decisions. Criterion 3 covers the tester's case. Criterion 4 checks the R12 text, its order and that both texts are equal. Criterion 5 has two rows of one parametrized test: the `tests` move counted as a round, and holding at `round_cap`.
   - Smoke test: both commands can run. `addopts` already sets `-q` and the pytest command passes none, so the summary line prints. The expectations (`1`; a summary with only `passed`) can be checked.
   - Docs criterion: names what the operator must know (review may send to the tester, it needs `tests` in `review`'s `next`, and it counts as a rework round). It dictates no sentences.
   - Architecture: the agent files and the shipped prompt constant in `factory.agents.domain`, which is where they belong. Tests go under `tests/agent_files/`. The pipeline definition (`factory/`, the template) is not touched (R14).
   - Scope: within F0060 as its Scope lists S0003, and nothing in its Out of scope.

   Route: `tests`, because the Interface changes agent files, `src/` and tests.
7. factory: started tests as vm.
8. tester: Tests written for every criterion. They are red on purpose where the agent texts and R12 still have to change.

   - criterion 1: tests/agent_files/test_review_to_tests_agent_files.py::test_the_reviewer_sends_findings_that_need_only_tests_to_the_tester. It reads the reviewer's `## Stage` before `### docs-review`, takes the lines that name `` `tests` ``, and needs one that holds each of: "allowed decisions", "own story", `` `doing` ``, and the word "all". Each is a parametrized row.
   - criterion 2: tests/agent_files/test_review_to_tests_agent_files.py::test_the_reviewer_sends_findings_to_doing_without_tests_among_the_allowed_decisions. It needs a line naming `` `tests` `` that also holds "allowed decisions", `` `doing` `` and a negation ("without", "not" or "no").
   - criterion 3: tests/agent_files/test_review_to_tests_agent_files.py::test_the_tester_answers_the_reviewers_test_findings_and_hands_to_the_coder. Its rows are fragments that step 0 of the tester's `## Stage` must contain: "reviewer", "exactly", "own story", "standing leave", "once", "end with `doing`", "each finding". Today "own story", "standing leave" and "each finding" are missing, so those rows fail.
   - criterion 4: tests/agent_files/test_review_to_tests_agent_files.py::test_r12_lists_review_to_tests_right_after_review_to_doing checks that R12's new list (as the Interface quotes it) appears exactly once and that `review → tests` appears exactly once. tests/agent_files/test_review_to_tests_agent_files.py::test_the_shipped_system_prompt_constant_equals_the_file checks that `SYSTEM_PROMPT` equals `agents/system-prompt.md`.
   - criterion 5: tests/agent_files/test_review_to_tests_agent_files.py::test_a_review_decision_tests_moves_to_the_tester_and_counts_a_round. It has two rows. In `first-to-tests`, review decides `tests` and the item goes to `tests`, round 1, not blocked. In `third-past-the-cap`, the third `tests` from review holds the item at `review`, round 3, blocked `round_cap`, with one round_cap post. The definition is TWO_ROUTES with `review: next [docs, doing, tests], round_cap: 2`. Both rows pass already, which fits the Interface: the pipeline needs no code change.
   - criterion 6: the coder's `make check`.
   - criterion 7 (docs): not a test; it is the documenter's.

   Earlier tests changed under the human's leave (journal entry 4). Each still checks the same thing:
   - tests/agent_files/test_claude_agent_texts_docs_slip.py: `REWORK_RULE` now holds the new R12 list. `OLD_REWORK_RULE` is still derived from it.
   - tests/support/shared_rules_support.py: the R12 entry now holds the new list.

   Moved under the standing leave in CLAUDE.md for shared test helpers, so the new test does not copy them:
   - From tests/pipeline/application/test_docs_route.py I moved `_step` (now `decide`), `WRITES` (now `STAGE_WRITES`) and `MAKEFILE` (now `EVERY_TARGET_MAKEFILE`) into tests/support/two_routes_support.py.
   - test_docs_route.py now imports them. Its test names and checks are unchanged, and it passed in the run.

   Files: created tests/agent_files/test_review_to_tests_agent_files.py. Changed tests/support/two_routes_support.py, tests/pipeline/application/test_docs_route.py, tests/agent_files/test_claude_agent_texts_docs_slip.py and tests/support/shared_rules_support.py.

   Test run, following CLAUDE.md (`uv run pytest -q` on the files above): no module failed to import. The expected failures are the reviewer and tester text rows named above, both R12 rows, test_every_shipped_agent_names_the_smoke_test_to_docs_rework and test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word. `make lint` is green.

   Open point for the reviewer: the Interface fixes no exact wording for the reviewer's and tester's new sentences, so criteria 1 to 3 check for key phrases, not whole sentences. The coder's text must contain the phrases listed above, including "own story" (as the Description words it) and "each finding" in the tester's step 0.

   `lint`: lint: green (0.2 s)
9. factory: started doing as vm.
10. coder: Question: three tests from earlier stories pin the reviewer's and tester's texts by checksum. The story has to change those texts, and your leave in entry 4 covers only R12's text. I need your leave for the tester to update these three tests, or another way forward.

    What is built (left in the working tree, uncommitted by me):
    - `agents/system-prompt.md` and `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`: R12 now lists `review → tests` right after `review → doing`, and the two texts are equal.
    - `agents/agents/reviewer.md`, `## Stage`: a new step 4. When `tests` is among the allowed decisions and every finding needs only a change to the tests of the work item's own story, the reviewer ends with `tests`. When any finding needs a change outside those tests, all findings go to `doing`. When `tests` is not among the allowed decisions, findings go to `doing` as before. The entry is the same either way.
    - `agents/agents/tester.md`, `## Stage`, step 0: a new case for when the latest result is the reviewer's. The tester writes or changes exactly the tests the findings name, only in its own story's tests or under the standing leave, runs those test files once, and ends with `doing`. Its entry names each finding and its test.

    Main choice: the reviewer's rule is a new step 4 rather than an edit to step 3, because `test_the_rest_of_the_reviewer_body_is_unchanged` pins step 3. I also tried mentioning `tests` in the Role's "Your recommendation is your decision" line and in docs-review's "steps 1 to 3 above", then reverted both: earlier tests pin those sentences word for word.

    All tests the tester named now pass, R12 included. In `make check`, lint, types, layers, sast, secrets and licenses are green; `make test` fails on exactly three earlier tests:
    1. `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: `E   AssertionError: assert 163580636 == 3903663111`. It takes a CRC32 of the reviewer's body after mapping each later story's text back to the earlier one.
    2. `tests/agent_files/test_shared_rules_system_prompt.py::test_every_agent_file_keeps_its_own_sections_word_for_word_in_order[reviewer]`: the `Stage` checksum in `PARTS_BEFORE` (`tests/support/shared_rules_support.py`) differs. The current text gives `1905995793`.
    3. The same test, row `[tester]`: the tester's `Stage` checksum differs. The current text gives `1483730218`.

    Any change to the reviewer's or tester's `## Stage` breaks these, so criteria 1 to 3 cannot be met without changing them.

    Options:
    (a) Give leave for the tester to update them, each still checking the same thing:
       - in test 1, add one more `.replace(<the new step-4 line>, "")` to `earlier`, as the test already does for each later story;
       - in `PARTS_BEFORE`, set reviewer `Stage` and tester `Stage` to the checksums of the new texts.
       I would then end with `tests`, naming exactly those changes.
    (b) Put the new rules outside `## Stage`. This contradicts the Interface, which names `## Stage`, and the reviewer's body CRC would still break.
    I would choose (a).

    Noticed, not touched: the story's Description is unchanged, because no journal entry changed the task's meaning. The step 4 refactor is pending until `make check` is green.
11. 2026-11-08 human: (a). Leave granted: the tester adds the new step-4 text as one more `.replace(..., "")` in `test_the_rest_of_the_reviewer_body_is_unchanged` (`tests/agent_files/test_claude_agent_texts_review_groups.py`), and sets the reviewer's and tester's `Stage` checksums in `PARTS_BEFORE` (`tests/support/shared_rules_support.py`) to the new texts; each test keeps its name and checks the same thing.
12. factory: started doing as vm.
13. coder: Test change for the tester, under the human's leave in entry 11. I changed no code this run. The agent texts and R12 from my last run are committed and unchanged. Two changes, each test keeping its name and checking the same thing:

    1. `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: add one more `.replace(<line>, "")` to `earlier`, where `<line>` is step 4 of `agents/agents/reviewer.md` `## Stage`, from its start up to and including its newline: "4. When `tests` is among the allowed decisions and every finding needs only a change to the tests of the work item's own story, end with `tests` instead of `doing`: …The entry with the findings is the same either way.\n".
    2. `tests/support/shared_rules_support.py`, `PARTS_BEFORE`: set the reviewer's `Stage` checksum to `1905995793` and the tester's `Stage` checksum to `1483730218`. These are the CRC32s of the current texts, measured in my last run.

    After the tester's change, `make check` should be green: in my last run these three were the only failures in `make test`, and lint, types, layers, sast, secrets and licenses were green. The refactor step comes once the check is green.

    Rejected: putting the new rule outside `## Stage`. The Interface names `## Stage`, and the reviewer's body checksum would break anyway.

    Noticed, not touched: the Description is unchanged, because the human's answers change no meaning of the task.
14. factory: started tests as vm.
15. tester: Question: one test still fails after the changes you allowed in entry 11. Fixing it needs one more `.replace` in the same test, which your leave does not cover. May I add it?

    I made the changes from entry 11. They are left in the working tree:
    - `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: I added a `findings_to_the_tester` string holding step 4 of the reviewer's `## Stage`, newline included, and one more `.replace(findings_to_the_tester, "")` in `earlier`.
    - `tests/support/shared_rules_support.py`, `PARTS_BEFORE`: the reviewer's `Stage` checksum is now `1905995793` and the tester's is `1483730218`.

    Test run (`uv run pytest -q` on the files below), and `make lint` is green:
    - `tests/agent_files/test_shared_rules_system_prompt.py`, `tests/agent_files/test_review_to_tests_agent_files.py` and `tests/agent_files/test_claude_agent_texts_docs_slip.py` all pass.
    - `test_the_rest_of_the_reviewer_body_is_unchanged` still fails: `tests/agent_files/test_claude_agent_texts_review_groups.py:113: AssertionError`, the CRC32 check against `_EARLIER_BODY_CRC32`.

    Why it still fails: the test builds the earlier reviewer body by putting `RULES_BEFORE` from `tests/support/shared_rules_support.py` back in as a `## Rules` section. Under your leave in entry 4, the tester changed `RULES_BEFORE`'s R12 entry to the new list. So the rebuilt body now holds `review → doing, review → tests, ` where the earlier body held `review → doing, `, and the checksum differs. The coder's entry 10 put the failure down to step 4 alone. Step 4 was only part of it.

    I tried one more `.replace("review → doing, review → tests, ", "review → doing, ")` in `earlier`. With it, the test passes (9 passed in the file). I then reverted it, because it is outside the leave.

    Options:
    (a) Allow that one extra `.replace` in `test_the_rest_of_the_reviewer_body_is_unchanged`. It maps the new R12 list back to the earlier one, as the test already does for each later story's text. The test keeps its name and checks the same thing. I would choose (a).
    (b) Put R12's old text back in `RULES_BEFORE`. That breaks `test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word`, which compares `RULES_BEFORE` with the current system prompt, so it goes against entry 4.

    Files changed: `tests/agent_files/test_claude_agent_texts_review_groups.py`, `tests/support/shared_rules_support.py`.
16. 2026-11-08 human: (a). Leave granted for that `.replace`. Beyond it, for the rest of this story: any earlier test whose only failure is this story's change of R12, the reviewer's `## Stage` or the tester's `## Stage` may be updated the same way (a mapping back to the earlier text, or the new checksum of the new text), each keeping its name and checking the same thing; name each in your entry.
17. factory: started tests as vm.
18. tester: Made the test change the human allowed in entry 16, (a). The changes from entry 11 were already committed and I left them as they were.

    - `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: added `review_to_tests_rework = "review → doing, review → tests, "` with a comment saying why. Added one more `.replace(review_to_tests_rework, "review → doing, ")` in `earlier`, right after the step-4 `.replace` and before `develop` → `main`. It maps the new R12 list in the rebuilt `## Rules` section back to the earlier list. The test keeps its name and still checks the earlier body's CRC32 `_EARLIER_BODY_CRC32`.

    No other earlier test needed a change under the wider leave in entry 16. When the coder ran `make test` (entry 10), the only failures were the three tests the leaves in entries 11 and 16 now cover.

    Test run, following CLAUDE.md (`uv run pytest -q` on `test_claude_agent_texts_review_groups.py`, `test_shared_rules_system_prompt.py`, `test_review_to_tests_agent_files.py` and `test_claude_agent_texts_docs_slip.py`): all pass, and no module failed to import. `make lint`: lint: green (0.1 s).

    Earlier test file changed, under the human's leave in entries 11 and 16: `tests/agent_files/test_claude_agent_texts_review_groups.py`. No files created in this run.

    The criteria still map to their tests as entry 8 lists them. The coder's `make check` comes next. The coder still has the refactor step to do.

    `lint`: lint: green (0.1 s)
19. factory: started doing as vm.
20. coder: The work is built. `make check` is green (`check: green`) and `make guides` is green. I changed no code in this run. The tester's changes from entries 15 to 18 made the last three failures pass.

    What is built (committed in earlier runs of this stage):
    - `agents/agents/reviewer.md`, `## Stage`: new step 4. When `tests` is among the allowed decisions and every finding needs only a change to the tests of the work item's own story, the reviewer ends with `tests`. When any finding needs a change outside those tests, all findings go to `doing`. When `tests` is not among the allowed decisions, findings go to `doing` as before. The entry is the same either way.
    - `agents/agents/tester.md`, `## Stage`, step 0: a new case for when the latest result before the run is the reviewer's. The tester writes or changes exactly the tests the findings name, only in its own story's tests or under the standing leave. It runs those test files once and ends with `doing`, and its entry names each finding and its test.
    - `agents/system-prompt.md` and `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`: R12 lists `review → tests` right after `review → doing`, and the two texts are equal.

    Main choice: the reviewer's rule is a new step 4 rather than an edit to step 3. Step 3 and the Role's "Your recommendation is your decision" line are pinned word for word by earlier tests, so I left them as they are. Rejected: putting the new rule outside `## Stage`, because the Interface names `## Stage`.

    Test run: the four test files the tester's latest entry names pass (`uv run pytest -q`). `make check` is green: lint, types, layers, sast, secrets, licenses and test (coverage 99.21 %).

    Refactor: I read my diff (`git diff develop -- . ':!factory' ':!tests'`) and found nothing to change. The new texts are now pinned by checksums in the earlier tests, so any rewording would need the tester again. The R12 line wrap in `prompts.py` is uneven but correct, and I left it.

    Description: unchanged. The human's answers (entries 4, 11, 16) gave leave for test changes but did not change the meaning of the task.

    Noticed, not touched: the docs criterion 7 (`docs/operator-guide/pipeline.md`) is the documenter's.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
21. factory: started review as vm.
22. reviewer: Findings:

    1. `agents/agents/reviewer.md:54` (`### docs-review`): this subsection still says it "replaces ... steps 1 to 3 above", so the new step 4 still applies in `docs-review`. There `tests` is not an allowed decision, so step 4 sends findings "to `doing` as before". That contradicts the subsection's own step 4 (`docs-only`), and `doing` is not an allowed decision in that stage. Fix: say "steps 1 to 4 above". The tester then updates the pinned texts (`test_the_rest_of_the_reviewer_body_is_unchanged` and the reviewer `Stage` checksum in `PARTS_BEFORE`) under the human's leave in entry 16. This needs a change to an agent file, so it goes to `doing`.
    2. `tests/agent_files/test_review_to_tests_agent_files.py::test_the_tester_answers_the_reviewers_test_findings_and_hands_to_the_coder` (criterion 3): four of its seven rows already pass on the step 0 text from before this story. Step 0 already held "reviewer" ("a criterion the reviewer added"), "exactly", "once" and "end with `doing`". No row checks the criterion's condition ("the latest result before its run is the reviewer's"), and the rows do not check that the fragments sit in the same sentence. Fix: add a row for "latest result before your run is the reviewer's". Check the fragments against the sentence that starts with that condition, not against the whole of step 0.
    3. `tests/agent_files/test_review_to_tests_agent_files.py::test_the_shipped_system_prompt_constant_equals_the_file`: this repeats a check that `tests/agents/adapters/test_claude_runtime_system_prompt.py:63` (and `tests/agent_files/test_context_system_prompt.py:17`) already makes, `SYSTEM_PROMPT_FILE.read_text(...) == SYSTEM_PROMPT`. Fix: drop the copy, and let the tester's entry name the existing test for criterion 4's second half.

    Checked and in order: criterion 1 and 2 (step 4 says both sides, and the tests read them from the lines that name `tests`), criterion 4 (R12 holds the new list once, in the right order, in the file and in `SYSTEM_PROMPT`), and criterion 5 (two rows of one parametrized test, with `round_cap: 2` and a third rework held at `review`). `make check` after the coder was green (entry 20). Architecture, security, docstrings and the Description all match what was built. The docs criterion is still right for the documenter.

    Notes on the side, not findings: the Role's sentence "`docs` passes, `doing` sends the work item back" does not name `tests`. The Interface scopes the change to `## Stage`, so I left it. Allowed decisions here are `docs`, `doing` and `question`. Finding 1 needs an agent-file change, so this goes to `doing` in any case.

    Earlier tests:
    - `tests/agent_files/test_claude_agent_texts_docs_slip.py`: the human's leave, journal entry 4 (R12's text in `REWORK_RULE`).
    - `tests/support/shared_rules_support.py`: the human's leave, entry 4 (the R12 entry) and entry 11 (the reviewer and tester `Stage` checksums).
    - `tests/agent_files/test_claude_agent_texts_review_groups.py`: the human's leave, entry 11 (the step 4 `.replace`) and entry 16 (the R12 mapping `.replace`).
    - `tests/pipeline/application/test_docs_route.py`: the standing leave to move a shared test helper. `_step`, `WRITES` and `MAKEFILE` moved to `tests/support/two_routes_support.py` as `decide`, `STAGE_WRITES` and `EVERY_TARGET_MAKEFILE`, and every test keeps its name and its checks.
    - `tests/support/two_routes_support.py`: the standing leave to move a shared test helper (it receives the moved helpers). `TWO_ROUTES` is unchanged.
23. factory: started doing as vm.
24. coder: Rework round 1. I fixed finding 1 and left findings 2 and 3, which are test changes, to the tester, along with the two pinned tests that the fix breaks.

    Built:
    - `agents/agents/reviewer.md:54` (`### docs-review`): "steps 1 to 3 above" now reads "steps 1 to 4 above". In `docs-review` the subsection now also replaces the new step 4, so step 4 can no longer send findings to `doing` there. This is the only change I made, and I changed no tests.

    Test changes for the tester (`uv run pytest -q tests/agent_files`; these are the only two failures):
    1. `tests/agent_files/test_claude_agent_texts_docs_route.py::test_the_reviewer_in_docs_review_replaces_its_code_review_and_judges_the_facts`, row `replaces-decisions-and-steps`: change the fragment `"its decisions, and steps 1 to 3"` to `"its decisions, and steps 1 to 4"`. This is under the human's leave in entry 16 (an earlier test whose only failure is this story's change of the reviewer's `## Stage`), and the test keeps its name and checks the same thing.
    2. `tests/support/shared_rules_support.py`, `PARTS_BEFORE`: set the reviewer's `Stage` checksum to `3113525091`, the CRC32 of the new text, also under entry 16. It currently holds `1905995793`.
    3. Reviewer finding 2: in `tests/agent_files/test_review_to_tests_agent_files.py::test_the_tester_answers_the_reviewers_test_findings_and_hands_to_the_coder`, add a row for the condition "latest result before your run is the reviewer's", and check the fragments against the sentence that starts with that condition, not against the whole of step 0.
    4. Reviewer finding 3: drop `test_the_shipped_system_prompt_constant_equals_the_file` from `tests/agent_files/test_review_to_tests_agent_files.py`. The entry then names `tests/agents/adapters/test_claude_runtime_system_prompt.py`'s existing check for the second half of criterion 4.

    `test_the_rest_of_the_reviewer_body_is_unchanged` still passes after the fix, so it needs no change.

    Main choice: the smallest fix the finding names (step 4 joins the steps that `docs-review` replaces). Rejected: adding to step 4 itself that it does not apply in `docs-review`. That says the same thing twice, and the docs-review subsection already lists what it replaces.

    `make check` is not run this round: it cannot be green until the tester changes the two pinned tests above. I run it after the tester hands the work item back.

    Noticed, not touched: the Role's sentence "`docs` passes, `doing` sends the work item back" does not name `tests`. The reviewer noted it, and the Interface scopes the change to `## Stage`. Description: unchanged, because the findings do not change the task's meaning.
25. factory: started tests as vm.
26. tester: I made the test changes listed in the coder's entry 24: the reviewer's findings 2 and 3, and the two pinned tests that the `docs-review` fix broke. The earlier tests changed under the human's leave in entry 16. Each keeps its name and checks the same thing.

    - Reviewer finding 2. In `tests/agent_files/test_review_to_tests_agent_files.py::test_the_tester_answers_the_reviewers_test_findings_and_hands_to_the_coder`:
      - I added the row `after-review` for the condition "latest result before your run is the reviewer's".
      - The rows now check the sentence of step 0 that starts with "When the latest result before your run is the reviewer's" and runs to the first ". " after it. They no longer check the whole of step 0.
      - The new helper is `_tester_sentence_after_review` (it replaces `_tester_step_zero`). It returns an empty string when that sentence is missing, so on step 0 from before this story every row fails.
      - I removed the `reviewer` row, because the condition row now covers it.
    - Reviewer finding 3. I dropped `test_the_shipped_system_prompt_constant_equals_the_file` from the same file, along with its imports that are now unused (`SYSTEM_PROMPT`, `SYSTEM_PROMPT_FILE`). The check for the second half of criterion 4 (`SYSTEM_PROMPT` equals the file) is the existing one in `tests/agents/adapters/test_claude_runtime_system_prompt.py`, which also exists in `tests/agent_files/test_context_system_prompt.py`.
    - `tests/agent_files/test_claude_agent_texts_docs_route.py::test_the_reviewer_in_docs_review_replaces_its_code_review_and_judges_the_facts`: I changed the fragment in row `replaces-decisions-and-steps` to `"its decisions, and steps 1 to 4"`. This is under the human's leave in entry 16.
    - `tests/support/shared_rules_support.py`, `PARTS_BEFORE`: I set the reviewer's `Stage` checksum to `3113525091`, the CRC32 of the new text. This is also under the human's leave in entry 16.

    Criteria to tests, updated from entry 8:
    - criterion 1: tests/agent_files/test_review_to_tests_agent_files.py::test_the_reviewer_sends_findings_that_need_only_tests_to_the_tester
    - criterion 2: tests/agent_files/test_review_to_tests_agent_files.py::test_the_reviewer_sends_findings_to_doing_without_tests_among_the_allowed_decisions
    - criterion 3: tests/agent_files/test_review_to_tests_agent_files.py::test_the_tester_answers_the_reviewers_test_findings_and_hands_to_the_coder
    - criterion 4: tests/agent_files/test_review_to_tests_agent_files.py::test_r12_lists_review_to_tests_right_after_review_to_doing, plus the existing check in tests/agents/adapters/test_claude_runtime_system_prompt.py
    - criterion 5: tests/agent_files/test_review_to_tests_agent_files.py::test_a_review_decision_tests_moves_to_the_tester_and_counts_a_round
    - criterion 6: the coder's `make check`
    - criterion 7 (docs): the documenter's

    Test run: I ran `uv run pytest -q` on the four files below. All passed and every module imported. `make lint`: lint: green (0.1 s).
    - test_review_to_tests_agent_files.py
    - test_claude_agent_texts_docs_route.py
    - test_shared_rules_system_prompt.py
    - test_claude_agent_texts_review_groups.py

    Files changed:
    - tests/agent_files/test_review_to_tests_agent_files.py
    - tests/agent_files/test_claude_agent_texts_docs_route.py (earlier test, entry 16)
    - tests/support/shared_rules_support.py (earlier test, entry 16)

    No files created. Next is the coder's `make check`.

    `lint`: lint: green (0.1 s)
27. factory: started doing as vm.
