---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 673
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-08T16:28:58.632262Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T16:28:24.038819Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T16:28:24.046470Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T16:28:53.708736Z'
  stage: intake
  run: 89275cf376904e7587057fca2ed7badf
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T16:28:58.632262Z'
  stage: tests
---

# The smoke tester routes a red check

## Description

After this feature the factory runs the whole `make check` once per story, after the smoke tester, on the tree that goes to the human's approval (`feature.md`, *The human's changes*). Today it runs it after every round of the coder and of the documenter, although the coder runs it itself before it hands forward: in the journals of F0053 to F0058, the factory's check after the coder was red once in 113 coder results.

A red check is a stall with the reason `check_red`. The factory writes the failing lines into the journal and runs the same stage again on the next tick (`docs/project-guide/pipeline.md`, *Stalls*). The smoke tester may write only the work item, so it cannot fix what failed. But its stage may already decide `doing` and `docs`. After this story, its agent file tells it what to do when it runs again after such a stall: send the work item to the stage that can fix the failure, and name the failure in its entry.

## Interface

- `agents/agents/smoke-tester.md` gets a rule for a run whose work item's latest journal record is a stall with the reason `check_red`:
  - The smoke tester does not run the smoke test again. It reads the failing lines in that stall entry.
  - A failing test of code, a type, lint, layer, security or licence finding, or a failing test it cannot place: it decides `doing`.
  - A failure in a file only the documenter may write (a README, a guide, the document check, the secrets check of a document): it decides `docs`.
  - Its entry names the failing tests or checks and the file each points to, in a sentence each, so the next stage starts from them.
- The rule names no project's commands beyond `make check`, which the shipped agent files already name.
- Nothing else in the smoke tester's file changes, and no factory code changes: the stall, its journal entry, the retry and the stage's `next` (`approval`, `doing`, `docs`) exist today.

The human's leave for earlier tests: none needed; the story adds a test module of its own under `tests/agent_files/`.

## Acceptance criteria

1. The smoke tester's agent file holds the rule: after a `check_red` stall it does not run the smoke test again, decides `doing` for a failure in code or tests and `docs` for a failure in a document, and names each failure in its entry (rows of one test over the file's sentences).
2. The rule sits in the smoke tester's own section, not in the shared rules R1 to R15 that every agent file repeats.
3. `make check` stays green.
4. docs: the project guide's description of the smoke tester's stage names the rule in one or two sentences.

## Smoke test

```bash
grep -c 'check_red' agents/agents/smoke-tester.md
```
Expect: a count of 1 or more.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: concrete. One file, `agents/agents/smoke-tester.md`, gets a rule in its `## Stage` section for a run whose latest journal record is a `check_red` stall: do not run the smoke test again, read the failing lines, decide `doing` (failures in code, types, lint, layers, security or licences, or a failure it cannot place) or `docs` (a failure only in a file the documenter writes), and name each failure and the file it points to. `check_red` exists as a `StallReason` (`docs/project-guide/pipeline.md`, *Stalls*), and the stall detail holds the check's last 15 lines. `smoke-test`'s `next` is already `[approval, doing, docs]` in `factory/pipeline.yml`. No code changes.
   - Criteria: each one can be tested. Criterion 1 is one parametrized test with a row per sentence of the rule (no rerun, `doing`, `docs`, naming the failures). The rows also cover the "cannot place → doing" branch and the "names no command beyond `make check`" constraint, because they pin the rule's exact sentences. Criterion 2 can be tested with the existing `stage_section("smoke-tester")` helper (`tests/agent_files/test_claude_agent_texts_docs_slip.py`): the rule sits in the Stage section and in no shared R1–R15 text. The rule is a routing table, not a validation, so its failing side is the other route, and criterion 1 covers both routes. Criterion 3 is the standard one.
   - Smoke test: `grep -c 'check_red' agents/agents/smoke-tester.md` runs from the repository root, and today it prints 0, so the expectation "1 or more" can be checked and is red until the story is built.
   - Docs criterion: it says what the reader must know (that the project guide's account of the smoke tester's stage, `docs/project-guide/agents.md` near the steps 5/6 lines, names the rule) and dictates no sentences.
   - Architecture: the change is to a shipped agent file only, and the new test module goes under `tests/agent_files/` as the project's test layout says. No dependency, no change under `factory/`, no change to another story's test. The existing docs-slip test pins steps 5 and 6, so the new rule must be added beside them without rewording them.
   - Scope: this is the feature's third scope line (S0002) and decision 4. It adds no new factory rule, which the feature lists as out of scope. The pipeline's own `smoke-test: checks: [check]` is the human's later change, not this story's.
   - Route: `tests`. The changed path, `agents/agents/smoke-tester.md`, is outside the documenter's write paths.
4. factory: started tests as vm.
