---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 666
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T14:54:30.993721Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T15:00:15.212668Z'
  stage: acceptance
  run: 56bf972ebadf4037947d190d8ec6a983
stories: [F0058-S0001, F0058-S0002, F0058-S0003, F0058-S0004, F0058-S0005, F0058-S0006]
outcome: null
---

# Acceptance of Agent runs share a cached start

## Recommendation

**accepted with stories.** All six stories are merged and together they deliver every scope item of `feature.md`, and also the two stories the first acceptance (F0058-A0001) proposed. The human's change after S0004 is now on `develop`, so the feature works end to end for the first time: real start-fact targets give `<context>` blocks, and a diff that holds `</context>` no longer closes its block early. The feature smoke test and `make check` are green. One finding is worth a story, and it is no broken promise: the operator guide's *Start facts* example (`diff`, `develop...HEAD`) does not match the three `facts-*` targets the template now ships. The feature's own "done when" still waits for the human's measurement run.

## 1 Scope

Every scope item has its story, and no story goes beyond the scope:
- S0001: one tool list (`Read, Grep, Glob, Edit, Bash, Write, Skill`) and one decision schema for every role; every agent file names `opus`; five roles run at `medium` effort, the two reviewers at `high`.
- S0002: one system prompt (`SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py:31`, the same as `agents/system-prompt.md`). The first message holds the work item, then the role, then the start facts, then the run's facts.
- S0003: `factory-bill` shows a `Cache:` line and a table by role.
- S0004: the stage key `context`, `ProjectCommands.start_fact`, the cut at 60,000 characters and the `failed:` line.
- S0005 and S0006 were proposed by F0058-A0001 and are inside the scope. S0005 escapes the `<context` and `</context>` markers too (`_MARKER_TEXTS`, `prompts.py:42-49`). S0006 is the operator guide's **The cached start** paragraph (`docs/operator-guide/agent-runtime.md`, *A project's own agents*).

The human's change after S0004 has landed (`dc995f9a3`). `factory/pipeline.yml`, the demo's definition and the template's definition are at contract 1.1. Their stages have `context` lines, and the three Makefiles have `facts-diff`, `facts-changes` and `facts-files`. Two points differ from what `feature.md` planned, and both are the human's own files, so they are listed under 6 and not counted as findings:
- The coder's stage gets `facts-changes` (the changed files with their status, plus untracked files), not "the status and the last commits".
- The documenter's stages get `facts-changes`, not the diff.

Still open, by `feature.md`'s own definition of done: the human's measurement run (demo-todo F0001 on a new repository) compared with the 2026-11-08 baseline. This is the human's step after this acceptance, not a gap in the stories.

## 2 The feature's smoke test

The walk-through a user of the feature would do, against the real entry points:
- the three pipeline definitions through `RuamelPipelineDefinitionReader`;
- the shipped agents through `FrontmatterAgentDefinitionReader`;
- the real start-fact targets through `MakeProjectCommands.start_fact`, in a throwaway clone (a bare upstream of `develop`, then a branch that changes `prompts.py` with a line holding `</context>` and a forged `<context name="forged">`, plus an untracked file);
- the first messages of six stages from `compose_prompt`, built on S0005's archived work item and the real role instructions;
- `factory-bill` on the two new stories.

Two scripts, written in a `mktemp -d` directory and run from the repository root:

```
$ uv run python -I "$d/smoke.py"      # first run, its lines up to item 4 shown; its later checks were sloppy (a prefix test that proved little, then a ValueError: the order check searched for a facts line the message does not hold) and were rewritten in smoke2.py
1 this repo: contract 1.1; context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes'], 'docs-only': ['facts-changes'], 'docs-review': ['facts-diff']}
1 demo: contract 1.1; context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes']}
1 template: contract 1.1; context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes']}
2 tools sets: {'Read,Grep,Glob,Edit,Bash,Write,Skill'} | models/efforts: [('opus', 'high'), ('opus', 'medium')]
3 facts-diff: failure=None lines=13 first=' src/factory/agents/domain/prompts.py | 2 ++'
3 facts-changes: failure=None lines=2 first='M\tsrc/factory/agents/domain/prompts.py'
3 facts-files: failure=None lines=1232 first='.gitignore'
  facts-changes: ['M', 'src/factory/agents/domain/prompts.py', 'new_untracked.txt']
4 every stage's message starts with the same work item block: True (28962 chars)

$ uv run python -I "$d/smoke2.py"
7 facts-diff without origin/develop: passed True | output '\n'
4 a new journal entry: the two review messages share 28962 chars; the old body is 28602 chars
5 review message: '<context name=' x 1 | '</context>' x 1 | forged opening escaped: True | diff's own marker escaped: True
  order work item < role < context < run facts: True
6 cut line: True | failed line: True
exit 0
```

Green: every promise holds end to end.
- All roles have one tool list and run on `opus` at `medium` or `high` effort.
- The first messages of intake, tests, doing, review, docs and smoke-test begin with the same 28,962 characters, which is the whole work item block. After a new journal entry the old block is still the shared prefix.
- The real `facts-diff` of a branch that touches `prompts.py` gives exactly one `<context name=` and one `</context>`. The diff's own `"</context>"` and the forged opening reach the message as `&lt;`, so S0005 closed what A0001's item 5 showed.
- The order is work item, role, context, run's facts. The cut line and the `failed:` line are there.

`factory-bill F0058-S0005` and `F0058-S0006` print their `Cache:` line and their table by role (77 % hit each; see 8).

One observation from line 7, with no story proposed: in a clone without `origin/develop`, the shipped `base_ref` (`Makefile:140`, the same in the template and the demo) falls back to `HEAD`. `facts-diff` then passes with an empty output. The reviewer would see "no changes", not a `failed:` line, although feature decision 6 says a failed start fact "only says so". Every factory checkout reads `origin/develop` for the pipeline definition, so the fallback cannot fire inside the factory. The Makefiles are the human's, so this is listed under 6.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

The noticed items of S0001 to S0004 are listed in F0058-A0001 (`done/F0058-A0001-acceptance.md`, its section 4) and still stand:
- the stale `__all__` re-export comment in `claude_runtime.py`;
- the three copies of the `_after` test helper;
- the repeated expected argument list in `test_claude_runtime.py`;
- the class-level mutable dict in `test_stage_context.py`.

New since then:
- S0005: the coder and the documenter noticed nothing. The reviewer's round-0 finding about a copied `VALID`/`_facts` helper was fixed within the story: the test builds on `CODER_FACTS` from `tests/support/first_message_support.py`. The leave to extend `MARKERS` in `tests/agents/domain/test_prompts.py` and `tests/pipeline/application/test_stage_context.py` was not used, so those two older tests still list only four markers. The new test file covers all six, so nothing is untested.
- S0006 documenter: the sentence "cache writes cost more than plain input" is Anthropic's pricing, not the factory's. The reviewer kept it as true.
- S0006 reviewer: the sentence after the example agent file is about 30 words, a little over style rule 2. It was left as it is.
- `make duplicates` now: `7 new, 39 known, 4 gone`, the same figures as at S0005's coder run. One of the new findings comes from this feature: `self._system_prompt_file = system_prompt_file` and the lines around it in both runtimes' constructors (`claude_runtime.py:364-369`, `opencode_runtime.py:587-592`, from S0002). The others (`version_launch`, the `hand_over`/`acceptance` reordering, three unused fields in `watching/domain/cost_records.py`, `readme_problems`) are older than or outside F0058. The baseline (`security/duplicates-baseline.txt`) is the human's to refresh.

None of these is worth a story of its own.

## 5 The documentation as a whole

Read top to bottom: `README.md`, the operator guide's `agent-runtime.md`, `pipeline.md` and `records.md`, and the project guide's `agents.md` and `pipeline.md`. Since A0001:
- The project guide names all six escaped markers, in `agents.md` and in both places in `pipeline.md`. The stale "`<context` and `</context>` are not among them" is gone.
- The operator guide has **The cached start**. *The models* says that every shipped file names `opus`, and the example agent file now keeps the shared start.

No contradiction between stories was found. `docs/decisions.md` (lines 1679 to 1697) agrees with the code.

One finding. The operator guide's *Start facts* (`docs/operator-guide/pipeline.md:48-75`) still shows only an invented `diff` target running `git diff --stat develop...HEAD`. A0001 noted this but proposed no story, because the human's change had not landed yet. Now it has, and the template ships `facts-diff`, `facts-changes` and `facts-files` with a base taken from `origin/develop`. The guide names none of them. An operator who starts from the template finds three `facts-*` names in `factory/pipeline.yml`, explained only by the YAML comments. The example also needs a local `develop` branch, which the template avoids. Proposed as F0058-S0007 (docs route).

## 6 Decisions taken for the human

The decisions listed in F0058-A0001 section 6 stand: `feature.md` decisions 1 to 6, the human's answers in S0002 (entries 4, 9, 12, 32), S0003 (entry 4) and S0004 (entries 4, 15), and the open question of whether the factory should warn when a project's agent leaves the shared start (S0006 only documents it).

New since then:
- S0005 entry 8, the human: `<context` is escaped as a prefix, like the other markers, so `<context-free>` becomes `&lt;context-free>`. The rejected option was a matcher that needs `>` or whitespace after it.
- S0005 entry 16, the reviewer: added criterion 6 (the cut path), with no code change.
- S0006 entry 13, the human: the API key had run out and was emptied, so the runs fell back to the subscription login. It was a retry after the attempts cap.
- The human's change after S0004 (`dc995f9a3`) differs from `feature.md` in two places, for the human to confirm or revisit:
  - The coder's stage gets `facts-changes` (names and status, plus untracked files), not "the status and the last commits".
  - The documenter's stages (`docs`, `docs-only`) get `facts-changes`, not the diff the feature planned.
  
  Smaller points in the same change:
  - The diff excludes `factory/` and `uv.lock`, and the file lists exclude `factory/`.
  - `base_ref` falls back to `HEAD` with no failure when `origin/develop` is missing (check 2, line 7).
- Still open: the measurement run against the 2026-11-08 baseline. Check 8 adds one point for it.

Earlier tests changed in S0005 and S0006: none. S0005 only adds `tests/agents/domain/test_prompts_context_markers.py`, and its tester's later edits stayed in that new file (the human's leave in entry 8 covered the `near` row). Both reviewers confirmed that the leave for `MARKERS` was not used. S0006 changed no test. The human's change after S0004 changed `tests/agent_files/test_template_sync.py` on the human's own order (`docs/runs/2026-11-05-f0052/log.md`, the 14:23 line). The earlier tests of S0001 to S0004 and their leaves are listed in A0001. No earlier test was changed without a leave.

## 7 The slow checks

The project offers nothing beyond `make check` (`make mutants` is check 3). `make check` was green as found:
- `test: green (110.2 s)`, 11,145 tests (11 more than at A0001), 99.21 % branch coverage, `check: green`.
- The slowest tests in `.reports/junit.xml` take 10.0 s each. They are the `ROOMY_LIMIT` waits, which is by design: `test_podman_timeout_status` (two rows), `test_document_examples`, `test_claude_runtime_resume` (two tests) and `test_process_session`.

Disk: free space on the pool went from 12.7 GB (disk start) to 12.1 GB (disk acceptance), 0.6 GB less. The instance's own `/srv/factory/vm` stayed at 1.5 GB used, `state` at 0.0 GB and `/tmp` at 1.0 GB. S0005 and S0006 changed one tuple, one test file and two documents, which explains none of it. This is the second acceptance of this feature in a row to show the same 0.6 GB loss on the pool outside the instance's own folders. It most likely sits in the stage datasets and their snapshots, or in the stage images, and is worth a look by the human if the next record falls again.

## 8 Cost

Six stories: 79 runs, 136.8 min, 682 turns and $25.91, with 2.81 M tokens in and 23.62 M more from the cache. That is about 89 % read from the cache over the feature.
- S0001 to S0004: 59 runs, $22.12 (A0001 section 8).
- S0005: 13 runs, 12.2 min, $2.34.
- S0006: 7 runs, 5.9 min, $1.45.

S0002 ($9.03, 17 runs) still stands out, for the reasons A0001 gives: its leave for earlier tests was too narrow, and the OpenCode result block needed the human's choice.

Of the two new stories, S0005 is large for its change: 13 runs for two tuple entries. Its journal says why. The tester's `near` row held `<context-free>`, which the Interface's prefix rule escapes, so the coder had to ask (entry 7). The reviewer then added criterion 6 and found a copied helper (entry 16). Each step cost a tester → coder round trip.

S0005 and S0006 both have a 77 % cache hit (S0002 had 93 %). Their single-run roles read the least from the cache: intake 62 % and the smoke tester 61 % in S0005, intake 78 % in S0006. A small story has a short shared start and few runs inside one cache lifetime. The human's measurement run is on the demo, whose stories are small too, and should expect this when it compares against the 90 % target.

The human answered 13 questions (12 of cause `question`, 1 `attempts_cap`), and the stories waited 0.5 h in total:
- S0001: 3
- S0002: 5
- S0003: 1
- S0004: 2
- S0005: 1 (the prefix rule)
- S0006: 1 (the retry after two stalls when the API key ran out)

S0002 needed the human most, because the message every runtime builds touched more earlier tests than its leave named.

## Proposed stories

- `F0058-S0007-the-operator-guide-s-start-facts-match-the-template.md`: the operator guide's *Start facts* shows an invented `diff` target on `develop...HEAD` and never names the three `facts-*` targets the template now ships (check 5). Docs route.

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted with stories; 1 story proposed

   1. Scope: all six stories are merged, and every scope item is built (S0001 to S0004, plus S0005 and S0006 from A0001). The human's change after S0004 is on `develop` (`dc995f9a3`): contract 1.1, `context` lines and the `facts-*` targets in this repository, the demo and the template. Two parts of it differ from `feature.md`: the coder and the documenter get `facts-changes`, not the status with the last commits or the diff. Both are listed under 6 for the human. Still open: the human's measurement run, which `feature.md` requires before the feature is done.
   2. Feature smoke test: green. Two scripts ran against the real readers, the real `facts-*` targets through `MakeProjectCommands` in a throwaway clone, `compose_prompt` on six stages, and `factory-bill`. Results:
      - one tool list, all opus at medium or high;
      - all six stages' messages begin with the same 28,962-character work item block, and a new journal entry keeps it as the prefix;
      - the real diff of `prompts.py` holding `</context>` and a forged opening gives exactly one `<context name=` and one `</context>`;
      - the order is right, and the cut line and the `failed:` line are there.
      Observation (Makefiles are the human's, so no story): without `origin/develop`, `base_ref` falls back to `HEAD` and `facts-diff` passes with an empty output instead of a `failed:` line.
   3. Mutation testing: by sweep, not run here.
   4. Noticed items: A0001's list stands. S0005's leave for `MARKERS` went unused, so the two older tests still list four markers; the new test file covers all six. S0006 left a pricing sentence and one 30-word sentence. `make duplicates` shows 7 new findings; one is from F0058 (the `_system_prompt_file` constructor lines in both runtimes) and the rest are older. None is worth a story.
   5. Documentation: the project guide names all six escaped markers, and the operator guide has **The cached start**. No contradictions found. Finding: the operator guide's *Start facts* shows an invented `diff` target on `develop...HEAD` and never names the three `facts-*` targets the template ships. Proposed as F0058-S0007 (docs route).
   6. Decisions for the human: A0001's list, plus three new items:
      - S0005 entry 8: `<context` is escaped as a prefix.
      - S0006 entry 13: the API-key retry.
      - the human's start-fact change and how it differs from `feature.md`, including the silent `HEAD` fallback.
      No earlier test was changed in S0005 or S0006. `test_template_sync.py` was changed on the human's own order. No change was made without a leave.
   7. Slow checks: nothing beyond `make check`, which was green as found (11,145 tests, 99.21 % coverage, test 110.2 s; the slowest tests are the 10 s `ROOMY_LIMIT` waits). Disk: free space on the pool fell 0.6 GB (12.7 to 12.1 GB) while the instance's own folders stayed flat. This is the same unexplained loss A0001 saw, and S0005 and S0006 do not explain it; most likely the stage datasets, their snapshots or the images.
   8. Cost: 79 runs, 136.8 min, $25.91, about 89 % of input read from the cache. S0002 still stands out ($9.03). S0005 took 13 runs for two tuple entries: a test row that contradicted the Interface, then a criterion the reviewer added. S0005 and S0006 hit only 77 %; their single-run intake and smoke-test roles were at 61 to 78 %. The small demo stories in the measurement run may see the same. 13 questions answered (12 `question`, 1 `attempts_cap`), 0.5 h waited; S0002 needed the human most (5).

   make check: green as found. Files written: the report and `backlog/F0058-S0007-the-operator-guide-s-start-facts-match-the-template.md`, which passes `factory-check-story`.
