---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T01:56:37.063998Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T01:56:37.057055Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T01:56:37.063998Z'
  stage: intake
---

# archive-feature.sh refuses a feature whose acceptance was refused

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

`operator/skill/kumpel/scripts/archive-feature.sh` counts a feature as finished when no story file is left in its `backlog/` or `in-progress/` and its last acceptance report is in `done/`. The factory also books a closed acceptance in `done/`, with `outcome: refused` in its front matter, so the script archives a refused feature, and `promote.sh` then promotes it to `main` (F0057-A0001, smoke test probe). This story makes the script read the outcome: a feature is finished only when its last acceptance in `done/` says `outcome: accepted`. What else counts as finished stays the same, and `promote.sh` is unchanged; it reads the archive.

## Interface

- `operator/skill/kumpel/scripts/archive-feature.sh <feature id>`: after its existing checks, it reads the front matter of the last acceptance report, the block between its first two `---` lines. The script refuses unless that block holds the line `outcome: accepted`, with `archive-feature.sh: <id> is not finished: its last acceptance <path> is not accepted` on stderr and exit status 1. Nothing is moved, committed or pushed, and the checkout stays on `develop` with no change.
- The existing refusals and their texts stay: a story in `backlog/` or `in-progress/`, no acceptance, and a last acceptance outside `done/`.
- `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 names the new refusal among the ones Kumpel reports to the human.
- Tests: a new module `tests/operator_scripts/test_operator_archive_outcome.py`, on a fake remote through the `operator` fixture.
- The human's leave, to be given when refining: `tests/operator_scripts/test_operator_develop.py`, whose `finished_feature` writes an acceptance report without front matter. The tester gives that text the front matter of a booked acceptance (`stage: done`, `outcome: accepted`), so far as the new rule requires. Every changed test keeps its name and what it checks.

## Acceptance criteria

1. `archive-feature.sh F0001` on a feature whose stories are all in `done/`, run against acceptance reports in `done/`, gives these results (rows of one test):
   - Last report has `outcome: accepted`: exits 0 and moves the feature to `factory/archive/` on the remote's `develop`.
   - Last report has `outcome: refused`: exits 1 with `archive-feature.sh: F0001 is not finished: its last acceptance <path> is not accepted`, and the remote's `develop` is unchanged.
   - Last report has front matter but no `outcome` line: refused the same way.
   - Last report has no front matter: refused the same way.
   - `F0001-A0001` refused and `F0001-A0002` accepted, both in `done/`: exits 0, since the last one counts.
2. The earlier refusals keep their texts and exit statuses (the earlier tests of `test_operator_develop.py` pass, changed only under the leave).
3. `make check` stays green.
4. docs: `operator/README.md` and `docs/operator-guide/install.md` (*The promotion*) say that only a feature whose last acceptance was accepted is archived and promoted; `docs/decisions.md`: none.

## Smoke test

```bash
uv run pytest tests/operator_scripts/test_operator_archive_outcome.py 2>&1 | tail -1
```
Expect: a line ending in `passed in <seconds>s` with no `failed`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
