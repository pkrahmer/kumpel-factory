---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 685
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-09T00:58:28.285777Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-09T01:05:28.242374Z'
  stage: acceptance
  run: 707adca439024d7d961545134e7fd58a
- number: 3
  speaker: factory
  kind: done
  at: '2026-11-09T01:06:17.044108Z'
  stage: done
stories: [F0061-S0001]
outcome: accepted
---

# Acceptance of Document examples share the check's uv cache

## Recommendation

**accepted.** The feature's one scope line is built and wired: the document check passes its own uv cache to every example. In a fresh copy of the repository, the first `uv run` takes 1 s from that cache, as `feature.md` promised. `make check` and `make documents` are green. One small observation remains: the examples lose the image's `UV_LINK_MODE=copy` under `env -i`, so uv's hardlink warning reaches their output. I propose one story for it. It is no broken promise, because every current example tolerates the warning.

## 1 Scope

None. The scope has one line, `UV_CACHE_DIR` for the examples' commands, and F0061-S0001 builds it:
- `uv_cache_directory` and `ProcessExampleRunner(uv_cache=...)` in `src/factory/shared/adapters/document_examples.py:23-45,113-128`;
- the wiring `ProcessExampleRunner(uv_cache=uv_cache_directory(os.environ))` in `src/factory/entry/check_documents.py:205`.

Both items of Out of scope hold:
- `EXAMPLE_TIME_LIMIT` is still 60 s;
- no cache is shared between instances; the examples use the cache of the process that runs the check.

The examples keep their own empty home and their own copy (`_fixed_environment`, `HOME` = the document's own folder). The goal's done condition holds on this branch, which is `develop` plus the report: `make check` ends `check: green` (test 109.6 s, coverage 99.21 %), and `make documents` ends `documents ok (50.4 s)`.

## 2 Feature smoke test

The walk-through is the feature's purpose end to end, through the real entry point `factory.entry.check_documents`:
1. Clone the repository.
2. Add to a listed document (`docs/project-guide/shared.md`, so a finding blocks) an example. It prints `$UV_CACHE_DIR`, then makes the document copy's **first** `uv run` (import `factory`) and states whether it finished within 10 s.
3. Commit, and run the check on the clone.

```
$ sh smoke.sh "$d"        # in d=$(mktemp -d), removed on exit
check's uv cache: /work/home/.cache/uv
--- check_documents --root (shared.md is listed, so a finding blocks)
Report (not checked yet):
README.md:15: not run (suite)
docs/operator-guide/install.md:27: not run (vm)
docs/operator-guide/install.md:35: not run (suite)
docs/operator-guide/records.md:53: not run (vm)
docs/project-guide/pipeline.md:142: not run (vm)
documents ok (50.5 s)
status 0
```

The added example expected these lines:
- `/work/home/.cache/uv`
- `linked`
- `first uv run under 10 s`

The check found no difference: green.

I also ran a fresh copy's first `uv run` by hand, offline (`UV_OFFLINE=1`, so nothing could come from the index). It ran under the examples' environment (`env -i PATH HOME=<empty> UV_CACHE_DIR=/work/home/.cache/uv TZ LANG`) and printed:

```
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 106 packages in 175ms
Bytecode compiled 4164 files in 415ms
linked
1 s, first uv run in a fresh copy, offline, with the check's cache
```

The goal's "about a second" is met, and every package came from the cache. The warning is the finding behind the proposed story (see 4).

The contrast run, the same first `uv run` without any cache, was declined by the permission prompt, because it would download from the package index. It is not shown here. S0001's criterion 2 has its `without-cache` row, and the goal's 7 s / 99 s measurements stand for that side.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- Coder (entries 10 and 16): `_fixed_environment` still reads `PATH` from `os.environ` inside the adapter, while the uv cache is now read in `entry` and passed in. So the fixed environment reads the process environment in two places. Adapters may do I/O, so no rule is broken. I propose no story; it is listed for the human.
- Coder: `make duplicates` reported `7 new, 39 known, 4 gone` in both rounds, and so it does now. None of the 7 new findings is in this feature's code:
  - `claude_runtime` / `opencode_runtime` similar lines, twice;
  - `hand_over` / `acceptance` similar lines;
  - `readme_problems` unused;
  - three `cost_records` fields unused.

  The reviewers did not mention them. They are drift in `security/duplicates-baseline.txt` (the human's file), left by earlier features.
- Reviewer round 0's one finding (test helpers copied from `test_document_examples.py`) was fixed by the tester's move to `tests/support/document_examples_support.py`. Nothing is open.
- Documenter: "stale text not mine to fix: none seen".
- My own, from the smoke test: under `env -i` the examples lose the stage image's `UV_LINK_MODE=copy` (`operator/vm/Dockerfile:61`). The cache (under `/work`) and the examples' folders (under `/tmp`) are on different filesystems, so every document's first `uv run` prints uv's three-line hardlink warning into the example's output (stderr is merged). The current examples pass only because they start with `...`. An example written to expect the first lines exactly would fail on one machine and pass on another. The same warning was found and fixed for agent runs in F0040 (`docs/decisions.md:1047`, `UV_LINK_MODE=copy`). This is proposed as F0061-S0002.

## 5 Documentation

None of weight. The newcomer's path agrees with what was built:
- `docs/project-guide/style.md:32` lists the fixed environment with `UV_CACHE_DIR` "when it has one".
- `docs/project-guide/shared.md:235-238` gives `env -i`, the fixed variables that a fixture cannot replace, the reason for the shared cache and the lookup order.
- `docs/project-guide/README.md:91` names the new support module.

Neither says that `UV_LINK_MODE` is absent. Once S0002 is built, its docs criterion covers that. `README.md`, the operator guide and `docs/decisions.md` do not describe the examples' environment and need nothing. `make documents` runs every example green.

## 6 Decisions taken for the human

1. (feature.md 1) Sharing the cache does not change what an example prints: uv's cache is content-addressed and safe for concurrent use. The smoke test confirms the value. One exception: uv's hardlink warning now appears where a cold start printed download lines before (see 4, S0002).
2. (feature.md 2) A separate feature, not part of F0060.
3. (S0001 intake, journal 3–4) The human chose option (a): an end-to-end criterion for the `entry` wiring (`tests/entry/test_check_documents_uv_cache.py`), rather than leaving the wiring to the reviewer.
4. (S0001 interface, intake) The lookup imitates uv's own order (`UV_CACHE_DIR`, `XDG_CACHE_HOME/uv`, `HOME/.cache/uv`), and an empty value counts as not set. It does not ask uv itself (`uv cache dir`), which would be a second process per check.
5. (S0001 coder) The cache goes into the one fixed environment, merged after the fixture's, so a fixture cannot change it. Rejected: adding it inside `run_document`, and reading `os.environ` in the adapter.

Earlier tests changed: `tests/shared/adapters/test_document_examples.py`, changed by the tester in round 1 under the standing leave to move a shared test helper (CLAUDE.md *Tests*). Its helpers `FIXTURE_VARIABLE`, `LIFTED_VALUE`, `EmptyFixture`, `LiftingFixture` and `_block`/`_document` (now `block`/`document`) moved to `tests/support/document_examples_support.py`. Every test keeps its name and checks the same thing. The reviewer's round 1 entry names the change and its leave. No earlier test was changed without a leave.

## 7 The slow checks

The project offers nothing beyond `make check` today, except `make mutants` (see 3). `make documents` took 50.4 s here, against 50.4 s and 51.0 s in the documenter's runs.

Slowest tests in `.reports/junit.xml` (11025 tests):
- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other`, 19.8 s;
- five tests of 10.0 s each, all held at a `ROOMY_LIMIT` on purpose (podman timeout status ×2, the document runner's past-the-limit folder test, the process kill, the claude runtime's time limit).

The feature's 13 tests take 0.04 s at most each.

Disk: free space fell from 9.0 GB at the start record to 8.4 GB now, on all three paths alike. The used space did not change (1.6 GB, 0.0 GB, 2.1 GB), so the 0.6 GB lie outside these paths. The feature changes no stored data: the examples' cache is the one uv already keeps, and their copies are removed after each document. The feature does not explain the 0.6 GB. They are more likely the stages' check runs or the image's overlay (`/` is at 87 %). Worth a look if the drop continues.

## 8 Cost

Cost: 10 runs, 16.8 min, 61 turns, 228242 tokens in (1973145 more from cache), 26234 out, **$2.06** for the one story. That is two runs more than one pass needs:
- intake ran twice, around the human's one question;
- the round 0 review finding (copied test helpers) cost a second tests, doing and review run.

No run stands out.

Human interventions: **1 question answered** (question 1, at S0001's intake), **0.0 h waited**. The intake asked because no criterion tested the `entry` wiring, the one line that makes the feature work. The human chose an end-to-end criterion in under a minute. S0001 is the only story, so it is also the one that needed the human most.

## Proposed stories

- `backlog/F0061-S0002-document-examples-copy-from-the-uv-cache-without-a-warning.md`: give the examples `UV_LINK_MODE=copy` with the uv cache. uv's cross-filesystem hardlink warning then no longer reaches every document's first `uv run` output. This is the same fix F0040 made for agent runs.

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted; 1 story proposed

   1. Scope: none.
      - The one scope line is built by F0061-S0001: `uv_cache_directory`, `ProcessExampleRunner(uv_cache=...)`, and the `entry` wiring at `src/factory/entry/check_documents.py:205`.
      - Out of scope holds: the limit is still 60 s, and no cache is shared between instances.
      - `make check` is green (99.21 %), and so is `make documents` (50.4 s).
   2. Feature smoke test: green.
      - The test ran on a clone of the repository through `factory.entry.check_documents`. A listed document got an example that prints `$UV_CACHE_DIR` and makes the copy's first `uv run`; the result was `documents ok (50.5 s)`, status 0.
      - An offline first `uv run` in a fresh copy took 1 s from the check's cache.
      - The no-cache contrast run (it downloads from the package index) was declined by the permission prompt and is not shown.
   3. Mutation testing: by sweep, not run here.
   4. Noticed:
      - `_fixed_environment` still reads `PATH` from `os.environ` in the adapter, while the uv cache comes from `entry`. Listed, no story.
      - `make duplicates` shows 7 new findings, none in this feature's code. They are drift in the duplicates baseline from earlier features.
      - My own: `env -i` drops the image's `UV_LINK_MODE=copy`. The cache and the examples' folders are on different filesystems, so uv's three-line hardlink warning reaches every document's first `uv run` output. Today's examples pass only because they start with `...`. Proposed as S0002.
   5. Docs: none of weight. `style.md:32` and `shared.md:235-238` match what was built. `make documents` is green.
   6. Decisions for the human:
      - the feature's two decisions;
      - the intake answer (a), which added an end-to-end criterion for the wiring;
      - the lookup that copies uv's own order, with an empty value counting as not set;
      - the cache placed in the one fixed environment, which a fixture cannot change.
      - One earlier test changed: `tests/shared/adapters/test_document_examples.py`, under the standing leave to move shared helpers. The reviewer names it.
   7. Slow checks: nothing beyond `make check`.
      - Slowest test: `test_documents_marker`, 19.8 s; next come five tests of 10 s each, all at `ROOMY_LIMIT`.
      - Free disk fell 0.6 GB (9.0 to 8.4 GB) on all three paths, with used space unchanged. The feature does not explain it.
   8. Cost: 10 runs, 16.8 min, $2.06 for the one story. Two of those runs came from the intake question and the review round for the copied test helpers.
      - 1 question answered (at S0001's intake: no criterion tested the wiring), 0.0 h waited.
3. factory: done (pull request merged); cost: 1 runs, 6.9 min, 24 turns, 59037 tokens in (1047491 more from cache), 18332 out, $0.87
