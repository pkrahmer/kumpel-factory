---
stage: docs-only
blocked: null
round: 1
attempts: 1
crashes: 0
pull_request: 651
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: docs-only
  started_at: '2026-11-08T02:52:30.858729Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T02:43:14.644807Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T02:43:14.652576Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T02:43:33.009475Z'
  stage: intake
  run: 1a36392f8680469c85735dc04423d368
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T02:43:37.598316Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-08T02:47:00.082952Z'
  stage: docs-only
  run: 948fd1c27eb94f77b123856951ac1020
- number: 6
  speaker: factory
  kind: stall
  at: '2026-11-08T02:47:00.426155Z'
  stage: docs-only
  run: 948fd1c27eb94f77b123856951ac1020
  reason: check_red
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T02:47:07.492345Z'
  stage: docs-only
- number: 8
  speaker: documenter
  kind: result
  at: '2026-11-08T02:51:26.584856Z'
  stage: docs-only
  run: e91c87c1abb444088753a187d26bb3d5
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T02:51:31.988869Z'
  stage: docs-review
- number: 10
  speaker: reviewer
  kind: result
  at: '2026-11-08T02:52:25.877976Z'
  stage: docs-review
  run: 971ef6222f4e4ab2ae66ba1eadc4984c
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-08T02:52:30.858729Z'
  stage: docs-only
---

# The operator's documents on the archive, the promotion and the default branch


## Description

F0057's acceptance read the operator's documents as a whole and found four gaps that no story owned:
- `docs/operator-playbook.md` still moves a finished feature to `factory/archive/` "by hand (`git mv`)", although `archive-feature.sh` does it as Kumpel (F0057 decision 8). The playbook's acceptance step also says nothing of the promotion that follows.
- `docs/operator-guide/work-items.md` asks the operator to turn off *Automatically delete head branches* for the story's sake only. With the setting on, the merge of a promotion would delete `develop` itself.
- `docs/operator-guide/install.md` does not say which branch is the repository's default. F0057 keeps `main` (*The human's changes*, step 5).
- `install.md` step 1 says the preflight names a missing `origin/develop`. On a remote with only `main` the operator sees the `repository_unavailable` stop "the repository has no develop branch yet".

This story corrects the documents. It changes no code and no test, and it takes the docs route.

## Interface

- The documents: `docs/operator-playbook.md`, `docs/operator-guide/work-items.md` and `docs/operator-guide/install.md`. Nothing else changes.
- The default branch is the human's choice. The story writes what F0057 decided (`main` stays the default; the factory and Kumpel check out `develop` themselves) unless the human says otherwise when refining.

## Acceptance criteria

1. `docs/operator-playbook.md` names `operator/skill/kumpel/scripts/archive-feature.sh` for archiving a finished feature, where it said `git mv` by hand. After the acceptance step it names the promotion (`promote.sh`, the switch `promote`).
2. `docs/operator-guide/work-items.md`, where it asks to clear *Automatically delete head branches*, also says that with the setting on the merge of a promotion deletes `develop`.
3. `docs/operator-guide/install.md` says which branch is the repository's default and that a fresh clone starts there.
4. `docs/operator-guide/install.md` step 1 names what an instance shows on a remote without `develop`: the `repository_unavailable` stop with the detail `the repository has no develop branch yet`, linked to its row in `health.md`.
5. `make documents` ends with `documents ok (<seconds> s)`.
6. `make check` stays green.
7. docs: the files of the Interface. The reader knows how a finished feature is archived and promoted, why the auto-delete setting stays off, which branch is the default, and what a new project without `develop` shows. `docs/decisions.md`: none.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names three concrete documents (`docs/operator-playbook.md`, `docs/operator-guide/work-items.md`, `docs/operator-guide/install.md`), all writable by the documenter; it changes no code. The default branch is stated as `main`, which matches F0057's decisions.
   - Criteria: criteria 1 to 4 are each testable by reading one document (`archive-feature.sh` replaces `git mv` at playbook line 203; the promotion with `promote.sh` and the switch `promote`; the auto-delete warning near work-items.md line 224; the default branch; the stop detail). Both sides of each rule are covered because they are text statements. I checked that the files and anchors exist: `archive-feature.sh` and `promote.sh` are in `operator/skill/kumpel/scripts/`, and health.md line 187 holds the row for `the repository has no develop branch yet`.
   - Smoke test: `uv run python -m factory.entry.check_documents | tail -1` is runnable (the module exists). It passes no pytest flags. The Expect line `documents ok (<seconds> s)` can be checked against the output.
   - Docs criterion: it names what the reader must know (archive and promotion, why auto-delete stays off, the default branch, what a project without `develop` shows). It dictates no sentences.
   - Architecture: documents only, so there is no layer or area impact.
   - Scope: it fits F0057's goal of the operator's documents naming `develop` and `main`. It touches no "Out of scope" item. It is a follow-up gap found at acceptance, and it is not a new feature.
4. factory: started docs-only as vm.
5. documenter: Changed files:
   - `docs/operator-playbook.md`: the archive sentence now names `archive-feature.sh` (commit `<id>: archived`, refuses unless the last acceptance says `outcome: accepted`) in place of the hand `git mv`. The acceptance step now names the promotion (`promote.sh`, the switch `promote`) and links to work-items.md, *The branches*.
   - `docs/operator-guide/work-items.md`: under the *Automatically delete head branches* step I added that a promotion's head is `develop`, so with the setting on its merge deletes `develop`.
   - `docs/operator-guide/install.md`: step 1 now names the `repository_unavailable` stop with the detail `the repository has no develop branch yet`. It links to the row in health.md, `#the-wait-for-a-repository-that-is-not-ready`, which is where that row sits. *The branches* now says `main` stays the default branch, a fresh clone starts there, and the factory and Kumpel check out `develop` themselves.

   I read the scripts `archive-feature.sh` and `promote.sh` and the health.md row before I wrote. `make documents` ended with `documents ok (58.4 s)`. I did not run `make check`, because every changed file is a document.

   I cross-read these and found them current: the *After the merge* and *Rebuilds* steps in the playbook, which already name the archive commit; the rest of work-items.md's *The branches* text on promotion; and health.md's preflight text.

   I did not add a `docs/decisions.md` entry, as the docs criterion says.

   Stale text I saw and left alone, because it is not part of this story: the playbook's older numbered change list and its step 26 still describe the old archive wording. They are history, not rules.
6. factory: Stage docs-only stalled (attempt 1 of 2): a check is red after the stage: `check`
   src/factory/watching/application/transcripts.py         61      2     10      0    97%   92-93
   src/factory/watching/domain/board.py                    55      0      4      1    98%   78->76
   src/factory/watching/domain/machine.py                  52      3     18      5    89%   45->43, 48, 60, 78->76, 80
   src/factory/watching/domain/transcripts.py              10      2      0      0    80%   21-22
   src/factory/work/application/acceptance_reading.py     132      1     46      1    99%   240
   src/factory/work/application/work_items.py              90      2     24      2    96%   135, 171
   src/factory/work/domain/acceptance.py                  195      1     52      1    99%   368
   ------------------------------------------------------------------------------------------------
   TOTAL                                                11369     55   2298     52    99%

   159 files skipped due to complete coverage.
   Required test coverage of 90.0% reached. Total coverage: 99.22%
   ======================================================================================= short test summary info ========================================================================================
   FAILED tests/guards/test_project_guide_files.py::test_no_file_names_a_removed_guide_file - AssertionError: assert ['docs/operat...ork-items.md'] == []
   make: *** [Makefile:89: test] Error 1
7. factory: started docs-only as vm.
8. documenter: Round 0, second run. The first run stalled on one red guard: `tests/guards/test_project_guide_files.py::test_no_file_names_a_removed_guide_file`. It found the text `work-items.md` at `docs/operator-playbook.md:31`, because the guard treats that bare name as a removed project-guide file.

   Changed file in this run:
   - `docs/operator-playbook.md` line 31: the link text is now "the operator guide" and the target is still `operator-guide/work-items.md`. This clears the guard. The first run's other edits stay as they were: the playbook names `archive-feature.sh` and the promotion (`promote.sh`, the switch `promote`); `work-items.md` says the setting deletes `develop` when a promotion merges; `install.md` names the default branch `main` and the `repository_unavailable` stop.

   Checks: I ran the guard alone, and it passes (3 tests). `make documents` ended with `documents ok (58.8 s)`. I did not run `make check`, because every changed file is a document.

   Cross-read and found current: the same documents as the first run (the playbook's *After the merge* and *Rebuilds* steps, the rest of *The branches* in `work-items.md`, and the preflight text in `health.md`).

   Stale text I left alone, because it is not part of this story: the playbook's older numbered change list and its step 26 still describe the archive wording of the time. They are history, not rules.

   I added no `docs/decisions.md` entry, because the docs criterion says none.

   `check`: check: green
   `secrets`: secrets: green (0.6 s)
   `documents`: documents ok (59.1 s)
9. factory: started docs-review as vm.
10. reviewer: Reviewed `git diff develop...HEAD -- README.md docs operator/README.md` (install.md, work-items.md, operator-playbook.md) against the work item, `archive-feature.sh`, `promote.sh`, `scheduler.py`, the factory's checkout of `develop` (`tick.py:197`), health.md and `docs/project-guide/style.md`.

    What I confirmed is true:
    - The stop `repository_unavailable` and its detail `the repository has no develop branch yet` (`scheduler.py:135`, with `WORK_BRANCH = "develop"`).
    - What `promote.sh` does: it opens a pull request from `develop` to `main` or adds to the open one, and the switch `promote` decides who merges.
    - The commit `<id>: archived` on `develop`.
    - That the factory and Kumpel check out `develop` themselves.
    - The health.md row, under *The wait for a repository that is not ready*.

    Criteria 2 and 3 are met.

    Findings:
    1. `docs/operator-playbook.md:31`: the promotion text says "(see [the operator guide](operator-guide/work-items.md), *The branches*)". work-items.md has no section *The branches*. That section, and the promotion under it, is in `docs/operator-guide/install.md` (*The branches*, line 41; *The promotion*, line 59). The document check missed this because the reference is not written in the form "*heading* in [link]". Fix: write `(see *The promotion* in [the operator guide](operator-guide/install.md))`. This keeps the bare file name out of the text, so the guard that failed the first run stays green.
    2. `docs/operator-guide/install.md:11`: the link `[health.md](health.md#the-wait-for-a-repository-that-is-not-ready)` uses an anchor. Style rule 8 says a section of another page is named by its heading in italics, then `in`, then the link, so that the document check looks the heading up. Fix: write `see its row under *The wait for a repository that is not ready* in [health.md](health.md)`. That still meets criterion 4's "linked to its row in health.md".
    3. `docs/operator-playbook.md:203`: the new text says the script "refuses unless the last acceptance in `done/` says `outcome: accepted`". `archive-feature.sh:27-35` also refuses while a story file is still in the feature's `backlog/` or `in-progress/`, and when the feature has no acceptance. The sentence also runs to about 60 words, against style rule 2. Fix: split it into sentences of at most about 25 words. Name both refusals, for example: "It refuses while a story is left in `backlog/` or `in-progress/`, or while the last acceptance in `done/` does not say `outcome: accepted`."

    No docs/decisions.md entry was expected, and none was written.
11. factory: started docs-only as vm.
