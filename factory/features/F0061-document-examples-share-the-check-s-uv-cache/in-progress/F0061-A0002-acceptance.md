---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 687
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-09T01:16:45.140736Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-09T01:25:16.036726Z'
  stage: acceptance
  run: 22cc8b17ae204c4c8271008542a3b6fe
stories: [F0061-S0001, F0061-S0002]
outcome: null
---

# Acceptance of Document examples share the check's uv cache

## Recommendation

**accepted.** Both stories are built, wired and documented. The document check passes its uv cache and `UV_LINK_MODE=copy` to every example. In the feature smoke test, a listed document's first `uv run` in a fresh copy ran in under 10 s, with no hardlink warning in its output, and `make documents` was green on the clone. `make check` is green. The one new finding is outside the feature's code: in one of four runs of the check, the fixture `instance` could not be prepared, and the finding gives no reason. I propose a story so that the reason can be traced. No promise of `feature.md` is broken.

## 1 Scope

None of weight. The scope's one line (`UV_CACHE_DIR` for the examples' commands) is built by F0061-S0001:
- `uv_cache_directory`, and `_fixed_environment` with `uv_cache` in `src/factory/shared/adapters/document_examples.py:23-48`;
- the wiring in `src/factory/entry/check_documents.py:205`.

F0061-S0002 adds `UV_LINK_MODE=copy` beside it (`document_examples.py:44-47`). That story was proposed by the first acceptance (F0061-A0001) and merged by the human. `feature.md` still names only S0001 under *Scope* and *Stories*: a note for the human, whose file it is.

Out of scope holds. `EXAMPLE_TIME_LIMIT` is still 60 s (`document_examples.py:16`). No cache is shared between instances; the examples use the cache of the process that runs the check. Each document keeps its own empty home and its own temporary folder (`_DocumentRun.__init__`).

The goal's done condition holds on this branch (`develop` plus the report): `make check` ends `check: green` (test 110.9 s, coverage 99.21 %), and `make documents` passed on a fresh clone (see 2).

## 2 Feature smoke test

The walk-through is the feature's purpose end to end, through the real entry point `factory.entry.check_documents`:
1. Clone the repository.
2. Add an example to a listed document (`docs/project-guide/shared.md`, so a finding blocks). The example prints the cache and link mode it gets. Then it makes the copy's **first** `uv run` (importing `factory`), counts hardlink warnings in that run's output, and states whether it finished under 10 s.
3. Commit, and run the check on the clone.
4. Run the same first `uv run` by hand, offline, with the cache but without `UV_LINK_MODE`. This is the side before S0002.

The added example expected these lines:

```
[/work/home/.cache/uv] [copy]
hardlink warnings: 0
linked
first uv run under 10 s
```

```
$ sh smoke.sh "$d"        # in d=$(mktemp -d), removed on exit
check's uv cache: /work/home/.cache/uv
--- check_documents --root (shared.md is listed, so a finding blocks)
Using CPython 3.12.15 interpreter at: /usr/local/bin/python3.12
Creating virtual environment at: .venv
   Building factory @ file:///tmp/tmp.ddBcP3f6OU/repo
      Built factory @ file:///tmp/tmp.ddBcP3f6OU/repo
Installed 106 packages in 295ms
Bytecode compiled 4164 files in 470ms
Report (not checked yet):
README.md:15: not run (suite)
docs/operator-guide/install.md:27: not run (vm)
docs/operator-guide/install.md:35: not run (suite)
docs/operator-guide/records.md:53: not run (vm)
docs/project-guide/pipeline.md:142: not run (vm)
documents ok (49.7 s)
status 0
--- the same first uv run, by hand, offline, with the cache but without UV_LINK_MODE (the before side)
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
linked
```

(The lines from `Using CPython` to `Bytecode compiled` come from the outer `uv run` that started the check on the new clone. They are not the example's output.)

The check found no difference: green. The cache (`/work`, ZFS) and the examples' folders (`/tmp`, overlay) are on different filesystems. So the before side shows the warning that S0002 removes, and the example under the check shows none.

To show that the block really runs, I changed its expectation to `[/work/home/.cache/uv] [hardlink]` on another fresh clone. The check failed with status 1 and `docs/project-guide/shared.md:328: the example printed [/work/home/.cache/uv] [copy]`.

That same run also blocked on `docs/operator-guide/install.md:188: fixture instance could not be prepared`, an example this feature did not touch. Two more full runs on fresh clones were green (`documents ok (49.1 s)` each). Preparing the fixture `instance` by hand three times on a fresh clone succeeded each time. So it happened once in four full runs, and its cause cannot be read: `_DocumentRun.environment` (`document_examples.py:93-95`) drops the `FixtureError`'s detail, which holds the failed git command and its output. This is behind the proposed F0061-S0003.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- S0002 coder, reviewer, documenter, smoke tester: nothing noticed beyond their work. The documenter found nothing stale. The reviewer judged that the `7 new` in `make duplicates` cannot come from S0002's diff.
- `make duplicates` now: `7 new, 39 known, 4 gone`, the same seven as at F0061-A0001, none in this feature's code:
  - `hand_over`/`acceptance` similar lines;
  - `claude_runtime`/`opencode_runtime` similar lines;
  - `readme_problems` unused;
  - three `cost_records` fields unused.

  Four of the seven pair up with the four `gone` entries (the same code, moved). This is drift in `security/duplicates-baseline.txt`, the human's file, and it is still open since the first acceptance.
- Still open from F0061-A0001: `_fixed_environment` reads `PATH` from `os.environ` inside the adapter, while the uv cache is read in `entry` and passed in. No rule is broken, so no story.
- S0002's tester added a local `_NoVariableFixture` (returns `{}`) to `tests/shared/adapters/test_document_examples_uv_cache.py`, because the support `EmptyFixture` always gives one variable. It is not a copy, as the reviewer confirmed. If a second module needs it, it belongs in `tests/support/document_examples_support.py`.
- My own: the intermittent `fixture instance could not be prepared` (see 2), whose reason the finding drops. Proposed as S0003.

## 5 Documentation

None of weight. `docs/project-guide/style.md:32` and `docs/project-guide/shared.md:236-239` agree with each other and with the code:
- the fixed variables, which a fixture cannot replace;
- `UV_CACHE_DIR` and `UV_LINK_MODE=copy` only when the check's process has a cache;
- the reason for each;
- the lookup order.

"Agent runs copy for the same reason" (`shared.md:238`) matches `operator/vm/Dockerfile:61` and `docs/decisions.md:1047`. `README.md` and the operator guide do not describe the examples' environment and need nothing. `make documents` was green on fresh clones.

`docs/decisions.md` has no entry for sharing the cache with the examples. The reason (feature decision 1: the cache is content-addressed and safe for concurrent use) lives only in `feature.md` and, in short, in `shared.md:237`. Neither story's docs criterion asked for an entry. It is listed under 6 for the human. I propose no story.

`shared.md:242` names the finding `fixture <name> could not be prepared`. S0003's docs criterion would update it.

## 6 Decisions taken for the human

1. (`feature.md` 1) Sharing the cache does not change what an example prints. The smoke test confirms it, now that S0002 also removed uv's hardlink warning.
2. (`feature.md` 2) A separate feature, not part of F0060.
3. (S0001 intake, journal 3–4) The human chose (a): an end-to-end criterion for the `entry` wiring (`tests/entry/test_check_documents_uv_cache.py`).
4. (S0001) The lookup imitates uv's own order (`UV_CACHE_DIR`, `XDG_CACHE_HOME/uv`, `HOME/.cache/uv`), and an empty value counts as not set. It does not ask `uv cache dir`, which would be a second process.
5. (S0001 coder) The cache is part of the one fixed environment, merged after the fixture's, so a fixture cannot change it.
6. (S0002 coder) `UV_LINK_MODE=copy` is set only together with a uv cache. Rejected: setting it always. Without a cache a fixture's own `UV_LINK_MODE` reaches the command.
7. (S0002 tester) A local fixture that gives no variable, rather than the support `EmptyFixture`. The caller's own `UV_LINK_MODE=clone` is set in the test, to show that it does not leak through `env -i`.
8. New for the human: whether `docs/decisions.md` should record decision 1 (see 5). Also, `feature.md` lists only S0001 (see 1).

Earlier tests changed:
- S0001: `tests/shared/adapters/test_document_examples.py`, changed in round 1 under the standing leave to move a shared test helper (`CLAUDE.md`, *Tests*). The S0001 reviewer named it, as F0061-A0001 recorded.
- S0002: only added two tests and one private class to S0001's own `tests/shared/adapters/test_document_examples_uv_cache.py`, and changed no test in it (reviewer entry 9).

No earlier test was changed without a leave.

## 7 The slow checks

The project offers nothing beyond `make check` today, except `make mutants` (see 3). `make documents` took 49.1 to 49.7 s on fresh clones here, and 51.0 s in S0002's docs stage.

Slowest tests in `.reports/junit.xml` (11029 tests):
- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other`, 20.0 s;
- six tests of 10.0 s each, all held at `ROOMY_LIMIT` on purpose (podman timeout status ×2, opencode events, opencode budget, claude runtime resume ×2).

The feature's tests take 0.04 s at most each.

Disk: the Disk now line is the same as the previous record line, with the same free and used space on all three paths. No growth to explain.

## 8 Cost

The stories cost 16 runs, 21.7 min and 91 turns, with 328985 tokens in (2595051 more from cache) and 36355 out: **$2.89**.
- S0001: 10 runs, $2.06.
- S0002: 6 runs, $0.83, one pass with no rework.

S0001 stands out. Its intake ran twice, around the human's question, and its round 0 review finding (copied test helpers) cost a second tests, doing and review run. F0061-A0001 cost a further $0.87, not counted in the stories' sum.

Human interventions: **1 question answered** (question 1), **0.0 h waited**. It was at S0001's intake: no criterion tested the `entry` wiring, the one line that makes the feature work, and the human chose an end-to-end criterion. So S0001 needed the human most. S0002 needed no answer.

## Proposed stories

- `backlog/F0061-S0003-a-fixture-that-could-not-be-prepared-says-why.md`: the finding of a fixture that could not be prepared ends with the `FixtureError`'s detail, joined into one line. A blocking `fixture instance could not be prepared`, as seen once in four runs here, can then be traced instead of stalling a docs stage blind.
  - It changes one earlier test's expected text, so the human must give a leave in `feature.md` first; the story proposes the words.
  - It lies at the edge of this feature's goal (docs stages stalling on examples they did not change). The human may move it to another feature.

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted; 1 story proposed

   1. Scope: none of weight.
      - S0001 built the scope line: `uv_cache_directory`, `UV_CACHE_DIR` in `_fixed_environment`, and the wiring at `check_documents.py:205`.
      - S0002 (proposed by F0061-A0001) added `UV_LINK_MODE=copy` with the cache.
      - Out of scope holds: the limit is still 60 s, and no cache is shared between instances.
      - `feature.md` still lists only S0001 under *Scope* and *Stories*. This is a note for the human.
      - `make check` is green (99.21 %).
   2. Feature smoke test: green.
      - I added an example to a listed document of a fresh clone and ran `factory.entry.check_documents`. It printed `[/work/home/.cache/uv] [copy]`, 0 hardlink warnings, and the first `uv run` finished under 10 s. Result: `documents ok (49.7 s)`, status 0.
      - The before side (cache without `UV_LINK_MODE`, by hand) shows uv's hardlink warning.
      - A wrong expectation was caught at the block's line. That same run also blocked on `install.md:188: fixture instance could not be prepared`, which this feature did not touch. Two more full runs were green, so it happened once in four, and the finding drops the reason.
   3. Mutation testing: by sweep, not run here.
   4. Noticed:
      - The S0002 stages noticed nothing more.
      - `make duplicates` still shows 7 new, the same as at A0001 and none in this feature's code. It is baseline drift in the human's file.
      - `_fixed_environment` reading `PATH` from `os.environ` is still open from A0001. No story.
      - My own: the intermittent fixture failure without a reason. Proposed as S0003.
   5. Docs: none of weight.
      - `style.md:32` and `shared.md:236-239` agree with the code and with each other.
      - `docs/decisions.md` has no entry for sharing the cache. Listed for the human, no story.
   6. Decisions for the human:
      - the feature's two decisions;
      - the S0001 intake answer (a);
      - uv's own lookup order, with an empty value counting as not set;
      - the cache in the fixed environment;
      - S0002's link mode set only with a cache, and its local no-variable fixture;
      - whether to add a decisions.md entry.
      - Earlier tests: S0001 changed `test_document_examples.py` under the standing leave to move a shared helper. S0002 changed none. None changed without a leave.
   7. Slow checks: nothing beyond `make check`.
      - Slowest test: `test_documents_marker`, 20.0 s; next, six tests of 10 s each at `ROOMY_LIMIT`.
      - The disk is the same as at the previous record.
   8. Cost: 16 runs, $2.89 (S0001 $2.06, S0002 $0.83).
      - S0001 stands out because of its intake question and a review round for copied test helpers.
      - 1 question answered (S0001's intake, about the untested `entry` wiring), 0.0 h waited.
