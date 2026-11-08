---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T21:33:18.434591Z'
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
