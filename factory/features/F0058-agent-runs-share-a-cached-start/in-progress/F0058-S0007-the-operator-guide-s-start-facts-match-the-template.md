# The operator guide's start facts match the template

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

Since the human's change after F0058-S0004, the template (`operator/template/Makefile` and `operator/template/factory/pipeline.yml`) ships three start-fact targets: `facts-diff` for the review stage, `facts-changes` for the coder's and the documenter's stages and `facts-files` for the tester's stage. Each is run against the point where the branch left `origin/develop`. The operator guide's *Start facts* (`docs/operator-guide/pipeline.md`) still shows only an invented example: a target `diff` running `git diff --stat develop...HEAD`. That example names a local `develop` branch, which a project's checkout may lack, and it does not match what the template ships. An operator who starts from the template finds three `facts-*` names in their pipeline definition that no guide explains. After this story, *Start facts* names the template's three targets, says what each shows and which stage gets it, and gives an example that measures the diff from where the branch left `origin/develop`, as the template does. It also says that a project may change or drop the targets. No code changes. The rules of start facts (order, the cut, the `failed:` line, the lease) stay as they are written.

## Interface

None: the story changes `docs/operator-guide/pipeline.md` only (the docs route).

## Acceptance criteria

1. *Start facts* in `docs/operator-guide/pipeline.md` names the template's three targets `facts-diff`, `facts-changes` and `facts-files`, says in one line each what each shows, and names the stages the template gives each to: `review` for `facts-diff`, `doing` and `docs` for `facts-changes`, `tests` for `facts-files`.
2. The section's example target measures its diff from where the branch left `origin/develop`, as `operator/template/Makefile` does; no example in the section names a local `develop` branch (`develop...HEAD`).
3. The section says that the targets are the project's own: a project may change what they show, or drop a stage's `context`, without any change to the factory.
4. `make check` stays green.
5. docs: the operator guide (`docs/operator-guide/pipeline.md`, *Start facts*), as criteria 1 to 3 say; the project guide's *Start facts* and `docs/decisions.md` need nothing, since the factory knows only the commands' names.

## Smoke test

```bash
grep -c 'facts-diff\|facts-changes\|facts-files' docs/operator-guide/pipeline.md
```
Expect: a number of at least `3`.

```bash
grep -c 'develop\.\.\.HEAD' docs/operator-guide/pipeline.md
```
Expect: `0`.

## Journal
