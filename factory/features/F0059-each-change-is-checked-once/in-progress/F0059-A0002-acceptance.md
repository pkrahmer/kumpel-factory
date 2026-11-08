---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 676
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T17:06:37.953009Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T17:12:50.732455Z'
  stage: acceptance
  run: 36807a47d9dc4da090fedfe9612aa7a8
stories: [F0059-S0001, F0059-S0002, F0059-S0003]
outcome: null
---

# Acceptance of Each change is checked once

## Recommendation

accepted. S0003, the story the first acceptance (F0059-A0001) proposed, repaired every stale passage that acceptance named, and the operator guide and the project guide now agree with the human's commit `77c97b622`: one full `make check` after the smoke tester, `make guides` in the docs stages, and a documents-only change that reuses the passed check. The feature smoke test, `make check`, `make guides` and `make documents` are green on this branch; no new finding is worth a story, and the one done-condition left open is the human's measurement run.

## 1 Scope

The scope lines and their stories are unchanged since F0059-A0001: the coder's first step (S0001, `agents/agents/coder.md`), the marker `documents` in `tests/conftest.py` (S0001) and the smoke tester's route after a red check (S0002, `agents/agents/smoke-tester.md`). The human's changes are on `develop` in `77c97b622`. S0003 is the follow-up of those changes: documents only (`docs/operator-guide/pipeline.md`, `docs/project-guide/README.md`), inside the feature's *The human's changes*, nothing out of scope. Between the first acceptance's merge (`9e52df6fc`) and S0003's archive (`f7724bbb4`) `develop` changed only those two documents, the story's own files, and one line of the human's `docs/runs/2026-11-05-f0052/log.md` (`0af1776e2`, the demo2 instance removed).

Of the Goal's done-conditions, all are met but the human's measurement run (demo-todo F0001 on a fresh repository against the baseline of 2026-11-08). It is the human's, after this acceptance; no story is owed for it.

## 2 Feature smoke test

One Python script against the real entry points, run on this branch with `uv run python <tmp>/smoke.py "$PWD"`: it loads `factory/pipeline.yml` through `RuamelPipelineDefinitionReader`, computes `check`'s key with `GitCli.work_tree_id(not_read)` in a fresh clone before and after a documents-only change (`README.md`, both guides, `tests/README.md`) and after a test-file change, then compares every YAML and Make line the operator guide's code blocks present, and its inline `smoke-test:` quote, with the three files the guide quotes (`operator/template/factory/pipeline.yml`, `operator/template/Makefile`, `factory/pipeline.yml`), and reads the project guide's marker paragraph.

```text
1. the pipeline definition loads; checks per stage:
   doing: checks=[] reports=['duplicates'] -> 42 of 60 min
   docs: checks=['guides', 'secrets', 'documents'] reports=[] -> 47 of 60 min
   smoke-test: checks=['check'] reports=[] -> 48 of 60 min
   docs-only: checks=['check', 'guides', 'secrets', 'documents'] reports=[] -> 55 of 60 min
2. documenter write paths not in check's not_read: []
3. documents-only change: check's key unchanged: True | whole tree changed: True
4. test-file change: check's key changed: True
5. every quoted YAML/Make line of the operator guide appears verbatim in the file it quotes:
   MISSING contract: '1.0'
   ok  roles:
   ok  tester:
   MISSING write_paths: ['tests/*', '{work_item}']
   ok  coder:
   MISSING write_paths: ['src/*', '{work_item}']
   MISSING testing: {role: tester, next: [doing], checks: [lint]}
   MISSING doing: {role: coder, next: [review], checks: [check]}
   MISSING review: {approval: true, next: [done, doing], round_cap: 3}
   ok  done: {}
   ok  facts-diff: {time_limit: 1}
   ok  facts-changes: {time_limit: 1}
   ok  facts-files: {time_limit: 1}
   ok  tests: {role: tester, next: [doing], checks: [lint], reports: [test], context: [facts-file
   ok  doing: {role: coder, next: [review, tests], context: [facts-changes]}
   ok  review: {role: reviewer, next: [docs, doing], round_cap: 3, context: [facts-diff]}
   ok  base_ref = $$(git merge-base HEAD origin/develop)
   ok  facts-diff:
   ok  base=$(base_ref); git diff --stat "$$base" -- . ':!factory' ':!uv.lock'; echo; git diff "$
   MISSING check: {time_limit: 10, not_read: ["notes/*.md", "notes/*.jsonl"]}
   ok  check: {time_limit: 8, not_read: ["docs/runs/*", "factory/features/*.md", "factory/feature
   ok  inline: smoke-test: {role: smoke-tester, next: [approval, doing, docs], checks: [check], round_cap: 3}
6. the project guide's marker paragraph:
   'Until then' gone: True | names make guides: True | names make check guides: True
   operator guide 'turn `make check` red' gone: True
```

The `MISSING` lines are not quotes: they are the guide's minimal example definition (`docs/operator-guide/pipeline.md:11-23`) and its `notes/*.md` example of a `not_read` pattern, both illustrations, as S0003's intake ruled. Every line the guide presents as a quote of one of the three files is found there.

The marker selections and the make targets, run in the foreground:

```text
$ uv run pytest --collect-only -q -m documents        -> 176 tests
$ uv run pytest --collect-only -q -m "not documents"  -> 11007 tests
$ uv run pytest --collect-only -q                     -> 11183 tests
$ make check 2>&1 | tail -2
test: green (104.5 s)
check: green
$ make guides 2>&1 | tail -1
guides: green (9.8 s)
$ make documents 2>&1 | tail -1
documents ok (85.0 s)
```

The leases fit, a documents-only change keeps `check`'s key so the passed check is reused, a test change runs it again, the two selections make up the whole suite, and the guides now say so. Green.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- S0003 reviewer, weighed and not counted (entry 11): step 3 of *The docs route* (`docs/operator-guide/pipeline.md:104`) says `check`'s `not_read` lists the documenter's write paths, which is true of kumpel-factory's definition only. The template has no docs route and its `check` has no `not_read` (`operator/template/factory/pipeline.yml:6`), so an operator who adds the route without the pattern pays one more `make check` per documents-only story; the section on `not_read` below explains how to add it. A cost, not a fault; no story.
- S0003 documenter (entry 5): the minimal example at `docs/operator-guide/pipeline.md:20` keeps `doing` with `checks: [check]`. It is an illustration of a definition with no smoke-test stage, where the check after the coder is the only one; right as it stands.
- S0003 reviewer findings of round 0 (a 50-word sentence, and "`make check` reads none of the documenter's files", false because `secrets` scans changed documents) were fixed in round 1; nothing left.
- Carried from F0059-A0001 and still open, both left to the human: the loose `"only" in text` assert of `tests/agent_files/test_claude_agent_texts_first_tests.py:30`, and `make duplicates`, still `7 new, 39 known, 4 gone` today. The seven predate F0059 (the `handed_over` copy in `hand_over`/`acceptance`, the runtimes' `version_launch` and `_system_prompt_file` lines, vulture's `readme_problems` and three `cost_records` fields); none of this feature's stories changed `src/`.

## 5 The documentation as a whole

`README.md`, `docs/operator-guide/` and `docs/project-guide/` read again for where the checks run. The six places F0059-A0001 named are repaired: the template's `doing`, `base_ref` and `smoke-test` quotes match their files, step 3 of the docs route names `make guides`, the `not_read` paragraph and its YAML block match `factory/pipeline.yml:10`, and `docs/project-guide/README.md:231` says what `make test` and `make guides` run now. `docs/project-guide/agents.md` (the smoke tester's `check_red` route) and `CLAUDE.md` (*Checks*) say the same thing as the operator guide. No contradiction, nothing explained twice differently, and `make documents` is green. The one generality of step 3 is under 4.

## 6 Decisions taken for the human

Accepted or revisited with F0059-A0001, listed again for one place:
1. `feature.md` decisions 1 to 4: S0001 before the `Makefile` change; the marked guards run in the docs stages and in the coder's `make check guides`; the marker is the project's; no factory check after the coder, and a red check after the smoke tester is a `check_red` stall that the smoke tester routes to `doing` or `docs`.
2. S0001's answered questions (entries 4, 9 and 18): `-q` dropped from the smoke test; `tests/operator_scripts/test_operator_site_check.py` marked as a whole; the tester's search widened to guards that read code as well as documents (licence headers, branch-name and mount-program searches), which now run only in `make guides`, still before every approval because every route passes a docs stage after the last coder run; `test_todays_install_guide_gives_no_settings_finding` moved under its name into `tests/guards/test_install_guide_settings.py`.
3. The human's `77c97b622` beyond the feature's list: the `base_ref` fallback dropped in the three Makefiles.

New with S0003: none. It took no decision for the human: no question, and its intake's ruling that the minimal example at `docs/operator-guide/pipeline.md:20` is an illustration and not a quote follows from the story's criterion 1.

Earlier tests changed: S0003 changed no test. S0001's and S0002's changes, each with its leave, are listed in F0059-A0001; no finding.

## 7 The slow checks

The project offers nothing beyond `make check` but `make mutants` (check 3): no image scan, no SBOM.

From `.reports/junit.xml` of this branch's `make check`: 11007 tests, 951 s of test time, 104.5 s wall. The slowest is still `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other` at 20.2 s (three pytest collections, unmarked, so every `make check` pays it on one worker); next the 10 s `ROOMY_LIMIT` tests (`test_podman_timeout_status` twice, `test_document_examples`, `test_opencode_events`). `make guides` took 9.8 s against its `time_limit` of 2 minutes, `make documents` 85.0 s against 2 minutes; the latter ran 60 to 70 s in the stories' runs, worth watching in the measurement run.

Disk: now `/srv/factory/vm` 11.8 GB free and 1.5 GB used, against 10.6 GB free and 1.5 GB used at the previous record (disk acceptance, F0059-A0001); `/srv/factory/vm/state` (0.0 GB used) and `/tmp` (2.1 GB used) show the same 1.2 GB more free space on the shared pool. No growth. The 0.6 GB that F0059-A0001 could not explain came back and more; the human's log line `0af1776e2` (demo2 instance removed) is the likely cause.

## 8 Cost

The stories cost 24 runs, 32.0 min, 168 turns and $9.29: S0001 13 runs and $6.02, S0002 6 runs and $1.75, S0003 5 runs, 4.6 min and $1.52. S0001 still stands out, for the reasons F0059-A0001 gave: the tester's search missed two modules, which cost a review finding, a question and three coder runs that changed nothing. S0003 took one rework round: the docs-review found a 50-word sentence and an untrue "`make check` reads none of the documenter's files", and the second documenter and reviewer runs cost $0.55. Outside the stories, F0059-A0001 cost $1.62 and one crashed run.

Human interventions: 3 questions answered, all of cause `question` and all in S0001 (intake, tests and doing), 0.1 h waited together. S0001 needed the human most, because its leave covered only `tests/guards/` and documents were read from modules outside it. S0002 and S0003 needed none.

## Proposed stories

None. The one finding of F0059-A0001 is repaired by S0003, and the observations under 4 are notes for the human, not changes worth a run.

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted; 0 stories proposed

   1. Scope: every scope line has its story (S0001, S0002). S0003 is the documents follow-up to the human's commit `77c97b622` and stays within scope. All done-conditions are met except the measurement run against the 2026-11-08 baseline, which is the human's.
   2. Feature smoke test: green.
      - The pipeline definition loads, and the leases fit (42, 47, 48 and 55 of 60 min).
      - Every documenter write path is in `check`'s `not_read`. A documents-only change keeps `check`'s key, and a test-file change changes it.
      - The marker selections are 176 + 11007 = 11183 tests, the whole suite.
      - Every line the operator guide presents as a quote matches its file verbatim. The only lines that don't match are two illustrations.
      - `make check`, `make guides` (9.8 s) and `make documents` are green.
   3. Mutation testing: by sweep, not run here.
   4. Noticed:
      - Step 3 of the docs route states the `not_read` reuse in general terms, but only kumpel-factory's definition has it. That costs a template user one more check run, not a fault.
      - The minimal example at `docs/operator-guide/pipeline.md:20` is right as an illustration.
      - Carried from F0059-A0001: the loose `"only"` assert and the 7 `make duplicates` findings that predate F0059. Both are left to the human.
   5. Documentation: the six stale passages F0059-A0001 named are repaired. The operator guide, the project guide, `agents.md` and `CLAUDE.md` agree, and nothing contradicts.
   6. Decisions: the feature's 4 decisions, S0001's 3 answered questions and the human's `base_ref` change are listed again. S0003 took no decision and changed no test.
   7. Slow checks: nothing beyond `make check`.
      - The slowest test is still the unmarked `test_documents_marker.py` at 20.2 s.
      - `make documents` took 85 s here, against 60 to 70 s in the stories.
      - Disk: 1.2 GB more free than at F0059-A0001 and no growth. The earlier unexplained drop is likely the removed demo2 instance (`0af1776e2`).
   8. Cost: 24 runs, $9.29.
      - S0001 cost $6.02 (a missed module led to a question and three idle coder runs).
      - S0003 cost $1.52, including one docs-review rework round worth $0.55.
      - The human answered 3 questions, all in S0001, and waited 0.1 h in total.
