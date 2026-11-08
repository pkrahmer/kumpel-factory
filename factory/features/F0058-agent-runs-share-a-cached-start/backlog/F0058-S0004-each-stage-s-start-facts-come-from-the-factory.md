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
- The common system prompt says that the `<context>` blocks are facts the factory gathered at the start, which the agent need not gather again.
- A stage without `context` gets a message as before.
- The pipeline definition's version rule applies to the new key (`docs/decisions.md`).

## Acceptance criteria

1. A stage with `context: [a, b]` gets a first message with the block of `a`, then the block of `b`, after the `<role-instructions>` block and before the run's facts (rows of one test).
2. Loading refuses a `context` name that is not a project command, and accepts one that is (rows of one test).
3. An output of 60,000 characters enters whole; one of 60,001 characters is cut, with the line naming the cut characters (rows of one test).
4. A failing command and one that runs out of time each give a block with `failed: <reason>`, and the agent's run still starts.
5. A marker text inside a command's output reaches the message escaped.
6. A stage without `context` gets the same message as without this story.
7. The commands run in the check container on the stage's base, never on the host.
8. `make check` stays green.
9. docs: the project guide's description of the pipeline definition names `context`, what the factory does with it, the size limit and the failure line; the operator's guide shows one example. `docs/decisions.md`: one entry, a stage's start facts come from project commands the factory runs before the agent, to save the agent's first turns.

## Smoke test

```bash
uv run python -c "from factory.pipeline.domain.pipeline_definition import StageDefinition; print('context' in StageDefinition.model_fields)"
```
Expect: `True`

## Journal
