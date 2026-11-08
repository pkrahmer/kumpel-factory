---
stage: review
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 673
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: review
  started_at: '2026-11-08T16:34:37.622892Z'
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
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-08T16:29:54.503814Z'
  stage: tests
  run: a4eee1da7f504230bf71ebd6a4678a47
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T16:29:59.436899Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-08T16:34:32.421383Z'
  stage: doing
  run: adf4838702014cb89cc7b3c0cc766ac1
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T16:34:37.622892Z'
  stage: review
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
5. tester: Wrote the tests for the smoke tester's `check_red` rule. They read the shipped agent file through `tests/support/shipped_agents.py`.
   - criterion 1: `tests/agent_files/test_claude_agent_texts_check_red.py::test_the_smoke_tester_routes_a_red_check_without_running_the_smoke_test_again`. It is one parametrized test over the rule's sentences. The rule is the paragraph (the lines between blank lines) of the smoke tester's `## Stage` section that holds `check_red`; a sentence is a line, or the text between full stops. Its rows check:
     - the stall is named;
     - one sentence says the smoke test is not or never run again;
     - one sentence names the "failing lines";
     - one sentence pairs `doing` with each of test, type, lint, layer, security, licence and "cannot place";
     - one sentence pairs `docs` with each of documenter, README, guide, "document check" and secrets;
     - one sentence names the entry, naming and the file;
     - every `make <target>` in the rule is `make check`, and the rule holds no `uv run`.
   - criterion 2: `tests/agent_files/test_claude_agent_texts_check_red.py::test_the_red_check_rule_sits_in_the_smoke_testers_stage_and_in_no_shared_rule`. It runs over every shipped agent: no `## Rules` section holds `check_red`, the smoke tester holds it only in its Stage section, and no other agent holds it.
   - criterion 3: the coder's `make check`.
   - criterion 4 (docs): the documenter's, not tested.

   Files created: `tests/agent_files/test_claude_agent_texts_check_red.py`. Every module imported; no collection errors.

   The run of the new file failed as intended. Every row except `only-make-check` failed, and so did the `smoke-tester` row of the placement test, because the rule is not in the file yet. `only-make-check` passes on an empty rule; it only constrains what the coder writes. `make lint` is green (I ran `ruff format` once on the new file).

   I did not pin exact wording, because the Interface dictates none. The rows check only the facts the Interface lists.

   Note for the coder: `tests/agent_files/test_claude_agent_texts_docs_slip.py` requires "end with `docs`" and "end with `approval`" to each appear exactly once in the smoke tester's Stage section. Write the new routes as "decides `doing`" and "decides `docs`" (as the Interface does), and leave steps 5 and 6 as they are.

   `lint`: lint: green (0.2 s)
6. factory: started doing as vm.
7. coder: Built the smoke tester's rule for a run after a `check_red` stall in `agents/agents/smoke-tester.md`. It is one paragraph in its `## Stage` section, after step 6, and it says four things:
   - The smoke tester does not run the smoke test again. It reads the failing lines in the stall entry.
   - It decides `doing` for a failing test of code, a type, lint, layer, security or licence finding, or a failing test it cannot place.
   - It decides `docs` for a failure in a file only the documenter may write: a README, a guide under `docs/`, the document check, or the secrets check of a document.
   - Its entry names each failing test or check and the file it points to, in a sentence each.

   Main choice: I wrote the rule as a separate paragraph after the numbered steps, using "decide `doing`" and "decide `docs`". Steps 5 and 6 stay word for word. That way "end with `docs`" and "end with `approval`" still appear once each, as `tests/agent_files/test_claude_agent_texts_docs_slip.py` requires.

   Rejected: a step 7 in the numbered list. The rule replaces the run's steps 1 to 6 rather than following them, so a step after them would read wrongly. The tester's paragraph-based reading of the rule also needs it to be one block without blank lines.

   The rule names no command except `make check`.

   Checks:
   - `tests/agent_files/` passes in full, including all rows of `tests/agent_files/test_claude_agent_texts_check_red.py`.
   - `make check`: check: green.
   - The smoke test's `grep -c 'check_red'` now prints 2.

   Refactor: nothing needed changing. The diff is one paragraph.

   The journal did not change the meaning of the task, so `## Description` is unchanged. Criterion 4 (the project guide, `docs/project-guide/agents.md`) is the documenter's and is not touched.

   `check`: check: green
   `duplicates`: duplicates: 7 new, 39 known, 4 gone
8. factory: started review as vm.
