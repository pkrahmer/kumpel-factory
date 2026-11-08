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
  started_at: '2026-11-08T10:42:00.046925Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T10:42:00.039045Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T10:42:00.046925Z'
  stage: intake
---

# Every role has the same tools and the same decision tool

## Description

A Claude Code request begins with its tool list, so two runs share a cached start only if their tools are the same. The cache is also per model, and a change of effort between requests invalidates the cached messages. Today the roles differ in four ways:
- Intake, the reviewer and the smoke tester have no `Write` tool.
- The decision tool's schema lists the stage's allowed decisions, so it differs from stage to stage.
- Intake and the documenter run on Sonnet, the other roles on Opus.
- Intake runs at low effort, the reviewer and the acceptance reviewer at high, the others at medium.

After this story, every role has the tools `Read, Grep, Glob, Edit, Bash, Write, Skill`. Intake and the documenter run on Opus at medium effort, so that they, the tester, the coder and the smoke tester share one model and one effort. The reviewer and the acceptance reviewer stay on Opus at high effort (the feature's decision 3). The decision tool's schema is the same for every request. The factory's write paths still decide what each role may write, as today. The runtime still refuses a decision outside the stage's allowed ones, as it does today after the run. The run's message still names the allowed decisions.

## Interface

- `agents/agents/*.md`: every agent file's `tools` is `[Read, Grep, Glob, Edit, Bash, Write, Skill]`.
- `agents/agents/intake.md` and `agents/agents/documenter.md`: `model: opus`, `effort: medium`. The other agent files keep their model and effort.
- `factory.agents.adapters.claude_runtime`: the `--json-schema` argument no longer depends on the request. `decision` is a string, and its description says the run's message names the allowed decisions.
- A decision outside the request's `allowed_decisions` is handled as today: the run's result is refused.
- No other launch argument changes.

## Acceptance criteria

1. Every agent file under `agents/agents/` has exactly the tools `Read, Grep, Glob, Edit, Bash, Write, Skill`, in this order (rows of one test over the files).
2. Every agent file has `model: opus`. Intake, the tester, the coder, the documenter and the smoke tester have `effort: medium`; the reviewer and the acceptance reviewer have `effort: high` (rows of one test over the files).
3. Two requests with different `allowed_decisions` give the same `--json-schema` argument.
4. A run whose decision is not in the request's `allowed_decisions` is refused, as before (an earlier test may change only in how it builds the schema).
5. Intake, the reviewer and the smoke tester still cannot write outside `{work_item}`: the factory's write-path verdict refuses a written file outside it, with `Write` as with `Edit` (rows of one test).
6. `make check` stays green.
7. docs: the project guide's description of the agent files and of the launch arguments says that every role has the same tools and the same decision tool, and why (the shared cached start). `docs/decisions.md`: one entry, every role has the same tools, and five roles share one model and one effort, for the prompt cache; the write paths, not the tool list, limit what a role writes.

## Smoke test

```bash
grep -h '^tools:' agents/agents/*.md | sort -u
```
Expect: exactly one line, `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]`

```bash
grep -h '^model:' agents/agents/*.md | sort -u
```
Expect: exactly one line, `model: opus`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
