---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 670
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T15:36:50.420578Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-08T15:39:10.333030Z'
  stage: acceptance
- number: 3
  speaker: factory
  kind: started
  at: '2026-11-08T15:39:11.912260Z'
  stage: acceptance
- number: 4
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T15:44:05.012371Z'
  stage: acceptance
  run: 099f341d55544b8ea92889e1822c06b5
stories: [F0058-S0001, F0058-S0002, F0058-S0003, F0058-S0004, F0058-S0005, F0058-S0006, F0058-S0007, F0058-S0008]
outcome: null
---

# Acceptance of Agent runs share a cached start

## Recommendation

**accepted.** All eight stories are merged. S0008 closed the one gap that A0003 found against the feature's goal: the shipped reviewer now reads its diff from the `facts-diff` start fact and runs the command only as a fallback, and S0008's own reviewer did exactly that (its entry 9). The feature smoke test and `make check` are green. Following `planning/later-topics.md` item 1, this fourth acceptance judges only what came after A0003 and proposes no story: what is left is noticed items, plus the human's measurement run, which `feature.md` names as the human's step.

## 1 Scope

Since A0003 (`e4d8a1240`), `develop` changed these paths outside `factory/`:
- `agents/agents/reviewer.md`;
- `docs/project-guide/agents.md`;
- `tests/agent_files/test_reviewer_start_facts.py`, which is new;
- `tests/agent_files/test_claude_agent_texts_review_groups.py`;
- one line of the human's run log.

All of it is S0008. A0001 to A0003 judged the code of S0001 to S0007, it has not changed, and their section 1 still holds.

S0008 is inside S0004's scope item ("so the agent saves the turns it spends gathering them"). It meets its criteria:
- `agents/agents/reviewer.md:81` (*Stage* step 1) and `:91` (*docs-review* step 1) each say the diff is in the first message's `<context>` block. Each runs the command only in three cases: no block holds the diff, the block says `failed:`, or the block ends in the cut line.
- Neither step names `facts-diff`.
- "in your first command" no longer appears anywhere in the reviewer's text.
- The stages that run the reviewer get `facts-diff` in all three definitions: `review` and `docs-review` here, `review` in the demo and the template (smoke test, lines 1 and 3).

The documenter still gathers its own diff. That is the human's choice, made in `dc995f9a3` (`facts-changes` rather than the diff) and listed by A0003 under 6. No scope item is without a story, and no story lies outside the scope.

Still open, by `feature.md`'s own definition of done: the human's measurement run (demo-todo F0001 on a new repository) against the 2026-11-08 baseline.

## 2 The feature's smoke test

The walk-through follows the feature's purpose end to end, with S0008's reviewer added. It uses the real entry points:
- `RuamelPipelineDefinitionReader` on the three pipeline definitions;
- `FrontmatterAgentDefinitionReader` on the shipped agents;
- `MakeProjectCommands.start_fact` on the real `facts-*` targets, in a throwaway clone of `develop`. A branch changes `prompts.py` with a line holding `"</context>"` and a forged `<context name="forged">`, and adds an untracked file;
- `compose_prompt` for all seven roles on S0008's archived work item (front matter stripped), each role with its real instructions and its stage's real start facts;
- `factory-bill F0058-S0008`.

The script was written to a `mktemp -d` folder and run from the repository root. It passed on its first run:

```
$ uv run python /tmp/tmp.9twh9U4kDm/smoke.py /tmp/tmp.9twh9U4kDm
1 this repo: context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes'], 'docs-only': ['facts-changes'], 'docs-review': ['facts-diff']}; names are project commands: True; reviewer stages {'review': ['facts-diff'], 'docs-review': ['facts-diff']}
1 demo: context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes']}; names are project commands: True; reviewer stages {'review': ['facts-diff']}
1 template: context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes']}; names are project commands: True; reviewer stages {'review': ['facts-diff']}
2 roles ['acceptance-reviewer', 'coder', 'documenter', 'intake', 'reviewer', 'smoke-tester', 'tester'] | tool sets {'Read,Grep,Glob,Edit,Bash,Write,Skill'} | model/effort [('opus', 'high'), ('opus', 'medium')]
3 reviewer step: True True True True True
3 reviewer step: True True True True True
3 'in your first command' left in reviewer: 0
4 facts-diff: passed=True lines=13 first=' src/factory/agents/domain/prompts.py | 2 ++'
4 facts-changes: passed=True lines=2 first='M\tsrc/factory/agents/domain/prompts.py'
4 facts-files: passed=True lines=1234 first='.gitignore'
5 seven messages share 18294 chars; all start with the 18267-char work item block: True
5 after a new journal entry the old body is a prefix: True
6 reviewer message: <context name= x 1 | </context> x 1 | forged escaped: True | marker escaped: True
6 order work item < role < context < run facts: True
6 the diff block holds the changed file: True | leaves out factory/: True
7 ['[10 more characters cut here; run the project command facts-diff yourself for its whole output]'] ['failed: exit status 2']
7 reviewer's 'cut line' and 'failed:' match the message's lines: True
exit 0
```

Line 3 checks each of the reviewer's two diff steps for five things: it names `<context>`, it names `failed:`, it names the cut line, it no longer says "first command", and it names no `facts-` command.

```
$ uv run factory-bill F0058-S0008
...
Cost: 6 runs, 5.9 min, 32 turns, 175223 tokens in (745240 more from cache), 16085 out, $1.87
Cache: 745240 read, 175171 written, 81 % hit
| intake | 82332 | 22236 | 79 % |
| tester | 275658 | 51591 | 84 % |
| coder | 86967 | 22846 | 79 % |
| reviewer | 68634 | 26641 | 72 % |
| documenter | 172578 | 31098 | 85 % |
| smoke-tester | 59071 | 20759 | 74 % |
| **total** | 745240 | 175171 | 81 % |
exit 0
```

Green. Every promise holds end to end:
- every role has one tool list and runs on `opus`;
- all seven first messages begin with the same work item block, and that block stays a prefix after a new journal entry;
- the reviewer's message carries exactly one `facts-diff` block, with the forged and the real markers escaped;
- the order is work item, role, start facts, run's facts;
- the reviewer's instructions name the same `failed:` and cut lines that the message writes.

The temporary folder could not be removed: both `rm -rf` and `shutil.rmtree` were refused by the session's permission check. It holds only the script and the clone, and it is lost with the stage's container.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

The lists in A0001, A0002 and A0003 (section 4 each) still stand. New from S0008:
- **Tester (entry 5) and reviewer (entry 9):** `docs_review_reads_the_diff` in `tests/agent_files/test_claude_agent_texts_review_groups.py` is dead. The test cuts the `### docs-review` subsection out before it replaces anything, so the string never matches. It was dead before S0008.
- **Coder (entry 7):** *Stage* step 1 was kept on one line because the tester's regex `(?m)^1\. Review .*? (?=Do not read the Makefile)` has no DOTALL. The bound in the new test (next step, blank line or heading) holds the same constraint. A later rewrap of that step, for instance a sub-bullet for the fallback, breaks both tests without changing the meaning.
- **Intake (entry 3) and documenter (entry 11):** the docs-route table in `docs/project-guide/agents.md` has no `reviewer | review` row. The documenter placed the `review` side in the list of pinned passages (`agents.md:306`). Both reviews accepted this.

Found here:
- The *docs-review* step reads "`git diff develop...HEAD -- README.md docs operator/README.md`" from a block that holds the whole `facts-diff` (everything but `factory/` and `uv.lock`). On the docs route, the Interface changes only those three paths, so in practice the two are the same. If the documenter ever changed something else, the reviewer would see more than its scope, and its "Nothing else is under review" still tells it what to judge.
- `make duplicates` is unchanged since A0002 (`7 new, 39 known, 4 gone`, after S0008's coder).

## 5 The documentation as a whole

S0008 changed only `docs/project-guide/agents.md`: a new bullet in the list of pinned reviewer passages (`:306`) and the `reviewer | docs-review` row (`:325`). Both are true of `reviewer.md:81` and `:91`, and they link *Start facts* in the project guide's `pipeline.md`. Its cut and `failed:` lines are the ones the steps name.

A search of `README.md`, `docs/`, `agents/` and `operator/` for "first command" and `develop...HEAD` turns up no text that still has the reviewer gather its diff first. The remaining `develop...HEAD` lines are each correct:
- the documenter, which gets only `facts-changes`;
- the reviewer's scope line;
- its earlier-tests check, which uses `--name-status`.

The operator guide and `docs/decisions.md` needed nothing, as the criterion says. A0003's documentation finding, the reviewer row at `agents.md:324`, is closed. There is no contradiction between stories and no missing section.

## 6 Decisions taken for the human

The lists in A0001, A0002 and A0003 (section 6 each) stand:
- `feature.md` decisions 1 to 6;
- the human's answers in S0002 to S0006;
- the start-fact change `dc995f9a3`, where the coder and the documenter get `facts-changes`, not the diff;
- the silent `HEAD` fallback of `base_ref`;
- the open question of a warning when a project's agent leaves the shared start.

New with S0008:
- **The reviewer trusts the block.** It runs the diff only when the block is missing, says `failed:`, or is cut, and does not re-run it as a check on the block. This was A0003's open question. The human settled it by starting S0008 as proposed (`docs/runs/2026-11-05-f0052/log.md`, 15:23 UTC).
- **The coder's formatting choice:** step 1 stays on one line to fit the pinning regex (section 4). It is accepted, but it is a constraint on later wording.

Earlier tests changed in S0008:
- `tests/agent_files/test_claude_agent_texts_review_groups.py`, under the human's leave written into S0008's Interface (the strings `review_reads_the_diff` and `docs_review_reads_the_diff`). The tester made `review_reads_the_diff` a regex over the whole of step 1, rewrote its partner `review_reads_both` and moved that substitution to the front. The reviewer (entry 9) judged both within "as far as the reviewer's new wording needs", and I agree: the CRC test still checks the same earlier body.
- `tests/agent_files/test_claude_agent_texts_docs_route.py`: unchanged, although the leave covered it.

No earlier test was changed without a leave.

## 7 The slow checks

The project offers nothing beyond `make check`. `make mutants` is check 3. `make check` was green as found:
- `test: green (109.8 s)`;
- 11,148 tests in `.reports/junit.xml`, 1 skipped;
- 99.21 % branch coverage;
- the last line was `check: green`.

The slowest tests are the 10.0 s `ROOMY_LIMIT` waits, by design:
- `test_podman_timeout_status`, two rows;
- `test_claude_runtime_resume`, two tests;
- `test_opencode_events`;
- `test_process_session`, two rows;
- `test_process`.

Disk: the previous record is "disk start". From it to now:

| Mount | Free before | Free now | Used before | Used now |
| :-- | --: | --: | --: | --: |
| `/srv/factory/vm` | 12.5 GB | 11.9 GB | 1.6 GB | 1.5 GB |
| `state` | 12.5 GB | 11.9 GB | 0.0 GB | 0.0 GB |
| `/tmp` | 12.5 GB | 11.9 GB | 1.0 GB | 1.0 GB |

All three mounts share one pool, and its free space fell by 0.6 GB while the instance's own folders shrank. S0008 changed five text files, which explains none of it. This is the third time an F0058 acceptance has seen the same 0.6 GB fall: A0001, A0002, and now A0004 with its crashed first run. That points at something per run or per start outside the instance's folders (stage datasets, snapshots or images), as `planning/later-topics.md` item 2 already says. It is not a finding of this feature, but the repetition strengthens the item.

## 8 Cost

The feature's eight stories cost 90 runs, 146.7 min, 739 turns and $29.07, with 3.11 M tokens in and 24.79 M more from the cache. About 89 % of the input was read from the cache.

| stories | runs | USD |
| :-- | --: | --: |
| S0001 to S0004 | 59 | 22.12 |
| S0005 | 13 | 2.34 |
| S0006 | 7 | 1.45 |
| S0007 | 5 | 1.29 |
| S0008 | 6 | 1.87 |

S0002 ($9.03, 17 runs) still stands out, for the reasons A0001 gives: its leave for earlier tests was too narrow, and the OpenCode result block needed the human's choice. S0008 was an ordinary small story: 6 runs, no rework round, 81 % hit. Its reviewer had the lowest hit rate (72 %). That is expected: the reviewer runs at high effort, has no shared chain, and ran once in the story.

The human answered 13 questions (12 of cause `question`, 1 `attempts_cap`), and the stories waited 0.5 h in total. S0008 needed none, because its leave was written in at refinement. S0002 needed the human most (5 of the 13), because the message every runtime builds touched more earlier tests than its leave named.

This is the feature's fourth acceptance. Each has cost about $1.50 to $1.80. The first run of this one crashed without a result after about two and a half minutes (journal entry 2).

## Proposed stories

None. The one gap A0003 found is closed by S0008, and what is left is noticed items (section 4), which `planning/later-topics.md` item 1 asks to keep out of new stories.

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit e8ada771ab08d76c91d3dedff3631fdbdb988481.
3. factory: started acceptance as vm.
4. acceptance-reviewer: accepted; 0 stories proposed

   1. Scope: all eight stories are merged. The only change since A0003 is S0008, which closes A0003's gap against the goal: `agents/agents/reviewer.md:81` and `:91` now read the diff from the `<context>` block. They run the command only when the block is missing, says `failed:`, or is cut, and they name no project command. S0008's own reviewer worked this way (its entry 9). Still open: the human's measurement run.
   2. Feature smoke test: green, run for real against the real entry points, without changes to the script.
      - The three pipeline definitions give the reviewer stages `facts-diff`.
      - Every role has one tool list and runs on opus.
      - The real `facts-*` targets ran in a throwaway clone.
      - All seven first messages start with the same 18,267-character work item block, which stays a prefix after a new journal entry.
      - The reviewer's message has exactly one escaped `facts-diff` block, in the right order.
      - The cut and `failed:` lines match the reviewer's fallback wording.
      - `factory-bill F0058-S0008` shows an 81 % hit.
   3. Mutation testing: by sweep, not run here.
   4. Noticed items: the lists in A0001 to A0003 stand. New:
      - the dead `docs_review_reads_the_diff` string in `test_claude_agent_texts_review_groups.py`;
      - step 1 must stay on one line for the pinning regex;
      - the docs-route table has no `reviewer | review` row;
      - the *docs-review* step names a narrower diff than the `facts-diff` block holds, which is harmless on the docs route.
      `make duplicates` is unchanged (7 new, 39 known, 4 gone).
   5. Documentation: `docs/project-guide/agents.md:306` and `:325` match the reviewer's new steps. No text still has the reviewer gather its diff first, and no contradiction or missing section was found.
   6. Decisions for the human: the earlier lists stand. New:
      - the reviewer trusts the block, settled by the human starting S0008 as proposed;
      - the coder's one-line constraint.
      S0008 changed `test_claude_agent_texts_review_groups.py` under the human's leave written into the story, within that leave. No earlier test was changed without a leave.
   7. Slow checks: nothing beyond `make check`. It was green as found: 11,148 tests (1 skipped), 99.21 % coverage, `test: green (109.8 s)`. The slowest tests are the 10 s `ROOMY_LIMIT` waits. Disk: the pool's free space fell from 12.5 to 11.9 GB while the instance's folders shrank. This is the third unexplained 0.6 GB fall in F0058's acceptances, which strengthens `planning/later-topics.md` item 2.
   8. Cost: 90 runs, 146.7 min, $29.07, about 89 % of input from the cache. S0002 still stands out ($9.03). S0008 cost $1.87 for 6 runs, with no rework. 13 questions were answered (12 `question`, 1 `attempts_cap`) and the stories waited 0.5 h; S0002 needed the human most and S0008 needed none.

   `make check` was green as found. Only the report changed. The temporary folder `/tmp/tmp.9twh9U4kDm` (the smoke script and a clone) could not be removed: the session's permission check refused both `rm -rf` and `shutil.rmtree`.
