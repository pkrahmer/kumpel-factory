---
stage: docs-only
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 708
comments_read: []
handed_over: null
claim:
  instance: self
  stage: docs-only
  started_at: '2026-11-17T07:53:04.000708Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T07:46:56.151183Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T07:46:56.158292Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T07:47:17.345058Z'
  stage: intake
  run: 58a833bd0df64c388bf4065d62ab95fd
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-17T07:47:22.117221Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-17T07:51:55.255880Z'
  stage: docs-only
  run: 8dbccf733bbd4497879d87810a0b7529
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-17T07:52:00.414052Z'
  stage: docs-review
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-17T07:52:58.565317Z'
  stage: docs-review
  run: 739ecc2a1a654bb384f3afead1ef314d
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-17T07:53:04.000708Z'
  stage: docs-only
---

# The guides catch up with the one layout and name every shared test helper


## Description

S0013 gave every project one layout, with the factory's makefile at `factory/Makefile`, but two sentences outside the pages its docs criterion named still describe the layouts before it. The project guide's `docs/project-guide/operator.md` says the packs' README tells how kit and pack are assembled "at the root or, for an existing repository, with `make_file: factory/Makefile`", and the operator guide's `docs/operator-guide/install.md`, *The project's make targets*, says the project defines its targets "in the Makefile at the root of its checkout", though the kit's definitions name `factory/Makefile`. Separately, the project guide's index `docs/project-guide/README.md` says that it names every module of `tests/support/`, and eight are missing from it, four of them this feature's (`kit_support.py`, `make_file_support.py`, `project_check_support.py`, `project_run_support.py`) and four older (`archive_feature_support.py`, `bill_cache_support.py`, `first_message_support.py`, `shared_rules_support.py`); S0013's documenter noticed the first. After this story the three pages agree with the one layout and the index keeps its promise. No code, no test and no file under `operator/` changes.

## Interface

- No module under `src/factory/`, no test and no file under `operator/` changes.
- `docs/project-guide/operator.md`, the bullet on `operator/packs/`: the assembly is described as the one way (every pack file but `CLAUDE.sections.md` and `TRAPS.md` into the project's `factory/`), without "at the root or, for an existing repository".
- `docs/operator-guide/install.md`, *The project's make targets*: the targets are defined in the makefile the pipeline definition names with `make_file` (`factory/Makefile` in a project assembled from the kit), else in the `Makefile` at the root of the checkout, with a link to *Name the makefile* in `pipeline.md`.
- `docs/project-guide/README.md`, the list of the modules of `tests/support/` that no earlier list holds: one bullet for each of the eight modules named in the Description, each with what it holds, in the style of the bullets around it.

## Acceptance criteria

1. `grep -c 'at the root or, for an existing repository' docs/project-guide/operator.md` prints `0`.
2. `grep -c 'Makefile at the root of its checkout' docs/operator-guide/install.md` prints `0`, and *The project's make targets* names `make_file` and `factory/Makefile`.
3. For every file `tests/support/<name>.py` but `__init__.py`, `docs/project-guide/README.md` holds the text `tests/support/<name>.py`.
4. `make documents` ends with `documents ok`, and `make guides` is green.
5. `make check` stays green.
6. docs: in `docs/project-guide/operator.md` and `docs/operator-guide/install.md`, the reader learns that a project assembled from the kit has its make targets in `factory/Makefile`, which the pipeline definition names, and that there is one way to assemble kit and pack; in `docs/project-guide/README.md`, what each of the eight shared test helpers holds.

## Smoke test

```bash
grep -c 'at the root or, for an existing repository' docs/project-guide/operator.md; grep -c 'Makefile at the root of its checkout' docs/operator-guide/install.md
```
Expect: `0`, then `0`.

```bash
for f in tests/support/*.py; do b=$(basename "$f"); [ "$b" = __init__.py ] || grep -q "tests/support/$b" docs/project-guide/README.md || echo "missing: $b"; done; echo done
```
Expect: the single line `done`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: accepted
   - Interface: it names three documents and the exact place in each: the `operator/packs/` bullet of `docs/project-guide/operator.md` (line 25 now holds "at the root or, for an existing repository"), *The project's make targets* in `docs/operator-guide/install.md` (line 230 now holds "Makefile at the root of its checkout"), and the list of `tests/support/` modules in `docs/project-guide/README.md`. It also states what stays unchanged: no `src/`, no test, nothing under `operator/`. *Name the makefile* exists in `docs/operator-guide/pipeline.md` (line 93), so the link has a target. I checked that the eight modules the Description names are the ones the index misses today, and they are.
   - Criteria: each one can be checked mechanically without further decisions. 1 and 2 are greps that must print `0`, and 2 also names `make_file` and `factory/Makefile`. 3 checks every support module against the index. 4 is `make documents` and `make guides`, and 5 is `make check`. Every Interface line has a criterion: removing the old wording (1 and 2), the new targets wording (2), the eight bullets (3). The "what it holds" part of each bullet is a matter of content, and the docs criterion covers it. The Interface states no rule with a failing side.
   - Smoke test: both blocks run from the checkout root as written. Each `Expect:` can be checked against the output (`0` then `0`; the single line `done`). Run today, the second block prints exactly the eight `missing` lines, so it tells the state before the story from the state after it.
   - Docs criterion: it says what the reader must know (a kit project's make targets live in `factory/Makefile`, which the pipeline definition names; there is one way to assemble kit and pack; what each of the eight helpers holds) and dictates no sentences.
   - Architecture: the story changes documents only. The documenter keeps the project guide and the operator guide (CLAUDE.md, *Docs*), and no code or layer is touched.
   - Scope: within F0062's "The guide for a fresh start and for a brownfield repository". It brings the pages into line with S0013's one layout and does not touch the feature's "Out of scope". Every path it changes is under `docs/`, which the documenter may write, so the route is `docs-only`.
4. factory: started docs-only as self.
5. documenter: Changed (documents only; no code, test or file under `operator/` touched):
   - `docs/project-guide/operator.md`, the `operator/packs/` bullet: the assembly is now described as the one way for a fresh start and an existing repository alike. Every pack file except `CLAUDE.sections.md` and `TRAPS.md` goes into the project's `factory/`, the pack's makefile becomes `<project>/factory/Makefile`, and the kit's pipeline definition names it with `make_file: factory/Makefile`. "at the root or, for an existing repository" is gone.
   - `docs/operator-guide/install.md`, *The project's make targets*: the targets are defined in the makefile the pipeline definition names with `make_file` (`<project>/factory/Makefile` in a project assembled from the kit), or else in the root `Makefile`. The sentence links to *Name the makefile* in `pipeline.md`. "Makefile at the root of its checkout" is gone.
   - `docs/project-guide/README.md`: added eight bullets after `write_path_support.py` in the list of `tests/support/` modules that no earlier list holds: `archive_feature_support`, `bill_cache_support`, `first_message_support`, `kit_support`, `make_file_support`, `project_check_support`, `project_run_support` and `shared_rules_support`. Each says what the module holds, taken from its docstrings and top-level names on the branch.

   `factory/Makefile` is written as `<project>/factory/Makefile` in prose. `make documents` treats a bare backticked `factory/Makefile` as a path in this repository and flagged it as missing; `pipeline.md` already uses the same `<project>/` form.

   Ran: both smoke-test blocks give `0`, `0` and the single line `done`. `make documents` ended `documents ok (48.4 s)`. `make guides` ended `guides: green`. That guides run came before the last small wording fix to the two make-target sentences. I did not run `make check`, because only documents changed.

   Cross-read and current: `docs/operator-guide/pipeline.md` *Name the makefile*, `operator/packs/README.md` *Assembling a project from the kit and a pack* (read only, not mine to write), and the rest of the `tests/support/` list in the project guide's index. I noticed no stale text outside this story.

   `check`: check: green (not run again: passed on tree 78201af5d622 at 2026-11-17T07:42:30Z)
   `guides`: guides: green (9.5 s)
   `secrets`: secrets: green (0.6 s)
   `documents`: documents ok (48.8 s)
6. factory: started docs-review as self.
7. reviewer: Reviewed `git diff develop...HEAD -- README.md docs operator/README.md` (three files) against the code on the branch and against `docs/project-guide/style.md`.

   Facts: everything the diff says is true of the branch.
   - The assembly in the `operator/packs/` bullet matches `operator/packs/README.md`, *Assembling a project from the kit and a pack*, and `pack_project_files`.
   - The make-target sentence in install.md matches *Name the makefile* in `docs/operator-guide/pipeline.md`, and the link anchor exists.
   - I checked each of the eight new bullets against the module's docstrings and top-level names, with one slip in finding 3.
   - Criteria 1 to 3 hold: the smoke-test blocks print `0`, `0` and `done`. Criterion 2's `make_file` and `factory/Makefile` are both named. The docs criterion is met in content.

   Findings, all against style.md's rule 2 for all documents ("Split a sentence of more than about 25 words. Use at most one parenthesis per sentence"):

   1. `docs/operator-guide/install.md:230`, *The project's make targets*: the second sentence ("It calls four targets, which … pipeline.md:") runs to about 50 words, and a semicolon joins the "see" clause onto it. Fix: split it. One sentence says the targets are in the makefile the definition names with `make_file`, else in the root `Makefile`. One says a project assembled from the kit names `<project>/factory/Makefile` (`make_file: factory/Makefile`). The pointer to *Name the makefile* gets its own sentence.
   2. `docs/project-guide/operator.md:25`, the `operator/packs/` bullet: the new sentence ("[Its README] says what each file is for and how kit and pack are assembled, the one way … `make_file: factory/Makefile`.") runs to about 55 words with three ideas. Fix: keep "says what each file is for and how kit and pack are assembled" as one sentence. Then say in one short sentence that there is one way, for a fresh start and an existing repository alike. Then one sentence on where the pack's files go and how the kit's definition names the makefile.
   3. `docs/project-guide/README.md:229`, the `kit_support.py` bullet:
      - The third sentence ("`kit_project_files` and `pack_project_files` give … and `run_kit_make` runs make in it.") runs to about 50 words. Fix: split it, for example the two `*_project_files` functions in one sentence and `pack_claude_md`, `forwarding_project` and `run_kit_make` in the next.
      - "It names their files and folders (… `LINES`, `PACKS`)" lists `LINES`, which is the kit's two lines `("thin", "full")` (`tests/support/kit_support.py:33`), not a file or folder. Fix: say it names the kit's lines and packs, or drop `LINES` from the parenthesis.
   4. `docs/project-guide/README.md:232`, the `project_run_support.py` bullet:
      - Its one sentence holds three parentheses (`(SeenRun)`, `(with make_file=)`, `(GREEN_SYNC, GREEN_CHECK, NAMED_MAKEFILE)`). Fix: split it into sentences of one parenthesis at most.
      - It counts `NAMED_MAKEFILE` among "the outputs and constants of a green sync and check". `NAMED_MAKEFILE` is the path `"factory/Makefile"` (`tests/support/project_run_support.py:25`) and belongs to neither. Fix: name it apart, as the makefile path a definition names.
8. factory: started docs-only as self.
