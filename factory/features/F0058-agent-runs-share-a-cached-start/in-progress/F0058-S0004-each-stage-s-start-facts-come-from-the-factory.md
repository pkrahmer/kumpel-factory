---
stage: approval
blocked: null
round: 2
attempts: 0
crashes: 0
pull_request: 662
comments_read: [6721852631, 6722094144]
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
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T13:07:12.864167Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T13:11:09.845180Z'
  stage: tests
  run: a3f54b09525a4b139bd898a37a9df388
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T13:11:14.753564Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-08T13:24:33.038223Z'
  stage: doing
  run: 22780fb365bf448f959efc65e7ec94a1
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-08T13:24:38.373452Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-08T13:27:23.021841Z'
  stage: review
  run: f086326a90a4400b9df29a601127f96a
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-08T13:27:28.524336Z'
  stage: doing
- number: 14
  speaker: coder
  kind: question
  at: '2026-11-08T13:27:57.905938Z'
  stage: doing
  run: 2ec1b27aff154065afe7db1398bb1e8c
  blocked: question
- number: 15
  speaker: human
  kind: comment
  at: '2026-11-08T13:29:44.913272Z'
  stage: doing
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-08T13:29:47.325954Z'
  stage: doing
- number: 17
  speaker: coder
  kind: result
  at: '2026-11-08T13:30:10.198658Z'
  stage: doing
  run: f92d504ae4c24d50a2e7b46a78d38870
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-08T13:30:15.525909Z'
  stage: tests
- number: 19
  speaker: tester
  kind: result
  at: '2026-11-08T13:32:59.949907Z'
  stage: tests
  run: 757565320d604194bf8b2094c5ec959a
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-08T13:33:05.190817Z'
  stage: doing
- number: 21
  speaker: coder
  kind: result
  at: '2026-11-08T13:37:58.631902Z'
  stage: doing
  run: e9b7ce6a06374bc788306432cb55a43e
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-08T13:38:04.006720Z'
  stage: review
- number: 23
  speaker: reviewer
  kind: result
  at: '2026-11-08T13:39:36.828110Z'
  stage: review
  run: 23353bd7c2754c7aacff4a414a4e3e14
- number: 24
  speaker: factory
  kind: started
  at: '2026-11-08T13:39:41.905972Z'
  stage: doing
- number: 25
  speaker: coder
  kind: result
  at: '2026-11-08T13:42:07.437647Z'
  stage: doing
  run: cb4d028b05f34b389f3b99d042ebc4b5
- number: 26
  speaker: factory
  kind: started
  at: '2026-11-08T13:42:12.311862Z'
  stage: tests
- number: 27
  speaker: tester
  kind: result
  at: '2026-11-08T13:43:36.756536Z'
  stage: tests
  run: 501c682f43d34680a8c53877418860aa
- number: 28
  speaker: factory
  kind: started
  at: '2026-11-08T13:43:42.098989Z'
  stage: doing
- number: 29
  speaker: coder
  kind: result
  at: '2026-11-08T13:48:00.175114Z'
  stage: doing
  run: cf1b0ab878e34232807534891c3c278a
- number: 30
  speaker: factory
  kind: started
  at: '2026-11-08T13:48:08.858413Z'
  stage: review
- number: 31
  speaker: reviewer
  kind: result
  at: '2026-11-08T13:49:02.602138Z'
  stage: review
  run: c1b99d70106d43288640f207310f9255
- number: 32
  speaker: factory
  kind: started
  at: '2026-11-08T13:49:08.056612Z'
  stage: docs
- number: 33
  speaker: documenter
  kind: result
  at: '2026-11-08T13:54:55.271024Z'
  stage: docs
  run: f866b7940def40c692425ef77dbf6cd0
- number: 34
  speaker: factory
  kind: started
  at: '2026-11-08T13:55:00.815077Z'
  stage: smoke-test
- number: 35
  speaker: smoke-tester
  kind: result
  at: '2026-11-08T13:55:15.046299Z'
  stage: smoke-test
  run: 45b43b5dc84544ca8c641d2a48dc182a
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
- The common system prompt says that the `<context>` blocks are facts the factory gathered at the start, which the agent need not gather again, in the shipped `agents/system-prompt.md` and the built-in fallback `SYSTEM_PROMPT` alike.
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
8. The common system prompt names the `<context>` blocks as start facts the agent need not gather again, in the shipped `agents/system-prompt.md` and the built-in fallback `SYSTEM_PROMPT` alike.
9. Loading refuses a stage whose `context` time limits push the role's `time_limit` plus its checks', reports' and context's `time_limit`s past its `lease_duration`, and accepts one that fits (rows of one test).
10. A definition with `contract: "1.0"` and one with `contract: "1.1"` both load, each with a stage carrying `context` (rows of one test).
11. A file a `context` command writes on the dataset is not there when the agent's run starts, and the take after the run does not carry it.
12. Each `context` command runs under its own `time_limit` from `project_commands`: two commands with different time limits each get their own.
13. Through the wiring's recording project commands, a start fact's run is written to the command records as a check's run is.
14. `make check` stays green.
15. docs: the project guide's description of the pipeline definition names `context`, what the factory does with it, the size limit and the failure line; the operator's guide shows one example. `docs/decisions.md`: one entry, a stage's start facts come from project commands the factory runs before the agent, to save the agent's first turns.

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
7. factory: started tests as vm.
8. tester: Tests written for every criterion. They fail for the right reason: loading refuses `stages.tests.context` as an unknown key, and neither system prompt mentions `<context>` yet. One run of the new files gave 16 failed. The stage without `context` passes now, and must keep passing. `make lint` is green. I skipped the type check, as the stage says.

   - criterion 1: `tests/pipeline/application/test_stage_context.py::test_the_context_blocks_follow_the_role_instructions_in_their_order_before_the_facts` (rows a-then-b, b-then-a)
   - criterion 2: `tests/pipeline/adapters/test_pipeline_context.py::test_a_context_name_must_be_a_project_command` (rows project-command, unknown)
   - criterion 3: `tests/pipeline/application/test_stage_context.py::test_an_output_beyond_the_limit_is_cut_with_a_line_naming_the_cut_characters` (rows 60000 whole, 60001 cut). The cut row expects one non-blank line after the first 60,000 characters, with the number `1` as a word in it.
   - criterion 4: `tests/pipeline/application/test_stage_context.py::test_a_failed_or_timed_out_command_gives_a_failed_line_and_the_run_starts` (rows fails, out-of-time). The out-of-time row uses a subclass of `ContainerMakeCommands` whose `run` returns a `time_limit` `CheckResult` for that one command. A `time_limit` is in whole minutes, so a real timeout cannot run within a test.
   - criterion 5: `tests/pipeline/application/test_stage_context.py::test_a_marker_text_in_an_output_reaches_the_message_escaped`
   - criterion 6: `tests/pipeline/application/test_stage_context.py::test_a_stage_without_context_gets_no_block_and_runs_no_command_before_its_agent`. The existing `tests/pipeline/application/test_task.py::test_the_request_shares_the_allowed_decisions_and_the_facts_of_the_context` also still pins the unchanged message.
   - criterion 7: `tests/pipeline/application/test_stage_context.py::test_the_context_commands_run_in_the_check_container_before_the_checks_not_on_the_host`
   - criterion 8: `tests/agent_files/test_context_system_prompt.py::test_the_system_prompt_names_the_context_blocks_as_facts_not_to_gather_again` (rows shipped = `agents/system-prompt.md`, fallback = `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`)
   - criterion 9: `tests/pipeline/adapters/test_pipeline_context.py::test_the_context_time_limits_count_toward_the_lease` (rows fits: 40+5+10+5 = 60; exceeds: 61)
   - criterion 10: `tests/pipeline/adapters/test_pipeline_context.py::test_a_definition_at_either_contract_loads_with_a_stage_carrying_context` (rows 1.0, 1.1)
   - criteria 11 and 12: no test of their own; they are `make check` and the docs stage.

   Files created: `tests/pipeline/application/test_stage_context.py`, `tests/pipeline/adapters/test_pipeline_context.py`, `tests/agent_files/test_context_system_prompt.py`. I changed no earlier test, so I did not use the human's leave. Every module imported; the failures are assertions and refused definitions, not collection errors.

   How the stage tests are built, for the coder:
   - They run a whole `tests` stage through `StageRunner` on the `boundaries` fixture's fake dataset, with `ContainerMakeCommands` as `project_commands`, and read the prompt that `FakeAgentRuntime` received.
   - The Makefile targets print the outputs, so the full output has to reach the message through `ProjectCommands.run`.
   - They find a block by its `<context name="…">` opening and the next `</context>`. They check order by position. They do not check the blank lines between parts.
   - A failed block must hold a line that starts with `failed: `. The reason itself is not pinned.

   Open, for the reviewer and the human: criterion 8 names "the operator template". No system prompt exists under `operator/template` (nor anywhere under `operator/`); the only two are the shipped `agents/system-prompt.md` and the `SYSTEM_PROMPT` fallback, which says the same. I tested those two and did not invent a template file. If the human meant another file, its row is missing.

   `lint`: lint: green (0.1 s)
9. factory: started doing as vm.
10. coder: Built the stage key `context` and the start facts. All tests pass, the tester's three new files included, and `make check` is green (`check: green`, coverage 99.21 %).

    What I built:
    - `src/factory/pipeline/domain/pipeline_definition.py`: `StageDefinition.context: list[str] = []`. `_command_faults` refuses a `context` name that is not a project command, as it does for checks and reports. `_minutes_at_stage` adds the `context` time limits to the lease total. The `PipelineDefinition` docstring says the contract is 1.1 since `context` and that 1.0 loads too. Loading checks only the major, so both load.
    - `src/factory/contract/pipeline-definition.schema.json`: regenerated with `uv run python -m factory.entry.contract`.
    - `src/factory/agents/domain/prompts.py`:
      - `StartFact` holds the command, its output, and the reason when it failed. `PromptFacts.start_facts` holds the list.
      - `compose_prompt` puts one `<context name="…">` block per fact after the role block and before the run's facts. A stage with no facts gets the same message as before.
      - Outputs are cut after `CONTEXT_LIMIT` (60,000 characters), followed by one line naming the cut characters and telling the agent to run the project command itself. A failed fact gives `failed: <reason>`. The S0002 marker texts are escaped with the existing `_escape_markers`.
      - The fallback `SYSTEM_PROMPT` gets the new sentence about `<context>` blocks. So does the shipped `agents/system-prompt.md`.
    - `src/factory/pipeline/application/task.py`:
      - `TaskComposer.start_facts(stage)` runs each `context` command through `boundaries.project_commands` (the check container) under its own time limit.
      - A red result gives `failed: exit status <n>: <last line>`, and a timeout gives `failed: ran out of its time limit of <n> min`. A `ProjectCommandError` (the command could not start) gives its message.
      - `TaskContext.start_facts` carries the facts into the prompt.
    - `src/factory/pipeline/application/stage.py`: `StageLauncher.launch` now prepares the stage environment first, then gathers the start facts on the new base, then composes the request. Before this change, compose came before prepare.
    - `src/factory/machine/application/stage_environment.py`: `ContainerEnvironment.run_agent` now rolls the dataset back to its base before the agent runs. Otherwise a file a start fact's command left on the dataset would reach the agent and the take.
    - `src/factory/pipeline/domain/checks.py` and `src/factory/machine/adapters/make_commands.py`: `CommandOutput(CheckResult)` keeps the whole `output`, and `whole_output(result)` reads it. A result without it falls back to `output_tail`. Both make implementations now return `CommandOutput`.

    Main choice, and what I rejected:
    - To get the whole output out of `ProjectCommands.run`, I first added `output: str` to `CheckResult`. `tests/pipeline/domain/test_checks.py::test_fields_are_exactly_the_generic_eight` pins its fields exactly, and that test is outside the human's leave. So I used a subclass instead. Its cost is one `isinstance` check in `whole_output`.
    - I also rejected a new abstract `ProjectCommands` method for start facts. The tester's `_SlowCommands` overrides only `run`, so its out-of-time row would have stopped working. A new abstract method on `StageEnvironment` for the rollback would have broken the test implementations in `test_stage_environment_calls.py` and `test_stall_environment.py`.
    - If the reviewer prefers the plain field, that needs the human's leave for `test_checks.py`.

    Open, for the reviewer and the human:
    - **Records contract version.** The Interface says the generated schema rises with the contract. The schemas carry the shared records version `RECORDS_CONTRACT = "4.4"`, and the version rule calls an added optional field a minor rise (4.5). Three earlier tests pin "4.4": `tests/shared/domain/test_contract_version_4.py`, `tests/shared/domain/test_contract_version_4_2.py` and `tests/pipeline/domain/test_contract.py:54`. None of them is in the leave, so I left it at 4.4. Raising it needs the human's word and a test change by the tester.
    - **The operator template.** As the tester noted, no system prompt exists under `operator/template`, so only the shipped file and the fallback carry the new sentence.
    - **Not touched.** Docs (`docs/project-guide`, operator guide, `docs/decisions.md`) are the documenter's. `factory/pipeline.yml` stays at 1.0 for the human.

    Refactor: I read my diff once and turned an if/else that ruff flagged into `_context_text`. Nothing else needed changing.

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
11. factory: started review as vm.
12. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'` against the work item. The tests cover criteria 1 to 10, and each test checks the criterion it is named after. Both sides of every stated limit are tested: the unknown name, 60,000 and 60,001 characters, the lease fitting and exceeded, contract 1.0 and 1.1, and both failure kinds. The coder's `make check` was green. No marker silences a check, and no string-built shell or SQL was added. `make duplicates` gave 7 new findings, and none of them is in a file this diff touches.

    Findings:
    1. `src/factory/shared/domain/contract.py:16` (`RECORDS_CONTRACT = "4.4"`) and `src/factory/contract/pipeline-definition.schema.json:3`: the schema gained the optional property `stages.*.context`, but `x-records-contract` stays at 4.4. The version rule in `docs/decisions.md:721` raises the minor for an added optional field, and the Interface says "the generated schema with it". Fix: raise it to 4.5 and regenerate with `uv run python -m factory.entry.contract`. That breaks `tests/shared/domain/test_contract_version_4.py:12,23`, `tests/shared/domain/test_contract_version_4_2.py:12,23` and `tests/pipeline/domain/test_contract.py:54`, which are outside the story's leave. The coder ends with `question` and asks the human for leave to change those three, for the tester.
    2. `src/factory/pipeline/application/task.py:129-135`: each start fact runs through `ContainerMakeCommands.run`, whose script is `"$1" sync && "$1" … "$2"` (`src/factory/machine/adapters/make_commands.py:37`). The output that reaches the `<context>` block therefore starts with all of `make sync`'s output: in this project, the `uv sync --frozen` echo, uv's lines and `sync: green (…)`. That text counts toward the 60,000 characters, and it is not the command's output, which is what the Interface puts in the block. The base was synced by `prepare` just before. The tests miss this because `stage_makefile()` has a silent `sync`. Fix: the block holds only the command's own output. Either run the command without the sync on the just-prepared base, or keep the outputs apart. Add a test row with a `sync` that prints.
    3. `src/factory/pipeline/domain/checks.py:99-107` (`CommandOutput`, `whole_output`): the caller gets the whole output back through an `isinstance` downcast that `ProjectCommands.run` (`src/factory/machine/application/project_commands.py:20`) does not declare. Any other implementation silently gives the start fact only `output_tail`, the last lines, and no error says so. The Interface needs the whole output to cut at 60,000 characters. Fix: let the interface declare the whole output. One way is an `output` field on `CheckResult`, which needs the human's leave for `tests/pipeline/domain/test_checks.py::test_fields_are_exactly_the_generic_eight`. The other is a declared operation that returns a DTO carrying it, which needs leave for the earlier test implementations of `ProjectCommands`, such as `tests/machine/application/test_interfaces.py:133`. Ask together with finding 1. The fix for finding 2 may settle this one too.
    4. Criterion 11 added: it needs its test. `ContainerEnvironment.run_agent` (`src/factory/machine/application/stage_environment.py:151`) now rolls the dataset back before the agent, so a file a start fact's command leaves on the dataset neither reaches the agent nor the take. No test pins this: the criterion 7 test only checks that the host's checkout lacks `ran-a`. The new criterion is: "A file a `context` command writes on the dataset is not there when the agent's run starts, and the take after the run does not carry it."

    Open, for the human, not a finding: criteria 8 and the Interface name "the operator template". No system prompt exists under `operator/template`. The two copies are the shipped `agents/system-prompt.md` and the built-in fallback `SYSTEM_PROMPT` (`src/factory/agents/domain/prompts.py:31`), which `docs/operator-guide/agent-runtime.md:353` describes as the same text. Both carry the sentence, and the tests cover both. If the human meant the fallback, the wording of criterion 8 can say so. I did not change it, because the journal does not settle it.

    Earlier tests: none changed. Every test file in the diff is new (status `A`).
13. factory: started doing as vm.
14. coder: Question. I changed no code this round. Three of the reviewer's four findings in entry 12 need the human's leave for earlier tests outside the story's list, and the fourth needs a test from the tester. Two decisions are needed:

    1. **Records contract version (finding 1).** The schema gained `stages.*.context`, so the version rule in `docs/decisions.md` raises `RECORDS_CONTRACT` from 4.4 to 4.5 (`src/factory/shared/domain/contract.py:16`), and the schemas are regenerated. Three earlier tests pin "4.4": `tests/shared/domain/test_contract_version_4.py:12,23`, `tests/shared/domain/test_contract_version_4_2.py:12,23` and `tests/pipeline/domain/test_contract.py:54`.
       - (a) Leave to change those three to 4.5. The tester changes them, then I raise the constant and regenerate.
       - (b) Keep 4.4, and the reviewer's finding stands as accepted.
       - I would choose (a).

    2. **How a start fact gets its whole output without `make sync`'s output (findings 2 and 3).** Today each `context` command runs through `ContainerMakeCommands.run`, which runs `make sync && make <command>`, so uv's sync lines start every `<context>` block and count toward the 60,000 characters. The whole output reaches the caller only through an `isinstance` downcast to `CommandOutput` (`src/factory/pipeline/domain/checks.py:99-107`), which the interface `ProjectCommands` does not declare. One change settles both findings:
       - (a) A declared operation `ProjectCommands.start_fact(command, *, time_limit) -> CommandOutput`, an abstract method like `run`. `CommandOutput` carries the whole output. `ContainerMakeCommands` runs it on the base with the taken files, without `sync`, because `prepare` synced that base just before. `MakeProjectCommands` and `RecordingProjectCommands` implement it, and `whole_output` and the downcast go away. This needs leave to add the method to the earlier test implementations of `ProjectCommands`: `tests/machine/application/test_interfaces.py`, `tests/pipeline/application/test_stage_finish.py`, `tests/pipeline/application/test_stage_time_limited_report.py` and `tests/support/preflight_support.py`. The tester would also move the out-of-time row of its own `tests/pipeline/application/test_stage_context.py` (`_SlowCommands`) to the new method, and add the row with a `sync` that prints.
       - (b) Add `output: str` to `CheckResult` itself, which needs leave for `tests/pipeline/domain/test_checks.py::test_fields_are_exactly_the_generic_eight`. This settles finding 3 but not finding 2: the output would still begin with the sync's lines unless `run` gains a flag to skip the sync.
       - (c) Keep the code as it is and accept both findings.
       - I would choose (a).

    After the answer, I end with `tests`. The tester then makes the approved test changes and adds the test for the new criterion 11 from finding 4 (a file a `context` command writes on the dataset is not there when the agent's run starts, and the take does not carry it). The code for criterion 11 is already in place: `ContainerEnvironment.run_agent` rolls the dataset back before the agent. After that, I implement the chosen options.

    Noticed, not touched: as entries 8, 10 and 12 say, no system prompt exists under `operator/template`. The sentence is in `agents/system-prompt.md` and in the fallback `SYSTEM_PROMPT`. If the human meant another file, criterion 8 should name it.
15. 2026-11-08 human: Answers from the human:

    1. (a). Leave to change `tests/shared/domain/test_contract_version_4.py`, `tests/shared/domain/test_contract_version_4_2.py` and `tests/pipeline/domain/test_contract.py` from 4.4 to 4.5. The tester changes them; the coder raises `RECORDS_CONTRACT` and regenerates the schemas.
    2. (a). Add the declared operation `ProjectCommands.start_fact(command, *, time_limit) -> CommandOutput`, without `sync`, and remove the downcast. Leave to add the method to the test implementations in `tests/machine/application/test_interfaces.py`, `tests/pipeline/application/test_stage_finish.py`, `tests/pipeline/application/test_stage_time_limited_report.py` and `tests/support/preflight_support.py`, and for the tester's changes to `tests/pipeline/application/test_stage_context.py` as described.

    On criterion 8: there is no system prompt under `operator/template`, and none is wanted. The sentence in `agents/system-prompt.md` and in the fallback `SYSTEM_PROMPT` meets the criterion; read "the operator template alike" as void.
16. factory: started doing as vm.
17. coder: Changed no code this round. The human's answers in entry 15 call for test changes, so I hand the item to the tester first. When it comes back, I will raise `RECORDS_CONTRACT` to 4.5, regenerate the schemas and add the declared operation.

    The test changes the human allowed (entry 15):

    1. **Contract version.** In `tests/shared/domain/test_contract_version_4.py`, `tests/shared/domain/test_contract_version_4_2.py` and `tests/pipeline/domain/test_contract.py:54`, change the pinned records contract from "4.4" to "4.5".
    2. **New interface operation.** `ProjectCommands` (`src/factory/machine/application/project_commands.py`) gets a second abstract method: `start_fact(self, command: str, *, time_limit: timedelta) -> CommandOutput`. `CommandOutput` already exists in `factory.pipeline.domain.checks`. It is a `CheckResult` with the whole `output: str`. The method runs the command on the stage's base without `make sync` first. Add this method to the test implementations of `ProjectCommands` in `tests/machine/application/test_interfaces.py`, `tests/pipeline/application/test_stage_finish.py`, `tests/pipeline/application/test_stage_time_limited_report.py` and `tests/support/preflight_support.py`.
    3. **`tests/pipeline/application/test_stage_context.py`**, two changes:
       - Move `_SlowCommands` to override `start_fact` instead of `run`. For `SLOW` it returns a `time_limit` `CommandOutput` with `output=""`, and otherwise it calls `super().start_fact(...)`.
       - Add a row whose Makefile `sync` target prints a line. The command's `<context>` block must not contain that line.
    4. **New test for criterion 11** (added by the reviewer in entry 12, finding 4): a file a `context` command writes on the dataset is not there when the agent's run starts, and the take after the run does not carry it. The code for this is already in place: `ContainerEnvironment.run_agent` rolls the dataset back to its base before the agent runs (`src/factory/machine/application/stage_environment.py`).

    What the journal changed in the task: entry 15 says criterion 8's "the operator template alike" is void. The sentence in `agents/system-prompt.md` and in the fallback `SYSTEM_PROMPT` is enough. I left the Description unchanged; criterion 8's test already covers those two.

    Noticed, not touched: once `start_fact` is in place, `whole_output` and the `isinstance` downcast in `src/factory/pipeline/domain/checks.py` go away, and `CommandOutput` stays as the operation's return type. That is my change for the next round.
18. factory: started tests as vm.
19. tester: Made the test changes the human allowed in entry 15, as the coder listed them in entry 17, and wrote the test for criterion 11. One run of the changed files gave 20 failed and 105 passed. The 20 failures are expected and fail for the right reason: the records contract is still 4.4, `ProjectCommands` has no `start_fact` yet, and the start facts still run through `run` with `make sync`'s output in front. `make lint` is green. I skipped the type check, as the stage says.

    Changes to earlier tests, under the leave in entry 15:
    - `tests/shared/domain/test_contract_version_4.py`, `tests/shared/domain/test_contract_version_4_2.py`, `tests/pipeline/domain/test_contract.py`: the pinned records contract goes from "4.4" to "4.5".
    - `tests/machine/application/test_interfaces.py`: `ProjectCommands.__abstractmethods__` is now `{"run", "start_fact"}`, and `Complete` implements `start_fact(command, *, time_limit) -> CommandOutput`.
    - `tests/pipeline/application/test_stage_finish.py` (`RecordingCommands`): `start_fact` records the call, then delegates.
    - `tests/pipeline/application/test_stage_time_limited_report.py` (`StoppedTestCommands`): `start_fact` delegates.
    - `tests/support/preflight_support.py` (`RecordingCommands`): `start_fact` raises `AssertionError`, because the preflight gathers no start fact.

    Changes to my own `tests/pipeline/application/test_stage_context.py`:
    - `_SlowCommands` now overrides `start_fact`. For `SLOW` it returns a `time_limit` `CommandOutput` with `output=""`, and for every other command it calls `super().start_fact(...)`.
    - `_Started.prompt` takes a `sync` target, which replaces the Makefile's silent one, and an optional `looked_for` path.
    - The order test has a new row, `a-then-b-with-a-printing-sync`. Its `sync` prints `the sync of the base`, and each block must still hold exactly its command's own line.
    - New test for criterion 11. A `context` command writes `tests/left_by_a_start_fact.txt` on the dataset. I put the file inside the tester's write paths, so the take would carry it if it were still there. A `WorkspaceRuntime` subclass notes at the agent's start whether the file is in the dataset's checkout. The test asserts that the file is gone at that point, and that the stage's pushed commit does not hold it. This test passes now, because `ContainerEnvironment.run_agent` already rolls the dataset back.

    Mapping:
    - criterion 1: `tests/pipeline/application/test_stage_context.py::test_the_context_blocks_follow_the_role_instructions_in_their_order_before_the_facts` (rows a-then-b, b-then-a, a-then-b-with-a-printing-sync)
    - criterion 4: `tests/pipeline/application/test_stage_context.py::test_a_failed_or_timed_out_command_gives_a_failed_line_and_the_run_starts` (the out-of-time row now goes through `start_fact`)
    - criterion 11: `tests/pipeline/application/test_stage_context.py::test_a_file_a_context_command_writes_is_gone_at_the_agent_s_start_and_not_taken`
    - The other criteria keep the tests from entry 8.

    Failing until the coder's change:
    - every row of the three contract-version tests
    - `test_project_commands_and_agent_runtime_have_exactly_their_operations_abstract`
    - the printing-sync row
    - the out-of-time row

    Files created: none this round. Every module imported; no test failed at collection.

    `lint`: lint: green (0.1 s)

    `lint`: lint: green (0.2 s)
20. factory: started doing as vm.
21. coder: Implemented the human's answers from entry 15, using the test changes the tester made in entry 19. All tests pass and `make check` is green (`check: green`, coverage 99.17 %).

    What I built:
    - `src/factory/machine/application/project_commands.py`: `ProjectCommands` has a second abstract method, `start_fact(command, *, time_limit) -> CommandOutput`. It runs the command on the stage's synced base with nothing before it and keeps the whole output. `RecordingProjectCommands.start_fact` delegates to the inner implementation and records the run as `run` does. Both now share the new private `_record`.
    - `src/factory/machine/adapters/make_commands.py`:
      - `ContainerMakeCommands.start_fact` runs `_START_FACT_SCRIPT` (`"$1" --no-print-directory "$2"`, without `sync`) in the same check container on the rolled-back base with the taken files. `run` and `start_fact` share `_run_script`, which takes the script to run.
      - `MakeProjectCommands.start_fact` runs `make --no-print-directory <command>`, and `run` delegates to it, since nothing runs before the command on the host.
      - `_read_result` is now typed to return `CommandOutput`. The `_check_result` wrapper is gone.
    - `src/factory/pipeline/domain/checks.py`: removed `whole_output` and the `isinstance` downcast. `CommandOutput` stays as the return type of `start_fact`.
    - `src/factory/pipeline/application/task.py`: `_start_fact` calls `project_commands.start_fact` and puts `result.output` into the fact.
    - `src/factory/shared/domain/contract.py`: `RECORDS_CONTRACT` is now "4.5". All five schemas under `src/factory/contract/` were regenerated with `uv run python -m factory.entry.contract`.

    Main choice: `start_fact` runs without `sync`. `ContainerEnvironment.prepare` syncs the dataset and moves the base forward just before the start facts run, and every check container resets to that base. So a second sync would only put uv's lines into the block. I rejected a `sync: bool` flag on `run`: it would have left the whole output undeclared on the interface, which was the reviewer's finding 3.

    Findings of entry 12: 1 is fixed (4.5 and the regenerated schemas). 2 and 3 are fixed by `start_fact`; the tester's printing-sync row covers 2. 4 is covered by the tester's test from entry 19, and the code for it was already in place.

    Refactor: I read my diff once and found nothing more to change.

    Noticed, not touched:
    - Coverage shows `RecordingProjectCommands.start_fact` (`project_commands.py:68-72`) as not run by any test. The wiring tests use the plain implementations for start facts. A test of it is the tester's if the reviewer wants one.
    - The docstring of the `ContainerMakeCommands` class still describes `run` only (`make sync && make <command>`). Each method's own docstring is accurate.
    - `make duplicates` was not run this round.

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
22. factory: started review as vm.
23. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'` (without `uv.lock`) against the work item. The findings from entry 12 are fixed:
    - Finding 1: `RECORDS_CONTRACT` is "4.5" and all five schemas were regenerated.
    - Findings 2 and 3: the new declared operation `ProjectCommands.start_fact` runs `_START_FACT_SCRIPT` without `sync`, and the `isinstance` downcast is gone. The `a-then-b-with-a-printing-sync` row covers finding 2.
    - Finding 4: `test_a_file_a_context_command_writes_is_gone_at_the_agent_s_start_and_not_taken` covers criterion 11.

    Criteria 1 to 11 each have a test that checks what the criterion says. Both sides of every stated limit are tested. The coder's `make check` was green. No marker silences a check, no shell or SQL is built from strings, and the command name stays an argument (`"$2"`), never part of the script. Start facts do not reach `KnownResults`, so a start fact can never be reused as a passed check.

    Findings:
    1. Criterion 12 added: it needs its test. The Interface says each `context` command runs "under its own `time_limit`", and `TaskComposer._start_fact` (`src/factory/pipeline/application/task.py:129`) reads it from `project_commands[command].time_limit`. No test pins the limit that reaches `start_fact`: every test command in `test_stage_context.py` has `time_limit: 1`, and `_SlowCommands` never checks the limit it gets. Fix: the tester adds a test in which two `context` commands with different `time_limit`s each reach `start_fact` with their own (for example, a recording `ProjectCommands` like `RecordingCommands` in `test_stage_finish.py`).
    2. Criterion 13 added: it needs its test. In production the wiring wraps `ContainerMakeCommands` in `RecordingProjectCommands` (`src/factory/entry/wiring.py:327`), so every start fact goes through `RecordingProjectCommands.start_fact` (`src/factory/machine/application/project_commands.py:66-72`). That code writes a `CommandRecord` per start fact, and no test runs it (the coder named this gap in entry 21). Fix: the tester adds a test that a start fact run through `RecordingProjectCommands` reaches the inner `start_fact` and writes its record, as the existing tests of `run` do.
    3. `src/factory/machine/adapters/make_commands.py:101`: the class docstring of `ContainerMakeCommands` still says it "Runs `make sync && make <command>`", but `start_fact` now runs the command without `sync`. Fix: the coder rewrites the docstring so it covers both operations, for example: it runs a project command in a check container on the base with the taken files, after `sync` as a check and without it as a start fact.

    Earlier tests:
    - `tests/machine/application/test_interfaces.py`: the human's leave, entry 15.
    - `tests/pipeline/application/test_stage_finish.py`: the human's leave, entry 15.
    - `tests/pipeline/application/test_stage_time_limited_report.py`: the human's leave, entry 15.
    - `tests/support/preflight_support.py`: the human's leave, entry 15.
    - `tests/pipeline/domain/test_contract.py`: the human's leave, entry 15.
    - `tests/shared/domain/test_contract_version_4.py`: the human's leave, entry 15.
    - `tests/shared/domain/test_contract_version_4_2.py`: the human's leave, entry 15.

    Notes:
    - The two closing criteria are now 14 (`make check`) and 15 (docs).
    - Criterion 8's "operator template" stays in the Interface and the criterion. The human said in entry 15 to read it as void, so it is not a finding.
24. factory: started doing as vm.
25. coder: Fixed the reviewer's finding 3 from entry 23. Findings 1 and 2 add criteria that only need tests, so I hand the item to the tester. `make check` is green (`check: green`).

    What I changed:
    - `src/factory/machine/adapters/make_commands.py`: rewrote the class docstring of `ContainerMakeCommands` so that it covers both operations. It says the class runs a project command in a check container on the base with the taken files. A check runs `make sync && make <command>`. A start fact runs `make <command>` alone, on the base that the stage's preparation has just synced. Nothing else changed in the code.

    For the tester (from entry 23):
    - **Criterion 12:** each `context` command runs under its own `time_limit` from `project_commands`. Add a test where two `context` commands with different `time_limit`s each reach `ProjectCommands.start_fact` with their own limit, for example through a recording `ProjectCommands` like `RecordingCommands` in `tests/pipeline/application/test_stage_finish.py`. The code that reads the limit is `TaskComposer._start_fact` in `src/factory/pipeline/application/task.py`.
    - **Criterion 13:** a start fact run through the wiring's recording project commands is written to the command records, as a check's run is. Add a test that a start fact run through `RecordingProjectCommands.start_fact` (`src/factory/machine/application/project_commands.py`) reaches the inner `start_fact` and writes its `CommandRecord`, as the existing tests of `RecordingProjectCommands.run` do. No test runs this code today.

    The code for both criteria is already in place, so both new tests should pass without a code change.

    Main choice: I fixed the docstring in this round instead of waiting for the tests to come back, because it does not depend on them and the next review round then has only the new tests to read. The alternative was to change no code and end with `tests` alone.

    What the journal changed: criteria 12 and 13 are already in the Description, before the two closing ones. I did not rewrite anything.

    Refactor: the diff is one docstring, so there was nothing to refactor.

    `check`: check: green
26. factory: started tests as vm.
27. tester: Wrote the tests for criteria 12 and 13, which the reviewer added in entry 23 and the coder passed on in entry 25. The code for both was already there, so both tests pass now. One run of the two files gave 13 passed. `make lint` is green. I also ran `make types`, which is green.

    - criterion 12: `tests/pipeline/application/test_stage_context.py::test_each_context_command_runs_under_its_own_time_limit`. Two `context` commands get `time_limit` 1 and 3 in `project_commands`. A `ContainerMakeCommands` subclass (`_LimitNotingCommands`) notes the limit each `start_fact` call receives. The test checks that one command got 1 minute and the other got 3. With both commands, the tests stage still fits its lease: 40 + 5 + 10 + 1 + 3 = 59, under 60.
    - criterion 13: `tests/machine/application/test_recording_start_fact.py::test_a_start_fact_reaches_the_inner_commands_and_is_recorded`. A start fact is run through `RecordingProjectCommands.start_fact` with an inner `ProjectCommands` whose `run` raises. The test checks three things: the inner `start_fact` gets the command and its limit, the whole output comes back, and one `CommandRecord` is written the way a check's run is recorded. The test calls the recorder directly rather than building it through the wiring; it is the same class the wiring puts around the container commands (`src/factory/entry/wiring.py`).
    - The other criteria keep the tests named in entries 8 and 19.

    Files created: `tests/machine/application/test_recording_start_fact.py`.
    Changed: my own `tests/pipeline/application/test_stage_context.py`. `_pipeline` and `_Started.prompt` take an optional `limits` for each command (the default stays 1 minute), and the file gains `_LimitNotingCommands` and the new test. I changed no other story's test.

    Every module imported.

    `lint`: lint: green (0.1 s)

    `lint`: lint: green (0.2 s)
28. factory: started doing as vm.
29. coder: Changed no code this round. The tester's tests from entry 27 cover the two criteria the reviewer added in entry 23, and both pass on the code already in place:
    - criterion 12: `tests/pipeline/application/test_stage_context.py::test_each_context_command_runs_under_its_own_time_limit`
    - criterion 13: `tests/machine/application/test_recording_start_fact.py::test_a_start_fact_reaches_the_inner_commands_and_is_recorded`

    I fixed the reviewer's finding 3 from entry 23, the class docstring of `ContainerMakeCommands`, in entry 25. So all three findings of entry 23 are now dealt with. `make check` is green (`check: green`, coverage 99.21 %).

    Main choice: I handed the item straight to review rather than changing anything more. The new tests pass without code changes, and the round asks only for the findings of the latest entries. The alternative I rejected was another refactor pass. The diff has not changed since the refactor in entry 21, which found nothing to change.

    Noticed, not touched: nothing new. `factory/pipeline.yml` stays at contract 1.0 for the human, and the docs are the documenter's.

    `check`: check: green

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
30. factory: started review as vm.
31. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'` against the work item, without the generated schemas under `src/factory/contract/`. I checked those through the stat and the records contract constant.

    no findings

    The three findings from entry 23 are fixed:
    - Finding 1 (criterion 12): `tests/pipeline/application/test_stage_context.py::test_each_context_command_runs_under_its_own_time_limit` gives two `context` commands the limits 1 and 3. Through `_LimitNotingCommands`, it checks that each limit reaches `start_fact`. That is the value `TaskComposer._start_fact` reads from `project_commands[command].time_limit` (`src/factory/pipeline/application/task.py:129`).
    - Finding 2 (criterion 13): `tests/machine/application/test_recording_start_fact.py::test_a_start_fact_reaches_the_inner_commands_and_is_recorded` covers `RecordingProjectCommands.start_fact`. It checks that the inner `start_fact` gets the command and its limit, that the whole output comes back, and that one `CommandRecord` is written the way `run` writes one. The inner `run` raises, so a start fact can never run as a check.
    - Finding 3: the class docstring of `ContainerMakeCommands` (`src/factory/machine/adapters/make_commands.py:101`) now covers both operations.

    I went through every group again:
    - **Criteria 1 to 13:** each has a test that checks what it says. Both sides of every stated limit are tested: an unknown and a known name, 60,000 and 60,001 characters, a lease that fits and one that is exceeded, contract 1.0 and 1.1, and both kinds of failure.
    - **Architecture:** `ProjectCommands.start_fact` is an `@abstractmethod` whose body is its docstring. The `isinstance` downcast is gone. The command name stays an argument (`"$2"`) and is never part of the script.
    - **Contract:** `RECORDS_CONTRACT` is "4.5" and the schemas were regenerated.
    - **Security:** nothing silences a check.
    - **`make check`:** green after the coder (entry 29).

    description corrected: "in the shipped agent files and the operator template alike" (Interface line and criterion 8) -> "in the shipped `agents/system-prompt.md` and the built-in fallback `SYSTEM_PROMPT` alike". This follows the human's answer in entry 15 that the operator template is void.

    Notes:
    - `tests/pipeline/application/test_stage_context.py` (`_LimitNotingCommands.limits`): the class-level mutable dict holds state across tests. The test resets it before it uses it, but a fixture would make that reset impossible to forget.
    - `tests/machine/application/test_recording_start_fact.py`: the test builds `RecordingProjectCommands` directly and not through `factory.entry.wiring`. It is the same class the wiring puts around `ContainerMakeCommands` (`src/factory/entry/wiring.py:327`).

    Earlier tests:
    - `tests/machine/application/test_interfaces.py`: the human's leave, entry 15.
    - `tests/pipeline/application/test_stage_finish.py`: the human's leave, entry 15.
    - `tests/pipeline/application/test_stage_time_limited_report.py`: the human's leave, entry 15.
    - `tests/support/preflight_support.py`: the human's leave, entry 15.
    - `tests/pipeline/domain/test_contract.py`: the human's leave, entry 15.
    - `tests/shared/domain/test_contract_version_4.py`: the human's leave, entry 15.
    - `tests/shared/domain/test_contract_version_4_2.py`: the human's leave, entry 15.
32. factory: started docs as vm.
33. documenter: Documented the stage key `context` and the start facts. `make documents` ended `documents ok (62.0 s)`. I changed only documents, so I did not run `make check`; the factory's checks after this stage decide.

    Files changed:
    - `docs/project-guide/pipeline.md`: adds `context` to the stage's fields. The lease rule and rule 7's fault table now include `context` (`stage <s>: context <c> is not a project command`). The contract rule notes 1.1 and that 1.0 also loads with `context`. *The prompt* now shows the `<context>` blocks between the role and the facts. The steps of `StageLauncher.launch` now follow the code: prepare, then the start facts and compose, then `run_agent`, with the cost record begun after the start facts. A new section, *Start facts*, covers: where the commands run, their time limits, the command records, that a start fact never reaches `KnownResults`, the rollback before the agent, the 60,000-character cut and its exact line, the `failed:` reasons, escaping, the lease, and a link to the decision.
    - `docs/project-guide/agents.md`: the system prompt's new sentence about `<context>` blocks, that the fallback `SYSTEM_PROMPT` says the same, and where the blocks sit in the first message.
    - `docs/project-guide/machine.md`: adds `ProjectCommands.start_fact` and its `CommandOutput`. `MakeProjectCommands.start_fact`/`run`. `ContainerMakeCommands.start_fact` runs without `sync`, and why. `run_agent` now rolls the dataset back to its base first.
    - `docs/project-guide/work.md` and `docs/operator-guide/records.md`: the records contract is now 4.5 (it was 4.4, which is now stale).
    - `docs/operator-guide/pipeline.md`: a `context` row in the stage keys table, `context` in the lease rule, and a new *Start facts* section with one example (a `diff` project command and its Makefile target) and the size limit, the failure line, the lease and the contract.
    - `docs/decisions.md`: a new entry, "A stage's start facts come from project commands the factory runs": the decision, why (from the Description), and the human's choice of `start_fact` without `sync` (entry 15). It has no "Rejected" line, because the story names no rejected option for the decision as a whole.

    Examples: I ran the operator guide's YAML through `RuamelPipelineDefinitionReader.parse` with `contract: '1.1'`, and it loaded with `context == ['diff']`. I did not run the example Makefile target `diff:` (`git diff --stat develop...HEAD`) inside a stage.

    Cross-read and found current: `docs/project-guide/README.md`, `glossary.md`, the rest of `machine.md` (the `sync` contract line still holds: the sync runs before every check, and start facts are not checks), `docs/operator-guide/README.md`, `agent-runtime.md`, `stops.md`, and the rest of the operator guide's `pipeline.md`. Its smallest definition at `'1.0'` still loads.

    Stale, not touched: nothing unrelated to this story.

    `check`: check: green
    `secrets`: secrets: green (3.2 s)
    `documents`: documents ok (61.4 s)
34. factory: started smoke-test as vm.
35. smoke-tester: I ran the smoke test once from the repository root, exactly as written. It met its `Expect:` line.

    Command 1: `uv run python -c "from factory.pipeline.domain.pipeline_definition import StageDefinition; print('context' in StageDefinition.model_fields)"`
    ```
    Bytecode compiled 4164 files in 50ms
    True
    ```
    Expect: `True`. Met. The line before it is uv's own output when it compiles the bytecode, not the command's output.

    Criteria: I read the acceptance criteria again. The smoke test shows that the stage key `context` exists on `StageDefinition`, and nothing in its output contradicts any criterion. The other criteria are tested by the tests named in entries 8, 19 and 27. `make check` was green after the coder (entry 29). After the docs stage, `make check`, `make secrets` and `make documents` were green (entry 33).

    No findings.
