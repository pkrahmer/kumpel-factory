---
stage: docs-only
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 667
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: docs-only
  started_at: '2026-11-08T15:03:09.309875Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T15:02:45.888108Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T15:02:45.895436Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T15:03:04.393548Z'
  stage: intake
  run: 5c275307b103426ab0cab092f4b243fe
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T15:03:09.309875Z'
  stage: docs-only
---

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

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: none; the story changes only `docs/operator-guide/pipeline.md` (*Start facts*, now at lines 48–75), a path the documenter may write, so the route is `docs-only`. The facts it must state match the template: `operator/template/Makefile:128-140` defines `facts-diff`, `facts-changes` and `facts-files`, with `base_ref` = `git merge-base HEAD origin/develop`. `operator/template/factory/pipeline.yml:23-26` gives `facts-files` to `tests`, `facts-changes` to `doing` and `docs`, and `facts-diff` to `review`.
   - Criteria: each one can be checked against the document. Criterion 1 needs the three names, one line each and the stage mapping. Criterion 2 needs an example measured from the merge base with `origin/develop` and no `develop...HEAD`. Criterion 3 needs the statement that the targets are the project's own. Criterion 4 is `make check`. There is no Interface rule, so no failing side is missing.
   - Smoke test: both greps can run from the checkout. Today they print a count of 0 for the `facts-` names and 1 for `develop...HEAD`, so each `Expect:` (at least 3, and 0) separates the before from the after.
   - Docs criterion: it names what the reader must know (the targets, what each shows, which stage gets each, that a project may change or drop them) and why the project guide and `docs/decisions.md` need nothing. It quotes no sentences to paste.
   - Architecture: no code changes. The factory knows only the commands' names, so the project guide's *Start facts* stays true.
   - Scope: within F0058, which covers S0004's start facts and the human's template change after it. The story leaves the start-fact rules (order, the cut, `failed:`, the lease) as written, and none of the feature's "Out of scope" items applies.
4. factory: started docs-only as vm.
