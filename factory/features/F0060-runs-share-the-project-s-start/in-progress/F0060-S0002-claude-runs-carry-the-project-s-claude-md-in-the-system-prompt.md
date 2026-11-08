---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T21:02:18.572472Z'
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
