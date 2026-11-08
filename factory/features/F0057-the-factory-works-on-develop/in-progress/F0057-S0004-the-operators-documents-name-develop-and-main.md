---
stage: docs-only
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 646
comments_read: [6715370076]
handed_over: null
claim:
  instance: vm
  stage: docs-only
  started_at: '2026-11-08T01:04:09.458261Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T00:59:32.597955Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T00:59:32.605075Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T00:59:49.265142Z'
  stage: intake
  run: 666d05e36618439fa27c8bb4c515b704
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T01:03:40.357080Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T01:03:42.716682Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T01:04:04.291193Z'
  stage: intake
  run: 2435763283c24c4da595bcada092ae31
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T01:04:09.458261Z'
  stage: docs-only
---

# The operator's documents name develop and main

## Description

After F0057-S0002 and S0003 the factory and Kumpel work on `develop`, and `main` is the protected line of accepted features. The operator's documents still name `main` as the branch the factory works on, about 130 times. This story corrects them, so that an operator knows which branch holds what, how to create `develop` for a new project, how to protect `main`, and how a feature reaches `main`. It changes no code and no test.

## Interface

- The documents: `docs/operator-guide/*.md`, `docs/operator-playbook.md`, the root `README.md` and `operator/README.md`. Every mention of the factory's working branch says `develop`; a mention of the line of accepted features says `main`. `docs/runs/` and the entries of `docs/decisions.md` stay as they are.
- `docs/operator-guide/install.md`: a new project needs `develop`, created from `main`; the preflight names a missing `origin/develop`.
- A section, in the operator guide page the documenter judges right, on protecting `main`: a ruleset that requires a pull request with zero approvals and blocks force pushes and deletion, and why zero (one identity for the factory, Kumpel and the human; GitHub refuses an author's own approval). The promotion: after a feature's acceptance, Kumpel archives the feature and promotes `develop` to `main` with a merge commit, behind the switch `promote`; `main` is never fixed directly.
- The stop `main_branch_failing` keeps its name and means the working branch (F0057 decision 6); `docs/operator-guide/stops.md` says so.
- The documenter finds the mentions by script (`grep -nE` for `main` as a branch in the files above) and quotes the script's list of the mentions left as `main` in its entry, each meaning the line of accepted features; the reviewer checks with the same script. No test changes; the story takes the docs route.

## Acceptance criteria

1. No document of the Interface names `main` as the branch the factory works on; every remaining `main` as a branch means the line of accepted features (the script of the Interface, its output quoted).
2. `install.md` tells a new project to create `develop` from `main`, and says that the preflight names a missing `origin/develop`.
3. The operator guide tells how to protect `main`: a ruleset that requires a pull request with zero approvals and blocks force pushes and deletion, and why zero approvals (one identity for the factory, Kumpel and the human; GitHub refuses an author's own approval).
4. The operator guide tells that after a feature's acceptance Kumpel archives the feature and then promotes `develop` to `main` with a merge commit, behind the switch `promote`.
5. The operator guide tells that `main` is never fixed directly: a fix goes to `develop` and reaches `main` with the next promotion.
6. `stops.md` says that `main_branch_failing` means the working branch.
7. `make documents` ends with `documents ok (<seconds> s)`.
8. `make check` stays green.
9. docs: the files of the Interface; the reader knows which branch holds what, how to set up and protect them, and how a feature is promoted.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Questions (the format check passed; the Interface, scope, architecture and route are fine, but two Interface behaviours have no criterion):

   1. The Interface says `install.md` states that the preflight names a missing `origin/develop`. Criterion 2 only covers "create `develop` from `main`". Should criterion 2 also require that `install.md` says the preflight names a missing `origin/develop`? I would choose yes: extend criterion 2.

   2. The Interface lists several separate behaviours of the promotion section: the ruleset blocks force pushes and deletion, the promotion is a merge commit, it runs behind the switch `promote`, Kumpel archives the feature first, and `main` is never fixed directly (a fix goes to `develop`). Criterion 3 says only "how to protect `main`, why zero approvals, how a feature reaches `main`". Each stated behaviour needs its own checkable criterion, or the documenter and reviewer will read criterion 3 two ways. I would choose to split criterion 3 into: (a) protecting `main`, with the ruleset's three rules and why zero approvals; (b) promotion after acceptance, as a merge commit behind the switch `promote`, after Kumpel archives the feature; (c) `main` is never fixed directly.

   Everything else is accepted as written. The smoke test is runnable and its Expect line is checkable. The docs criterion names what the reader must know and dictates no sentences. The story is within F0057's scope.
4. 2026-11-08 human: 1. Yes. 2. Yes, split criterion 3 into (a), (b) and (c) as you wrote them.
5. factory: started intake as vm.
6. intake: accepted, with the human's answer (journal entry 4) carried into the story: criterion 2 now also requires that `install.md` says the preflight names a missing `origin/develop`; criterion 3 is split into 3 (protecting `main`: the ruleset's three rules and why zero approvals), 4 (promotion after acceptance: Kumpel archives first, then a merge commit, behind the switch `promote`) and 5 (`main` is never fixed directly). The later criteria are renumbered (6 stops, 7 documents, 8 `make check`, 9 docs, the last two kept last).
   - Interface: names concrete documents only (`docs/operator-guide/*.md`, `docs/operator-playbook.md`, `README.md`, `operator/README.md`); no code or signatures change. All of these are paths the documenter may write, apart from `docs/operator-playbook.md`, which the Interface and criterion 9 name explicitly.
   - Criteria: each is checkable by reading the documents or by the quoted script. Every stated behaviour of the Interface has its own criterion. Failing sides do not apply, because the story states no validation rule.
   - Smoke test: `uv run python -m factory.entry.check_documents | tail -1` is runnable. It does not run pytest, so the `-q` rule does not apply. The `Expect:` line is checkable.
   - Docs criterion: names what the reader must know and dictates no sentences.
   - Architecture: no code is touched, so the layers are unaffected. `main_branch_failing` keeps its name as `CLAUDE.md` and decision 6 require.
   - Scope: within F0057 (S0004 is the operator's documents), and `docs/runs/` and decision-log entries are excluded as the feature says.
   Route: docs-only.
7. factory: started docs-only as vm.
