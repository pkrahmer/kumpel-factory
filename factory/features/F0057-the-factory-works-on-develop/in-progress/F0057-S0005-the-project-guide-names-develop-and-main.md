---
stage: docs-approval
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 647
comments_read: []
handed_over: docs-approval
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T01:28:06.900773Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T01:28:06.908023Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T01:28:24.740341Z'
  stage: intake
  run: 58d18eff216448f4a4d1421409871cb2
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T01:28:29.396342Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-08T01:34:28.170704Z'
  stage: docs-only
  run: ceb3439427b044c6908d8cf7daa98926
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T01:34:33.224979Z'
  stage: docs-review
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-08T01:35:26.619144Z'
  stage: docs-review
  run: a44b8f1b58424fa69de17292dcd987b5
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T01:35:31.481318Z'
  stage: docs-only
- number: 9
  speaker: documenter
  kind: result
  at: '2026-11-08T01:39:48.044112Z'
  stage: docs-only
  run: 11e2f1fdad65485f99f2c3547cc29eb6
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T01:39:53.380311Z'
  stage: docs-review
- number: 11
  speaker: reviewer
  kind: result
  at: '2026-11-08T01:40:28.965984Z'
  stage: docs-review
  run: 9cedb7c3b3b24204ae7c4209378a0575
---

# The project guide names develop and main

## Description

After F0057-S0002 the factory's code reads and writes `origin/develop` through the constant `WORK_BRANCH`, but the project guide still says `origin/main` about 100 times, in the descriptions of the pipeline, the work items, the watching, the machine, the hosting and the agents. This story corrects the project guide, so that a developer reads the branch the code uses. It changes no code and no test.

## Interface

- The documents: `docs/project-guide/*.md`. Every mention of the factory's working branch says `develop`, or names `WORK_BRANCH` where the page describes the code; a mention of the line of accepted features says `main`.
- `docs/project-guide/work.md`, the `paths` table: `WORK_BRANCH` in `factory.shared.domain.paths` names the working branch, and the guard `tests/guards/test_work_branch_search.py` keeps the name out of every other file.
- The stop reason `main_branch_failing` keeps its name and means the working branch (F0057 decision 6), where a page names it.
- The documenter finds the mentions by script (`grep -nE` for `main` as a branch in `docs/project-guide/`) and quotes the script's list of the mentions left as `main` in its entry, each meaning the line of accepted features; the reviewer checks with the same script. The tables of the project guide that the document check reads keep their rows. No test changes; the story takes the docs route.

## Acceptance criteria

1. No page of `docs/project-guide/` names `main` as the branch the factory works on; every remaining `main` as a branch means the line of accepted features (the script of the Interface, its output quoted).
2. `work.md`'s `paths` table names `WORK_BRANCH` and the guard that keeps the name in one place.
3. `make documents` ends with `documents ok (<seconds> s)`.
4. `make check` stays green.
5. docs: the files of the Interface; a developer reads the branch the code uses.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names concrete documents (`docs/project-guide/*.md`), `WORK_BRANCH` in `factory.shared.domain.paths`, and the guard `tests/guards/test_work_branch_search.py`, which exists. The `paths` table in `work.md` (line 394) still shows `main` as the value, so there is something to change. The story changes only documents, so the Interface needs no signatures.
   - Criteria: 1 is checked by the grep script and its quoted output. 2 is checked by reading the `paths` table. 3 and 4 are the make targets. No Interface rule has a failing side that needs a test, because the story only edits documents.
   - Smoke test: `uv run python -m factory.entry.check_documents | tail -1` is runnable and does not call pytest, so the `-q` question does not arise. Its `Expect:` line, `documents ok (<seconds> s)`, can be checked against the output.
   - Docs criterion: it names the files and what the reader must know (a developer reads the branch the code uses). It dictates no sentences.
   - Architecture: nothing under `src/` changes. The paths are in `docs/`, which the documenter may write.
   - Scope: this is S0005 of F0057, which lists the project guide in its scope. It keeps `main_branch_failing` as decision 6 says. No code or test change, so the route is docs-only.
4. factory: started docs-only as vm.
5. documenter: Changed `docs/project-guide/` so every mention of the factory's working branch says `develop`. No code, test or other file was touched.

   Files changed, one line each:
   - `README.md`: the `remote` fixture's `develop`, and the stories started on `develop` (`stage_run_support`).
   - `agents.md`: `origin/develop` for the stage-file and pipeline-definition reads. It also covers the push to `develop`, the test files `develop` already holds, `git diff --name-status develop...HEAD`, `git diff develop...HEAD` and `push_file("develop", ...)`.
   - `hosting.md`: `WORK_BRANCH` is `"develop"`, and "the main branch" is now "the working branch (`develop`)". It also covers the `remote` fixture, `human.start` and `human.merge`, and every `origin/main` is now `origin/develop`.
   - `machine.md`: the preflight's `lint`, the probe stop text, the project's stage file on `develop`, `git diff develop`, and `origin/develop` everywhere.
   - `operator.md`: `reset-to-tag.sh` moves `develop`. I added "`main` is left alone, since only a promotion reaches it", which I took from the script's own header.
   - `pipeline.md`: the restore (`checkout("develop", start_point="origin/develop")`), the publish and archive steps, and the stop records published to `develop`. I added a note on `main_branch_failing`: the name is kept and means the working branch (decision 6).
   - `watching.md` and `work.md`: `origin/develop` everywhere.
   - `work.md`: the `paths` table now reads `origin`, `develop`. Its bullet names `WORK_BRANCH` and says `tests/guards/test_work_branch_search.py` fails on the literals `origin/main`, `heads/main`, `-b main` and `--initial-branch=main`. I checked these against the guard's `LITERALS`.
   - `shared.md`: only `origin/main` became `origin/develop`.

   **The script.** I found the mentions with `grep -rnE "\bmain\b" docs/project-guide`, minus the names that are not a branch. The list left after my edits:
   - **Intended `main` (the line of accepted features):** `operator.md:133` ("`main` is left alone") and `work.md:396`, where the guard's old literals are quoted. Neither is the working branch.
   - **Not a branch:**
     - `main` as the entry-point function: `watching.md` 93, 103, 104, 246 and 251; `work.md` 313, 366 and 477; `pipeline.md` 755, 756, 883 and 885; `README.md` 207, 464, 467 and 477; `shared.md` 288.
     - Real code names kept: `stage_file_on_main`, `red_main`, `MainRow`, `MainRun`, and `main_probed`/`main_failed`.
     - The variable `main` in `prepare(main, WORK_BRANCH, ...)` (`machine.md:400`).
     - "its main function" (`style.md:112`).
   - **Left as an example ref name:** `hosting.md:332`, `hosting.md:336` and `hosting.md:338`. They use `+main`, `^main` and "the factory's names (`main`, `work-item/<id>`)" as ref-name examples, and the tests (`test_git_cli_arguments.py`, `test_git.py`) use the same strings. The last one, "the factory's names", is now slightly off, since the working branch is `develop`. Say if you want it changed.

   **Cross-read.**
   - Current: `docs/project-guide/style.md` and `glossary.md` have no branch mention.
   - Not read: `docs/operator-guide/`, `README.md` and `docs/decisions.md`, which are outside the story's files. A grep of `docs/operator-guide` shows `records.md` has only an unrelated "not run (vm)" match.

   `make documents` ends `documents ok (57.8 s)`. I ran no `make check`, since I changed only documents.

   I wrote no decision-log entry.

   `check`: check: green
   `secrets`: secrets: green (2.0 s)
   `documents`: documents ok (57.5 s)
6. factory: started docs-review as vm.
7. reviewer: Docs review, round 0. I read the work item and `git diff develop...HEAD -- README.md docs operator/README.md`, which covers the nine files under `docs/project-guide/`. I checked the claims against the code on the branch:
   - `WORK_BRANCH = "develop"` and `REMOTE = "origin"` are in `src/factory/shared/domain/paths.py:12-13`.
   - `PIPELINE_REF = f"{REMOTE}/{WORK_BRANCH}"` is in `src/factory/pipeline/application/pipeline_loading.py:15`.
   - The restore's `git.checkout(WORK_BRANCH, start_point=_WORK_REF)` is in `src/factory/pipeline/application/tick.py:197`.
   - The guard's `LITERALS` are in `tests/guards/test_work_branch_search.py:9`.
   - `prepare(main, WORK_BRANCH, ...)`, where `main` is a variable, is in `src/factory/machine/application/preflight.py:286`.
   - The `reset-to-tag.sh` header and its "left main alone" line are in `operator/skill/kumpel/scripts/reset-to-tag.sh:4-5, 93`.
   - The ref-name examples `+main` and `^main` are in `tests/hosting/adapters/test_git_cli_arguments.py:159, 229`.
   All of these match. Criterion 2 is met at `work.md:394-396`.

   I ran the Interface's script: `grep -rnE "\bmain\b" docs/project-guide`, with code names and entry-point functions filtered out. The documenter filtered whole lines by code name, so it missed a working-branch mention on a line that also holds `stage_file_on_main`. Criterion 1 is not met yet.

   Findings:
   1. `docs/project-guide/machine.md:723`: "beside where the preflight probes `main`". The preflight probes the working branch (`_WORK_REF`, `src/factory/machine/application/preflight.py:509`), so this line breaks criterion 1. Fix: say "probes `develop`" (or "the working branch"), and keep `stage_file_on_main` as the code name.
   2. `docs/project-guide/README.md:174`: "give the rig after one probe of a red main". This means a failing working branch, not the code name `red_main`. Fix: "after one probe of a red `develop`" (or "of a failing working branch"), and keep the fixture name `red_main` as it is.
   3. `docs/project-guide/hosting.md:338`: "the factory's names (`main`, `work-item/<id>`)". The factory's branch names are now `develop` (`WORK_BRANCH`) and `work-item/<id>`, so this line is stale, as the documenter's own entry says. Fix: change it to "(`develop`, `work-item/<id>`)". Leave the examples `+main` and `^main` on lines 332, 336 and 338, because the tests use those strings.

   Not findings, but checked:
   - `operator.md:133` (`main` as the line of accepted features) and `work.md:396` (the guard's old literals) are rightly left as `main`.
   - `pipeline.md`'s note that `main_branch_failing` keeps its name matches F0057 decision 6.
   - The other remaining matches are entry-point `main` functions, the variable at `machine.md:400`, or code names.
8. factory: started docs-only as vm.
9. documenter: Round 1: fixed exactly the reviewer's three findings in `docs/project-guide/`. No other file touched.
   - `machine.md:723`: "where the preflight probes `main`" now says `develop`; `stage_file_on_main` stays as the code name.
   - `README.md:174`: "after one probe of a red main" now says "a red `develop`"; the fixture name `red_main` stays.
   - `hosting.md:338`: "the factory's names (`main`, `work-item/<id>`)" now reads "(`develop`, `work-item/<id>`)". The `+main` and `^main` examples on lines 332 and 336 stay, since the tests use those strings.

   Remaining `main` as a branch: `operator.md:133` and `work.md:396`, both meaning the line of accepted features or the guard's old literals, as in round 0. The other matches are the entry-point function, the variable at `machine.md:400`, or code names.

   Cross-read: the other pages were read in round 0 and I changed nothing in them this round.

   `make documents` ends `documents ok (58.5 s)`. I ran no `make check`, since I changed only documents. I wrote no decision-log entry.

   `check`: check: green
   `secrets`: secrets: green (2.0 s)
   `documents`: documents ok (57.9 s)
10. factory: started docs-review as vm.
11. reviewer: Docs review, round 1. I read the work item and `git diff develop...HEAD -- README.md docs operator/README.md`: 9 files under `docs/project-guide/`, 92 lines changed.

    The three round-0 findings are fixed:
    - `machine.md:723` now says "probes `develop`". This matches `src/factory/machine/application/preflight.py:509`, which resolves `_WORK_REF`. `stage_file_on_main` stays as the code name, as in `src/factory/entry/run.py:252`.
    - `README.md:174` now says "a red `develop`". The fixture name `red_main` stays.
    - `hosting.md:338` now names the factory's names as (`develop`, `work-item/<id>`). The ref-name examples `+main` and `^main` stay, because the tests use those strings.

    Criterion 1: I ran the Interface's script, `grep -rnE "\bmain\b" docs/project-guide`. I also ran a second grep for `Main`, `main branch`, `main_branch` and `the main`.
    - `main` as the line of accepted features: `operator.md:133`.
    - The guard's old literals: `work.md:396`.
    - Ref-name examples: `hosting.md:332, 336, 338`.
    - `main_branch_failing` at `pipeline.md:507`, with its note that the name is kept and means the working branch (F0057 decision 6).
    - Every other match is an entry-point function, the variable `main` (`machine.md:400`, `preflight.py:278`), "its main function" (`style.md:112`), or a code name (`MainRow`, `MainRun`).
    - No match names `main` as the working branch.

    Criterion 2: the `paths` table at `work.md:394` gives `REMOTE`, `WORK_BRANCH` as `origin`, `develop`. Its bullet at `work.md:396` names `tests/guards/test_work_branch_search.py` and lists that guard's `LITERALS`. Its scope ("no code under `src/factory/` and no test") matches the guard's `SCOPE = ("src/factory", "tests")`.

    Criteria 3 and 4: the journal records `documents ok (57.9 s)` and `check: green`.

    The round-1 edits are single-word replacements and change none of round 0's style findings.

    no findings
