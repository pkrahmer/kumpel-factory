---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 644
comments_read: [6713932106, 6714015757]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-07T22:45:20.655055Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-07T22:33:05.195233Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-07T22:33:05.202549Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-07T22:33:28.704130Z'
  stage: intake
  run: c1b8954b7ca34ff28866b36deca13c21
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-07T22:35:18.009384Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-07T22:35:20.544134Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-07T22:35:37.297263Z'
  stage: intake
  run: c98cc6325c964b32992cb3debfb095ed
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-07T22:35:42.206941Z'
  stage: tests
- number: 8
  speaker: tester
  kind: question
  at: '2026-11-07T22:41:27.009826Z'
  stage: tests
  run: 8bd5b9bd525e4f47b0ace72f15100c07
  blocked: question
- number: 9
  speaker: human
  kind: comment
  at: '2026-11-07T22:45:18.355109Z'
  stage: tests
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-07T22:45:20.655055Z'
  stage: tests
---

# The factory works on develop

## Description

`main` is to become the protected line of accepted features, so the factory moves its work to `develop`: the archive after a merge, the closes, the acceptance's booking, the stop records, the claims' base and every read of `origin/<working branch>` (F0057, decision 1). With F0057-S0001 merged, this is one value: `WORK_BRANCH` becomes `"develop"`. The agent files and the project template name the branch too, so they follow. A remote without `develop` must be clear at once, so the preflight's existing finding for a missing working branch names it. The human creates `develop` and moves the factory over at this story's merge (feature, *The human's changes*).

## Interface

- `factory.shared.domain.paths`: `WORK_BRANCH = "develop"`.
- `agents/agents/*.md`: every mention of the factory's working branch (`origin/main`, `main...HEAD`, "on `main`") names `develop`, about 13 lines. The human's leave (2026-11-07): the tester changes the earlier tests that pin these agent texts only so far as the branch's name requires, and any other earlier test whose only failure is the new value of `WORK_BRANCH`; every changed test keeps its name and what it checks, and the entry names each.
- `operator/template/CLAUDE.md` and `operator/template/Makefile`: every `origin/main` and every mention of the working branch says `develop`, so that a project made from the template works on `develop` as the factory does.
- `factory.machine.application.preflight`: the finding for a remote without the working branch (today `no origin/main to prepare the stage environment from`) names `origin/develop`, as it follows from the constant; no new item.
- `src/factory/` otherwise unchanged: every other use follows the constant.

## Acceptance criteria

1. `WORK_BRANCH` is `"develop"` (one test).
2. On a fake remote that has `main` but no `develop`, the preflight's finding names `origin/develop` (one test).
3. No file under `agents/agents/` or `operator/template/` holds any of these forms, one row each (rows of the guard of F0057-S0001, widened to these two folders): `origin/main`; `main...HEAD`; `git diff main`; the working-branch prose uses of `main` (R10's "reaches `main` only through the human's merge", the acceptance reviewer's "writes your report to `main`", "that `main` already holds", "on `main` itself" in the template's `CLAUDE.md` and `Makefile`), which say `develop`. Phrases like "the main choice" stay.
4. `make check` stays green.
5. docs: `docs/decisions.md`: one entry for F0057's decisions 1 to 7, with the rejected options. The other documents follow in S0004 and S0005.

## Smoke test

```bash
uv run python -c "from factory.shared.domain.paths import WORK_BRANCH; print(WORK_BRANCH)"
```
Expect: `develop`

## Journal

1. 2026-11-07 human: created.
2. factory: started intake as vm.
3. intake: Format check passed. I found one gap that blocks the story, so I am asking.

   1. **Criterion 3 does not cover most of the behaviour the Interface states.**
      - The Interface says every mention of the working branch in `agents/agents/*.md` names `develop`: `origin/main`, `main...HEAD`, and "on `main`". It also says every mention in `operator/template/CLAUDE.md` and `operator/template/Makefile` does.
      - Criterion 3 tests only the string `origin/main`. A grep of those folders shows the other forms are the bulk of the mentions:
        - `git diff main...HEAD` in the documenter and reviewer files.
        - `git diff main -- ...` in the coder file.
        - "every test file that `main` already holds" and `git diff --name-status main...HEAD` in the reviewer file.
        - "reaches `main` only through the human's merge" (R10) in every agent file.
        - "writes your report to `main`" in the acceptance-reviewer file.
        - "every tracked file on `main` itself" in the template `CLAUDE.md` and `Makefile`.
      - A coder could change only `origin/main` and pass every criterion. The agents would then still diff against `main`.
      - I would choose to widen criterion 3 to name the forms, with one row each: `origin/main`, `main...HEAD`, `git diff main`, and the working-branch uses of `main` in the prose (R10, the acceptance reviewer's report, the template's "on main itself").
      - **The one thing I need from you:** are the R10 sentence ("reaches `main` only through the human's merge") and the acceptance-reviewer's "writes your report to `main`" working-branch mentions that must say `develop`? The first is arguably correct as `main`, since a promotion is a merge. I would choose `develop` for the report sentence and `main` for none of the prose.
      - A guard that matches the word `main` would also hit "the main choice" and "the main design decision" in `coder.md`, so the criterion must name the exact forms.

   2. **Not a finding, noted for the record.**
      - Criterion 2 and the smoke test are testable as written.
      - The docs criterion names what the reader must know and dictates no sentences.
      - Scope and architecture fit feature.md (S0002: constant, agent files, template, preflight).
      - The preflight's rule (a missing working branch is a finding) is covered by criterion 2.
4. 2026-11-07 human: Widen criterion 3 as you propose, one row per form. All the prose mentions you list are the working branch and say `develop`, R10 included: the human's merge lands on `develop`; `main` is reached only by Kumpel's promotion, which no agent file needs to name. "the main choice" and the like stay.
5. factory: started intake as vm.
6. intake: accepted
   - Interface: concrete. It names `factory.shared.domain.paths.WORK_BRANCH = "develop"`, the agent files, the two template files and the preflight finding. The human's leave for the earlier tests is stated.
   - Criteria: each is testable by one test. Criterion 1 is the constant. Criterion 2 is the fail side, a remote with `main` and no `develop`. Criterion 3 is widened with the human's answer (journal entry 4) into one row per form: `origin/main`, `main...HEAD`, `git diff main`, and the working-branch prose uses of `main`. Phrases like "the main choice" stay. This is the human's edit carried in, not mine.
   - Smoke test: the command is runnable. `Expect: develop` is checkable against the output. The command runs no pytest.
   - Docs criterion: it names what the reader must know, one `docs/decisions.md` entry for decisions 1 to 7 with the rejected options. It dictates no sentences.
   - Architecture: a constant, text files and a finding that follows from the constant. No new layer or item.
   - Scope: within F0057 S0002. Nothing is in "Out of scope". `main_branch_failing` is untouched.
   Route: tests, because the Interface changes `src/` and `agents/`, which the documenter may not write.
7. factory: started tests as vm.
8. tester: I wrote the tests for all criteria. I stopped short of `doing` because one case the story leaves open breaks earlier tests: the operator's Kumpel scripts.

   **Question.** The scripts under `operator/skill/kumpel/scripts/` hard-code `main`:
   - `start-story.sh` and `next-story.sh` run `git checkout -q main`.
   - `approval.sh` diffs `origin/main...$branch`.
   - `reset-to-tag.sh` moves `refs/heads/main`.
   - `merge.sh` and `status.sh` say "the archive commit on main".

   Their tests (`tests/operator_scripts/test_operator_skill_scripts.py`, `test_operator_skill_signature.py`, `test_operator_merge_reset.py`) build the remote and the expected refs from `WORK_BRANCH`. With `WORK_BRANCH = "develop"`, 18 of them fail ("pathspec 'main' did not match", "bad revision 'origin/main...'", "PATCH .../heads/main: 404"). The Interface does not name these scripts.

   Options:
   - (a) The scripts stay on `main` in this story. Under your leave ("an earlier test whose only failure is the new value of `WORK_BRANCH`"), I change those three test files to name the scripts' branch through a constant `"main"` of their own in `tests/support/operator_skill_support.py`, instead of `WORK_BRANCH`. A later story (S0004/S0005, or your own change, since the skill is yours) moves the scripts.
   - (b) Widen the Interface. The scripts that start, pick, approve and archive (`start-story.sh`, `next-story.sh`, `approval.sh`, `merge.sh`, `status.sh`) work on `develop`, and the tests keep `WORK_BRANCH`. `reset-to-tag.sh` stays on `main` and its tests get the constant from (a).
   - (c) Widen the Interface the same way, but `reset-to-tag.sh` moves to `develop` too.

   I would choose (b). Once you move the factory over at the merge, a `start-story.sh` that pushes to `main` would start nothing, because the factory reads `develop`. Resetting `main` to a tag fits Kumpel's promotion line.

   **Criteria → tests** (all red until the coder's change):
   - criterion 1: `tests/shared/domain/test_work_branch.py::test_the_working_branch_is_one_constant_named_work_branch`. It is the earlier test, kept by name, its value changed to `"develop"`.
   - criterion 2: `tests/machine/application/test_preflight_working_branch.py::test_a_remote_with_main_but_no_develop_gets_a_finding_naming_origin_develop`
   - criterion 3: `tests/guards/test_working_branch_in_agent_texts.py::test_no_agent_or_template_file_names_main_as_the_working_branch`, with one row per form:
     - `remote-ref` (origin/main)
     - `three-dot-diff`
     - `git-diff`
     - `human-merge`
     - `acceptance-report`
     - `already-holds`
     - `on-itself` (with or without backticks, for the template's `Makefile`)
   - criterion 3, the side that stays ("the main choice"): `tests/guards/test_working_branch_in_agent_texts.py::test_main_as_an_ordinary_word_stays_in_the_agent_files`.
   - criteria 4 and 5: no test. They are `make check` and docs.

   **Placement.** I put criterion 3 in a new guard module rather than widening `tests/guards/test_work_branch_search.py`. That guard scans `src/factory` and `tests` for literals like `-b main`, which are not this criterion's forms. The new module builds the remote ref from `REMOTE`, so the S0001 guard does not flag it.

   **Files created:**
   - `tests/machine/application/test_preflight_working_branch.py`
   - `tests/guards/test_working_branch_in_agent_texts.py`

   **Earlier test files changed, under your leave of 2026-11-07.** Every test keeps its name and what it checks.
   - Agent and template texts, only the branch's name:
     - `tests/agent_files/test_claude_agent_texts.py`: the reviewer anchor "that `develop` already holds".
     - `tests/agent_files/test_claude_agent_texts_docs_route.py`: `DOCS_DIFF` uses `develop...HEAD`.
     - `tests/agent_files/test_claude_files.py`: "on `{WORK_BRANCH}` itself".
     - `tests/agent_files/test_claude_agent_texts_review_groups.py`: the earlier-body CRC maps `develop` back to `main` before hashing.
   - Only failure is the new value of `WORK_BRANCH`; I found these by running the suite once with the constant flipped by hand, then put the constant back. In each, a literal `"main"` became `WORK_BRANCH`:
     - `tests/shared/domain/test_paths.py`
     - `tests/hosting/domain/test_hosting.py`
     - `tests/entry/test_wiring_run.py`
     - `tests/guards/test_human_clone.py`
     - `tests/agents/application/test_project_agents.py`
     - `tests/machine/application/test_container_environment.py`
     - `tests/pipeline/application/test_claims_refusals.py`
     - `tests/pipeline/application/test_preflight_stops_commit.py`
     - `tests/pipeline/application/test_stop_publisher.py`
     - `tests/pipeline/application/test_tick_stop_records.py`
     - `tests/work/application/test_acceptance_service.py`
     - `tests/work/application/test_acceptance_snapshots.py`
     - `tests/work/domain/test_stop_table.py`
   - Two changes go beyond swapping the literal:
     - `tests/hosting/adapters/test_git_cli_reading.py`: in the sorted remote-branch list, `develop` now sorts before `feature-b`.
     - `tests/hosting/adapters/test_git_cli_branches.py`: git writes "Merge branch 'other' into develop", and leaves out " into …" only for `main`. This test is red until the constant changes.
   - `tests/agent_files/test_template_makefile.py` needs no change: its secrets and mutants cases go green once the template `Makefile` says `origin/develop`.

   **Runs.** One `uv run pytest` over the changed and new test files. The failures are the new tests and the texts not yet changed: the preflight finding and the guard rows. `make lint` is green.

   **Modules not importable:** none. Every failure is a wrong result.

   **Open:** the question above. The 18 operator-script tests are untouched until you answer.

   The factory left out changes outside the write paths: src/factory/shared/domain/paths.py.
9. 2026-11-07 human: (a). The Kumpel scripts are F0057-S0003's (already planned there, reset-to-tag.sh included, moving develop). In this story they stay on main, and their three test files take the scripts' branch from a constant `"main"` of their own in tests/support/operator_skill_support.py; S0003 replaces it.
10. factory: started tests as vm.
