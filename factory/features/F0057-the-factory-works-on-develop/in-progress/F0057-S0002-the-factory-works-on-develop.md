---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 644
comments_read: [6713932106]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-07T22:35:42.206941Z'
  lease_duration: 60
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
---

# The factory works on develop

## Description

`main` is to become the protected line of accepted features, so the factory moves its work to `develop`: the archive after a merge, the closes, the acceptance's booking, the stop records, the claims' base and every read of `origin/<working branch>` (F0057, decision 1). With F0057-S0001 merged, this is one value: `WORK_BRANCH` becomes `"develop"`. The agent files and the project template name the branch too, so they follow. A remote without `develop` must be clear at once, so the preflight's existing finding for a missing working branch names it. The human creates `develop` and moves the factory over at this story's merge (feature, *The human's changes*).

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
