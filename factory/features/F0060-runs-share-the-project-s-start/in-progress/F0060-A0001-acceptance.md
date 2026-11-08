---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 681
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T22:01:32.604579Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T22:10:21.341700Z'
  stage: acceptance
  run: 42ca702dc6a240adbcfec45e9b5cbb59
stories: [F0060-S0001, F0060-S0002, F0060-S0003]
outcome: null
---

# Acceptance of Runs share the project's start

## Recommendation

**accepted with stories.** The three stories together build what `feature.md` promised: the feature's smoke test shows all seven shipped roles getting one identical system prompt (orientation, the shared `## Rules`, then the project's `CLAUDE.md` in its `<project-instructions>` block), first messages without the rules or `CLAUDE.md`, both Claude switches set, opencode left alone, and a reviewer able to send test-only findings to the tester. `make check` is green on `develop` as I found it. The findings are worth stories but none breaks a promise: agent texts frozen by checksums cost four of the six questions the human answered, the reviewer's `## Role` still names only `doing` for sending back, and the decision log has no entry for the move of the rules. One step of the feature's "done when" is the human's and is still open: `review` does not offer `tests` yet in any of the three pipeline definitions, so the new route stays dormant until that commit lands.

## 1 Scope

No story is missing and no story is outside the scope. Each scope line has its story: the rules in the system prompt (S0001: `agents/system-prompt.md`, `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`, the seven `agents/agents/*.md` without `## Rules`); the root `CLAUDE.md` in the Claude run's system prompt with Claude Code's loading switched off, and the five-minute cache (S0002: `SWITCHES`, `_project_instructions` and `_instructions_text` in `src/factory/agents/adapters/claude_runtime.py`); the reviewer's route to the tester (S0003: step 4 of the reviewer's `## Stage`, the tester's step 0, R12). The out-of-scope items stayed out: no story text in the system prompt, opencode unchanged (`opencode_runtime.py` untouched), no nested `CLAUDE.md` files, nothing in the cost records.

Not reached yet, and the human's own work (`feature.md`, *The human's changes*):
- On `develop`, `review` still reads `next: [docs, doing]` in `factory/pipeline.yml:38`, `operator/template/factory/pipeline.yml:25` and `demo/todo-service/project/factory/pipeline.yml:26`. The test expectation `["docs", "doing"]` in `tests/agent_files/test_claude_agent_texts_docs_slip.py:57` is still the old one. Until that commit, the reviewer never sees `tests` among its allowed decisions, and the 58-of-65 relay the Goal names keeps happening.
- The `CLAUDE.md` change after S0001 is made (its first paragraph names `agents/system-prompt.md`).
- Instance `vm`: this acceptance run itself still got `## Rules` in its `<role-instructions>` block, and its `CLAUDE.md` came through Claude Code's own loading. The instance therefore still runs the agent home and code from before F0060, as `feature.md` foresees ("when it moves to the promoted F0060"). The trial lines in `factory.local.env` and the check of `ephemeral_5m` writes in the next story's transcripts are still to come.

Also outside the code: the system prompt is now about 28,800 characters with this repository's `CLAUDE.md`. Every shipped role runs on `opus`, but the reviewer and the acceptance reviewer run at `effort: high` and the other five at `medium`, and `docs/operator-guide/agent-runtime.md:351` says a change of effort cuts the cache. So the shared start is shared within each of the two effort groups, not across all seven roles. The Goal's 13 % was measured on real runs, so this is already priced in. It is a note, not a finding.

## 2 The feature's smoke test

A user's walk-through of the feature's purpose: the seven shipped roles run through the real `ClaudeCodeRuntime`, with the real agent home `agents/`, the real `compose_prompt`, and a checkout holding this repository's real `CLAUDE.md`. `claude` is the tests' stand-in, which records its arguments, environment and files. Then one coder run goes through the real `OpencodeRuntime`, and the three pipeline definitions are read through the real `RuamelPipelineDefinitionReader`.

Command (from the checkout's root; both scripts were kept in a `mktemp -d` folder that removed itself):

```bash
PYTHONPATH=tests uv run python "$d/feature_smoke.py"      # Claude part (the opencode part of this file failed, see below)
PYTHONPATH=tests uv run python "$d/feature_smoke_oc.py"   # opencode part and the review route
```

The Claude part does this for each name of `FrontmatterAgentDefinitionReader(Path("agents")).names()`:
- `compose_prompt(PromptFacts(..., role=role, role_instructions=agent.instructions))`;
- `ClaudeCodeRuntime(stand-in, state, system_prompt_file=agents/system-prompt.md).run(AgentRunRequest(..., working_directory=work))`.

It then compares the seven `--append-system-prompt-file` files and the seven `-p` messages. The opencode part runs `OpencodeRuntime(stand-in, ..., system_prompt_file=agents/system-prompt.md)` for the shipped coder and reads the agent `prompt` of its configuration.

Output (uv's `Bytecode compiled` lines removed):

```
roles: ['acceptance-reviewer', 'coder', 'documenter', 'intake', 'reviewer', 'smoke-tester', 'tester']
claude calls: 7
instructions files identical across roles: True
system prompt chars: 28769 (~ 7192 tokens)
system prompt '## Rules' headings: 1
system prompt rules R1..R15 once each: True
system prompt carries CLAUDE.md in its block: True
system prompt names review → tests: True
  acceptance-reviewer  first message chars=  8187 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
  coder                first message chars=  5350 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
  documenter           first message chars=  8333 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
  intake               first message chars=  5867 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
  reviewer             first message chars= 10764 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
  smoke-tester         first message chars=  3938 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
  tester               first message chars=  6442 rules_heading=False R14_line=False claude_md_in_message=False MDS=1 TTL=5m
opencode takes system_prompt_file: True
Traceback (most recent call last):
  ...
factory.shared.domain.errors.AgentRuntimeError: agent runtime failed: the opencode runtime has no model for opus: set FACTORY_OPENCODE_MODELS
```

The traceback is a fault in my script, not in the factory: I gave the opencode runtime a model map without `opus`, and the error is the one the runtime promises. With the map fixed (second script):

```
opencode agent prompt holds '## Rules': True | R15 line: True | <project-instructions>: False | CLAUDE_CODE_DISABLE_CLAUDE_MDS in env: False
factory/pipeline.yml: review allows ['docs', 'doing', 'question']
operator/template/factory/pipeline.yml: review allows ['docs', 'doing', 'question']
demo/todo-service/project/factory/pipeline.yml: review allows ['docs', 'doing', 'question']
factory/pipeline.yml with the human's change: review allows ['docs', 'doing', 'tests', 'question']
reviewer.md step 4 (findings that need only tests -> `tests`): True
tester.md step 0 (after the reviewer's result): True
```

Result: **green** for what the stories built. Under Claude Code every role's system prompt is byte for byte the same and carries the rules and `CLAUDE.md`; no first message carries either; both switches are set; opencode gets the rules and no project block. The route to the tester is in the agent texts and loads in a definition, but the shipped definitions do not offer it yet (the human's open change, check 1). The movement `review → tests` and its round count are pinned by `tests/agent_files/test_review_to_tests_agent_files.py::test_a_review_decision_tests_moves_to_the_tester_and_counts_a_round`, which `make check` ran green. The cache effect itself, a first request that reads more than 6,683 tokens, can be seen only in a real instance's transcripts once `vm` moves to F0060.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- **Agent texts frozen by checksums** (S0001 entries 5 and 9, S0003 entries 10, 15 and 22). S0001 added crc32 pins of every agent file's sections (`PARTS_BEFORE` in `tests/support/shared_rules_support.py`) and a word-for-word copy of the rules (`RULES_BEFORE`). `test_the_rest_of_the_reviewer_body_is_unchanged` (`tests/agent_files/test_claude_agent_texts_review_groups.py`, from F0048) rebuilds an earlier body through a growing `.replace` chain. Every story that touched an agent text stopped on them: S0003 needed three leaves (entries 4, 11, 16), two of them for these pins. Another pin, the written-out `SWITCHES` dict in `tests/agents/adapters/test_claude_runtime.py`, cost S0002 its first question (entry 7). → **F0060-S0004**.
- **The reviewer's `## Role` still names only `doing` for sending back** (S0003 reviewer entries 22 and 30, coder entries 24 and 28). The S0003 coder also chose a new step 4 rather than editing step 3 because step 3 was pinned (entry 10). → **F0060-S0005**.
- **The reviewer's ways out are not in the operator guide**; the smoke tester's are (S0003 documenter, entry 32). → F0060-S0005's docs criterion.
- **Orientation repeats "apply to every agent in every stage"** (S0001 coder, entry 11): deliberate, since criteria 4 and 5 each ask for one of the two sentences. No story.
- **`make documents` timed out on a slow package index** (S0001 entries 23 to 34, two stalls and an `attempts_cap`). The human already holds the fix as F0061 (`F0061-S0001-document-examples-use-the-check-s-uv-cache.md` in its backlog). No story from here.
- **The trial `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` lines on the instances are now redundant** (S0002 documenter, entry 33). This is the human's own change in `feature.md`. No story.
- **Test helpers rebuilt locally**: `_on_the_host` and `_in_a_container` in `tests/agents/adapters/test_claude_runtime_project_instructions.py:121-136` rebuild the runtime instead of using the module's `_runtime` (S0002 reviewer notes, entries 24 and 31). `_sentences` in `test_shared_rules_system_prompt.py:59` is a variant, not a copy (S0001 entry 21). Too small for a story.
- **The R12 line wrap in `prompts.py:121-123` is uneven** (S0003 entries 20 and 30). Cosmetic; no story.
- **`make duplicates` stands at `7 new, 39 known, 4 gone`**, the same in every coder entry of F0060 and in 14 of 16 such lines of F0058 and F0059. The drift predates this feature: three line shifts of known `claude_runtime`/`opencode_runtime` and `hand_over`/`acceptance` pairs, and four dead-code findings in `folder_readmes.py` and `cost_records.py`. Nobody owns refreshing `security/duplicates-baseline.txt`; that is the human's file. No story.

## 5 The documentation as a whole

I read `docs/operator-guide/agent-runtime.md` (*The project's `CLAUDE.md` under Claude Code*, *The agent files*, *A project's own agents*, *The cached start*, *The shipped agents and settings*), `docs/operator-guide/pipeline.md` (*More than one route*), `docs/project-guide/agents.md`, `docs/decisions.md` and `README.md`. What the three documenters wrote agrees with itself and with the code. `## Rules` is described in one place only, and the five `SWITCHES` are listed the same way in both guides. Findings:
- **No decision entry for the move of the shared rules.** The S0002 entry covers `CLAUDE.md` only, and S0001 changed only the log's introduction. The F0058 entry *The role's instructions follow the work item in the first message* (`docs/decisions.md:1688`) still says "The system prompt says that the role's instructions are the agent's rules", which the system prompt no longer says. → **F0060-S0006**.
- **No decision entry for the route from review to the tester.** Its reason is in `feature.md` (58 of 65), its rejected alternative in decision 5. → F0060-S0005's docs criterion.
- **A sentence that the human's own change will make false.** `docs/operator-guide/pipeline.md:98` says "The template's `review` lists only `[docs, doing]`", which stops being true with the human's commit after S0003. → F0060-S0005, which starts after that commit. The human could also fix the sentence in the same commit.
- No example broke: `make guides` and `make documents` were green at each docs stage of the feature (S0003 entry 32: `documents ok (59.3 s)`).

## 6 Decisions taken for the human

To accept or revisit:
1. `feature.md` decisions 1 to 6, as written there (the leave for S0001; the fallback `SYSTEM_PROMPT` equals the file; only the root `CLAUDE.md`; five-minute cache as a switch, not a setting; `review → tests` counts a round and a mixed review sends all findings to `doing`; the leave for S0003).
2. S0001, coder entry 7: the orientation says the role's instructions "add to these rules: follow them with the same weight". The coder rejected "follow them with the same weight as these rules" because it broke `test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is`. The wording followed a test, not a choice of meaning.
3. S0002, human entry 27: a root `CLAUDE.md` that is a symbolic link is not followed. A project whose `CLAUDE.md` links to `AGENTS.md` now runs with no project instructions, and nothing reports it (`docs/operator-guide/agent-runtime.md:44` says so). A preflight warning would make this visible. I make no proposal; it is a product question.
4. S0002, reviewer entry 31: the Description was corrected to name the link and the directory cases.
5. S0002, coder entry 18: `_block` in `prompts.py` became the public `block`, reused by the Claude adapter.
6. S0003, coder entries 10 and 20: the reviewer's rule is a new step 4, not an edit of step 3, because step 3 was pinned. Human entry 16 widened the leave for the rest of S0003 to "any earlier test whose only failure is this story's change of R12, the reviewer's `## Stage` or the tester's `## Stage`".
7. S0001 entries 27 and 32: retries chosen by the human while the package index was slow; the fix is F0061.

Earlier tests changed, each with its leave (all named by the reviewers; none without a leave):
- S0001, under `feature.md` decision 1 ("any other test whose only failure is this move" for the last four):
  - `tests/agent_files/test_claude_agent_refusal.py`
  - `tests/agent_files/test_claude_agent_skills.py`
  - `tests/agent_files/test_claude_agent_texts.py` (also the standing leave, for `headings` and `WITHOUT_ROLE`)
  - `tests/agent_files/test_claude_agent_texts_check_red.py`
  - `tests/agent_files/test_claude_agent_texts_docs_slip.py`
  - `tests/agent_files/test_claude_agent_texts_review_groups.py`
  - `tests/agent_files/test_claude_settings_git.py`
  - `tests/agent_files/test_first_message_agent_files.py`
  - `tests/agent_files/test_shipped_agents_r14.py`
  - `tests/support/shipped_agents.py`: the standing leave.
- S0002: `tests/agents/adapters/test_claude_runtime.py`, the human's leave in entry 8 (two switches added to the local `SWITCHES` dict).
- S0003:
  - `tests/agent_files/test_claude_agent_texts_docs_slip.py`: the human's leave in entry 4 (`REWORK_RULE`).
  - `tests/support/shared_rules_support.py`: entries 4, 11 and 16 (the R12 entry, and the reviewer and tester `Stage` checksums).
  - `tests/agent_files/test_claude_agent_texts_review_groups.py`: entries 11 and 16 (two `.replace` mappings).
  - `tests/agent_files/test_claude_agent_texts_docs_route.py`: entry 16 ("steps 1 to 4").
  - `tests/pipeline/application/test_docs_route.py` and `tests/support/two_routes_support.py`: the standing leave (helpers moved as `decide`, `STAGE_WRITES`, `EVERY_TARGET_MAKEFILE`).

## 7 The slow checks

The project offers nothing beyond `make check` but `make mutants` (check 3); no image scan or SBOM. `make check` as found: `check: green`, `test: green (139.8 s)`, coverage 99.21 %. In `.reports/junit.xml` (11,001 tests, 1,253 s summed over the workers):
- The slowest test is `tests.guards.test_documents_marker::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other` (30.9 s). The next are the time-limit tests at their `ROOMY_LIMIT` of 10 s.
- The feature's own tests take 9.6 s together. The slowest of them is `test_a_review_decision_tests_moves_to_the_tester_and_counts_a_round[third-past-the-cap]` (6.5 s), a world with a real git remote.

Disk: at the start, `/srv/factory/vm` had 9.1 GB free with 1.5 GB used; now it has 8.8 GB free with 1.5 GB used. `/srv/factory/vm/state` (0.0 GB used) and `/tmp` (2.1 GB used) are unchanged too. The three paths share one filesystem, and none of them grew, so the 0.3 GB of free space went elsewhere on it. The likely places are the ZFS datasets and snapshots of the stage runs, or podman's images and containers. The feature changed only text and Python, which cannot explain 0.3 GB. I cannot name the consumer from here; the operator's `zfs list -t all` and `podman system df` would.

## 8 Cost

Cost of the stories: 46 runs, 84.4 min, 327 turns, $14.62:

| Story | Runs | Minutes | Cost | Round |
|---|---|---|---|---|
| S0001 | 15 | 46.8 | $5.68 | 1 |
| S0002 | 16 | 20.4 | $4.38 | 2 |
| S0003 | 15 | 17.3 | $4.56 | 1 |

S0001 stands out in time. Four docs runs (entries 23 to 34) waited on `make documents`, which timed out twice on a slow package index: two stalls, then an `attempts_cap` that the human retried. That cost was the machine's, not the story's (F0061 holds the fix).

Every story also shows the relay that S0003 removes, a coder run that changed nothing and passed the work item to the tester: S0001 entries 15 and 19, S0002 entry 10, S0003 entry 13.

Human interventions: 7 questions answered, 6 of them `question` and 1 `attempts_cap`, with 0.4 h waited in all:

| Story | Answers | Entries | Cause |
|---|---|---|---|
| S0001 | 2 | 27; 32 (`attempts_cap`) | documents check on the slow index |
| S0002 | 2 | 8; 27 | a pinned earlier test; a criterion outside the coder's write paths |
| S0003 | 3 | 4, 11, 16 | leaves for pinned agent texts |

S0003 needed the human most. All three of its questions asked leave to change earlier tests that pin agent texts word for word or by checksum, which is why F0060-S0004 is proposed. Counting S0002's entry 7, four of the six questions were such leaves.

## Proposed stories

- `backlog/F0060-S0004-agent-texts-are-not-frozen-by-checksums.md`: retires the crc32 and whole-text pins of the agent files and the rules, which cost four of the six questions, and adds a guard against new ones.
- `backlog/F0060-S0005-the-reviewer-s-role-names-its-route-to-the-tester.md`: the reviewer's `## Role` names `tests` as step 4 does. The operator guide lists the reviewer's ways out and the template's `review` as it stands, and the decision log records the route. It starts after the human's `next` change.
- `backlog/F0060-S0006-the-decision-log-records-the-shared-rules-in-the-system-prompt.md`: the missing decision entry for S0001's move, and the F0058 sentence it supersedes. Docs route.

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted with stories; 3 stories proposed

   1. Scope: every scope line has its story, and none of them goes outside the scope. One step of "done when" is still open and is the human's: `review` still offers only `[docs, doing]` in all three pipeline definitions, so the route to the tester is unused until that commit. The instance `vm` also still runs the agent home from before F0060: this run got `## Rules` in its role instructions.
   2. Feature smoke test: green. Seven shipped roles ran through the real `ClaudeCodeRuntime` with the real agent home and `CLAUDE.md`.
      - All seven got the same system prompt: the rules once each, R1 to R15, then the project's `CLAUDE.md` in its block.
      - No first message held the rules or `CLAUDE.md`, and every call had `MDS=1` and `TTL=5m`.
      - opencode got the rules and no project block.
      - The definition with `tests` added loads. My first opencode attempt failed because of a fault in my script (a model map without `opus`), not in the factory; the report pastes both runs.
   3. Mutation testing: by sweep, not run here.
   4. Noticed by the stories:
      - Agent texts are pinned by crc32 and word for word, which cost four of the human's six questions (→ S0004).
      - The reviewer's `## Role` names only `doing` (→ S0005).
      - `make documents` timed out on a slow package index; F0061 already holds the fix.
      - Smaller test-helper notes and a uneven line wrap; no story.
      - The `make duplicates` drift ("7 new") predates F0060.
   5. Docs: they agree with themselves and with the code. Three gaps:
      - No decision entry for the shared rules moving into the system prompt, and the F0058 entry's sentence on the system prompt is out of date (→ S0006).
      - No decision entry for `review → tests` (→ S0005).
      - `docs/operator-guide/pipeline.md:98` will be false once the human changes the template (→ S0005).
   6. Decisions for the human: `feature.md` decisions 1 to 6, the "add to these rules" wording chosen to keep an earlier test passing, a `CLAUDE.md` that is a link running silently without instructions, step 4 placed because step 3 was pinned, and the widened leave of S0003 entry 16. Every earlier test changed under a named leave.
   7. Slow checks: nothing beyond `make check`, which is green (test 139.8 s, coverage 99.21 %). The slowest test is the documents-marker guard (30.9 s); the feature's tests take 9.6 s. Free disk fell by 0.3 GB while none of the three named paths grew, which the text-only changes cannot explain; ZFS snapshots or podman images are the likely cause.
   8. Cost: 46 runs, 84.4 min, $14.62. S0001 took the most time (46.8 min) because of four docs runs on the slow index. S0003 needed the human most, three times, every time for leave on pinned agent texts. 7 answers in all (6 questions, 1 `attempts_cap`), 0.4 h waited. Each story still shows the coder relay that S0003 removes.
