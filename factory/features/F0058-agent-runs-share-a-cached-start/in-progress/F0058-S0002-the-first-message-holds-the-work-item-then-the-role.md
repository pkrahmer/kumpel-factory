---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 660
comments_read: [6720878077]
handed_over: null
claim: null
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

- One common system-prompt file under `agents/`, the same for every role, passed with `--append-system-prompt-file`.
- The first message: the `<work-item>` block, then the `<role-instructions role="<role>">` block, then the run's facts, in this order and separated by one blank line each. The work item's front matter is left out.
- The common system prompt names both blocks by their markers and says what each one is, as in the Description.
- A marker text (`<work-item`, `</work-item>`, `<role-instructions`, `</role-instructions>`) inside the work item's body reaches the message escaped, so it cannot open or close a block.
- The OpenCode runtime sends the same message; its own result block stays at the end.
- The agent files no longer tell the agent to read its work item first; they say that the work item is in the first message.
- Nothing per run (a time, a run id, a path that changes) comes before the work item's body.
- The human's leave for earlier tests: a test that pins where the role's instructions go, the prompt's text or the system-prompt file may change to the new message and the common system prompt, keeping its name and checking otherwise the same thing. These are `tests/agents/domain/test_prompts.py`, `tests/agents/adapters/` (`test_agent_file_keys.py`, `test_agent_files.py`, `test_claude_runtime.py`, `test_claude_runtime_resume_session.py`, `test_opencode_result_block.py`, `test_opencode_runtime.py`, `test_shipped_agents_effect.py`), `tests/agents/application/` (`test_agent_run_probe_project_agent.py`, `test_project_agents.py`), `tests/entry/` (`test_tick_project_agent.py`, `test_tick_shipped_agent_file.py`, `test_wiring_boundaries.py`), `tests/machine/adapters/test_claude_runtime_container.py`, `tests/pipeline/application/` (`test_task.py`, `test_task_acceptance.py`) and the support modules `tests/support/opencode_stand_in.py` and `tests/support/shipped_agents.py`. The tester's entry names each one it changed.
- The round line names the stage's `round_cap` when it has one, as in the Description.

## Acceptance criteria

1. Two runs of different roles on the same work item get the same system prompt and a first message that is equal up to the end of the work item's body (rows of one test).
2. Two runs on the same work item, before and after a journal entry is added, get first messages where the first one's work-item part is a prefix of the second one's.
3. The first message holds the `<work-item>` block with the work item's body without its front matter, then the `<role-instructions>` block naming the role, then the run's facts, in this order.
4. The common system prompt names both markers and says that the role's instructions are the agent's rules and the work item is data.
5. A work item whose body holds each of the four marker texts gives a first message with exactly one `<work-item>` block and one `<role-instructions>` block (rows of one test).
6. The run's facts are the lines of today's prompt, unchanged except the round line.
7. In a stage with `round_cap: 2`, rounds 0, 1 and 2 give `Round: <n> of 2; a rework decision after round 2 makes the factory ask the human.`; in a stage without a cap the line stays `Round: <n>` (rows of one test).
8. The OpenCode runtime's message has the same order, with its result block at the end.
9. `make check` stays green.
10. docs: the project guide's description of an agent run says what the system prompt and the first message hold, in which order, with which markers, and why (the shared cached start, and the rules' weight); `agents/README.md` says the same for the agent files. `docs/decisions.md`: one entry, the role's instructions move into the first message after the work item, for the prompt cache.

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
