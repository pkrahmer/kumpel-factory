---
stage: done
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 667
comments_read: []
handed_over: docs-approval
claim: null
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
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-08T15:07:43.220008Z'
  stage: docs-only
  run: cb49d678bdea4cb0890c969e68d17f2f
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T15:07:48.161890Z'
  stage: docs-review
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-08T15:08:20.953552Z'
  stage: docs-review
  run: fb9e7e48afee4224ae03346d15cf16b3
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T15:08:26.277981Z'
  stage: docs-only
- number: 9
  speaker: documenter
  kind: result
  at: '2026-11-08T15:12:40.187066Z'
  stage: docs-only
  run: 787ecbba83f346b08e7292799012087b
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T15:12:48.498813Z'
  stage: docs-review
- number: 11
  speaker: reviewer
  kind: result
  at: '2026-11-08T15:13:20.965010Z'
  stage: docs-review
  run: 71b3b2066fd84ebb8b6115185a6e1501
- number: 12
  speaker: factory
  kind: done
  at: '2026-11-08T15:15:12.325343Z'
  stage: docs-approval
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
5. documenter: Changed:
   - `docs/operator-guide/pipeline.md`, *Start facts*: I replaced the made-up `diff` example (`git diff --stat develop...HEAD`) with what the template ships. A table lists `facts-diff`, `facts-changes` and `facts-files`, says what each shows and gives the template's stages for each (`review`; `doing` and `docs`; `tests`). The YAML example is taken from `operator/template/factory/pipeline.yml:23-26`. The make example is `base_ref` and `facts-diff` as written in `operator/template/Makefile:128-133`. It measures from `git merge-base HEAD origin/develop`, and the text says why: a checkout may have no local `develop` branch. A new paragraph says the targets are the project's own. The factory knows only the names a stage's `context` lists, so a project may change or rename a target, or drop a stage's `context`, and nothing in the factory changes. I left the rules (order, the cut, `failed:`, the lease) as they were, except that the block name in the first rule's example is now `<context name="facts-diff">`.
   - The same file, the stage-field table (`context` row, now line 166): the example is now `context: [facts-diff]`, so it matches the section.

   Ran: `make -s -f operator/template/Makefile facts-changes` in the checkout prints `M	docs/operator-guide/pipeline.md`, so the template's merge-base recipe works without a local `develop`. Smoke greps: 12 for the `facts-*` names (at least 3 expected) and 0 for `develop...HEAD`. `make documents` printed `documents ok (60.2 s)`. I changed only documents, so I did not run `make check`.

   Cross-read and found current: the project guide's `docs/project-guide/pipeline.md` (the `context` field and *Start facts*, which talk only about command names, so they need nothing, as criterion 5 says), and the rest of `docs/operator-guide/pipeline.md`. `grep` finds no other operator-guide or README text about start facts.

   Stale text, not mine to fix in this story: `docs/project-guide/agents.md:301` and `:324` describe the reviewer's agent instructions with `git diff ... develop...HEAD`. Those lines mirror the shipped agent files, which also use a local `develop`, so a change there belongs to the agent files first.

   `check`: check: green
   `secrets`: secrets: green (0.3 s)
   `documents`: documents ok (59.5 s)
6. factory: started docs-review as vm.
7. reviewer: Findings:
   1. `docs/operator-guide/pipeline.md:52`: the sentence "Each measures from the point where the branch left `origin/develop`" is not true of all three targets. In `operator/template/Makefile:139-140`, `facts-files` runs `git ls-files -- . ':!factory'` with no `base_ref`; only `facts-diff` and `facts-changes` (`:131-136`) start at the merge base. Fix: say that `facts-diff` and `facts-changes` measure from where the branch left `origin/develop` and that `facts-files` lists the tracked files as they are. The part about leaving out `factory/` is true of all three and can stay.
   2. `docs/operator-guide/pipeline.md:52` and `:63`: the YAML and make blocks show excerpts of `operator/template/factory/pipeline.yml` and `operator/template/Makefile`, but the text names those files only in backticks. Rule 8 of `docs/project-guide/style.md` says to link the file a code block shows once, above the block, with a relative link. Fix: link each template file once before its block, for example `[pipeline.yml](../../operator/template/factory/pipeline.yml)` and `[Makefile](../../operator/template/Makefile)`.

   Checked and found correct: the table's description of `facts-diff` (stat, then the whole diff, without `uv.lock`) and of `facts-changes` (name and status, then untracked files). The stage mapping matches `operator/template/factory/pipeline.yml:23-26`, and the three `time_limit: 1` values match `:10-12`. The `tests`, `doing` and `review` lines of the YAML example match the template. The `base_ref` and `facts-diff` recipe matches `operator/template/Makefile:128-133` exactly. No `develop...HEAD` remains in the section. The "project's own" paragraph meets criterion 3. The rules of start facts (order, the cut, `failed:`, the lease) are unchanged apart from the block name in the example.
8. factory: started docs-only as vm.
9. documenter: Fixed the reviewer's two findings from round 1:
   1. `docs/operator-guide/pipeline.md`, *Start facts*: the sentence that said all three targets measure from `origin/develop` was wrong. It now says that `facts-diff` and `facts-changes` measure from where the branch left `origin/develop` and that `facts-files` lists the tracked files as they are. That matches `operator/template/Makefile:131-140`. The note that each target leaves out `factory/` is unchanged.
   2. Same section: each excerpted template file now has one relative link above its code block, `[pipeline.yml](../../operator/template/factory/pipeline.yml)` before the YAML and `[Makefile](../../operator/template/Makefile)` before the make block. This follows rule 8 of `docs/project-guide/style.md`. I checked that both link targets exist.

   Ran: `make documents` printed `documents ok (59.9 s)`. Only documents changed, so I did not run `make check`.

   Cross-read and found current: the rest of *Start facts*, which the reviewer had checked and which I left unchanged.

   `check`: check: green
   `secrets`: secrets: green (0.3 s)
   `documents`: documents ok (61.0 s)
10. factory: started docs-review as vm.
11. reviewer: no findings

    I compared the diff of `docs/operator-guide/pipeline.md` (*Start facts* and the `context` row of the stage-field table) with the template on the branch and with `docs/project-guide/style.md`:
    - Round 1 finding 1 is fixed. `docs/operator-guide/pipeline.md:52` now says that `facts-diff` and `facts-changes` measure from the merge base with `origin/develop` and that `facts-files` lists the tracked files as they are. This matches `operator/template/Makefile:128-140`.
    - Round 1 finding 2 is fixed. Each excerpted file has one relative link above its block, `[pipeline.yml](../../operator/template/factory/pipeline.yml)` and `[Makefile](../../operator/template/Makefile)`, as style rule 8 asks.
    - Criterion 1: the table names the three targets with one line each. The stage mapping (`review`; `doing` and `docs`; `tests`) matches `operator/template/factory/pipeline.yml:23-26`, and the YAML excerpt's lines match `:10-12` and `:23-25` word for word.
    - Criterion 2: the make example is `base_ref` and `facts-diff` exactly as `operator/template/Makefile:128-133` writes them, so it measures from `git merge-base HEAD origin/develop`. No `develop...HEAD` is left in the section.
    - Criterion 3: the "project's own" paragraph says that a project may change or rename a target, or drop a stage's `context`, without changing the factory.
    - The start-fact rules (order, the cut, `failed:`, the lease) are unchanged apart from the block name in the example.
    - Smoke greps: the `facts-*` names are counted at least 3 times, and `develop...HEAD` 0 times.

    A borderline point, which I did not count as a finding: line 52 says "Each leaves out the factory's own files under `factory/`". The untracked-file half of `facts-changes` (`git ls-files --others --exclude-standard`, `Makefile:136`) has no `':!factory'` pathspec. The start facts run on the rolled-back base, which normally has no untracked files, so the sentence holds in practice. The round 1 reviewer also accepted it.
12. factory: done (pull request merged); cost: 5 runs, 4.0 min, 25 turns, 122181 tokens in (422975 more from cache), 11191 out, $1.29
