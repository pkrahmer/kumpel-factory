# The factory works on develop

## Goal

`main` is to be protected: no direct pushes, only merges of pull requests (the human, 2026-11-07). Today the factory, Kumpel and the human push to `main` directly: ten kinds of commits, from the archive after a merge to Kumpel's log (`planning/branch-protection-candidate.md`). This feature moves all that work to a branch named `develop`, which stays unprotected, and makes `main` the line of accepted features. `develop` reaches `main` only through a promotion pull request after a feature's acceptance. The branch's name stays one constant in the code, so that the factory has a single place that names it. Done when every story below is merged, `make check` is green on `develop`, the factory runs on `develop`, and `main` is protected.

## Before it starts

F0055 is archived (done on 2026-11-07). No pull request is open.

## Scope

- One constant names the working branch, and every test uses it (S0001).
- The constant says `develop`; the agent files and the project template follow it; the preflight names the missing branch (S0002).
- Kumpel works on `develop`, archives a finished feature, and promotes `develop` to `main` behind a switch; every commit Kumpel makes names Kumpel (S0003).
- The documents name `develop` as the working branch and `main` as the line of accepted features (S0004 for the operator's documents, S0005 for the project guide).

## Out of scope

- A setting for the branch's name: the human chose the constant (2026-11-07).
- A separate identity for the factory, a bypass, and a required review: the design does not need them (`planning/branch-protection-candidate.md`).
- The stop reason `main_branch_failing`: its name stays, since it is part of the records contract and of `factory/stops.jsonl`'s history; the documents say it means the working branch (decision 6).
- `docs/runs/` and the entries of `docs/decisions.md` already written: they record their time.
- The Factory Timeline (`pkrahmer/factory-timeline`), a repository of its own, which then reads `develop`.

## Stories

- S0001: The tests name the working branch through one constant
- S0002: The factory works on develop
- S0003: Kumpel works on develop and promotes accepted features to main
- S0004: The operator's documents name develop and main
- S0005: The project guide names develop and main

## The human's changes

- **At S0002's merge, in this order, with no pull request open and the factory paused:**
  1. Wait for the archive commit of S0002 on `main`.
  2. Create `develop` on the remote at `main`'s tip.
  3. On `develop`: `Makefile`, every `origin/main` becomes `origin/develop` (`make secrets` lines 62 to 66, `make mutants` lines 110 and 117); `CLAUDE.md`, every mention of the working branch says `develop`. Pull, commit and push to `develop`.
  4. Move factory-vm to `origin/develop` (the session's `move_vm.sh` names the branch) and check it is active with no stops.
  5. Protect `main` with a ruleset: require a pull request before merging, zero required approvals (the factory, Kumpel and the human share one identity, and GitHub refuses an author's own approval), block force pushes and deletion. `main` stays the default branch.
- **After S0003's merge:** the session's own scripts (`approval.sh`, `night_watch.sh`, `move_vm.sh`) read `develop`.
- **After the feature's acceptance:** the first promotion, `develop` to `main`, by Kumpel's `promote.sh` or by hand.

## Decisions taken for the human

1. **`develop` is the working branch, `main` the line of accepted features** (the human, 2026-11-07). Rejected: a protected `stable` with `main` as the working branch, which needed no code; a setting for the branch's name; every factory write as its own pull request; a bypass for a separate identity.
2. **The constant is named `WORK_BRANCH`** (in `factory.shared.domain.paths`, today `MAIN_BRANCH`), since `main` keeps a meaning of its own after this feature.
3. **Kumpel promotes, behind a switch `promote`, off by default** (the human, 2026-11-07). With it off, Kumpel opens the promotion pull request and the human merges it.
4. **A promotion carries `develop`'s tip** (the human, 2026-11-07). Rejected: the feature's archive commit through a short branch, which keeps a next feature already started out of `main`. A promotion therefore runs best before the next feature starts.
5. **A promotion is a merge commit, never a squash or a rebase.** `make mutants` finds a feature's code by its story commits (`work item <id>: ...`), and a squash would make the next promotion conflict. `main` is never fixed directly: a fix goes to `develop` and reaches `main` with the next promotion.
6. **The stop reason `main_branch_failing` keeps its name**, for the records contract and the history of `factory/stops.jsonl`.
7. **Every commit Kumpel makes names Kumpel** (`Kumpel <kumpel@noreply.invalid>`) as its author, not only the start (the human, 2026-11-07).
8. **Kumpel archives a finished feature** with a script, instead of the human's `git mv` by hand, so that a promotion can check the feature is archived.
9. **The tests' change is behaviour-free and comes first** (S0001), so that S0002 changes one value and the tests follow it.
