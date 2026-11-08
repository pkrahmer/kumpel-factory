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
