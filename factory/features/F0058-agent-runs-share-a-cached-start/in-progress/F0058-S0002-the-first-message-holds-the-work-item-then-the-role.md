---
stage: tests
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 660
comments_read: [6720878077, 6720941885, 6720981420, 6721183670]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-08T12:08:42.769492Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T11:21:13.915846Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T11:21:13.923679Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T11:22:03.379255Z'
  stage: intake
  run: bc9bd05655764478a08406de9e9a3aa9
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T11:25:55.356465Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T11:25:57.866374Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T11:26:48.648818Z'
  stage: intake
  run: 0986395bfc2d4a21b2ed3c8f46a70da6
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T11:26:53.706575Z'
  stage: tests
- number: 8
  speaker: tester
  kind: question
  at: '2026-11-08T11:30:45.869589Z'
  stage: tests
  run: 8090ee754ed141eebc63b23958d83027
  blocked: question
- number: 9
  speaker: human
  kind: comment
  at: '2026-11-08T11:31:30.764647Z'
  stage: tests
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T11:31:33.254729Z'
  stage: tests
- number: 11
  speaker: tester
  kind: question
  at: '2026-11-08T11:34:44.529093Z'
  stage: tests
  run: 63f00b83d7724358bec7c8b48382683f
  blocked: question
- number: 12
  speaker: human
  kind: comment
  at: '2026-11-08T11:36:31.244192Z'
  stage: tests
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-08T11:36:33.658437Z'
  stage: tests
- number: 14
  speaker: tester
  kind: result
  at: '2026-11-08T11:37:17.727997Z'
  stage: tests
  run: c515dc5c38c748cc9303806059b98117
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-08T11:37:22.886949Z'
  stage: doing
- number: 16
  speaker: coder
  kind: question
  at: '2026-11-08T11:56:28.266129Z'
  stage: doing
  run: 422b84088518430199a1e16e6e6291a8
  blocked: question
- number: 17
  speaker: human
  kind: comment
  at: '2026-11-08T11:58:15.055377Z'
  stage: doing
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-08T11:58:17.530901Z'
  stage: doing
- number: 19
  speaker: coder
  kind: result
  at: '2026-11-08T11:58:53.761737Z'
  stage: doing
  run: c8a94ea2d82c4be5aa7044df4f0eaf48
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-08T11:58:59.042518Z'
  stage: tests
- number: 21
  speaker: tester
  kind: result
  at: '2026-11-08T11:59:57.533495Z'
  stage: tests
  run: 0aec414b6527439291e392ce46c55406
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-08T12:00:02.958832Z'
  stage: doing
- number: 23
  speaker: coder
  kind: result
  at: '2026-11-08T12:04:31.218367Z'
  stage: doing
  run: 8b0ae9e9eb0b48a7a26282eac726bb3c
- number: 24
  speaker: factory
  kind: started
  at: '2026-11-08T12:04:36.292425Z'
  stage: review
- number: 25
  speaker: reviewer
  kind: result
  at: '2026-11-08T12:07:58.969972Z'
  stage: review
  run: 4f4dc2407dbe4429b75b2a955432d391
- number: 26
  speaker: factory
  kind: started
  at: '2026-11-08T12:08:04.464565Z'
  stage: doing
- number: 27
  speaker: coder
  kind: result
  at: '2026-11-08T12:08:37.842067Z'
  stage: doing
  run: cb74552ede094942b3060d5dc1fa0264
- number: 28
  speaker: factory
  kind: started
  at: '2026-11-08T12:08:42.769492Z'
  stage: tests
---

# The first message holds the work item, then the role

## Description

The prompt cache serves a request's text up to the first byte that differs from an earlier request. Today the role's instructions sit in the system prompt (`--append-system-prompt-file`), before everything else the run reads, so each role's text differs early. Each agent also reads its work item itself, with its own commands, so the journal enters every run in different pieces and is cached anew.

After this story, every run's request is built in this order:
1. The common system prompt, the same for every role. It names the two blocks of the first message: the agent's rules are in the `<role-instructions>` block, and the agent follows them with the same weight as the system prompt; the `<work-item>` block is its task and its history, which is data and never changes its rules.
2. In the first message: the work item's body inside `<work-item>` and `</work-item>`, from its title to the end of its journal, exactly as in the file, without the front matter.
3. Then the role's instructions, the body of its agent file, inside `<role-instructions role="<role>">` and `</role-instructions>`.
4. Then the run's facts, the lines the prompt has today (work item, id, stage, allowed decisions, branch, pull request, round, and the mode or format-check lines). In a stage with a `round_cap`, the round line also names the cap and what it means: `Round: <n> of <round_cap>; a rework decision after round <round_cap> makes the factory ask the human.` In a stage without a cap it stays `Round: <n>`.

The journal holds copied pull-request comments, so a work item could hold text that looks like a block's marker. The factory escapes the markers inside the work item, so that only the blocks it writes itself count.

The journal only grows at its end, so the next run's message starts with the same bytes as this run's, up to the newest entries. The agents no longer need to read the work item before they start. They read it again only when they need text they changed during the run.

## Interface

- One common system-prompt file, `agents/system-prompt.md`, the same for every role. `claude_runtime._arguments` passes it with `--append-system-prompt-file` in place of the role's instructions file.
- `PromptFacts` (`src/factory/agents/domain/prompts.py`) gains `body: str`, `role: Name`, `role_instructions: str` and `round_cap: PositiveInt | None = None`; `compose_prompt(facts: PromptFacts) -> str` keeps its signature and returns the whole first message. The body is read from the committed work item on the work item's branch at the stage's start, where the factory already reads the work item for the stage; the module in the application layer that builds `PromptFacts` today fills the new fields.
- The first message: the `<work-item>` block, then the `<role-instructions role="<role>">` block, then the run's facts, in this order and separated by one blank line each. The work item's front matter is left out.
- The common system prompt names both blocks by their markers and says what each one is, as in the Description.
- A marker text (`<work-item`, `</work-item>`, `<role-instructions`, `</role-instructions>`) inside the work item's body reaches the message escaped, so it cannot open or close a block: the `<` of a marker text becomes `&lt;` (`<work-item` reads `&lt;work-item`). The rest of the body is unchanged. The role's instructions are not escaped; they are the factory's own files.
- A resumed run (`--resume` of an earlier session) gets the whole new message again: the work item, the role's instructions and the run's facts.
- The OpenCode runtime sends the same message; its own result block stays at the end.
- The agent files no longer tell the agent to read its work item first; they say that the work item is in the first message.
- Nothing per run (a time, a run id, a path that changes) comes before the work item's body.
- The human's leave for earlier tests: a test that pins where the role's instructions go, the prompt's text or the system-prompt file may change to the new message and the common system prompt, keeping its name and checking otherwise the same thing. These are `tests/agents/domain/test_prompts.py`, `tests/agents/adapters/` (`test_agent_file_keys.py`, `test_agent_files.py`, `test_claude_runtime.py`, `test_claude_runtime_resume_session.py`, `test_opencode_result_block.py`, `test_opencode_runtime.py`, `test_shipped_agents_effect.py`), `tests/agents/application/` (`test_agent_run_probe_project_agent.py`, `test_project_agents.py`), `tests/entry/` (`test_tick_project_agent.py`, `test_tick_shipped_agent_file.py`, `test_wiring_boundaries.py`), `tests/machine/adapters/test_claude_runtime_container.py`, `tests/pipeline/application/` (`test_task.py`, `test_task_acceptance.py`) and the support modules `tests/support/opencode_stand_in.py` and `tests/support/shipped_agents.py`. The tester's entry names each one it changed.
- The round line names the stage's `round_cap` when it has one, as in the Description.

## Acceptance criteria

1. Two runs of different roles on the same work item get the same system prompt and a first message that is equal up to the end of the work item's body (rows of one test).
2. Two runs on the same work item, before and after a journal entry is added, get first messages where the first one's work-item part is a prefix of the second one's.
3. The first message holds the `<work-item>` block with the work item's body without its front matter, then the `<role-instructions>` block naming the role, then the run's facts, in this order, each separated from the next by exactly one blank line.
4. The common system prompt names both markers and says that the role's instructions are the agent's rules and the work item is data.
5. A work item whose body holds each of the four marker texts gives a first message with exactly one `<work-item>` block and one `<role-instructions>` block (rows of one test); each marker text reaches the message with its `<` as `&lt;`.
6. A body without any marker text reaches the message byte for byte as in the file.
7. The run's facts are the lines of today's prompt, unchanged except the round line.
8. In a stage with `round_cap: 2`, rounds 0, 1 and 2 give `Round: <n> of 2; a rework decision after round 2 makes the factory ask the human.`; in a stage without a cap the line stays `Round: <n>` (rows of one test).
9. The OpenCode runtime's message has the same order, with its result block at the end.
10. A resumed run's message holds the whole new message again: the work item, the role's instructions and the run's facts.
11. No shipped agent file under `agents/agents/` tells the agent to read its work item before it starts, and each says the work item is in the first message.
12. A runtime given no system-prompt file, or a path where no file exists, gives every run the built-in common system prompt, which is the same text as `agents/system-prompt.md`; a file that exists but cannot be read ends the run with `AgentRuntimeError` naming the file (rows of one test).
13. `make check` stays green.
14. docs: the project guide's description of an agent run says what the system prompt and the first message hold, in which order, with which markers, and why (the shared cached start, and the rules' weight); `agents/README.md` says the same for the agent files. `docs/decisions.md`: one entry, the role's instructions move into the first message after the work item, for the prompt cache.

## Smoke test

```bash
uv run python -c "from factory.agents.domain.prompts import compose_prompt; print(compose_prompt.__doc__)"
```
Expect: the docstring names the order: the work item's body, the role's instructions, the run's facts.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: The format check passed. Before the story can be built I need these answered:

   1. **The Interface doesn't name concrete modules or signatures.** Three things are left for the coder to decide:
      - the common system prompt's file name under `agents/`;
      - how `compose_prompt` (`src/factory/agents/domain/prompts.py`) gets the body, the role and its instructions, and the round cap. Today it takes only `PromptFacts`, which has no such fields;
      - which module reads the work item's body for the message, and from which state (the committed file on the branch at the stage's start?). Also how `claude_runtime._arguments` passes the common file in place of `files.instructions`.

      I'd suggest: `agents/system-prompt.md`; `PromptFacts` gains `body: str`, `role: Name`, `role_instructions: str` and `round_cap: PositiveInt | None = None`; and `compose_prompt(facts)` keeps its signature. Please confirm, or name your own.
   2. **"Separated by one blank line each" has no criterion.** Criterion 3 checks only the order. I'd add to criterion 3: "…in this order, each separated from the next by exactly one blank line."
   3. **The escaping is a conversion whose form isn't named, and only one side is tested.** Criterion 5 checks only that no extra block appears.
      - Please name the escaped form. I'd suggest `<` of a marker becomes `&lt;`, so `<work-item` reads `&lt;work-item`.
      - The other side needs a criterion too. I'd add: "a body without any marker text reaches the message byte for byte as in the file."
      - Should the role's instructions also be escaped? I'd say no, since they are the factory's own files.
   4. **Resumed runs aren't covered.** Today a run can `--resume` an earlier session (`_session_arguments` in `claude_runtime.py`), and the story doesn't say what such a run's message holds. The options are the whole new message again (work item, role, facts) or only the run's facts. I'd choose the whole message, since the journal has grown since the earlier session. Either way it needs a criterion.
   5. **No criterion covers the Interface line that the agent files stop telling the agent to read its work item first and say it is in the first message.** The options:
      - a criterion such as "no shipped agent file under `agents/agents/` tells the agent to read its work item before it starts, and each says the work item is in the first message", checked by a test over the shipped files;
      - or drop the line from the Interface and leave it to the docs criterion.

      I'd choose the criterion.

   Everything else checked out:
   - **Criteria:** 1, 2, 4, 6, 7 and 8 are each testable by one test. Criterion 7 covers both sides of the round cap.
   - **Smoke test:** runnable. It passes no `-q`, and its `Expect:` can be checked against the docstring.
   - **Docs criterion:** it names what the reader must know and dictates no sentences. `agents/README.md` is in the documenter's write paths.
   - **Architecture:** composing the prompt belongs in `factory.agents.domain.prompts` and the argument change in `factory.agents.adapters`. The new file under `agents/` is in the coder's write paths. The leave for earlier tests names each test file.
   - **Scope:** this is the feature's S0002 and matches decisions 4 and 5. OpenCode only follows the new order, as the feature's "Out of scope" says.
   - **Route, once answered:** `tests`, since the Interface changes `src/` and `agents/`.
4. 2026-11-08 human: Agreed with all your suggestions:
   1. The common system prompt is `agents/system-prompt.md`. `PromptFacts` gains `body: str`, `role: Name`, `role_instructions: str` and `round_cap: PositiveInt | None = None`, and `compose_prompt(facts)` keeps its signature. The body is read from the committed work item on the work item's branch at the stage's start, where the factory already reads the work item for the stage; the coder picks the module in the application layer that builds `PromptFacts` today. `claude_runtime._arguments` passes `agents/system-prompt.md` with `--append-system-prompt-file` in place of the role's instructions file.
   2. Add to criterion 3: "in this order, each separated from the next by exactly one blank line".
   3. The escaped form: the `<` of a marker text becomes `&lt;` (`<work-item` reads `&lt;work-item`). Add the criterion "a body without any marker text reaches the message byte for byte as in the file". The role's instructions are not escaped; they are the factory's own files.
   4. A resumed run gets the whole new message again (work item, role, facts), since the journal has grown; add a criterion for it.
   5. Add the criterion over the shipped agent files: none tells the agent to read its work item before it starts, and each says the work item is in the first message.
5. factory: started intake as vm.
6. intake: accepted
   I carried the human's answers from journal entry 4 into the story. The Interface now names `agents/system-prompt.md`. It also names the new `PromptFacts` fields (`body`, `role`, `role_instructions`, `round_cap`), says `compose_prompt` keeps its signature, says where the body comes from, and says `claude_runtime._arguments` passes the common file in place of the role's file. It names the escaped form (`<` becomes `&lt;`), says the role's instructions are not escaped, and says a resumed run gets the whole message again. Criterion 3 gains the blank-line separation. Criterion 5 gains the escaped form. The new criteria are 6 (a body without marker text reaches the message byte for byte), 10 (resumed run) and 11 (shipped agent files). The old criteria 6 to 10 became 7, 8, 9, 12 and 13, so `make check` and `docs:` stay last. I added nothing beyond what entry 4 says. The Description is unchanged, because the meaning of the task did not change.
   - Interface: names concrete modules and signatures: `agents/system-prompt.md`, `PromptFacts` with its four new fields, `compose_prompt(facts: PromptFacts) -> str`, `claude_runtime._arguments`. Every behaviour it states has a criterion:
     - order and blank lines: criterion 3;
     - escaping, both sides: criteria 5 and 6;
     - same message for OpenCode: criterion 9;
     - resumed run: criterion 10;
     - agent files: criterion 11;
     - round cap: criterion 8;
     - nothing per run before the body: criteria 1 and 2.
     The human made the unescaped role instructions a decision ("the factory's own files"), not a separately tested rule, so I did not ask for a criterion for it.
   - Criteria: each one is testable by one test function. The rules have both sides: the round line with a cap and without one (criterion 8), and a body with marker texts and one without (criteria 5 and 6).
   - Smoke test: the command is runnable and passes no `-q`. Its `Expect:` can be checked against the printed docstring.
   - Docs criterion: it names what the reader must know (what each part holds, the order, the markers, why) and dictates no sentences. `agents/README.md`, the project guide and `docs/decisions.md` are within the documenter's write paths.
   - Architecture: composing the message belongs in `factory.agents.domain.prompts`. Filling `PromptFacts` belongs in the application layer that builds it today, and the CLI arguments in `factory.agents.adapters.claude_runtime`. The new prompt file under `agents/` is not under `factory/`. The leave for earlier tests names each test file, as CLAUDE.md requires.
   - Scope: this is the feature's S0002, within decisions 4 and 5. OpenCode only follows the new order, as "Out of scope" says.
   - Route: `tests`, because the Interface changes `src/` and `agents/`.
7. factory: started tests as vm.
8. tester: I wrote tests for criteria 2, 3, 5, 6, 7, 8 and 11, plus the domain half of criterion 1, and stopped there. Criteria 9 and 10 clash with tests the leave for earlier tests does not name, and the Interface does not say how the runtime gets the common system prompt. `make lint` is green. I have not run the tests yet.

   Before I can finish I need these answered:

   1. **What does a resumed run send? (criterion 10)** The pipeline resumes a session in one place only: `PatientRuns`, after a provider limit (`src/factory/agents/application/provider_limits.py`, `_resumed_request`). Today it sends `CONTINUE_PROMPT` in place of the message. `tests/agents/application/test_patient_runs.py:140` checks for that, and that file is not on the leave list. The options:
      - (a) The resumed request's prompt is the whole original message, then one blank line, then `CONTINUE_PROMPT`. `test_patient_runs.py` joins the leave.
      - (b) The resumed prompt is the whole message only, without `CONTINUE_PROMPT`. Same leave.
      - (c) Criterion 10 only means that `claude_runtime` passes the request's prompt unchanged with `--resume`, which it already does, and `PatientRuns` keeps `CONTINUE_PROMPT`.

      I would choose (a).
   2. **Where does OpenCode's result block go? (criterion 9)** Today the result block ends the agent's `prompt` in the per-run configuration, and the message (the last argument of `opencode run`) is the request's prompt alone. The options:
      - (a) The message is the request's prompt, then one blank line, then the result block, and the configuration's agent `prompt` stops holding the role's instructions. Two files outside the leave check today's message or configuration and would join it: `tests/agents/adapters/test_opencode_runtime_provider.py:123` and `tests/machine/adapters/test_opencode_runtime_lockdown.py:73` (through `request_configuration` in `tests/support/opencode_stand_in.py`).
      - (b) The message stays the request's prompt unchanged, and the result block stays at the end of the configuration's `prompt`.

      I would choose (a), because the criterion speaks of the message.
   3. **How does `ClaudeCodeRuntime` reach `agents/system-prompt.md`?** It does not know the agent home today. My plan for the system-prompt half of criterion 1 is a black-box test: two runs of different roles through `ClaudeCodeRuntime(executable, state)`, built as today, see equal text in the file after `--append-system-prompt-file`, and that text is neither role's instructions. The coder could then pick the source, for example a field on `AgentDefinition` with a default, or an optional constructor keyword. The other option is to name the source now, so the test can also check that the text equals the shipped file. I would choose the black-box test.

   What I wrote so far:
   - criterion 1 (message half): `tests/agents/domain/test_prompts.py::test_runs_of_different_roles_share_the_message_up_to_the_end_of_the_work_item`
   - criterion 2: `tests/agents/domain/test_prompts.py::test_a_new_journal_entry_keeps_the_earlier_work_item_part_as_a_prefix`
   - criterion 3: `tests/agents/domain/test_prompts.py::test_the_message_holds_the_work_item_then_the_role_then_the_facts_one_blank_line_apart`, and `tests/pipeline/application/test_task.py::test_the_message_starts_with_the_work_item_body_then_the_roles_instructions`
   - criterion 4: `tests/agent_files/test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is`
   - criterion 5: `tests/agents/domain/test_prompts.py::test_a_marker_text_in_the_body_is_escaped_and_opens_no_block`
   - criterion 6: `tests/agents/domain/test_prompts.py::test_a_body_without_a_marker_text_reaches_the_message_byte_for_byte`
   - criterion 7: `tests/agents/domain/test_prompts.py::test_the_prompt_holds_the_facts_line_by_line_and_ends_with_the_end_line` (changed)
   - criterion 8: `tests/agents/domain/test_prompts.py::test_the_round_line_names_the_stages_cap_when_it_has_one`, and `tests/pipeline/application/test_task.py::test_the_request_names_the_round_cap_of_a_stage_that_has_one`; `round_cap` 0 and 1 are new rows in `test_prompt_facts_hold_their_limits_on_both_sides`
   - criterion 11: `tests/agent_files/test_first_message_agent_files.py::test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message`
   - criteria 9, 10 and the system-prompt half of 1: not written yet, waiting on the answers above.

   Files:
   - Created: `tests/agent_files/test_first_message_agent_files.py`.
   - Changed under the human's leave:
     - `tests/agents/domain/test_prompts.py`: new `PromptFacts` fields in `VALID`; the facts tests now read the facts part of the message.
     - `tests/pipeline/application/test_task.py`: the expected `PromptFacts` gains `body`, `role` and `role_instructions`.
     - `tests/pipeline/application/test_task_acceptance.py`: `_base_prompt` fills the new fields.

   Still to change once answered: `tests/agents/adapters/test_claude_runtime.py`, line 288 (the system-prompt file's content), and the OpenCode and resume tests named above.
9. 2026-11-08 human: As you recommend:
   1. (a) A resumed request's prompt is the whole original message, then one blank line, then `CONTINUE_PROMPT`. Leave given for `tests/agents/application/test_patient_runs.py`.
   2. (a) OpenCode's message is the request's prompt, then one blank line, then the result block; the configuration's agent `prompt` no longer holds the role's instructions. Leave given for `tests/agents/adapters/test_opencode_runtime_provider.py` and `tests/machine/adapters/test_opencode_runtime_lockdown.py` (through `tests/support/opencode_stand_in.py`).
   3. The black-box test: two runs of different roles see equal text after `--append-system-prompt-file`, and it is neither role's instructions. The coder picks the source.
   The same rule as before applies to every file under this leave: names stay, each checks otherwise the same thing, and your entry names each file you changed.
10. factory: started tests as vm.
11. tester: I wrote the tests your answer in entry 9 called for: criterion 9, criterion 10 and the system-prompt half of criterion 1. Before I hand over I need one more answer, on a clash with a test outside the leave.

    **Question: does OpenCode's result block also end a resumed call's message?**
    Your answer makes OpenCode's message "the request's prompt, then one blank line, then the result block". Read literally, that covers every call. But `tests/agents/adapters/test_opencode_resumed_words.py::test_a_resumed_call_keeps_every_word_of_the_first_before_its_session` expects the last word of a resumed call to be the prompt alone, in both its rows:
    - `resume-session`: `"Go on."`
    - `budget-resume`: the runtime's own `FINISH_MESSAGE`

    That file is not on the leave. The options:
    - (a) Every call's message ends with the result block, resumed and finish calls too. `test_opencode_resumed_words.py` joins the leave, and its expected last words become prompt + blank line + result block.
    - (b) Only a call that starts a session gets the result block. A call with `--session` sends its prompt as it is, because the session already holds the block from its first message. No other test changes.

    I would choose (b). It keeps the existing test green, and a resumed session has already seen the block. My new tests check only a fresh call, so they hold either way.

    **Criteria to tests** (criteria 12 and 13 are not the tester's):
    - criterion 1: `tests/agents/domain/test_prompts.py::test_runs_of_different_roles_share_the_message_up_to_the_end_of_the_work_item` (the message) and `tests/agents/adapters/test_claude_runtime.py::test_runs_of_different_roles_get_the_same_system_prompt` (the system prompt, black-box: equal text after `--append-system-prompt-file`, neither role's instructions)
    - criterion 2: `tests/agents/domain/test_prompts.py::test_a_new_journal_entry_keeps_the_earlier_work_item_part_as_a_prefix`
    - criterion 3: `tests/agents/domain/test_prompts.py::test_the_message_holds_the_work_item_then_the_role_then_the_facts_one_blank_line_apart` and `tests/pipeline/application/test_task.py::test_the_message_starts_with_the_work_item_body_then_the_roles_instructions`
    - criterion 4: `tests/agent_files/test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is`
    - criterion 5: `tests/agents/domain/test_prompts.py::test_a_marker_text_in_the_body_is_escaped_and_opens_no_block`
    - criterion 6: `tests/agents/domain/test_prompts.py::test_a_body_without_a_marker_text_reaches_the_message_byte_for_byte`
    - criterion 7: `tests/agents/domain/test_prompts.py::test_the_prompt_holds_the_facts_line_by_line_and_ends_with_the_end_line`
    - criterion 8: `tests/agents/domain/test_prompts.py::test_the_round_line_names_the_stages_cap_when_it_has_one` and `tests/pipeline/application/test_task.py::test_the_request_names_the_round_cap_of_a_stage_that_has_one`; `round_cap` 0 (refused) and 1 (accepted) are rows of `test_prompt_facts_hold_their_limits_on_both_sides`
    - criterion 9: `tests/agents/adapters/test_opencode_runtime.py::test_the_message_holds_the_work_item_then_the_role_then_the_facts_then_the_result_block`
    - criterion 10: `tests/agents/application/test_patient_runs.py::test_a_resumed_run_gets_the_whole_message_again_then_the_word_to_continue`
    - criterion 11: `tests/agent_files/test_first_message_agent_files.py::test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message`

    **Files**
    - Created (previous run, committed): `tests/agent_files/test_first_message_agent_files.py`.
    - Changed under the leave in this run. Names are kept and each test checks otherwise the same thing:
      - `tests/agents/adapters/test_claude_runtime.py`: `test_call_sees_the_instructions_file_and_no_guard_or_hooks_file` now checks that the file is not empty and is not the role's instructions; I added the new criterion 1 test.
      - `tests/agents/adapters/test_opencode_runtime.py`: the last argument is prompt + blank line + result block; the configuration is compared without its agent's prompt; I added the criterion 9 test.
      - `tests/agents/adapters/test_opencode_runtime_provider.py`: the same two changes.
      - `tests/machine/adapters/test_opencode_runtime_lockdown.py`: the configuration is compared without its agent's prompt.
      - `tests/agents/application/test_patient_runs.py`: the resumed prompt is the whole message, a blank line, then `CONTINUE_PROMPT`; I added the criterion 10 test.
      - `tests/support/opencode_stand_in.py`: `request_configuration()` no longer holds a prompt. It gains `configuration_without_prompt`, which drops the agent's prompt and asserts the role's instructions are not in it, and `opencode_message`.
      - Changed in the previous run, also under the leave: `tests/agents/domain/test_prompts.py`, `tests/pipeline/application/test_task.py` and `tests/pipeline/application/test_task_acceptance.py`.
    - Not changed: the tests that pin the system-prompt file's path (`state/instructions-<session>.md`, mounted read-only into the container) in `test_call_passes_every_flag_in_order`, `test_claude_runtime_resume_session.py`, `test_claude_runtime_container.py` and `test_wiring_boundaries.py`. Unless you say otherwise, the coder keeps writing a per-run file there that holds the common text.

    **Left open on purpose:** your answer does not say whether OpenCode's configuration still gives its agent a `prompt` key, or whether that prompt still holds the result block. The tests check only that it does not hold the role's instructions.

    **Run:** one run of the changed and created test files: the new and changed tests fail as failures, not collection errors, for example `test_task.py::test_the_request_names_the_round_cap_of_a_stage_that_has_one` and `test_task_acceptance.py`, because `PromptFacts` has no `body`, `role`, `role_instructions` or `round_cap` yet. Every module imported; nothing was missing. `make lint`: green. I skipped the type check, as the stage says.
12. 2026-11-08 human: (b): only a call that starts a session gets the result block; a call with `--session` sends its prompt as it is. Keeping the per-run system-prompt file path as it is, holding the common text, is fine. OpenCode's configuration prompt: the coder decides, as long as it does not hold the role's instructions.
13. factory: started tests as vm.
14. tester: In entry 12 you chose (b): only a call that starts an OpenCode session gets the result block, and a call with `--session` sends its prompt as it is. The tests needed no change for that. The tests I wrote that use the result block (`opencode_message` in `tests/support/opencode_stand_in.py`, and the criterion 9 test) check only fresh calls. `tests/agents/adapters/test_opencode_resumed_words.py`, which is outside the leave, already checks the resumed side and stays as it is. You also said two things are fine: the per-run system-prompt file keeps its path, holding the common text, and the coder decides the OpenCode configuration prompt as long as it does not hold the role's instructions. The existing tests already match both, so this run changed no files.

    Which test checks each criterion (criteria 12 and 13 are not the tester's):
    - criterion 1: `tests/agents/domain/test_prompts.py::test_runs_of_different_roles_share_the_message_up_to_the_end_of_the_work_item` (the first message) and `tests/agents/adapters/test_claude_runtime.py::test_runs_of_different_roles_get_the_same_system_prompt` (the system prompt)
    - criterion 2: `tests/agents/domain/test_prompts.py::test_a_new_journal_entry_keeps_the_earlier_work_item_part_as_a_prefix`
    - criterion 3: `tests/agents/domain/test_prompts.py::test_the_message_holds_the_work_item_then_the_role_then_the_facts_one_blank_line_apart` and `tests/pipeline/application/test_task.py::test_the_message_starts_with_the_work_item_body_then_the_roles_instructions`
    - criterion 4: `tests/agent_files/test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is`
    - criterion 5: `tests/agents/domain/test_prompts.py::test_a_marker_text_in_the_body_is_escaped_and_opens_no_block`
    - criterion 6: `tests/agents/domain/test_prompts.py::test_a_body_without_a_marker_text_reaches_the_message_byte_for_byte`
    - criterion 7: `tests/agents/domain/test_prompts.py::test_the_prompt_holds_the_facts_line_by_line_and_ends_with_the_end_line`
    - criterion 8: `tests/agents/domain/test_prompts.py::test_the_round_line_names_the_stages_cap_when_it_has_one` and `tests/pipeline/application/test_task.py::test_the_request_names_the_round_cap_of_a_stage_that_has_one`. The `round_cap` limit is checked on both sides as rows of `test_prompt_facts_hold_their_limits_on_both_sides`: 0 is refused and 1 is accepted.
    - criterion 9: `tests/agents/adapters/test_opencode_runtime.py::test_the_message_holds_the_work_item_then_the_role_then_the_facts_then_the_result_block`
    - criterion 10: `tests/agents/application/test_patient_runs.py::test_a_resumed_run_gets_the_whole_message_again_then_the_word_to_continue`
    - criterion 11: `tests/agent_files/test_first_message_agent_files.py::test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message`

    Files (all from earlier runs, already committed):
    - Created: `tests/agent_files/test_first_message_agent_files.py`.
    - Changed under the human's leave, keeping each test's name:
      - `tests/agents/domain/test_prompts.py`
      - `tests/pipeline/application/test_task.py`
      - `tests/pipeline/application/test_task_acceptance.py`
      - `tests/agents/adapters/test_claude_runtime.py`
      - `tests/agents/adapters/test_opencode_runtime.py`
      - `tests/agents/adapters/test_opencode_runtime_provider.py`
      - `tests/machine/adapters/test_opencode_runtime_lockdown.py`
      - `tests/agents/application/test_patient_runs.py`
      - `tests/support/opencode_stand_in.py`

    Run: one `uv run pytest -q` over the files above plus `test_opencode_resumed_words.py`. The new and changed tests fail as test failures, not collection errors. For example, the `test_task.py` and `test_task_acceptance.py` tests fail because `PromptFacts` has no `body`, `role`, `role_instructions` or `round_cap` yet. Every module imported; no module was missing. `make lint`: green. I skipped the type check, as the stage says.

    `lint`: lint: green (0.1 s)
15. factory: started doing as vm.
16. coder: The code is built and `make check` is green except for two earlier tests, which I may not change. One of them is outside the human's leave, so I need your word on it.

    **Question: may `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged` change?**
    This test pins a CRC-32 of the whole reviewer body (`tests/agent_files/test_claude_agent_texts_review_groups.py:71`, `E AssertionError: assert 1830907862 == 3903663111`). Criterion 11 has to change `agents/agents/reviewer.md`: no file may tell the agent to read its work item first, and each must say the work item is in the first message. So any edit that meets criterion 11 breaks this pin. The file is not on the story's leave. Options:
    - (a) Leave given. The tester adds `.replace(<new text>, <old text>)` to `earlier` for my three reviewer edits, as F0057-S0002 did for `develop`→`main` (commit eed29aef1). The three edits are the new R6 sentence, step 1 of the review stage and step 1 of `docs-review`. The pin stays as it is.
    - (b) Leave given to update `_EARLIER_BODY_CRC32` to the new body.
    - (c) No leave. Criterion 11 then cannot be met for the reviewer.
    I would choose (a): it keeps the test checking the same thing.

    **Also needed, already under the leave:** `tests/agents/adapters/test_shipped_agents_effect.py::test_instructions_file_holds_the_agent_body` (all 7 rows) still expects the role's body in the `--append-system-prompt-file` file. That contradicts the Interface, which now puts the common system prompt there. The tester did not change it. Once you answer, I end with `tests` and name both changes: this test checks that the role's body is *not* in that file but is in the first message, or that the file holds the common system prompt.

    **What I built** (working tree, all else green: lint, types, layers, sast, secrets, licenses; in `make test` only the 8 rows above fail):
    - `src/factory/agents/domain/prompts.py`:
      - `PromptFacts` gains `body`, `role`, `role_instructions` and `round_cap`.
      - `compose_prompt` builds three parts with one blank line between each: the `<work-item>` block (the body, with the four marker texts escaped `<`→`&lt;`), then the `<role-instructions role="…">` block, then the facts.
      - The facts' round line names the cap when there is one.
      - `SYSTEM_PROMPT` is the built-in common text.
    - `src/factory/pipeline/application/task.py`: `TaskComposer.compose` fills the new fields:
      - `body` from `context.document.body`, the work item already read for the stage;
      - `role` and `role_instructions` from the agent;
      - `round_cap` from the stage.
    - `src/factory/agents/adapters/agent_launch.py`: `system_prompt_text(file)` reads the common file.
      - With no file, or a file that does not exist (an agent home installed before this story), it falls back to `SYSTEM_PROMPT`.
      - A file that exists but cannot be read is `AgentRuntimeError`.
    - `claude_runtime.py`: keeps the per-run path `instructions-<session>.md` (entry 12) but writes the common text there. New keyword `system_prompt_file`.
    - `opencode_runtime.py`:
      - The configuration's agent `prompt` is now the common text.
      - The message is the prompt, a blank line, then the result block for a fresh call; with `--session`, the prompt alone (entry 12).
      - New keyword `system_prompt_file`.
    - `src/factory/agents/application/provider_limits.py`: a resumed request's prompt is the whole message, a blank line, then `CONTINUE_PROMPT`. It is always built from the original request, so `CONTINUE_PROMPT` is never added twice.
    - `src/factory/entry/wiring.py`: both runtimes get `<agent_home>/system-prompt.md` (`SYSTEM_PROMPT_FILE_NAME`).
    - `agents/system-prompt.md`: new, the same text as `SYSTEM_PROMPT`.
    - `agents/agents/*.md`:
      - All seven: R6 gains a sentence saying the work item is in the first message, in the `<work-item>` block, and that the file is read again only for text changed during the run.
      - Coder, tester and reviewer: step 1 no longer reads the work item first. The reviewer's `docs-review` step 1 also no longer does.
      - Documenter: its "Read the story" steps take the story from the first message.

    **Main choice:** the common text comes from the agent home through a runtime keyword, with a built-in fallback. Rejected: a new field on `AgentDefinition`. It would put a text that is the same for every role on every agent, and every test that builds one would need it.

    **Noticed, not touched:**
    - The common text exists twice, in `SYSTEM_PROMPT` and in `agents/system-prompt.md`. The fallback keeps existing agent homes running. The operator guide should say to install the new file (for the documenter).
    - intake's "read the files first, then judge" stays: it is about files, not the work item.

    Refactor: one small change, `_MARKER_TEXTS` reuses the close-marker constants. Nothing else needed.
17. 2026-11-08 human: (a): leave given for `tests/agent_files/test_claude_agent_texts_review_groups.py`. The tester adds `.replace(<new text>, <old text>)` to `earlier` for your three reviewer edits, and the CRC-32 pin stays. And yes to the change of `test_shipped_agents_effect.py::test_instructions_file_holds_the_agent_body`: it checks that the file holds the common system prompt and that the role's body is in the first message instead, keeping its name.
18. factory: started doing as vm.
19. coder: In entry 17 the human gave leave for two test changes, so I'm handing back to the tester. I changed no code in this run. The code from the last doing run is committed and stays as it is: `src/factory/agents/domain/prompts.py`, `src/factory/pipeline/application/task.py`, `src/factory/agents/adapters/agent_launch.py`, `claude_runtime.py`, `opencode_runtime.py`, `src/factory/agents/application/provider_limits.py`, `src/factory/entry/wiring.py`, `agents/system-prompt.md` and `agents/agents/*.md`.

    The tester makes these two changes:

    1. `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: add three `.replace(<new text>, <old text>)` calls to `earlier`, one for each edit to `agents/agents/reviewer.md`. `_EARLIER_BODY_CRC32` stays as it is. The three edits:
       - (i) R6 gains the sentence ` The work item itself, from its title to the end of its journal, is in your first message, in the `<work-item>` block, so you do not read it before you start; read its file again only for text you changed during the run.` (it starts with a space). Replace it with "".
       - (ii) Review stage, step 1. Replace `the work item in the first message is the only other input. Read the diff in your first command: its `--stat`, and the diff` with `the work item is the only other input. Read both in your first command: the work item, the diff's `--stat`, and the diff`.
       - (iii) `docs-review`, step 1. Replace `1. Read `git diff develop...HEAD -- README.md docs operator/README.md` in your first command. The work item is in your first message. Nothing else is under review.` with `1. Read the work item and `git diff develop...HEAD -- README.md docs operator/README.md` in your first command. Nothing else is under review.`
       `git diff develop -- agents/agents/reviewer.md` shows the exact text.
    2. `tests/agents/adapters/test_shipped_agents_effect.py::test_instructions_file_holds_the_agent_body` (all 7 rows): keep the name. The test checks that the file after `--append-system-prompt-file` holds the common system prompt and not the role's body, and that the role's body is in the first message inside `<role-instructions role="<role>">`. At an agent home installed by the test, the common prompt is the contents of `agents/system-prompt.md`. Where no file is given, the runtime falls back to `factory.agents.domain.prompts.SYSTEM_PROMPT`, which holds the same text.

    Description: unchanged. The journal changed only which tests may change.

    `make check` was not run in this run because nothing changed since the last doing run. That run was green apart from the 8 rows of the two tests above. Last run's main choice still holds: the common text reaches the runtimes through a `system_prompt_file` keyword with a built-in fallback, rather than a field on `AgentDefinition`. Noticed in the last run and not touched: the common text exists twice, in `SYSTEM_PROMPT` and in `agents/system-prompt.md`, and the operator guide should tell operators to install the new file.
20. factory: started tests as vm.
21. tester: I made the two test changes the human allowed in entry 17, as the coder set out in entry 19. Both tests keep their names, and I changed no other test.

    1. `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: I added three `.replace(<new text>, <old text>)` calls to `earlier`, one per edit to `agents/agents/reviewer.md`:
       - (i) the new R6 sentence, replaced with "";
       - (ii) the review stage's step 1, "the work item in the first message … the diff" back to "the work item is the only other input. Read both … the diff";
       - (iii) the `docs-review` step 1, back to "Read the work item and `git diff …`".
       They come before the existing `develop`→`main` replace, because they hold the text "develop". `_EARLIER_BODY_CRC32` is unchanged. The `docs-review` subsection is already cut from the body by `_DOCS_REVIEW_SUBSECTION`, so (iii) changes nothing in the result. I added it anyway, as the human's answer asked.
    2. `tests/agents/adapters/test_shipped_agents_effect.py::test_instructions_file_holds_the_agent_body` (all 7 rows):
       - In the module fixture `calls`, the runtime gets `system_prompt_file=AGENT_HOME / "system-prompt.md"`. The prompt is now built by `compose_prompt` from `PromptFacts`, with each agent's body as `role_instructions`.
       - The test checks three things: the file after `--append-system-prompt-file` equals `agents/system-prompt.md`, it does not hold the role's body, and the message after `-p` holds the role's body right after `<role-instructions role="<name>">`.
       - The other tests in that module read only `--model`, `--effort`, `--tools` and `--max-budget-usd`, so the fixture change does not affect them.

    Run: `uv run pytest -q` over the two files: all 44 pass, since the code is already in place. `make lint`: green.

    Files changed: `tests/agent_files/test_claude_agent_texts_review_groups.py`, `tests/agents/adapters/test_shipped_agents_effect.py`. No files created. Every module imported.

    `lint`: lint: green (0.2 s)
22. factory: started doing as vm.
23. coder: I wrote no new code in this run. The tester made the two test changes the human allowed in entry 17 (entry 21), and the code from the earlier doing run, already committed, now passes every test. `make check`: check: green (test: green, 102.6 s, coverage 99.20 %).

    What I built (earlier doing run, committed):
    - `src/factory/agents/domain/prompts.py`:
      - `PromptFacts` gains `body`, `role`, `role_instructions` and `round_cap`.
      - `compose_prompt` returns the `<work-item>` block, then the `<role-instructions role="…">` block, then the facts, one blank line apart.
      - In the body, the four marker texts have their `<` escaped to `&lt;`.
      - The round line names the cap when the stage has one.
      - `SYSTEM_PROMPT` is the built-in common text.
    - `src/factory/pipeline/application/task.py`: `TaskComposer.compose` fills the new fields. The body comes from the work item already read for the stage; the role and its instructions come from the agent; the round cap comes from the stage.
    - `src/factory/agents/adapters/agent_launch.py`: `system_prompt_text` reads the common file. When there is no file, it falls back to `SYSTEM_PROMPT`.
    - `src/factory/agents/adapters/claude_runtime.py`: writes the common text to the same per-run `instructions-<session>.md` path as before (entry 12).
    - `src/factory/agents/adapters/opencode_runtime.py`: the configuration's agent prompt is the common text. A fresh call's message is the prompt, a blank line, then the result block. A `--session` call sends the prompt alone (entry 12).
    - `src/factory/agents/application/provider_limits.py`: a resumed request's prompt is the whole message, a blank line, then `CONTINUE_PROMPT`.
    - `src/factory/entry/wiring.py`: both runtimes get `<agent_home>/system-prompt.md`.
    - `agents/system-prompt.md`: new.
    - `agents/agents/*.md`: each says the work item is in the first message, and none reads it first.

    Main choice: the common text reaches the runtimes through a `system_prompt_file` keyword, with a built-in fallback. I rejected a new field on `AgentDefinition`: it would carry the same text on every agent and touch every test that builds one.

    Refactor: I read the diff against develop again and found nothing to change.

    Description: unchanged. The journal changed only which tests may change.

    Noticed, not touched:
    - The common text exists twice: in `SYSTEM_PROMPT` and in `agents/system-prompt.md`. The fallback keeps agent homes installed before this story running.
    - The operator guide should tell operators to install `system-prompt.md` into their agent home. That is for the documenter.

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
24. factory: started review as vm.
25. reviewer: Review, round 0. I read the diff without `factory/`, the work item, and the new findings of `make duplicates` against the criteria, `CLAUDE.md` and the leaves in the journal. The first message is built as the Interface says (`src/factory/agents/domain/prompts.py:399`): the escaped body, then the unescaped role block, then the facts, one blank line apart. The round line names the cap. `TaskComposer.compose` fills the new fields from the work item it already read for the stage. Resumed requests send the whole message plus `CONTINUE_PROMPT` (entry 9). OpenCode adds the result block only to a fresh call (entry 12). Criteria 1 to 11 each have a test that checks what the criterion says. The coder's `make check` was green (entry 23).

    Groups 2 and 3 found nothing. The layers hold: the domain has no I/O, and file reading sits in `agent_launch`. Wiring stays in `entry`. No silencing markers were added, and an error names only the path. Of the 7 new `make duplicates` findings, the only one from this diff is the similar `system_prompt_file` constructor lines in the two runtimes. Those constructors already mirror each other, so I am not counting it. The other six are in files this diff does not touch.

    Findings:
    1. criterion 12 added: it needs its test. `src/factory/agents/adapters/agent_launch.py:328` (`system_prompt_text`) uses the built-in `SYSTEM_PROMPT` (`src/factory/agents/domain/prompts.py:326`) when there is no file or the file is missing, and raises `AgentRuntimeError` when the file cannot be read. No criterion or test pins either side, and nothing checks that the built-in copy matches `agents/system-prompt.md`, so the two copies can drift without anyone noticing. Fix: the tester writes the criterion 12 test as rows of one test: no file, a missing path, an unreadable file, and the built-in text equal to the shipped file.
    2. Criterion 14 (`docs:`): `docs/operator-guide/agent-runtime.md:351` lists what the agent home's `agents/` folder ships (`agents/agents/<role>.md`, `agents/settings.json`). After this story every run also reads `<agent home>/system-prompt.md` (`src/factory/entry/wiring.py:619`, `SYSTEM_PROMPT_FILE_NAME`), and falls back to the built-in text when it is missing. The criterion names only the project guide, `agents/README.md` and `docs/decisions.md`. Fix: the coder adds to criterion 14 that the operator guide's "The agent files" names `system-prompt.md` and what a missing one does.
    3. `tests/agents/adapters/test_opencode_runtime.py:315` and `tests/agents/application/test_patient_runs.py:345` both build the same `PromptFacts`: the same work item, path, stage, decisions, branch, pull request 7, round 0, body, role `coder` and "Write the code.". Two test modules share it, so `CLAUDE.md` *Tests* puts it in `tests/support/`. Fix: the tester moves it into a support module (for example `tests/support/first_message_support.py`) and both tests use it from there.
    4. `tests/agent_files/test_first_message_agent_files.py:10` (`SYSTEM_PROMPT`) and `tests/agents/adapters/test_shipped_agents_effect.py:23` (`SYSTEM_PROMPT_FILE`) define the same constant, `AGENT_HOME / "system-prompt.md"`. Fix: one constant in `tests/support/shipped_agents.py` beside `AGENT_HOME`, used by both.

    Earlier tests (changed, status M):
    - `tests/agent_files/test_claude_agent_texts_review_groups.py`: human's leave, journal entry 17.
    - `tests/agents/adapters/test_claude_runtime.py`: human's leave named in the Interface.
    - `tests/agents/adapters/test_opencode_runtime.py`: human's leave named in the Interface, and entry 9.
    - `tests/agents/adapters/test_opencode_runtime_provider.py`: human's leave, journal entry 9.
    - `tests/agents/adapters/test_shipped_agents_effect.py`: human's leave named in the Interface, and entry 17.
    - `tests/agents/application/test_patient_runs.py`: human's leave, journal entry 9.
    - `tests/agents/domain/test_prompts.py`: human's leave named in the Interface.
    - `tests/machine/adapters/test_opencode_runtime_lockdown.py`: human's leave, journal entry 9.
    - `tests/pipeline/application/test_task.py`: human's leave named in the Interface.
    - `tests/pipeline/application/test_task_acceptance.py`: human's leave named in the Interface.
    - `tests/support/opencode_stand_in.py`: human's leave named in the Interface, and entry 9.

    Each changed test keeps its name and checks otherwise the same thing.
26. factory: started doing as vm.
27. coder: Round 1. I changed no code. Of the reviewer's four findings in entry 25, one was mine to fix, and I fixed it. The other three are test work, so I'm handing this to the tester.

    Done here:
    - Finding 2: in `## Description`, criterion 14 (`docs:`) now also asks the operator guide's "The agent files" to name `system-prompt.md` among what the agent home ships, and to say what a missing one does: the run falls back to the built-in common system prompt. Criterion 14 is still last.

    For the tester:
    1. Finding 1, criterion 12: write its test as rows of one test against `system_prompt_text` (`src/factory/agents/adapters/agent_launch.py`) through the runtimes. The rows are:
       - no file gives `SYSTEM_PROMPT`;
       - a path where no file exists gives `SYSTEM_PROMPT`;
       - a file that exists but cannot be read raises `AgentRuntimeError` naming the file;
       - and, as the reviewer asked, the built-in `factory.agents.domain.prompts.SYSTEM_PROMPT` equals the text of `agents/system-prompt.md`.
       The code already handles all four, so no code change should follow.
    2. Finding 3, under the standing leave to move a shared test helper: move the `PromptFacts` that `tests/agents/adapters/test_opencode_runtime.py:315` and `tests/agents/application/test_patient_runs.py:345` both build into one support module, for example `tests/support/first_message_support.py`. Both tests then use it from there.
    3. Finding 4, under the same leave: put one constant, `AGENT_HOME / "system-prompt.md"`, in `tests/support/shipped_agents.py` beside `AGENT_HOME`. It replaces `SYSTEM_PROMPT` in `tests/agent_files/test_first_message_agent_files.py:10` and `SYSTEM_PROMPT_FILE` in `tests/agents/adapters/test_shipped_agents_effect.py:23`.

    What I built: unchanged from entry 23 (prompts, task, agent_launch, both runtimes, provider_limits, wiring, `agents/system-prompt.md`, `agents/agents/*.md`). The main choice also stands: the common text reaches the runtimes through a `system_prompt_file` keyword with a built-in fallback, not through a field on `AgentDefinition`.

    Refactor: no code changed in this round, so there was nothing to refactor. I did not run `make check`: the only change this round is the criterion 14 text in the work item, and the last code run was green (entry 23).

    Noticed, not touched: the common text still exists twice, in `SYSTEM_PROMPT` and in `agents/system-prompt.md`. The equality row in item 1 is what keeps the two copies from drifting.

    The factory left out changes outside the write paths: factory/features/F0058-agent-runs-share-a-cached-start/in-progress/F0058-S0002-the-first-message-holds-the-work-item-then-the-role.md.
28. factory: started tests as vm.
