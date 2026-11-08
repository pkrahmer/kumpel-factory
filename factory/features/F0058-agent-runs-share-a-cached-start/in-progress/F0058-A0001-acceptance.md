---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 663
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T13:57:14.326980Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-08T13:59:55.490549Z'
  stage: acceptance
- number: 3
  speaker: factory
  kind: started
  at: '2026-11-08T13:59:57.047705Z'
  stage: acceptance
- number: 4
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T14:07:15.711640Z'
  stage: acceptance
  run: 1fdf05f031d947f9a0f376e6a1f7ce1e
stories: [F0058-S0001, F0058-S0002, F0058-S0003, F0058-S0004]
outcome: null
---

# Acceptance of Agent runs share a cached start

## Recommendation

**accepted with stories.** The four stories together deliver every scope item of `feature.md`: one tool list, one decision schema and one system prompt for every role, intake and the documenter on Opus at medium effort, the first message ordered work item → role → start facts → run's facts, the bill's cache figures, and the stage key `context`. The feature smoke test is green and `make check` is green. Two findings are worth stories, neither a broken promise: the `<context>` markers are not escaped, so a start fact holding `</context>` (the diff of `prompts.py` itself) closes its block early; and the operator guide never says what a project's own agent must keep to share the cached start. The feature's goal is not yet reached in practice: the human's change after S0004 (start-fact targets, `context` lines, contract 1.1) is not on `develop`, and the measurement run is still due.

## 1 Scope

Every scope item has its story, and no story goes beyond the scope:
- S0001: all seven agent files have `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]` and `model: opus`; five roles are at `medium` effort, the reviewer and the acceptance reviewer at `high` (decision 3). `_DECISION_SCHEMA` in `src/factory/agents/adapters/claude_runtime.py:163` is one constant, and `decision` is a string. `_answered` still refuses a decision outside the allowed ones.
- S0002: `agents/system-prompt.md` equals the built-in `SYSTEM_PROMPT` (`src/factory/agents/domain/prompts.py:31`). `compose_prompt` builds `<work-item>`, then `<role-instructions role=…>`, then the facts. The round line names the cap. OpenCode follows the same order, with its result block at the end.
- S0003: `factory-bill` prints a `Cache:` line and a table by role.
- S0004: the stage key `context`, `ProjectCommands.start_fact`, the 60,000-character cut, the `failed:` line, the lease rule, contract 1.1 and `RECORDS_CONTRACT` 4.5.

Open, and the human's own work rather than a gap in the stories: *The human's changes, after S0004's merge* are not on `develop`. `factory/pipeline.yml`, `demo/todo-service/project/factory/pipeline.yml` and `operator/template/factory/pipeline.yml` are still at `contract: "1.0"` with no `context`. The `Makefile` has no start-fact targets. This run's own message holds no `<context>` block. Until that change lands, S0004 saves no turns, and the measurement run would measure S0001 to S0003 only.

## 2 The feature's smoke test

A user's walk through the feature: the shipped agents through the real reader, the first messages of all seven roles on a real work item (S0002's archived file), the launch arguments of two stages, a pipeline definition with `context` through the real YAML reader, a message with start facts, and then `factory-bill` on archived stories. The script was written to a `mktemp -d` directory and run from the repository root:

```
$ uv run python -I "$d/smoke.py"
1 roles: acceptance-reviewer, coder, documenter, intake, reviewer, smoke-tester, tester
  tools sets: {'Read,Grep,Glob,Edit,Bash,Write,Skill'}
  model/effort: [('opus', 'high'), ('opus', 'medium')]
  system prompt file == built-in: True
2 shared start of all roles' first messages: 70393 chars; ends with </work-item>: True
  after a new journal entry the old work-item part is a prefix: True
3 decision schema same across stages: True | tools same: True | decision: {'type': 'string', 'description': "one of the allowed decisions that the run's message names"}
4 pipeline with context loads: ['diff']
  unknown context name refused: PipelineDefinitionInvalid
5 context blocks (diff then failed status):
  <context name="diff">
  +CONTEXT_CLOSE = "</context>"
  +x
  </context>
  
  <context name="status">
  failed: exit 2
  </context>
  
  
  '</context>' occurrences in message: 3 for 2 blocks
exit 0
$ uv run factory-bill F0058-S0002 | tail -12
Cost: 17 runs, 49.7 min, 249 turns, 854719 tokens in (11001115 more from cache), 127919 out, $9.03
Cache: 11001115 read, 854265 written, 93 % hit

| role | cache read | cache written | hit rate |
| :-- | --: | --: | --: |
| intake | 201015 | 36444 | 85 % |
| tester | 3492990 | 210676 | 94 % |
| coder | 3657467 | 338491 | 92 % |
| reviewer | 2367527 | 166759 | 93 % |
| documenter | 1213309 | 83864 | 94 % |
| smoke-tester | 68807 | 18031 | 79 % |
| **total** | 11001115 | 854265 | 93 % |
```

The smoke test is green: every promise of the feature holds end to end. Item 5 shows the one weakness. An output that holds `</context>` gives three closing markers for two blocks, so the diff's block appears to end early. S0004 promised only the four markers of S0002, so this is no broken promise. It is real, though: once the reviewer's stage gets a diff as a start fact, every story that touches `prompts.py` or its tests shows it. Proposed as F0058-S0005.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- S0001 coder, three times: the comment above `__all__` in `claude_runtime.py:70` re-exports names that moved to `agent_launch` "for earlier callers". Today only `ClaudeCodeRuntime` and `SWITCHES` are imported from there (`src/factory/entry/wiring.py`, `tests/entry/`). This is a candidate for `make duplicates` / vulture, not for this feature.
- S0001 reviewer: `tests/agents/adapters/test_claude_runtime.py:218-248` repeats the expected argument list of `test_call_passes_every_flag_in_order`. This is test quality only.
- S0002 coder, several times: the common system prompt exists twice, in `SYSTEM_PROMPT` and in `agents/system-prompt.md`. This is by design (the fallback for older agent homes), and the criterion 12 test keeps the two equal.
- S0002 reviewer: `tests/agents/adapters/test_claude_runtime_system_prompt.py:58` finds the flag's value inline. Three `_after` helpers do the same: `test_claude_runtime.py:110`, `test_shipped_agents_effect.py:86` and `tests/support/claude_resume_support.py:98`. A move to one support helper falls under the standing leave.
- S0002 documenter: criterion 14 names the operator guide's section "The agent files", but the right place was *The shipped agents and settings*. It was written there.
- S0004 intake, reviewer and coder: criterion 8's "operator template" holds no system prompt. The human read it as void (entry 15).
- S0004 coder: `RecordingProjectCommands.start_fact` was not covered by any test, and the `ContainerMakeCommands` docstring described `run` only. Both are settled: the reviewer's criterion 13 added `tests/machine/application/test_recording_start_fact.py`, and the docstring at `src/factory/machine/adapters/make_commands.py:101` now names both.
- S0004 reviewer: the class-level mutable dict in `tests/pipeline/application/test_stage_context.py` (`_LimitNotingCommands.limits`) is reset by hand; a fixture would make that reset impossible to forget. The same reviewer noted that `test_recording_start_fact.py` builds the class directly and not through the wiring.
- S0004 documenter: the records contract is now 4.5 in `docs/project-guide/work.md` and `docs/operator-guide/records.md`. This was done.

None of these is worth a story of its own. The test-quality points (the `_after` copies, the mutable dict) suit a later tester under the standing leave.

## 5 The documentation as a whole

The project guide (`agents.md`, `pipeline.md`), `docs/decisions.md` (three entries, lines 1681 to 1697) and the operator guide's *Start facts* (`docs/operator-guide/pipeline.md:48`) and bill section (`records.md:120`) agree with each other and with the code. One section the feature made necessary is missing. `docs/operator-guide/agent-runtime.md` never mentions the cached start. *A project's own agents* invites the operator to copy and change a shipped agent, and its example file (`model: sonnet`, `tools: [Read, Write]`, `effort: low`, line 318) is exactly the kind that loses the shared start, with nothing to say so. *The models* (line 212) still reads "the agent files name `opus`, `sonnet` and `haiku`", while every shipped file names `opus`. Proposed as F0058-S0006. A smaller point: the *Start facts* example uses `git diff --stat develop...HEAD`, which needs a local `develop` in the check container's checkout. That holds on this VM (`git branch -a`), but a project's checkout may lack it. It is noted here, and no story is proposed.

## 6 Decisions taken for the human

From `feature.md`, for the human to accept or revisit:
1. Every role gets the union of tools; intake, the reviewer and the smoke tester gain `Write`. The write paths still limit them: S0001 criterion 5, `tests/pipeline/application/test_take_refuses_write_and_edit.py`.
2. The decision is a free string in the schema and is checked after the run.
3. Intake and the documenter move to Opus at medium effort; the two reviewers stay at high.
4. The role's instructions move from the system prompt into the first message.
5. The work item enters without its front matter.
6. Start facts are project commands, put after the role's block, cut at 60,000 characters, and never a gate.

The human's answers in the stories:
- S0002 entry 4: the escape form `&lt;`. Entry 9: a resumed run gets the whole message, then `CONTINUE_PROMPT`; OpenCode's result block follows the message. Entry 12: only a call that starts a session gets the result block. Entry 32: the operator-guide line on `system-prompt.md`.
- S0003 entry 4: the exact `Cache:` line and role table, no total across work items, the bill only, round half up, `-h`/`--help`.
- S0004 entry 4: `context` counts toward the lease, and contract 1.1, with the human raising `factory/pipeline.yml`. Entry 15: `RECORDS_CONTRACT` 4.5 and the declared operation `ProjectCommands.start_fact`; "the operator template" read as void.

Still open for the human: the start-fact make targets and the `context` lines in this repository, the demo and the operator template (see 1), then the measurement run against the 2026-11-08 baseline. Another open question is whether the factory should warn when a project's own agent differs from the shared start in tools, model or effort; S0006 only documents it.

Earlier tests changed, each with its leave. Checked against `git diff --name-status` of the four merges; every modified earlier test is named:
- S0001: `tests/agents/adapters/test_claude_runtime.py` (criterion 4's leave), `tests/support/shipped_agents.py` (the human, entry 22), `tests/agents/domain/test_prompts.py` (a test added only).
- S0002, under the leave named in the Interface: `test_claude_runtime.py`, `test_opencode_runtime.py`, `test_shipped_agents_effect.py`, `test_prompts.py`, `test_task.py`, `test_task_acceptance.py`, `tests/support/opencode_stand_in.py`.
- S0002, under the human's later entries: `test_opencode_runtime_provider.py`, `test_patient_runs.py`, `tests/machine/adapters/test_opencode_runtime_lockdown.py` (entry 9), and `tests/agent_files/test_claude_agent_texts_review_groups.py` (entry 17).
- S0002, under the standing leave to move a shared helper: `tests/support/shipped_agents.py` (`SYSTEM_PROMPT_FILE`) and the move of `CODER_FACTS` to `tests/support/first_message_support.py`.
- S0003: `tests/entry/test_bill.py` (the leave in the Interface).
- S0004, under the human's entry 15: `tests/machine/application/test_interfaces.py`, `tests/pipeline/application/test_stage_finish.py`, `tests/pipeline/application/test_stage_time_limited_report.py`, `tests/support/preflight_support.py`, `tests/pipeline/domain/test_contract.py`, `tests/shared/domain/test_contract_version_4.py` and `tests/shared/domain/test_contract_version_4_2.py`.

No earlier test was changed without a leave.

## 7 The slow checks

The project offers nothing beyond `make check` (`make mutants` is check 3). `make check` was green as found: `test: green (109.8 s)`, 11,134 tests, 99.21 % branch coverage, `check: green`. The slowest tests in `.reports/junit.xml` take 10.0 s each. They are the `ROOMY_LIMIT` waits in `test_podman_timeout_status`, `test_document_examples`, `test_claude_runtime_resume`, `test_claude_runtime_provider_limit` and `tests/guards/test_opencode_resume_session`, which is by design.

Disk: free space on the shared pool went from 13.9 GB (disk start) to 13.3 GB (disk acceptance), 0.6 GB less. The instance's own `/srv/factory/vm` fell from 1.6 to 1.5 GB used, and `state` and `/tmp` stayed at 0.0 GB. The 0.6 GB went elsewhere on the pool, most likely the stage datasets and their snapshots (`/work` holds 868 MB now) or the stage image. The feature's changes (text, prompts and a few modules) do not explain it. It is small, and the next record should show whether it grows.

## 8 Cost

Four stories cost 59 runs, 118.7 minutes, 592 turns and $22.12, with 2.31 M tokens in and 21.92 M more from the cache. That is a hit rate of about 90 % over the feature, from 86 % (S0001) to 93 % (S0002), 82 % (S0003) and 91 % (S0004), each from `factory-bill`. The per-run comparison with the demo baseline is the human's measurement run: this repository's work items and `CLAUDE.md` are far larger, so its figures do not compare.

The human answered 11 questions, all of cause `question`, and the stories waited 0.4 h for them: S0001 3, S0002 5, S0003 1, S0004 2.

S0002 stands out: 17 runs, 49.7 min and $9.03, two fifths of the feature. Its journal says why. The Interface's leave for earlier tests did not cover the OpenCode tests (entry 9) or the CRC-pinned review-groups test (entry 17). A shipped prompt's text needed the human's choice on OpenCode's result block (entry 12). The docs criterion lacked the operator-guide line (entry 32). Each was a stop for the human, followed by a tester → coder round trip. S0002 needed the human most, for the same reason: a story that rewrites the message every runtime builds touches more earlier tests than its leave named. S0004 ($7.11, 16 runs) had the second-most rounds, for the same cause: the contract version tests and the interface's test implementations (entry 15).

## Proposed stories

- `F0058-S0005-the-context-markers-are-escaped-too.md`: a start fact or a work item holding `<context`/`</context>` forges or closes a block early (check 2, item 5). The fix is one domain constant, with tests.
- `F0058-S0006-the-operator-guide-says-what-keeps-the-cached-start.md`: the operator guide never says that a project's own agent with other tools, model or effort loses the shared cached start, and its *The models* paragraph is stale (check 5). Docs route.

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit 4ea8cc962f5fb60ec75588357a374f71c960ebca.
3. factory: started acceptance as vm.
4. acceptance-reviewer: accepted with stories; 2 stories proposed

   1. Scope: all four scope items are built (S0001 to S0004), and nothing was built outside the scope. Still open: the human's change after S0004. `factory/pipeline.yml`, the demo and the operator template are still at contract 1.0 with no `context` lines, and the `Makefile` has no start-fact targets. Until it lands, S0004 saves no turns.
   2. Feature smoke test: green. One script against the real reader, `compose_prompt`, `claude_runtime._arguments`, the YAML reader and `factory-bill` showed:
      - one tool list for every role, and one decision schema across stages;
      - opus at medium or high effort;
      - the system prompt file equals the built-in one;
      - all seven roles' first messages share their start up to `</work-item>`;
      - a pipeline with `context` loads, and an unknown `context` name is refused;
      - the bill shows a 93 % hit on S0002.
      One weakness: a start fact whose output holds `</context>` closes its block early (three closing markers for two blocks). F0058-S0005 is proposed for it.
   3. Mutation testing: by sweep, not run here.
   4. Noticed items: the stale `__all__` re-export comment in `claude_runtime.py`; three copies of the `_after` test helper; a duplicated expected argument list in `test_claude_runtime.py`; a class-level mutable dict in `test_stage_context.py`; the "operator template" wording, which the human read as void. The coverage gap and the docstring point from S0004 are already fixed. None is worth a story.
   5. Documentation: the project guide and the decision log agree with the code. The operator guide never mentions the cached start: its example project agent (sonnet, low effort, other tools) would lose the shared start without saying so, and *The models* is stale. F0058-S0006 (docs route) is proposed for it.
   6. Decisions for the human: feature decisions 1 to 6, and the human's answers in S0002 entries 4, 9, 12 and 32, S0003 entry 4 and S0004 entries 4 and 15, are listed in the report. Open: the start-fact targets and `context` lines, the measurement run, and whether the factory should warn when a project's agent breaks the shared start. Every earlier test changed in the four merges has a named leave; none was changed without one.
   7. Slow checks: nothing beyond `make check`, which is green (11,134 tests, 99.21 % coverage, test 109.8 s; the slowest tests are 10 s `ROOMY_LIMIT` waits). Disk: free space on the pool fell by 0.6 GB (13.9 to 13.3 GB) while the instance's own usage fell by 0.1 GB. The feature's changes do not explain it; most likely the stage datasets, their snapshots or the image.
   8. Cost: 59 runs, 118.7 min, $22.12; about 90 % cache hit over the feature (86 / 93 / 82 / 91 % per story). 11 questions answered, 0.4 h waited. S0002 stands out at $9.03, 17 runs and 5 questions, because its Interface's leave for earlier tests missed the OpenCode tests and the CRC-pinned review-groups test, and its docs criterion missed the operator-guide line. S0002 needed the human most.

   make check: green as found. Files written: the report and `backlog/F0058-S0005-the-context-markers-are-escaped-too.md` and `backlog/F0058-S0006-the-operator-guide-says-what-keeps-the-cached-start.md`; both pass `factory-check-story`.
