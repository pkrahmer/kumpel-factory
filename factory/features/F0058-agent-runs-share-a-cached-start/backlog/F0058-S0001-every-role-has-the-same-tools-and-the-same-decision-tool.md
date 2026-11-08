# Every role has the same tools and the same decision tool

## Description

A Claude Code request begins with its tool list, so two runs share a cached start only if their tools are the same. Today the roles differ in two ways:
- Intake, the reviewer and the smoke tester have no `Write` tool.
- The decision tool's schema lists the stage's allowed decisions, so it differs from stage to stage.

After this story, every role has the tools `Read, Grep, Glob, Edit, Bash, Write, Skill`. The decision tool's schema is the same for every request. The factory's write paths still decide what each role may write, as today. The runtime still refuses a decision outside the stage's allowed ones, as it does today after the run. The run's message still names the allowed decisions.

## Interface

- `agents/agents/*.md`: every agent file's `tools` is `[Read, Grep, Glob, Edit, Bash, Write, Skill]`.
- `factory.agents.adapters.claude_runtime`: the `--json-schema` argument no longer depends on the request. `decision` is a string, and its description says the run's message names the allowed decisions.
- A decision outside the request's `allowed_decisions` is handled as today: the run's result is refused.
- No other launch argument changes.

## Acceptance criteria

1. Every agent file under `agents/agents/` has exactly the tools `Read, Grep, Glob, Edit, Bash, Write, Skill`, in this order (rows of one test over the files).
2. Two requests with different `allowed_decisions` give the same `--json-schema` argument.
3. A run whose decision is not in the request's `allowed_decisions` is refused, as before (an earlier test may change only in how it builds the schema).
4. Intake, the reviewer and the smoke tester still cannot write outside `{work_item}`: the factory's write-path verdict refuses a written file outside it, with `Write` as with `Edit` (rows of one test).
5. `make check` stays green.
6. docs: the project guide's description of the agent files and of the launch arguments says that every role has the same tools and the same decision tool, and why (the shared cached start). `docs/decisions.md`: one entry, every role has the same tools for the prompt cache; the write paths, not the tool list, limit what a role writes.

## Smoke test

```bash
grep -h '^tools:' agents/agents/*.md | sort -u
```
Expect: exactly one line, `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]`

## Journal
