---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 662
comments_read: [6721852631]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T13:02:10.250331Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T13:02:10.258739Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T13:02:48.412555Z'
  stage: intake
  run: f1cae251b2d24c42b4c30f28b31b5299
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T13:06:37.371105Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T13:06:39.837783Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T13:07:07.805443Z'
  stage: intake
  run: 2e29510f597e4db3aea3d7f8d758ec58
---

# Each stage's start facts come from the factory

## Description

Almost every agent run begins with the same one or two shell commands, which gather the facts the run needs. The 2026-11-08 run's transcripts show them (`docs/runs/2026-11-08-e2e-demo-todo-2/eval.md`):
- **The reviewer:** `git diff --stat`, `git diff --name-status` and the full `git diff develop...HEAD` without `factory/` and `uv.lock`. The full diff is often too long for the tool's output, and the reviewer then pages through it with `sed` or `Read`.
- **The documenter:** the diff's file list, `ls docs` and `git status --short`.
- **The tester:** `git ls-files` without `factory/`.
- **The coder:** `git status --short` and `git log --oneline -5`.
- **The acceptance reviewer:** `git log --oneline`, the feature's tree and its stories.

Each of these is a full model turn. A run makes only 2 to 8 tool calls, so these start calls are about a quarter to a third of all turns.

After this story, a stage in the pipeline definition may name project commands as its start facts, under the new key `context`. The factory runs them in the check container on the stage's base before the agent starts, as it runs a stage's checks. It puts each output into the first message as a block of its own, after the role's instructions and before the run's facts. The agent then starts with these facts and needs no turn to gather them.

The commands are project commands, so the project decides what they show; the factory knows only their names.

## Interface

- `factory/pipeline.yml`: a stage may have `context: [<project command>, ...]`, naming project commands of `project_commands`, as `checks` and `reports` do. Loading refuses a name that is not a project command, as it does for `checks`.
- Before the agent's run, the factory runs each of the stage's `context` commands in the check container on the stage's base, each under its own `time_limit`.
- The first message gets one block per command, in the order of `context`: `<context name="<command>">`, its output, `</context>`. The blocks come after the `<role-instructions>` block and before the run's facts.
- An output longer than 60,000 characters is cut to its first 60,000, followed by a line saying how many characters were cut and that the agent can run the command itself.
- A command that fails or runs out of time gives a block holding the line `failed: <reason>`; the run goes ahead. A start fact is a help, not a gate.
- The marker texts of S0002 are escaped inside a context block, as inside the work item.
- The common system prompt says that the `<context>` blocks are facts the factory gathered at the start, which the agent need not gather again, in the shipped agent files and the operator template alike.
- The `context` commands count toward the lease: loading refuses a stage whose role's `time_limit` plus the `time_limit`s of its `checks`, `reports` and `context` exceed its `lease_duration`.
- A stage without `context` gets a message as before.
- The pipeline definition's version rule applies to the new key (`docs/decisions.md`): the pipeline definition's contract rises to 1.1, and the generated schema with it. A definition with `contract: "1.0"` and one with `"1.1"` both load, and both may carry `context`. This story does not change `factory/pipeline.yml`; the human raises it to 1.1, with its `context` lines, after this story.

The human's leave for earlier tests: this story may change these earlier tests where they pin the first message, the stage keys, the loading of the pipeline definition, or what runs in the check container before the agent, and only there:
- `tests/agents/domain/test_prompts.py`, `tests/support/first_message_support.py`
- `tests/pipeline/application/test_task.py`, `tests/pipeline/application/test_task_acceptance.py`
- `tests/pipeline/domain/test_pipeline_definition.py`, `tests/support/definition_support.py`
- `tests/pipeline/application/test_pipeline_loading.py`, `tests/pipeline/application/test_pipeline_loading_rules.py`, `tests/pipeline/application/test_pipeline_loading_strict_values.py`
- `tests/pipeline/adapters/test_pipeline_yaml.py`, `tests/pipeline/adapters/test_pipeline_rules.py`, `tests/pipeline/adapters/test_pipeline_strict_values.py`
- `tests/pipeline/application/test_stage_environment_calls.py`, `tests/pipeline/application/test_stage_on_container_fakes.py`, `tests/support/tick_support.py`
- `tests/agent_files/test_claude_files.py`, `tests/agent_files/test_template_sync.py` (for the system prompt's new sentence)

## Acceptance criteria

1. A stage with `context: [a, b]` gets a first message with the block of `a`, then the block of `b`, after the `<role-instructions>` block and before the run's facts (rows of one test).
2. Loading refuses a `context` name that is not a project command, and accepts one that is (rows of one test).
3. An output of 60,000 characters enters whole; one of 60,001 characters is cut, with the line naming the cut characters (rows of one test).
4. A failing command and one that runs out of time each give a block with `failed: <reason>`, and the agent's run still starts.
5. A marker text inside a command's output reaches the message escaped.
6. A stage without `context` gets the same message as without this story.
7. The commands run in the check container on the stage's base, never on the host.
8. The common system prompt names the `<context>` blocks as start facts the agent need not gather again, in the shipped agent files and the operator template alike.
9. Loading refuses a stage whose `context` time limits push the role's `time_limit` plus its checks', reports' and context's `time_limit`s past its `lease_duration`, and accepts one that fits (rows of one test).
10. A definition with `contract: "1.0"` and one with `contract: "1.1"` both load, each with a stage carrying `context` (rows of one test).
11. `make check` stays green.
12. docs: the project guide's description of the pipeline definition names `context`, what the factory does with it, the size limit and the failure line; the operator's guide shows one example. `docs/decisions.md`: one entry, a stage's start facts come from project commands the factory runs before the agent, to save the agent's first turns.

## Smoke test

```bash
uv run python -c "from factory.pipeline.domain.pipeline_definition import StageDefinition; print('context' in StageDefinition.model_fields)"
```
Expect: `True`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Questions. The format check passed. I read `feature.md` (decision 6 matches the story), `StageDefinition` and the lease rule in `src/factory/pipeline/domain/pipeline_definition.py`, and the version rule in `docs/decisions.md`. Three Interface lines cannot be tested or built without a further decision:

   1. **The system prompt's new sentence has no criterion.** The Interface says the common system prompt tells the agent that `<context>` blocks are facts the factory gathered at the start, which it need not gather again. No criterion tests this, although the leave covers `tests/agent_files/test_claude_files.py` and `test_template_sync.py`.
      - (a) Add a criterion before the two closing ones: "The common system prompt names the `<context>` blocks as start facts the agent need not gather again, in the shipped agent files and the operator template alike."
      - (b) Drop the line from the Interface.
      - I would choose (a).

   2. **It is open whether the lease covers the `context` commands.** The load-time lease rule (`_lease_faults`, `pipeline_definition.py:185-200`) requires a role's `time_limit` plus the `time_limit`s of its stage's `checks` and `reports` to fit within its `lease_duration`. The `context` commands also run inside the claim, before the agent, but the Interface does not say whether they count.
      - (a) They count. Add an Interface line and a criterion with both rows: a stage whose `context` pushes the total past `lease_duration` is refused, and one that fits is accepted.
      - (b) They do not count. Say so in the Interface; the lease may then run out during a slow start fact.
      - I would choose (a).

   3. **"The version rule applies to the new key" has no criterion and no value.** `factory/pipeline.yml` declares `contract: "1.0"`. An added optional key is a minor change under the rule in `docs/decisions.md`. Two coders could read this two ways: raise the definition's contract to `1.1` (and the generated schema in `src/factory/contract/`, if the definition is in `CONTRACT`), or change nothing because loading checks only the major.
      - (a) State the expected value in the Interface ("the pipeline definition's contract rises to 1.1"). Add a criterion that a definition with `contract: "1.0"` and one with `"1.1"` both load with `context`, if older definitions must keep loading.
      - (b) Drop the line and leave the version to the reviewer's check.
      - I would choose (a). Note that a change to `factory/pipeline.yml` itself is the human's (CLAUDE.md, *Not without asking*).

   The rest needs no answer:
   - **Criteria:** criteria 1 to 7 are each testable by one test. The order, both sides of the size limit, both failure kinds, the escaping, the stage without `context` and the place where the commands run all have criteria.
   - **Smoke test:** it is runnable and `True` can be checked against its output.
   - **Docs criterion:** it names what the reader must know and dictates no sentences.
   - **Architecture:** a `StageDefinition` field in pipeline/domain, project commands run through the existing check container, the blocks built in agents/domain `prompts.py`. Nothing calls a tool outside a wrapper.
   - **Scope:** this is S0004 of F0058, decision 6, and not in "Out of scope". The human's leave names every earlier test it may change.
4. 2026-11-08 human: Answers from the human:

   1. (a). Add the criterion: the common system prompt names the `<context>` blocks as start facts the agent need not gather again, in the shipped agent files and the operator template alike.
   2. (a). The `context` commands count toward the lease. Add the Interface line and a criterion with both rows: a stage whose `context` time limits push the total past `lease_duration` is refused, and one that fits is accepted.
   3. (a). The pipeline definition's contract rises to 1.1. Add a criterion that a definition with `contract: "1.0"` and one with `"1.1"` both load, and that both may carry `context`. The human raises `factory/pipeline.yml` itself to 1.1 after this story, together with its `context` lines; this story does not change `factory/` beyond the work item.
5. factory: started intake as vm.
6. intake: accepted. I added the human's answers from journal entry 4 to the story. Interface: the system prompt line now covers the shipped agent files and the operator template alike. A new line says that the `context` commands count toward the lease. The version line now says the contract rises to 1.1 with its generated schema (`PipelineDefinition` is in `CONTRACT`, `src/factory/shared/domain/contract.py:42`), that definitions at 1.0 and 1.1 both load and may carry `context`, and that `factory/pipeline.yml` stays the human's. Criteria: new criteria 8 (system prompt), 9 (lease, both rows) and 10 (1.0 and 1.1 both load with `context`) go before the two closing ones, now 11 and 12. The Description's meaning did not change, so I did not rewrite it.
   - Interface: names the key `context` in `StageDefinition` (`src/factory/pipeline/domain/pipeline_definition.py`), the block format, its order and place, the 60,000-character limit with its cut line, the failure line, escaping, the lease rule and the contract value. Each is concrete.
   - Criteria: each is testable by one test. Every rule has both sides: an unknown `context` name refused and a known one accepted; 60,000 characters whole and 60,001 cut; a failed command and a timed-out one; lease exceeded and lease fitting; contract 1.0 and 1.1; a stage without `context` unchanged; the system prompt sentence; commands running in the check container.
   - Smoke test: runnable with `uv run python -c`, and `Expect: True` can be checked against its output.
   - Docs criterion: names what the reader must know (the key, what the factory does with it, the size limit, the failure line, one operator example, one decision entry) and dictates no sentences.
   - Architecture: the stage key and the lease rule belong in pipeline/domain. The commands run through the existing project-commands interface in the check container, as checks do. The blocks are built in agents/domain prompts. No tool is called outside its wrapper. The contract schema is regenerated with `factory.entry.contract`.
   - Scope: within F0058, whose decision 6 matches this story, and not in its Out of scope. The human's leave names every earlier test the story may change. Route `tests`, because the Interface changes `src/`.
