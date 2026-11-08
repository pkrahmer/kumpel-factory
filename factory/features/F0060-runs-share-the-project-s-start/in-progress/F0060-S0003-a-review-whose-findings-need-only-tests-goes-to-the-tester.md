---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 680
comments_read: [6727432579]
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T21:34:45.259023Z'
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
---

# A review whose findings need only tests goes to the tester

## Description

Most review findings are missing tests: an untested side of a rule, a criterion without its test. The reviewer can send them only to `doing`, so the coder reads them, changes nothing and passes the work item to the tester. In F0050 to F0059, 58 of the 65 coder runs right after review findings did only that. After this story the reviewer decides `tests` when `tests` is among its allowed decisions and every finding needs only a change to the tests of the work item's own story; any finding that needs a change elsewhere sends all findings to `doing`, as today. The tester, when the latest result before its run is the reviewer's, writes or changes exactly the tests those findings name and ends with `doing`, so the coder runs once, after the tester, before the next review. The rule R12 names the new rework route. Whether the review stage offers `tests` is the pipeline definition's: the human adds it to `review`'s `next` after this story, and until then, or in a project that does not add it, the reviewer keeps deciding `doing`. The coder's handling of test findings in a mixed review stays as it is.

## Interface

- `agents/agents/reviewer.md`, `## Stage`: the choice between `tests` and `doing`, as the Description says; the entry with the findings is the same in both cases.
- `agents/agents/tester.md`, `## Stage`, step 0: the case where the latest result before the tester's run is the reviewer's: the tester writes or changes exactly the tests the reviewer's findings name, only in the tests of its own story (or under the standing leave of `CLAUDE.md`), runs those test files once, and ends with `doing`; its entry names each finding and the test that answers it.
- `agents/system-prompt.md` and `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`: R12's list of rework rounds gains `review → tests`; both texts stay equal.
- No code of the factory changes: a decision other than the first of a stage's `next` already counts as a rework round against the stage's `round_cap`.
- Tests: `tests/agent_files/test_review_to_tests_agent_files.py` for the criteria below.

## Acceptance criteria

1. The reviewer's `## Stage` says to decide `tests` when `tests` is among the allowed decisions and every finding needs only a change to the tests of the work item's own story, and to decide `doing` with all findings when any finding needs a change outside them.
2. The reviewer's `## Stage` says that without `tests` among the allowed decisions, findings go to `doing` as before.
3. The tester's step 0 says that when the latest result before its run is the reviewer's, it writes or changes exactly the tests the findings name, only in its own story's tests or under the standing leave, runs those test files once and ends with `doing`, naming each finding and its test in the entry.
4. R12 in `agents/system-prompt.md` lists `review → tests` among the rework rounds, and `SYSTEM_PROMPT` equals the file.
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
