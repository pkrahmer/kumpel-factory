---
stage: doing
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 644
comments_read: [6713932106, 6714015757, 6714081152, 6714164393, 6714248996]
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
- number: 21
  speaker: human
  kind: comment
  at: '2026-11-07T23:00:07.516301Z'
  stage: doing
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-07T23:00:10.052206Z'
  stage: doing
- number: 23
  speaker: coder
  kind: result
  at: '2026-11-07T23:01:00.993861Z'
  stage: doing
  run: a2af38650a854b71ae65fe104243b0f7
- number: 24
  speaker: factory
  kind: started
  at: '2026-11-07T23:01:06.274330Z'
  stage: tests
- number: 25
  speaker: tester
  kind: result
  at: '2026-11-07T23:02:01.527579Z'
  stage: tests
  run: db2d49bea1ad4f0e8b02fa0cb07edcba
- number: 26
  speaker: factory
  kind: started
  at: '2026-11-07T23:02:06.715177Z'
  stage: doing
- number: 27
  speaker: coder
  kind: question
  at: '2026-11-07T23:05:55.163206Z'
  stage: doing
  run: f0300b8c51ae44989114f78f826cbdfb
  blocked: question
- number: 28
  speaker: human
  kind: comment
  at: '2026-11-07T23:07:44.223466Z'
  stage: doing
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
21. 2026-11-07 human: (a), as you describe it: the scheduler's message follows WORK_BRANCH, the private names, comments and docstrings that mean the working branch are reworded without behaviour change, a new criterion (a remote with main and no develop: the repository stop names develop), and the tester has my leave to make the four pinned tests follow the constant. health.md:187 goes into this story's docs criterion.
22. factory: started doing as vm.
23. coder: Round 1, after the human's answer (a) in entry 21. No code changed this round. The working tree is still as entry 16 left it, and `make check` was green there. The new criterion needs its test before the code can change, so this goes to the tester first.

    **For the tester (the human's answer in entry 21):**
    - **New criterion, placed before `make check` and docs:** on a fake remote that has `main` but no `develop`, the repository stop (`repository_unavailable`) names `develop`. Its detail is `the repository has no develop branch yet`. The test should be red against today's literal in `src/factory/pipeline/application/scheduler.py:135`.
    - **The human's leave to change earlier tests:** the four places that pin the old text `the repository has no main branch yet` follow `WORK_BRANCH`, for example `f"the repository has no {WORK_BRANCH} branch yet"`. Each test keeps its name and what it checks:
      - `tests/pipeline/application/test_repository_waiter.py:32` (`NO_MAIN`)
      - `tests/entry/test_health.py:64` and `:73`
      - `tests/entry/test_run_waiter.py:40`

    **What I will do once those tests are red:**
    - The scheduler's message follows `WORK_BRANCH`.
    - I will reword the private names, comments and docstrings that mean the working branch, with no change in behaviour:
      - `_MAIN_REF` and `_NO_MAIN_TO_PREPARE` in `machine/application/preflight.py`
      - `_ORIGIN_MAIN` and `_main_fault` in `pipeline/application/scheduler.py`
      - `_MAIN_REF` in `pipeline/application/tick.py`
      - `_require_commit_beyond_main` and its message in `pipeline/application/stops.py`
      - the docstrings and comments in `handlers/merged.py`, `handlers/reject.py`, `handlers/closed.py` and `tick.py`
    - Before renaming the message in `stops.py`, I will check whether a test pins it. If one does, I will ask.

    **The Description is not rewritten yet; it needs a hand.** I tried to rewrite `## Description`, `## Interface` and the criteria to match entry 21, and the edit was refused. These are the changes it should carry, for the stage that may write it:
    - Interface: the scheduler's line and the renames, as listed above.
    - A new criterion 4, with the text above. `make check` and docs become 5 and 6.
    - The docs criterion gains one more item. `docs/operator-guide/health.md:187` (the row "the repository has no main branch yet") names `develop`.

    **Noticed, not touched:**
    - The next row of `health.md`, "`origin/main` has no factory/pipeline.yml yet", probably follows the constant already. The documenter should check both rows together.
24. factory: started tests as vm.
25. tester: I made the test changes the human approved in entry 21, as the coder listed them in entry 23. I also wrote the test for the new criterion. All the new and changed tests are red for the right reason.

    Criterion → test:
    - criterion 4 (a remote with `main` and no `develop` gives a repository stop naming `develop`): `tests/pipeline/application/test_repository_waiter.py::test_a_remote_with_main_but_no_develop_is_a_stop_naming_develop`
      - The remote is a bare repository whose only branch is `main`, and it holds `factory/pipeline.yml`.
      - The test checks that `prepare()` returns False and that the only `repository_unavailable` detail is `the repository has no develop branch yet`.
    - Criteria 1 to 3 keep the tests named in entries 8 and 11. Criteria 5 and 6 (`make check`, docs) have no test.

    Earlier tests changed under the human's leave (entry 21). Each keeps its name and what it checks; only the expected text now follows `WORK_BRANCH`:
    - `tests/pipeline/application/test_repository_waiter.py`: `NO_MAIN` is now `f"the repository has no {WORK_BRANCH} branch yet"`.
    - `tests/entry/test_health.py`: the stop's detail and the printed line, lines 64 and 73. I added an import of `WORK_BRANCH`.
    - `tests/entry/test_run_waiter.py`: the expected detail at line 40.

    Work item: I rewrote `## Interface` and `## Acceptance criteria` to match entry 21, since the coder's edit of it was refused (entry 23).
    - Interface: added the scheduler's message, which follows the constant, and the renames with no change in behaviour.
    - Criteria: the new criterion is 4; `make check` and docs are now 5 and 6. The docs criterion also names `docs/operator-guide/health.md`'s row "the repository has no main branch yet".
    - `## Description` is unchanged.
    - If the take drops this edit, the next stage should carry it.

    Run (`uv run pytest -q` on the three files):
    - 4 tests fail: the new one, `test_a_remote_without_any_commit_is_a_stop_at_the_clocks_time` and `test_a_repeated_fault_is_reported_once_and_a_changed_fault_again` in the waiter file, and `test_run_instance_over_a_remote_without_commits_stops_and_pauses_thirty_seconds`. Each fails on a wrong result: today's code still says `main`.
    - `test_health.py` passes. It reads a stop that the test writes itself, so it does not depend on the code.
    - Every module imported; no import errors.

    `make lint` is green.

    Files created: none. Files changed: the three test files above and the work item.

    The factory left out changes outside the write paths: factory/features/F0057-the-factory-works-on-develop/in-progress/F0057-S0002-the-factory-works-on-develop.md.

    `lint`: lint: green (0.1 s)
26. factory: started doing as vm.
27. coder: **Question (round 1).** I made the change you approved in entry 21. `make check` is still red, and the only failure comes from two tests disagreeing. I can't fix it without changing a test.

    The new criterion-4 test `tests/pipeline/application/test_repository_waiter.py::test_a_remote_with_main_but_no_develop_is_a_stop_naming_develop` (lines 175 and 177) writes the literal `--initial-branch=main`. The guard from F0057-S0001, `tests/guards/test_work_branch_search.py::test_no_file_in_the_source_or_the_tests_writes_the_working_branch_by_name`, forbids that literal everywhere under `tests/`. From the failed `make test` run:
    ```
    E   AssertionError: assert ['tests/pipel...-branch=main'] == []
    E     Left contains one more item: 'tests/pipeline/application/test_repository_waiter.py: --initial-branch=main'
    tests/guards/test_work_branch_search.py:28: AssertionError
    ```
    Every other test passes, the criterion-4 test included. Every other target is green: lint, types, layers, sast, secrets and licenses. Coverage is 99 %.

    Options:
    - (a) The tester names the other branch through a module constant, `OTHER_BRANCH = "main"`, and uses `f"--initial-branch={OTHER_BRANCH}"` on lines 175 and 177 (and in the push on line 180). `tests/machine/application/test_preflight_working_branch.py:14` already does this for criterion 2. The test keeps its name and what it checks. I would then end the next round with `tests` naming exactly this change.
    - (b) The guard allows this literal in that one file. That weakens S0001's guard, so I reject it.

    I would choose (a).

    **What I built this round** (left in the working tree, no behaviour change other than the one message):
    - `src/factory/pipeline/application/scheduler.py`:
      - The repository stop's detail is now `f"the repository has no {WORK_BRANCH} branch yet"`.
      - `_ORIGIN_MAIN` is renamed `_WORK_REF` and `_main_fault` is renamed `_work_branch_fault`.
    - `src/factory/machine/application/preflight.py`:
      - `_MAIN_REF` is renamed `_WORK_REF` and `_NO_MAIN_TO_PREPARE` is renamed `_NO_WORK_BRANCH_TO_PREPARE`.
      - The module docstring, the class docstring and four comments now say the working branch.
    - `src/factory/pipeline/application/tick.py`: `_MAIN_REF` is renamed `_WORK_REF`, and the two comments are reworded.
    - `src/factory/pipeline/application/stops.py`:
      - `_require_commit_beyond_main` is renamed `_require_commit_beyond_work_branch`. Its message now names `{WORK_BRANCH}`; no test pins it.
      - The `StopPublisher` docstrings are reworded.
    - `handlers/merged.py`, `handlers/reject.py` and `handlers/closed.py`: the docstrings and the comment now say the working branch.

    **Main choice.** I renamed the names in each module to `_WORK_REF`, matching the name each module already used for itself. I rejected adding one shared `WORK_REF` constant to `factory.shared.domain.paths`, because that goes beyond the listed rewording.

    **Refactor.** I read the diff once. I only reworded one comment in `closed.py` that had become ambiguous ("the branch").

    **Noticed, not touched:**
    - The preflight's `main_branch_failing` details still say "on main at …" (`preflight.py:474`, `:559`, `:572`–`575`). Tests pin them (`test_preflight_run.py`, `test_preflight_run_environment.py`, `test_preflight_stale_main_stop.py`), and they are outside the list you approved. The local variables named `main` and the stamp fields `main_failed`/`main_probed` are also unchanged.
    - Other modules still have their own `_MAIN_REF`/`_ORIGIN_MAIN` for `origin/develop`, which is outside the approved list: `work/application/work_items.py:37`, `work/application/acceptance.py:69`, `work/application/acceptance_reading.py:41`, `watching/application/watcher.py:18` and `entry/wiring.py:184`.
    - The tester's rewrite of `## Interface` and the criteria (entry 25) was left out of the take, so the work item still lists only criteria 1–5. My write paths do not include the work item either. Criterion 4 (a remote with `main` and no `develop` gives a repository stop naming `develop`) and the `health.md:187` item of the docs criterion still need to be written in by a stage that may write it.
28. 2026-11-07 human: (a).
