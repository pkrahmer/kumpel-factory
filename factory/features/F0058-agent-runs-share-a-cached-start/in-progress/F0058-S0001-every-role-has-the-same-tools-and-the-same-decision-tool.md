---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 659
comments_read: [6720500729]
handed_over: null
claim: null
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
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T10:42:16.102298Z'
  stage: intake
  run: ef6a83a45f83442b91a5a7273813c5ae
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T10:46:05.246265Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T10:46:07.615751Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T10:46:24.851541Z'
  stage: intake
  run: 734c7f7de2b54a51aaefde992fbd6480
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
6. The `--json-schema` argument's `decision` property has type `string` and no `enum`, and its description says the run's message names the allowed decisions.
7. The message built for a request contains each of its `allowed_decisions`.
8. The launch arguments of a request, with the `--json-schema` value removed, equal those before this story (the model and effort of intake and the documenter come from their agent files and are covered by criterion 2).
9. `make check` stays green.
10. docs: the project guide's description of the agent files and of the launch arguments says that every role has the same tools and the same decision tool, and why (the shared cached start). `docs/decisions.md`: one entry, every role has the same tools, and five roles share one model and one effort, for the prompt cache; the write paths, not the tool list, limit what a role writes.

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
3. intake: Format check passed. Questions:

   1. The Interface says the `--json-schema` `decision` is a string and "its description says the run's message names the allowed decisions". No criterion tests that. Criterion 3 only compares two schemas. Please add one, for example: "the schema's `decision` property has type `string` and no `enum`, and its description mentions the allowed decisions". I would choose that.

   2. The Description says "The run's message still names the allowed decisions". Nothing tests it. Please add a criterion, for example: "the message built for a request contains each of its `allowed_decisions`". This matters most because the schema no longer lists them.

   3. The Interface says "No other launch argument changes". No criterion pins it, and two coders could read it differently. Please add a criterion, for example: "the launch arguments of a request, with the `--json-schema` value removed, equal those before this story". Alternatively, say it is not tested and drop the line. I would add the criterion.

   Everything else is fine: criteria 1, 2, 4 and 5 each have one test, and the refused side is covered by criteria 4 and 5. The smoke commands are runnable and their Expect lines are checkable. The docs criterion names what the reader must know and dictates no sentences. The architecture fits, because only the `agents` adapters and `agents/agents/*.md` change. The scope fits S0001 in `feature.md`.
4. 2026-11-08 human: Agreed on all three, as you propose:
   1. Add the criterion: the schema's `decision` property has type `string` and no `enum`, and its description says the run's message names the allowed decisions.
   2. Add the criterion: the message built for a request contains each of its `allowed_decisions`.
   3. Add the criterion: the launch arguments of a request, with the `--json-schema` value removed, equal those before this story (the model and effort of intake and the documenter come from their agent files and are covered by criterion 2).
5. factory: started intake as vm.
6. intake: accepted. I carried in the human's answer (journal entry 4) by adding three criteria before the two closing ones: new 6 (the schema's `decision` is a string with no `enum`, and its description says the message names the allowed decisions), new 7 (the message contains each of the request's `allowed_decisions`) and new 8 (launch arguments other than `--json-schema` are unchanged). `make check` and `docs:` are now criteria 9 and 10. The Description did not change.
   - Interface: it names concrete paths (`agents/agents/*.md` with their `tools`, `model` and `effort` values, and `factory.agents.adapters.claude_runtime`'s `--json-schema` argument). Every behaviour it states now has a criterion.
   - Criteria: each is testable by one test function. The failing sides are covered: criterion 4 refuses a decision outside `allowed_decisions`, criterion 5 refuses a write outside `{work_item}`, and criterion 6 requires no `enum`. Each effort value has its own row in criterion 2.
   - Smoke test: both `grep ... | sort -u` commands are runnable, and each `Expect:` line is checkable against the output. The commands run no pytest.
   - Docs criterion: it names what the reader must know (same tools and decision tool for every role, and why) and the one decisions entry. It dictates no sentences.
   - Architecture: only the `agents` adapters and the agent files change. The write paths stay in the factory.
   - Scope: this matches S0001 in `feature.md` and decisions 1 to 3. Route: `tests`, because the Interface changes code.
