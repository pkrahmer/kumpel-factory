---
stage: docs-review
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 675
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T16:54:47.174428Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T16:54:47.182111Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T16:55:10.923524Z'
  stage: intake
  run: 594970d673e940baa1eba21e1321388b
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T16:55:15.716406Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-08T17:00:29.623798Z'
  stage: docs-only
  run: 3a76458105644cda9b3734f71ebdea7b
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T17:00:35.074101Z'
  stage: docs-review
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-08T17:01:15.758031Z'
  stage: docs-review
  run: a8e29700b6f242afb041bfba734df291
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T17:01:20.960123Z'
  stage: docs-only
- number: 9
  speaker: documenter
  kind: result
  at: '2026-11-08T17:03:57.430522Z'
  stage: docs-only
  run: fede1f6a1ac94234b8c375f389853fcb
---

# The guides describe one full check per story

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

The human's changes after F0059 (commit `77c97b622`) moved the full `make check` to the smoke-test stage, gave the docs stages the project command `guides`, took the marked tests out of `make test`, and added the documenter's write paths to `check`'s `not_read`. No stage kept the guides true to that commit, so the operator guide and the project guide still describe the pipeline as it was before it. An operator who reads them is told that the template checks after the coder, that a documents-only change can turn `make check` red, and that kumpel-factory's `not_read` keeps `README.md` and `docs/` in the key. An agent that reads the project guide is told that `make test` still runs the marked tests. After this story the operator guide's quotes of the template and of kumpel-factory's definition match the files they quote, its account of the docs route names `guides`, and the project guide's section on the marker `documents` says what `make guides` and `make test` run now. The files the guides quote stay as they are: this story changes documents only.

## Interface

Documents only; no code and no test changes.

- `docs/operator-guide/pipeline.md`:
  - The template's `stages` quote under *Start facts* (today `doing: {role: coder, next: [review, tests], checks: [check], context: [facts-changes]}`) matches `operator/template/factory/pipeline.yml`: `doing` has no `checks`.
  - The template's `base_ref` quote below it matches `operator/template/Makefile` (`git merge-base HEAD origin/develop`, with no fallback), and the sentence before it stays true of that line.
  - *More than one route* quotes the template's `smoke-test` line as it is today, with `checks: [check]`, and says in a sentence that the template's one full check runs after the smoke tester.
  - *The docs route*, step 3: after `docs-only` the factory runs `make check` (reused when only the documenter's files changed, since `check`'s `not_read` lists them) and, in kumpel-factory, `make guides` beside `secrets` and `documents`.
  - The paragraph on kumpel-factory's own `not_read` and its YAML block say what `factory/pipeline.yml` holds today: the documenter's write paths are left out of `check`'s key, because `make test` leaves out the tests marked `documents` and `make guides` runs them; a documents-only change can turn `make guides` red, not `make check`.
- `docs/project-guide/README.md`, *The marker `documents`*: the paragraph that begins "The marker exists so that" says that `make test` runs `-m "not documents"`, that `make guides` runs the marked tests in the docs stages and in the coder's own `make check guides`, and that the factory reuses its passed `make check` after a documents-only change. The sentence "Until then `make test` still runs every test, the marked ones included." is gone.

## Acceptance criteria

1. Every YAML or Make line that `docs/operator-guide/pipeline.md` presents as a quote of `operator/template/factory/pipeline.yml`, `operator/template/Makefile` or kumpel-factory's `factory/pipeline.yml` appears verbatim in that file; a line that no longer appears there is a finding of the reviewer.
2. `docs/operator-guide/pipeline.md` no longer says that a documents-only change can turn `make check` red, and it names `make guides` as the check that reads the documents in kumpel-factory.
3. `docs/project-guide/README.md` no longer says that `make test` runs the marked tests, and it names `make guides` and where it runs (the docs stages and the coder's `make check guides`).
4. `make documents` ends with `documents ok`.
5. `make check` stays green.
6. docs: the operator guide (`docs/operator-guide/pipeline.md`) and the project guide (`docs/project-guide/README.md`) say where the full `make check` runs after F0059 and which command checks the documents, as criteria 1 to 3 describe.

## Smoke test

```bash
grep -c 'A documents-only change can therefore turn `make check` red' docs/operator-guide/pipeline.md
```
Expect: `0`

```bash
grep -c 'Until then `make test` still runs every test' docs/project-guide/README.md
```
Expect: `0`

```bash
grep -c 'doing: {role: coder, next: \[review, tests\], checks: \[check\], context: \[facts-changes\]}' docs/operator-guide/pipeline.md
```
Expect: `0`

```bash
grep -c 'smoke-test: {role: smoke-tester, next: \[approval, doing, docs\], checks: \[check\], round_cap: 3}' docs/operator-guide/pipeline.md
```
Expect: `1`

```bash
grep -c 'origin/develop 2>/dev/null' docs/operator-guide/pipeline.md
```
Expect: `0`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names the two documents and the passages to change: in `docs/operator-guide/pipeline.md` the template's `doing` quote (line 69), the `base_ref` quote (line 76), the `smoke-test` quote under *More than one route* (line 96), *The docs route* step 3, and the paragraph and YAML block on kumpel-factory's `not_read` (lines 131–135); in `docs/project-guide/README.md` the paragraph on the marker at line 231. I checked each against the files it quotes. `operator/template/factory/pipeline.yml:24` has `doing` with no `checks`, and `:27` has `smoke-test` with `checks: [check], round_cap: 3`. `operator/template/Makefile:128` is `base_ref = $$(git merge-base HEAD origin/develop)`. `factory/pipeline.yml` has `guides` (line 12), `docs` and `docs-only` with `guides` among their checks (lines 39 and 41), and `check`'s `not_read` with `README.md`, `docs/*` and the other README paths (line 10). `pyproject.toml` sets `-m "not documents"` nowhere, but the feature's list of the human's changes says the Makefile's `test` runs it; the documenter takes it from the `Makefile`. The minimal example at `docs/operator-guide/pipeline.md:20` (`doing: {role: coder, next: [review], checks: [check]}`) is an illustration, not a quote of any of the three files, so criterion 1 does not reach it.
   - Criteria: each can be checked on the documents. Criterion 1 by comparing each presented quote with its file. Criteria 2 and 3 by the sentence that is gone and the sentence that names `make guides` and where it runs. Criteria 4 and 5 by their commands. Criterion 6 is the docs criterion. The failing sides are the stale quotes and sentences that must be gone, and smoke tests 1, 2, 3 and 5 pin them.
   - Smoke test: five `grep -c` commands that run from the repository root, each with an exact count to expect. I checked them against the current files: today they give 1, 1, 1, 0 and 1. The escaped brackets match the literal YAML. No pytest command, so the `-q` rule does not apply.
   - Docs criterion: it names what the reader must know (where the one full `make check` runs after F0059, and which command checks the documents) and points to criteria 1 to 3 for the details. The Interface quotes only lines of the files the guide quotes, to be matched, and dictates no prose.
   - Architecture: documents only, inside the documenter's write paths (`README.md`, `docs/*`). No code, test, contract or pipeline file changes. `factory/pipeline.yml`, `operator/template/*` and `CLAUDE.md` stay as they are.
   - Scope: this is the follow-up to the human's changes listed in F0059's `feature.md` (*The human's changes*, decisions 1 and 2). It keeps the guides true to them and does not touch the feature's *Out of scope*.
   - Route: `docs-only`, because every path the Interface changes is under `docs/`.
4. factory: started docs-only as vm.
5. documenter: Wrote the whole change; documents only.
   - `docs/operator-guide/pipeline.md`:
     - Under *Start facts*, the template's `doing` quote no longer has `checks: [check]`. It now matches `operator/template/factory/pipeline.yml:24`.
     - The `base_ref` quote is now `base_ref = $$(git merge-base HEAD origin/develop)`, as in `operator/template/Makefile:128`. The sentence before it now says the merge-base is taken against `origin/develop`.
     - *More than one route* now quotes the template's `smoke-test` line with `checks: [check]`. A new sentence says this is the template's one full check, run after the smoke tester.
     - *The docs route*, step 3: `make check` runs after `docs-only` and is reused after a documents-only change, because `check`'s `not_read` lists the documenter's write paths. In kumpel-factory `make guides` runs beside `secrets` and `documents`.
     - The paragraph on kumpel-factory's `not_read` now says the documenter's write paths are left out of the key. The reason it gives: `make test` runs `-m "not documents"` and `make guides` runs the marked tests, so a documents-only change can turn `make guides` red, not `make check`. The YAML block is now the `check:` line of `factory/pipeline.yml:10`, copied verbatim from the file.
   - `docs/project-guide/README.md`, *The marker `documents`*: the paragraph now says `make test` runs `-m "not documents"`. It also says `make guides` runs the marked tests after `docs` and `docs-only` and in the coder's `make check guides`, and that the factory reuses the passed `make check` after a documents-only change. The sentence "Until then `make test` still runs every test…" is gone.

   Checked against the files:
   - I compared each quote with `operator/template/factory/pipeline.yml`, `operator/template/Makefile`, `factory/pipeline.yml` and the `Makefile`'s `test`/`guides` targets (lines 88–99).
   - The five smoke-test greps give 0, 0, 0, 1, 0.
   - `make documents` ended `documents ok (70.4 s)`.
   - I did not run `make check`, because only documents changed.

   Cross-read and found current:
   - The rest of `docs/operator-guide/pipeline.md`. The template quote of `tests` and the start-facts table match the template.
   - The `checks` row of its Reference table.
   - `docs/project-guide/pipeline.md`.
   - The rest of *The marker `documents`*.

   Not touched: the minimal example at `docs/operator-guide/pipeline.md:20` (`doing: {role: coder, next: [review], checks: [check]}`). It is an illustration, not a quote, as the intake ruled.

   `check`: check: green
   `guides`: guides: green (9.7 s)
   `secrets`: secrets: green (0.5 s)
   `documents`: documents ok (62.0 s)
6. factory: started docs-review as vm.
7. reviewer: Reviewed `git diff develop...HEAD -- README.md docs operator/README.md` (from the facts-diff block). I checked it against `operator/template/factory/pipeline.yml`, `operator/template/Makefile`, `factory/pipeline.yml`, the `Makefile` targets `check`, `test`, `guides` and `secrets`, and `docs/project-guide/style.md`.

   What holds:
   - Criterion 1: every quote now appears verbatim in the file it quotes.
     - The template's `doing` line has no `checks`.
     - `base_ref = $$(git merge-base HEAD origin/develop)` is `operator/template/Makefile:128`.
     - The `smoke-test` line is template line 27.
     - The `check:` line is `factory/pipeline.yml:10`.
   - Criterion 2: the "turn `make check` red" sentence is gone, and `make guides` is named.
   - Criterion 3: the "Until then" sentence is gone. `make guides` is named, with the docs stages and `make check guides`.
   - The five smoke-test greps match their expected counts on the diff.
   - Docs route step 3 says what the Interface asks for, and it is true of `factory/pipeline.yml:41`, where `docs-only` checks `check`, `guides`, `secrets` and `documents`.

   Findings:
   1. `docs/operator-guide/pipeline.md:131`. Problem: the sentence "It also leaves out the documenter's write paths (…), because no test of `make check` reads them: `make test` runs … in the docs stages." is about 50 words and has two parentheses. That breaks rule 2 of `docs/project-guide/style.md`: split a sentence of more than about 25 words, and use at most one parenthesis per sentence. Fix: split it into three sentences. The first says what is left out, the second why `make test` does not read the documents, and the third what `make guides` runs. Keep one parenthesis at most in each.
   2. `docs/project-guide/README.md:231`. Problem: "So `make check` reads none of the documenter's files" is not true of the code. `make check` runs `secrets` (`Makefile:21`), and `secrets` scans every file changed against `origin/develop`, documents included (`Makefile:64-72`). Fix: say that no test of `make check` reads the documenter's files, as the operator guide says at line 131.
8. factory: started docs-only as vm.
9. documenter: Fixed the reviewer's two findings from docs-review. Both changes are in documents only.

   - `docs/operator-guide/pipeline.md:131` (finding 1): split the 50-word sentence with two parentheses into three sentences, with no parenthesis in the first two and one in the third.
     - The first lists what is left out of the key: `README.md`, `docs/*`, `operator/README.md` and the folder READMEs.
     - The second says why no test of `make check` reads them: `make test` runs `-m "not documents"`.
     - The third says what `make guides` runs: the marked tests, in the docs stages.
   - `docs/project-guide/README.md:231` (finding 2): "So `make check` reads none of the documenter's files" now reads "So no test of `make check` reads the documenter's files". It no longer contradicts `secrets`, which scans every file changed against `origin/develop`, documents included. The operator guide uses the same words.

   Checks:
   - `make documents` ended `documents ok (61.5 s)`.
   - I did not run `make check`, because only documents changed.
   - No line of the smoke-test greps was touched.

   `check`: check: green (not run again: passed on tree 54896b72b82a at 2026-11-08T16:57:15Z)
   `guides`: guides: green (9.7 s)
   `secrets`: secrets: green (0.5 s)
   `documents`: documents ok (63.4 s)
