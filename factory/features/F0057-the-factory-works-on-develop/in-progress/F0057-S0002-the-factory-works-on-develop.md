---
stage: doing
blocked: question
round: 1
attempts: 0
crashes: 0
pull_request: 644
comments_read: [6713932106, 6714015757, 6714081152]
handed_over: null
claim: null
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
- number: 11
  speaker: tester
  kind: result
  at: '2026-11-07T22:46:26.022950Z'
  stage: tests
  run: af5c2e717b1443c0889dbe4991b4ba31
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-07T22:46:31.131853Z'
  stage: doing
- number: 13
  speaker: coder
  kind: question
  at: '2026-11-07T22:49:25.819070Z'
  stage: doing
  run: 5619743c38af4e23a3ec51066b212cc5
  blocked: question
- number: 14
  speaker: human
  kind: comment
  at: '2026-11-07T22:50:12.510452Z'
  stage: doing
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-07T22:50:14.896936Z'
  stage: doing
- number: 16
  speaker: coder
  kind: result
  at: '2026-11-07T22:54:32.458092Z'
  stage: doing
  run: 9a1c7ee26b3248b393ce2425800b17f9
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-07T22:54:37.685909Z'
  stage: review
- number: 18
  speaker: reviewer
  kind: result
  at: '2026-11-07T22:55:50.091052Z'
  stage: review
  run: 1db7e5caa92a4e14b1e3529efe9333de
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-07T22:55:55.571410Z'
  stage: doing
- number: 20
  speaker: coder
  kind: question
  at: '2026-11-07T22:56:16.585094Z'
  stage: doing
  run: ecdbcaed85e3476f95b4d04c1fc923d6
  blocked: question
---

# The factory works on develop

## Description

`main` is to become the protected line of accepted features, so the factory moves its work to `develop`: the archive after a merge, the closes, the acceptance's booking, the stop records, the claims' base and every read of `origin/<working branch>` (F0057, decision 1). With F0057-S0001 merged, this is one value: `WORK_BRANCH` becomes `"develop"`. The agent files, the project template and the todo demo's project made from it (`demo/todo-service/project/Makefile` and `CLAUDE.md`) name the branch too, so they follow. A remote without `develop` must be clear at once, so the preflight's existing finding for a missing working branch names it. The human creates `develop` and moves the factory over at this story's merge (feature, *The human's changes*).

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
11. tester: I applied the human's answer (a) from entry 9. The criteria tests from entry 8 are already committed and unchanged. This round only made the Kumpel scripts' tests independent of `WORK_BRANCH`.

    **The change.**
    - `tests/support/operator_skill_support.py` now has its own constant, `SCRIPTS_BRANCH = "main"`: the branch the skill scripts work on. `make_bare_remote` builds the remote and the seed push on it, and the module no longer imports `WORK_BRANCH`. F0057-S0003 replaces this constant when it moves the scripts.
    - In the three operator-script test files, `WORK_BRANCH` is now `SCRIPTS_BRANCH`, imported from the support module. Every test keeps its name and checks the same thing:
      - `tests/operator_scripts/test_operator_skill_scripts.py`: the `log` and `ls-tree` of the pushed branch.
      - `tests/operator_scripts/test_operator_skill_signature.py`: the `log` of the pushed branch.
      - `tests/operator_scripts/test_operator_merge_reset.py`: the `PATCH /git/refs/heads/<branch>` routes and requests. ruff format re-wrapped one line.
    - The S0001 guard `tests/guards/test_work_branch_search.py` stays green. A plain `"main"` is not one of its literals.

    **Criteria → tests** (from entry 8, unchanged):
    - criterion 1: `tests/shared/domain/test_work_branch.py::test_the_working_branch_is_one_constant_named_work_branch` (the earlier test, its value changed to `"develop"`)
    - criterion 2: `tests/machine/application/test_preflight_working_branch.py::test_a_remote_with_main_but_no_develop_gets_a_finding_naming_origin_develop`
    - criterion 3: `tests/guards/test_working_branch_in_agent_texts.py::test_no_agent_or_template_file_names_main_as_the_working_branch`, one row per form: `remote-ref`, `three-dot-diff`, `git-diff`, `human-merge`, `acceptance-report`, `already-holds`, `on-itself`
    - criterion 3, the side that stays: `tests/guards/test_working_branch_in_agent_texts.py::test_main_as_an_ordinary_word_stays_in_the_agent_files`
    - criteria 4 and 5: no test (`make check` and docs).

    **Files created**, both in the previous round: `tests/machine/application/test_preflight_working_branch.py` and `tests/guards/test_working_branch_in_agent_texts.py`.

    **Earlier test files changed:**
    - In this round, under the human's answer in entry 9: `tests/support/operator_skill_support.py` and the three `tests/operator_scripts/` files above.
    - In the previous round, under the human's leave of 2026-11-07: the files listed in entry 8.

    **Run.** One `uv run pytest -q` over the three operator-script files, both guards and the two criterion test files. Five still fail, as they should until the coder's change: criterion 1, criterion 2, and the guard rows `acceptance-report`, `already-holds` and `on-itself`. The operator-script tests pass. They no longer depend on `WORK_BRANCH`, so they stay green after the constant changes. `make lint` is green.

    **Modules not importable:** none. Every failure is a wrong result.

    **For the coder:**
    - Set `WORK_BRANCH = "develop"` in `src/factory/shared/domain/paths.py`.
    - Change the agent files and `operator/template/CLAUDE.md` and `Makefile`.
    - `tests/hosting/adapters/test_git_cli_branches.py` stays red until the constant changes, as entry 8 says.

    `lint`: lint: green (0.2 s)
12. factory: started doing as vm.
13. coder: **Question.** `make check` is red on one earlier test, and I can't fix it from inside my write paths.

    The test is `tests/agent_files/test_demo_makefile_secrets.py::test_the_todo_demos_secrets_target_is_the_templates`. It asserts that the `secrets` recipe in `demo/todo-service/project/Makefile` is the same as the one in `operator/template/Makefile`. To meet criterion 3 (guard row `remote-ref`), the template now says `origin/develop`. The demo still says `origin/main`, so the two recipes differ. The pytest summary line:
    `FAILED tests/agent_files/test_demo_makefile_secrets.py::test_the_todo_demos_secrets_target_is_the_templates - assert ['\t$(start)'..., '\tfi', ...] == ['\t$(start)'..., '\tfi', ...]`

    `demo/` is not in the coder's write paths in `factory/pipeline.yml`, and the Interface does not name it.

    Options:
    - (a) The demo follows the template. Either you commit the change on this branch, or you add `demo/*` to the coder's write paths for this story and I make it. The change is `sed -i -e 's#origin/main#origin/develop#g' -e 's/on main itself/on develop itself/' demo/todo-service/project/Makefile`. That covers lines 64–65, 68 and 114. The same forms are in `demo/todo-service/project/CLAUDE.md` lines 39–40 (`origin/main`, "on `main` itself") and would follow for consistency, though no test needs them.
    - (b) The template's `secrets` recipe keeps `origin/main`. That breaks criterion 3's `remote-ref` row, so I reject it.
    - (c) The demo test stops comparing against the template. That changes what the test checks, so I reject it.

    I would choose (a): the demo is a project made from the template, and the story says such a project works on `develop`.

    **What I built** (left in the working tree):
    - `src/factory/shared/domain/paths.py`: `WORK_BRANCH = "develop"`. The preflight finding follows from the constant: "no origin/develop to prepare the stage environment from".
    - `agents/agents/*.md`, every working-branch mention now says `develop`:
      - R10's "reaches `develop` only through the human's merge", in all seven files.
      - `develop...HEAD` in the documenter and reviewer files.
      - `git diff develop --` in the coder file.
      - "that `develop` already holds" in the reviewer file.
      - "writes your report to `develop`" in the acceptance-reviewer file.
      - "the main choice" and "the main decision" stay.
    - `operator/template/CLAUDE.md` and `operator/template/Makefile`: every `origin/main` is now `origin/develop`, and "on (`)main(`) itself" is now `develop`.

    **Main choice.** I did everything with the constant and text edits, with no new code, as the Interface says. I rejected extra work such as a preflight item of its own for `develop`.

    **Checks.** Every other test passes, including criteria 1–3. The targets before `make test` ran green; the targets after it did not run because the test target failed.

    **Refactor.** Nothing to simplify in this diff.

    **Noticed, not touched:**
    - `src/factory/machine/application/preflight.py:79`: the private names `_MAIN_REF` and `_NO_MAIN_TO_PREPARE` now hold `origin/develop`. The Interface says `src/factory/` is otherwise unchanged, so I left the names as they are. Renaming them would be a small refactor if you want it.

    The journal changed criterion 3 (entry 4) and settled the Kumpel scripts (entry 9). The Description already reflects both; I did not rewrite it.
14. 2026-11-07 human: (a). The coder may now write demo/todo-service/project/Makefile and demo/todo-service/project/CLAUDE.md (factory/pipeline.yml on main, for this story only). Make your sed change in both files.
15. factory: started doing as vm.
16. coder: I applied the human's answer (a) from entry 14. `make check` is now green: the last line is `check: green`, and `test: green (101.6 s)` with coverage at 99.22 %.

    **What I built this round:**
    - `demo/todo-service/project/Makefile`: every `origin/main` is now `origin/develop`. That is the `secrets` comment and recipe (lines 64–65 and 68) and `MUTATED` (line 114). "on main itself" is now "on develop itself". The demo's `secrets` recipe matches the template's again, so `tests/agent_files/test_demo_makefile_secrets.py::test_the_todo_demos_secrets_target_is_the_templates` passes.
    - `demo/todo-service/project/CLAUDE.md`: lines 39–40 now say `origin/develop` and "on `develop` itself".
    - I used the sed from entry 13, widened to the backticked form in the demo's `CLAUDE.md`.

    **Built in round 0** (already committed, see entry 13):
    - `src/factory/shared/domain/paths.py`: `WORK_BRANCH = "develop"`. The preflight finding follows from it.
    - `agents/agents/*.md`: every working-branch mention says `develop`.
    - `operator/template/CLAUDE.md` and `operator/template/Makefile`: the same, for a project made from the template.

    **Main choice.** Constant and text edits only, as the Interface says. I rejected a preflight item of its own for `develop`. For the demo, I rejected keeping `origin/main` in the template (it breaks criterion 3) and changing the demo test (that is a test edit).

    **Refactor.** I read the diff again and found nothing to change.

    **Description.** Not rewritten. Entry 4 (criterion 3) and entry 9 (the Kumpel scripts) are already in it. Entry 14 only widened the coder's write paths to the demo files and does not change what the task means.

    **Noticed, not touched:**
    - `src/factory/machine/application/preflight.py:79`: the private names `_MAIN_REF` and `_NO_MAIN_TO_PREPARE` now hold `origin/develop`. The Interface keeps `src/factory/` otherwise unchanged, so I left them.
    - The Kumpel scripts under `operator/skill/kumpel/scripts/` still work on `main`, as entry 9 decides; F0057-S0003 moves them.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
17. factory: started review as vm.
18. reviewer: Review, round 0. I read the work item and `git diff main...HEAD -- . ':!factory'`, then grepped `agents/agents`, `operator/template`, the demo and `src/factory` for the `main` that remains.

    Checked and fine:
    - Criteria 1–3 each have a test that checks what it is named after: `test_work_branch.py`, `test_preflight_working_branch.py`, and the guard `test_working_branch_in_agent_texts.py` with one row per form plus the "the main choice" side.
    - The forms are gone from `agents/agents/` and `operator/template/`. The only `main` left there is the ordinary word (coder.md:9 and 65, reviewer.md:59).
    - `make check` was green after the coder (entry 16).
    - No new suppression markers, secrets or string-built shell.

    Findings:
    1. `src/factory/pipeline/application/scheduler.py:135`: the problem is a remote that has `main` but no `develop`, which is the very case the Description says "must be clear at once". On such a remote, `_main_fault` now reports `repository_unavailable: the repository has no main branch yet`. That literal does not follow the constant, so the Interface's line "every other use follows the constant" is false here. No criterion covers this message.
       - Fix: write it as `f"the repository has no {WORK_BRANCH} branch yet"`.
       - That needs the human to widen the Interface. `src/` is "otherwise unchanged" today, so the coder should ask with `question`. The human would also add a criterion with a test: a remote with `main` and no `develop` gives a stop naming `develop`.
       - The tests that pin the old text need the human's leave too: `tests/pipeline/application/test_repository_waiter.py:32` (`NO_MAIN`), `tests/entry/test_health.py:64` and `:73`, and `tests/entry/test_run_waiter.py:40`.
       - `docs/operator-guide/health.md:187` should follow, in S0004 or in this story's docs.
    2. `src/factory` names and comments now say `main` where they mean the working branch, which is now `develop`. A reader of the code will be misled.
       - Names: `_MAIN_REF` and `_NO_MAIN_TO_PREPARE` (`machine/application/preflight.py:79`), `_ORIGIN_MAIN` and `_main_fault` (`pipeline/application/scheduler.py:18`, `:132`), `_MAIN_REF` (`pipeline/application/tick.py:35`), `_require_commit_beyond_main` and its message (`pipeline/application/stops.py:111` to `135`).
       - Docstrings and comments: `handlers/merged.py:2`, `:22`, `:29`; `handlers/reject.py:38`; `handlers/closed.py:67`; `tick.py:121`, `:195`.
       - No later F0057 story covers these: S0003 is Kumpel, S0004 and S0005 are documents.
       - Fix: rename them to the working branch (for example `_WORK_REF`, "on the working branch") with the same widened Interface as finding 1. The coder already noted the preflight names twice (entries 13 and 16); asking about them together with finding 1 costs no extra round.

    description corrected: "The agent files and the project template name the branch too, so they follow." -> "The agent files, the project template and the todo demo's project made from it (`demo/todo-service/project/Makefile` and `CLAUDE.md`) name the branch too, so they follow." This follows the human's answer in entry 14.

    Earlier tests (item 6):
    - These test files were changed only to follow the new `WORK_BRANCH` or the agent and template texts, under the human's leave in the Interface (2026-11-07; tester's entries 8 and 11):
      - `tests/agent_files/test_claude_agent_texts.py`
      - `tests/agent_files/test_claude_agent_texts_docs_route.py`
      - `tests/agent_files/test_claude_agent_texts_review_groups.py`
      - `tests/agent_files/test_claude_files.py`
      - `tests/agents/application/test_project_agents.py`
      - `tests/entry/test_wiring_run.py`
      - `tests/guards/test_human_clone.py`
      - `tests/hosting/adapters/test_git_cli_branches.py`
      - `tests/hosting/adapters/test_git_cli_reading.py`
      - `tests/hosting/domain/test_hosting.py`
      - `tests/machine/application/test_container_environment.py`
      - `tests/pipeline/application/test_claims_refusals.py`
      - `tests/pipeline/application/test_preflight_stops_commit.py`
      - `tests/pipeline/application/test_stop_publisher.py`
      - `tests/pipeline/application/test_tick_stop_records.py`
      - `tests/shared/domain/test_paths.py`
      - `tests/shared/domain/test_work_branch.py`
      - `tests/work/application/test_acceptance_service.py`
      - `tests/work/application/test_acceptance_snapshots.py`
      - `tests/work/domain/test_stop_table.py`
    - These were changed under the human's answer in journal entry 9 (`SCRIPTS_BRANCH = "main"`):
      - `tests/support/operator_skill_support.py`
      - `tests/operator_scripts/test_operator_merge_reset.py`
      - `tests/operator_scripts/test_operator_skill_scripts.py`
      - `tests/operator_scripts/test_operator_skill_signature.py`
19. factory: started doing as vm.
20. coder: **Question (round 1).** Both of the reviewer's findings (entry 18) need you to widen the Interface. It says `src/factory/` is "otherwise unchanged", and finding 1 also touches earlier tests. I changed nothing this round.

    I confirmed finding 1. `src/factory/pipeline/application/scheduler.py:135` returns the literal `"the repository has no main branch yet"` when `origin/develop` does not resolve. On a remote that has `main` but no `develop`, which is the case the Description says "must be clear at once", the stop names the wrong branch. The text is pinned by:
    - `tests/pipeline/application/test_repository_waiter.py:32` (`NO_MAIN`)
    - `tests/entry/test_health.py:64` and `:73`
    - `tests/entry/test_run_waiter.py:40`
    - the docs: `docs/operator-guide/health.md:187`

    Options:
    - **(a) Widen for both findings.**
      - The scheduler's message becomes `f"the repository has no {WORK_BRANCH} branch yet"`.
      - The private names and comments that mean the working branch are renamed or reworded, with no change in behaviour:
        - `_MAIN_REF` and `_NO_MAIN_TO_PREPARE` in `machine/application/preflight.py`
        - `_ORIGIN_MAIN` and `_main_fault` in `pipeline/application/scheduler.py`
        - `_MAIN_REF` in `pipeline/application/tick.py`
        - `_require_commit_beyond_main` and its message in `pipeline/application/stops.py`
        - the docstrings and comments in `handlers/merged.py`, `handlers/reject.py`, `handlers/closed.py` and `tick.py`
      - You add a criterion: on a remote with `main` and no `develop`, the repository stop names `develop`.
      - You give the tester leave to make the four pinned tests above follow the constant. I would end the next round with `tests` naming that criterion and those tests, then make the code change once they are red.
      - `health.md:187` follows in S0004, or in this story's docs criterion if you prefer.
    - **(b) Finding 1 only.** Same as (a), but the renames and comments stay for a later story.
    - **(c) Neither.** Both stay as they are, and a later story takes them on (R13).

    I would choose (a). The wrong message is a real fault on exactly the remote this story warns about. The renames are cheap and make no difference to behaviour, and no later F0057 story covers them (S0003 is Kumpel; S0004 and S0005 are documents).

    **State.** The working tree is as entry 16 left it, and `make check` was green there.
