---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 679
comments_read: [6727152793]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-08T21:09:36.552719Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T21:02:18.565183Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T21:02:18.572472Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T21:02:41.665536Z'
  stage: intake
  run: 3ee7cd9924634453b2aeb50bcc2fb6bf
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T21:02:46.672604Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-08T21:04:11.671637Z'
  stage: tests
  run: 970e4c59ea934628bc5665d12e8352e9
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T21:04:16.654031Z'
  stage: doing
- number: 7
  speaker: coder
  kind: question
  at: '2026-11-08T21:08:31.089536Z'
  stage: doing
  run: 8721668f1cca4f1cb839dc86b6c2bdce
  blocked: question
- number: 8
  speaker: human
  kind: comment
  at: '2026-11-08T21:09:17.967687Z'
  stage: doing
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T21:09:20.447330Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-08T21:09:31.683613Z'
  stage: doing
  run: 79126f0bc1c94dcaad634bd0f6c7669b
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-08T21:09:36.552719Z'
  stage: tests
---

# Claude runs carry the project's CLAUDE.md in the system prompt

## Description

Claude Code loads the project's `CLAUDE.md` itself and puts it at the start of the run's first message, so every run writes it into the prompt cache anew and no later run reads it back (about 7,300 tokens in kumpel-factory). After this story the Claude runtime writes the project's root `CLAUDE.md`, as the run's checkout holds it when the run starts, into the run's instructions file after the system prompt, inside a `<project-instructions>` block introduced by one sentence, and starts Claude Code with `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, so that it no longer loads the file itself. The runtime also starts Claude Code with `CLAUDE_CODE_PROMPT_CACHE_TTL=5m`, so every cache write is a five-minute one, the factory's own setting from now on instead of an instance's trial. A checkout without a root `CLAUDE.md` gets the system prompt alone, as today. A resumed call (after a budget stop) uses the same instructions file. The opencode runtime does not change: it reads the project's instructions itself.

## Interface

- `src/factory/agents/adapters/claude_runtime.py` (`adapters`):
  - `SWITCHES` gains `CLAUDE_CODE_DISABLE_CLAUDE_MDS: "1"` and `CLAUDE_CODE_PROMPT_CACHE_TTL: "5m"`; the comment above it says why each is set.
  - The instructions file of a run is the system prompt's text; when the checkout the run works in holds a regular file `CLAUDE.md` at its root, it is followed by a blank line, the line `The project's instructions, its CLAUDE.md, follow; obey them as you obey this system prompt.`, the line `<project-instructions>`, the file's text, and the line `</project-instructions>`.
  - The file's text is taken as it is, read as UTF-8 when the run starts; a root `CLAUDE.md` that exists and cannot be read as UTF-8 text raises `AgentRuntimeError` naming its path, as an unreadable system prompt file does today.
  - A root `CLAUDE.md` that is a directory or absent adds nothing.
- `src/factory/agents/adapters/opencode_runtime.py`: unchanged.
- Tests: `tests/agents/adapters/test_claude_runtime_project_instructions.py` for the criteria below; the existing tests of the instructions file keep passing for a checkout without `CLAUDE.md`.

## Acceptance criteria

1. A Claude run whose checkout holds a root `CLAUDE.md` gets an instructions file that is the system prompt's text, a blank line, the introducing sentence, `<project-instructions>`, the file's text and `</project-instructions>`, in that order.
2. A Claude run whose checkout has no root `CLAUDE.md`, or a directory of that name, gets an instructions file that is the system prompt's text alone: rows of one parametrized test.
3. A root `CLAUDE.md` that cannot be read as UTF-8 text makes the run raise `AgentRuntimeError` with the file's path in its message.
4. Every Claude call's environment holds `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_PROMPT_CACHE_TTL=5m`, with and without the container environment: rows of one parametrized test.
5. A call resumed after a budget stop gets the same instructions file as the call it resumes.
6. A `CLAUDE.md` changed on the work item's branch reaches the next run in its changed text.
7. An opencode run's agent `prompt` holds no `<project-instructions>` block.
8. `make check` stays green.
9. docs: the operator guide (`docs/operator-guide/agent-runtime.md`) says that under Claude Code the run's system prompt carries the project's root `CLAUDE.md` and Claude Code does not load it itself, that `CLAUDE.md` files below the root, `CLAUDE.local.md` and `.claude/CLAUDE.md` are therefore not read, that every cache write is a five-minute one, and why (later runs read the system prompt from the cache; the one-hour cache costs more than it saves); `docs/decisions.md` records the decision with the measurement of 2026-11-08 (`docs/runs/2026-11-05-f0052/log.md`).

## Smoke test

```bash
uv run python -c "from factory.agents.adapters.claude_runtime import SWITCHES; print(SWITCHES['CLAUDE_CODE_DISABLE_CLAUDE_MDS'], SWITCHES['CLAUDE_CODE_PROMPT_CACHE_TTL'])"
```
Expect: `1 5m`

```bash
uv run pytest tests/agents/adapters/test_claude_runtime_project_instructions.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names concrete places: `SWITCHES` in `src/factory/agents/adapters/claude_runtime.py` (today three switches at line 85) gains two exact key/value pairs and a why-comment. The instructions file is written in `_write_files` (line 461) from `system_prompt_text`, so the exact layout of the root `CLAUDE.md` block fits there: blank line, the introducing sentence, the `<project-instructions>` lines, the file's text as it is. The UTF-8 rule and the `AgentRuntimeError` that names the path follow the existing system-prompt error path. `opencode_runtime.py` stays unchanged.
   - Criteria: each one can be tested by a single test function. The layout and its order (1). Absent and directory are rows of one test (2). The failing side of the UTF-8 read is criterion 3, so the rule has both sides. Both switches, with and without the container environment, are rows of one test (4). The resumed call reuses the same file (5). A changed `CLAUDE.md` reaches the next run (6). Opencode is unchanged (7). Existing tests compare the environment with the `SWITCHES` name, not a written-out dict (`test_claude_runtime_environment.py:70`), so they keep passing with no change to tests another story wrote.
   - Smoke test: both commands can run. The pytest command passes no `-q`, which is right because `addopts` already sets `-q`, so pytest still prints the summary line. Both `Expect:` lines can be checked: the exact output `1 5m`, and a summary line with only `passed`.
   - Docs criterion: it names what the reader must know: the root `CLAUDE.md` is carried in the system prompt, nested files, `CLAUDE.local.md` and `.claude/CLAUDE.md` are not read, every cache write is a five-minute one, and why. It also names the decision-log record and its measurement source. It dictates no sentences.
   - Architecture: the change stays inside the Claude runtime's adapter (R12 wrapper). It adds no new module, dependency or interface, and touches no DTO in the contract.
   - Scope: this is S0002 of `feature.md` (the root `CLAUDE.md` in the system prompt, the switch-off, the five-minute cache). It matches decisions 3 and 4, and it stays clear of "Out of scope": OpenCode handling, nested files and the story text are untouched.
   Route: `tests`, because the Interface changes `src/`.
4. factory: started tests as vm.
5. tester: Wrote the tests for every criterion in one new file, `tests/agents/adapters/test_claude_runtime_project_instructions.py`. I changed no earlier test and wrote no new support module.
   - criterion 1: `::test_a_root_claude_md_follows_the_system_prompt_in_its_block`
   - criterion 2: `::test_a_checkout_without_a_root_claude_md_file_gets_the_system_prompt_alone` (rows `absent`, `directory`)
   - criterion 3: `::test_a_root_claude_md_that_is_not_utf8_text_is_an_error_naming_its_path`
   - criterion 4: `::test_every_claude_call_switches_off_claude_md_and_writes_five_minute_cache` (rows `host`, `container`; the container row reads the environment of the fake container call)
   - criterion 5: `::test_a_resumed_call_gets_the_same_instructions_file` (budget stop, then resume; same `--append-system-prompt-file` path and the same text, which holds the block)
   - criterion 6: `::test_a_claude_md_changed_on_the_branch_reaches_the_next_run` (a real git checkout from the `checkout` fixture; `CLAUDE.md` is committed on a work-item branch, then changed and committed again between two runs of one runtime)
   - criterion 7: `::test_an_opencode_agent_prompt_holds_no_project_instructions_block`
   - criteria 8 and 9: not test criteria (the check and the docs).

   How the layout is compared: the instructions file must equal, line by line, the system prompt's lines, `""`, the introducing sentence, `<project-instructions>`, the file's lines and `</project-instructions>`. The test also checks that the file starts with `SYSTEM_PROMPT` exactly. The project text in the tests has no closing newline. Both choices the Interface leaves open (whether the file ends with a newline, and whether a newline is added after a text that already ends with one) therefore pass, and the test does not decide them.

   Run (`uv run pytest -q` on the new file): 5 failed for the right reason, and the rest passed. The failures are 1, 3, 4 (both rows), 5 and 6: the block is missing, no error is raised for a file that is not UTF-8, and the switches are missing. Criterion 2's rows and criterion 7 pass already, because they pin behaviour that exists today. Every module imported; none was missing. `make lint` is green after `ruff format` on the new file. I skipped the type check, as the stage says.

   `lint`: lint: green (0.1 s)
6. factory: started doing as vm.
7. coder: Stopped before review: the code is built, but one test from an earlier story fails because of the new switches, and I may not change it.

   Built, left in the working tree: `src/factory/agents/adapters/claude_runtime.py`.
   - `SWITCHES` gains `CLAUDE_CODE_DISABLE_CLAUDE_MDS: "1"` and `CLAUDE_CODE_PROMPT_CACHE_TTL: "5m"`. The comment above it now says why each is set.
   - New `instructions_text(system_prompt, checkout)` with private `_project_instructions` and `_ended_line`. `_write_files` now takes the request's `working_directory` and writes the system prompt, a blank line, the introducing sentence and the root `CLAUDE.md` in its `<project-instructions>` block. A root `CLAUDE.md` that is absent or not a regular file (`is_file()`) adds nothing. An `OSError` or `UnicodeDecodeError` while reading it raises `AgentRuntimeError` naming the path. A resumed call reuses the file written once per run.
   - Main choice: the text is read in the Claude adapter from the host checkout (`request.working_directory`) when the run starts. I rejected putting it into the shared `system_prompt_text` in `agent_launch`, because opencode must not get the block.

   Result: all 9 tests in `tests/agents/adapters/test_claude_runtime_project_instructions.py` pass. In `make check`, lint, types, layers, sast, secrets and licenses are green. `make test` fails on exactly one test:

   ```
   FAILED tests/agents/adapters/test_claude_runtime.py::test_call_gets_only_the_requests_environment_and_the_switches
   E   AssertionError: assert {'CLAUDE_CODE...YTECODE', ...} <= {'CLAUDE_CODE...'TOKEN_PROBE'}
   E     Extra items in the left set:
   E     'CLAUDE_CODE_PROMPT_CACHE_TTL'
   E     'CLAUDE_CODE_DISABLE_CLAUDE_MDS'
   ```

   Cause: `tests/agents/adapters/test_claude_runtime.py:25` defines its own written-out `SWITCHES` dict with the three old switches. It does not import the runtime's `SWITCHES`. The intake entry assumed the existing tests use the runtime's name, but this one does not. The Interface requires the two new switches, so this test cannot pass without a change, and it is a test another story wrote. The standing leave covers only moving shared helpers, so this needs your leave.

   Options:
   (a) The tester adds `"CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"` and `"CLAUDE_CODE_PROMPT_CACHE_TTL": "5m"` to the local `SWITCHES` dict at `tests/agents/adapters/test_claude_runtime.py:25`. The test keeps pinning the exact values on its own. **I recommend this.**
   (b) The tester replaces the local dict with an import of `SWITCHES` from `factory.agents.adapters.claude_runtime`. Simpler, but the test would then no longer pin the values independently.
   (c) Drop the switches from the Interface. I would not, because the story depends on them.

   With your answer for (a) or (b), I end with `tests`, naming that change.
8. 2026-11-08 human: (a). Leave granted: the tester adds `"CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"` and `"CLAUDE_CODE_PROMPT_CACHE_TTL": "5m"` to the local `SWITCHES` dict in `tests/agents/adapters/test_claude_runtime.py`; the test keeps its name and keeps pinning the values on its own.
9. factory: started doing as vm.
10. coder: Sent back to the tester with the human's leave from entry 8. The tester should add `"CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"` and `"CLAUDE_CODE_PROMPT_CACHE_TTL": "5m"` to the local `SWITCHES` dict at `tests/agents/adapters/test_claude_runtime.py:25`. `test_call_gets_only_the_requests_environment_and_the_switches` keeps its name and still pins the values itself.

    I made no code change in this run. The implementation in `src/factory/agents/adapters/claude_runtime.py` from entry 7 is already on the branch. The human's answer changes no meaning of the task, so `## Description` stays as it is.

    Once that test is updated I expect `make check` to be green, but that is not yet checked. Entry 7 is the last run: every target except `make test` was green, and `make test` failed only on this test.
11. factory: started tests as vm.
