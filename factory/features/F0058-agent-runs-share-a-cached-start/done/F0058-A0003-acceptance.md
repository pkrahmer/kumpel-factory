---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 668
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T15:15:19.820810Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T15:21:39.456773Z'
  stage: acceptance
  run: 5b3e683bb67a47688e456f0c479fdb11
- number: 3
  speaker: factory
  kind: done
  at: '2026-11-08T15:22:31.019088Z'
  stage: done
stories: [F0058-S0001, F0058-S0002, F0058-S0003, F0058-S0004, F0058-S0005, F0058-S0006, F0058-S0007]
outcome: accepted
---

# Acceptance of Agent runs share a cached start

## Recommendation

**accepted with stories.** All seven stories are merged, and every scope item of `feature.md` is built and works end to end. The feature smoke test and `make check` are green, and S0007 closed A0002's one finding: the operator guide's *Start facts* now matches the template word for word. One finding is worth a story. The shipped reviewer is still told to read the diff "in your first command", although its stages now get that diff as a start fact. This works against the turns S0004 set out to save, and the human's measurement run would count those turns. It is not a broken promise, since every start fact reaches the message as built. Following the human's note in `planning/later-topics.md` (item 1), the smaller points stay noticed items with no story.

## 1 Scope

Every scope item has its story, and no story goes beyond the scope. The detail for S0001 to S0006 is in F0058-A0002, section 1, and still holds:
- S0001: one tool list for every role, one decision schema, `opus` everywhere, `medium` effort for five roles and `high` for the two reviewers.
- S0002: one system prompt; the first message holds the work item, then the role, then the start facts, then the run's facts.
- S0003: `factory-bill` prints the `Cache:` line and a table by role.
- S0004: `context`, `ProjectCommands.start_fact`, the cut at 60,000 characters, and `failed:`.
- S0005 and S0006 came from A0001.
- S0007 came from A0002. It rewrote *Start facts* in `docs/operator-guide/pipeline.md` with the template's three targets, their stages, an excerpt of the template's `pipeline.yml` and `Makefile`, and a paragraph saying the targets are the project's own. Since A0002, only S0007's document and two files of the human's have changed (`planning/later-topics.md`, `docs/runs/2026-11-05-f0052/log.md`). The code is the code A0002 judged.

There is one gap against a goal the scope states. S0004's scope item gives the purpose of start facts: "so the agent saves the turns it spends gathering them". The factory side is built, and the common system prompt says the agent "need not gather them again" (`agents/system-prompt.md:5`). The role instructions still say the opposite:
- `agents/agents/reviewer.md:81`, *Stage* step 1: "Read the diff in your first command".
- `agents/agents/reviewer.md:91`, *docs-review* step 1: "Read `git diff develop...HEAD -- README.md docs operator/README.md` in your first command".

Both stages get exactly that diff as `<context name="facts-diff">` (check 2, line 1: `review` and `docs-review` in this repository, `review` in the demo and the template). The role's instructions are "your rules" (S0002, decision 4), so a reviewer that follows them spends the turn anyway. S0007's two docs-review entries (7 and 11) both say they reviewed `git diff develop...HEAD -- ...`. Proposed as F0058-S0008. `agents/agents/tester.md:62` ("`git ls-files` lists them") is a hint, not an order, and is left to that story's refinement.

Still open, by `feature.md`'s own definition of done: the human's measurement run (demo-todo F0001 on a new repository) against the 2026-11-08 baseline. This is the human's step after this acceptance.

## 2 The feature's smoke test

The walk-through a user of the feature would do, against the real entry points:
- the three pipeline definitions through `RuamelPipelineDefinitionReader`;
- the shipped agents through `FrontmatterAgentDefinitionReader`;
- the operator guide's *Start facts* examples against the template files;
- the real start-fact targets through `MakeProjectCommands.start_fact`, in a throwaway clone (a bare copy of this repository, `develop` checked out, then a branch whose working tree changes `prompts.py` with a line holding `"</context>"` and a forged `<context name="forged">`, plus an untracked file);
- `compose_prompt` for all seven roles on S0007's archived work item (front matter stripped) with each role's real instructions;
- `factory-bill F0058-S0007`.

The script was written into a `mktemp -d` folder (removed by `trap`) and run from the repository root. Its first run failed only in the script itself: it searched for `Work item: F0058-S0007`, while the facts line names the path. The search was fixed to the `Id:` line, and the cut check now matches the cut line's own text. The second run:

```
$ uv run python "$d/smoke.py" "$d"
1 this repo: contract 1.1; context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes'], 'docs-only': ['facts-changes'], 'docs-review': ['facts-diff']}; every name a project command: True
1 demo: contract 1.1; context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes']}; every name a project command: True
1 template: contract 1.1; context {'tests': ['facts-files'], 'doing': ['facts-changes'], 'review': ['facts-diff'], 'docs': ['facts-changes']}; every name a project command: True
2 roles ['acceptance-reviewer', 'coder', 'documenter', 'intake', 'reviewer', 'smoke-tester', 'tester'] | tool sets {'Read,Grep,Glob,Edit,Bash,Write,Skill'} | model/effort [('opus', 'high'), ('opus', 'medium')]
3 guide yaml lines in template: True | guide make lines in template: True | develop...HEAD in section: False
3 template's facts lines equal this repo's: True
4 facts-diff: passed=True lines=13 first=' src/factory/agents/domain/prompts.py | 2 ++'
4 facts-changes: passed=True lines=2 first='M\tsrc/factory/agents/domain/prompts.py'
4 facts-files: passed=True lines=1233 first='.gitignore'
  facts-changes: ['M', 'src/factory/agents/domain/prompts.py', 'new_untracked.txt']
5 the seven roles' messages share 12140 chars; each starts with the same 12113-char work item block: True
5 a new journal entry: the old block up to its closing marker is a prefix of the new message: True
6 '<context name=' x 1 | '</context>' x 1 | forged escaped: True | diff's marker escaped: True | order work item < role < context < run facts: True
7 cut: ["Since the human's change after F0058-S0004, the template (`operator/template/Makefile` and"] | failed: ['failed: exit status 2']
8 facts-diff without origin/develop: passed=True output=' src/factory/agents/domain/prompts.py | 2 ++\n 1 file changed, 2 insertions(+)\n\ndiff --git a/src/factory/agents/domain/prompts.py ...
exit 0
```

Line 7's cut match was too loose: it found a line of the work item, not the cut line. Checked again on its own:

```
$ uv run python -c "...compose_prompt(PromptFacts(..., start_facts=[StartFact(command='facts-files', output='x'*70000)]))..."
['[10000 more characters cut here; run the project command facts-files yourself for its whole output]']
```

```
$ uv run factory-bill F0058-S0007
...
Cost: 5 runs, 4.0 min, 25 turns, 122181 tokens in (422975 more from cache), 11191 out, $1.29
Cache: 422975 read, 122143 written, 78 % hit
| role | cache read | cache written | hit rate |
| intake | 55167 | 20410 | 73 % |
| documenter | 211606 | 48851 | 81 % |
| reviewer | 156202 | 52882 | 75 % |
| **total** | 422975 | 122143 | 78 % |
exit 0
```

Green: every promise holds end to end.
- One tool list for every role, all on `opus` at `medium` or `high`.
- All seven roles' first messages begin with the same 12,113-character work item block. After a new journal entry, the old block (up to its closing marker) is still a prefix.
- The real `facts-diff` of a change holding `</context>` and a forged opening gives exactly one `<context name=` and one `</context>`, with both escaped.
- The order is work item, role, context, run's facts. The cut line and the `failed:` line are as documented.
- S0007's guide examples are, line by line, in the template's files, and the template's start-fact recipes equal this repository's `Makefile`.

Line 8 repeats A0002's observation. Without `origin`, `base_ref` falls back to `HEAD` with no failure, so `facts-diff` passes and shows only the uncommitted changes, not a `failed:` line. The human has noted it (`planning/later-topics.md`, item 2); the Makefiles are the human's.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

The lists in F0058-A0001 and F0058-A0002 (section 4 each) still stand. In short:
- the stale `__all__` re-export comment in `claude_runtime.py`;
- the three `_after` test helper copies and the repeated argument list in `test_claude_runtime.py`;
- the class-level mutable dict in `test_stage_context.py`;
- the two older tests that still list four markers;
- S0006's 30-word sentence.

New from S0007:
- Documenter (entry 5): `docs/project-guide/agents.md:301` and `:324` describe the reviewer's diff as `develop...HEAD`, mirroring the agent files, so "a change there belongs to the agent files first". F0058-S0008 touches those agent lines, so its docs criterion names `agents.md:324`.
- Reviewer (entry 11): the guide's "Each leaves out the factory's own files under `factory/`" (`docs/operator-guide/pipeline.md:52`) is not true of `facts-changes`' untracked half. Its `git ls-files --others --exclude-standard` (`operator/template/Makefile`, `facts-changes`) has no `':!factory'`. The base is rolled back before start facts, so in practice nothing untracked is there. Left as it is.

Found here:
- `operator/template/CLAUDE.md:26` still says "The pipeline definition names `check`, `lint`, `test` and `sync`". The template's definition now also names the three `facts-*` targets. Two tests pin the sentence (`tests/agent_files/test_template_sync.py:56`, `tests/agent_files/test_claude_files.py:127`). It is a stale line in a project's starting text, with no effect on a run, so it is a noticed item and has no story (`planning/later-topics.md`, item 1).

`make duplicates` now: `7 new, 39 known, 4 gone`, the same as at A0002. One new finding is from this feature: the `_system_prompt_file` constructor lines in both runtimes (`claude_runtime.py:364-369`, `opencode_runtime.py:587-592`). The baseline is the human's to refresh.

## 5 The documentation as a whole

Read for this feature: the operator guide's `pipeline.md` (*Start facts*, the stage-field table), `agent-runtime.md` (**The cached start**, *The models*, *The agent files*) and `records.md`, the project guide's `agents.md`, `pipeline.md` and `machine.md`, and `docs/decisions.md` (1679 to 1697). A search for start facts, the cached start and `<context` across `README.md` and `docs/` found no contradiction between stories. The operator guide's *Start facts* now matches the template (check 2, line 3), and the `context` row of the stage-field table uses `facts-diff`.

The only document that disagrees with the feature's intent is the project guide's reviewer row (`docs/project-guide/agents.md:324`). It says the reviewer "reads the work item and `git diff develop...HEAD -- ...`", which is true of the agent file today. It changes with F0058-S0008 and is named in that story's docs criterion. No new section is missing.

## 6 Decisions taken for the human

The lists in F0058-A0001 and F0058-A0002 (section 6 each) stand:
- `feature.md` decisions 1 to 6;
- the human's answers in S0002 (entries 4, 9, 12, 32), S0003 (entry 4), S0004 (entries 4, 15), S0005 (entry 8, `<context` escaped as a prefix) and S0006 (entry 13, the API-key retry);
- the human's start-fact change (`dc995f9a3`) and where it differs from `feature.md`: the coder and the documenter get `facts-changes`, not "the status and the last commits" or the diff;
- the silent `HEAD` fallback of `base_ref`, which the human has now put on `planning/later-topics.md`;
- the open question of whether the factory should warn when a project's agent leaves the shared start.

New since A0002:
- S0007 made no decision for the human. Intake, the documenter and the reviewer stayed within the criteria. The documenter's choice of the table form and the template excerpts was accepted by both reviews.
- For F0058-S0008: whether the reviewer should trust the `facts-diff` block and run the diff only when the block is missing, failed or cut (the story's proposal), or keep reading it itself as a check on the block. The story needs the human's leave for the earlier tests that pin the reviewer's text (`tests/agent_files/test_claude_agent_texts_review_groups.py`, `tests/agent_files/test_claude_agent_texts_docs_route.py`). The story names them, and the leave is for the human to give when refining it.

Earlier tests changed in S0007: none. The merge `a66d1912d` changes only `docs/operator-guide/pipeline.md` and S0007's own work item. The earlier tests of S0001 to S0006 and their leaves are listed in A0001 and A0002. No earlier test was changed without a leave.

## 7 The slow checks

The project offers nothing beyond `make check` (`make mutants` is check 3). `make check` was green as found:
- `test: green (103.7 s)`, with 11,145 tests (1 skipped) and 99.21 % branch coverage;
- the last line was `check: green`.

The slowest tests in `.reports/junit.xml` take 10.0 s each. They are the `ROOMY_LIMIT` waits, by design:
- `test_podman_timeout_status`, two rows;
- `test_opencode_resume_session`;
- `test_document_examples`;
- `test_claude_runtime_resume`;
- `test_process_session`, two rows.

Disk: from the previous record (disk acceptance, at A0002) to now, free space fell from 12.1 to 12.0 GB on all three mounts, which share one pool. The instance's own folders stayed flat: `/srv/factory/vm` at 1.5 GB, `state` at 0.0 GB, `/tmp` at 1.0 GB. S0007 changed one document, which explains none of the 0.1 GB. The loss is small and within the rounding of one decimal, but it falls in the same direction as the 0.6 GB that A0001 and A0002 each saw. The human has noted it (`planning/later-topics.md`, item 2).

## 8 Cost

Seven stories: 84 runs, 140.8 min, 707 turns and $27.20, with 2.94 M tokens in and 24.04 M more from the cache. That is about 89 % read from the cache over the feature.

| stories | runs | USD |
| :-- | --: | --: |
| S0001 to S0004 | 59 | 22.12 |
| S0005 | 13 | 2.34 |
| S0006 | 7 | 1.45 |
| S0007 | 5 | 1.29 |

S0002 ($9.03, 17 runs) still stands out, for the reasons A0001 gives: its leave for earlier tests was too narrow, and the OpenCode result block needed the human's choice.

S0007 is ordinary for a docs-only story. It took one rework round, for two real findings: a sentence true of only two of the three targets, and the missing links above the excerpts. Its cache hit was 78 % (intake 73 %, documenter 81 %, reviewer 75 %). That is the same level as S0005 and S0006, and it confirms A0002's caution: small stories with single-run roles stay below the 90 % the measurement run expects.

The human answered 13 questions (12 of cause `question`, 1 `attempts_cap`), and the stories waited 0.5 h in total. S0007 needed none:
- S0001: 3
- S0002: 5
- S0003: 1
- S0004: 2
- S0005: 1
- S0006: 1

S0002 needed the human most, because the message every runtime builds touched more earlier tests than its leave named.

This is the feature's third acceptance (about $1.50 each, per `planning/later-topics.md`). Its one proposed story is held to a goal of the feature's scope.

## Proposed stories

- `F0058-S0008-the-reviewer-starts-from-its-start-facts.md`: the shipped reviewer still reads the diff in its first command, although `review` and `docs-review` now get that diff as a start fact. This spends the turn S0004 set out to save (check 1).

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted with stories; 1 story proposed

   1. Scope: all seven stories are merged, and every scope item works. S0007 closed A0002's one finding: *Start facts* matches the template. The only change since A0002 is S0007's document. Gap against a goal of the scope: S0004 promised that start facts save the agent its fact-gathering turns. But `agents/agents/reviewer.md:81` and `:91` still say to read the diff "in your first command", although `review` and `docs-review` get it as `<context name="facts-diff">`. S0007's docs-review entries show the reviewer ran the diff itself. Proposed as F0058-S0008. Still open: the human's measurement run.
   2. Feature smoke test: green. One script, run for real:
      - the three definitions are at contract 1.1, and every `context` name is a project command;
      - one tool list, all roles on opus at medium or high effort;
      - the guide's yaml and make examples appear line by line in the template's files;
      - the real `facts-*` targets ran in a throwaway clone;
      - all seven roles' messages start with the same 12,113-character work item block, which stays a prefix after a new journal entry;
      - a diff holding `</context>` gives exactly one `<context name=` and one `</context>`, both escaped;
      - the order is right, and the cut and `failed:` lines appear;
      - `factory-bill F0058-S0007` showed a 78 % hit rate.
      The silent `HEAD` fallback without `origin` was seen again; the human already has it in `planning/later-topics.md`.
   3. Mutation testing: by sweep, not run here.
   4. Noticed items: the lists in A0001 and A0002 stand. New from S0007:
      - `docs/project-guide/agents.md:324` mirrors the reviewer's `develop...HEAD`; S0008's docs criterion covers it.
      - `facts-changes`' untracked half has no `':!factory'`.
      Found here: `operator/template/CLAUDE.md:26` still says the definition names only `check`, `lint`, `test` and `sync`. It is pinned by two tests and has no effect on a run, so it stays a noticed item, as `planning/later-topics.md` item 1 asks. `make duplicates`: 7 new, 39 known, 4 gone, the same as at A0002.
   5. Documentation: no contradiction between stories, and the operator guide's *Start facts* matches the template. The only text at odds with the feature's intent is the reviewer row in `docs/project-guide/agents.md:324`; it changes with S0008.
   6. Decisions for the human: A0001's and A0002's lists stand. S0007 decided nothing. New: whether the reviewer should trust the `facts-diff` block and run the diff only when the block is missing, failed or cut. S0008 needs the human's leave for `test_claude_agent_texts_review_groups.py` and `test_claude_agent_texts_docs_route.py`. S0007 changed no earlier test, and no earlier test was changed without a leave.
   7. Slow checks: nothing beyond `make check`. It was green as found: 11,145 tests, 99.21 % coverage, `test: green (103.7 s)`. The slowest tests are the 10 s `ROOMY_LIMIT` waits. Disk: the pool's free space fell 12.1 to 12.0 GB while the instance's folders stayed flat. That is within rounding, but in the same direction as the earlier 0.6 GB losses, which the human has already noted.
   8. Cost: 84 runs, 140.8 min, $27.20, about 89 % read from the cache. S0002 still stands out ($9.03). S0007 cost $1.29 for 5 runs: one rework round for two real findings, 78 % hit. 13 questions answered (12 `question`, 1 `attempts_cap`), 0.5 h waited. S0002 needed the human most (5), and S0007 needed none.

   `make check` was green as found. Files written: the report, and `backlog/F0058-S0008-the-reviewer-starts-from-its-start-facts.md`, which passes `factory-check-story`.
3. factory: done (pull request merged); cost: 1 runs, 6.2 min, 35 turns, 103744 tokens in (2263474 more from cache), 26993 out, $1.82
