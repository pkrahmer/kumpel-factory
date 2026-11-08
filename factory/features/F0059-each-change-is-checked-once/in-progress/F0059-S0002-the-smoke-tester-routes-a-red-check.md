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
  started_at: '2026-11-08T16:28:24.046470Z'
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
