---
stage: docs-only
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 665
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: docs-only
  started_at: '2026-11-08T14:39:20.250744Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T14:38:46.936806Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T14:38:46.944671Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T14:39:15.262805Z'
  stage: intake
  run: 7573b9f541154314961c9e65d0ae4017
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T14:39:20.250744Z'
  stage: docs-only
---

# The operator guide says what keeps the cached start

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

Since this feature, every shipped agent has the same tools, intake, the tester, the coder, the documenter and the smoke tester share one model and one effort, and every run gets one common system prompt, so that the runs share a cached start. The project guide and `docs/decisions.md` say so; the operator guide does not. An operator who copies a shipped agent to `<project>/factory/agents/` and changes its `tools`, `model` or `effort`, as the guide's own example file (`model: sonnet`, `tools: [Read, Write]`, `effort: low`) invites, gives that role a cached start of its own and pays the cache writes again, with nothing to say why. The paragraph *The models* also still reads as if the agent files name `opus`, `sonnet` and `haiku`, while every shipped file names `opus`. After this story, the operator guide's `docs/operator-guide/agent-runtime.md` says what a project's own agent must keep to share the cached start, what it costs when it does not, and where the operator sees it (`factory-bill`'s role table, in `docs/operator-guide/records.md`). No code changes.

## Interface

None: the story changes `docs/operator-guide/agent-runtime.md` only (the docs route).

## Acceptance criteria

1. *A project's own agents* in `docs/operator-guide/agent-runtime.md` says that a project's agent shares the cached start of the other roles only when its `tools` are the shipped ones and its `model` and `effort` match the roles it should share with, and that a project's agent which differs starts a cache of its own.
2. The same section says where the effect shows: the hit rate per role in `factory-bill`'s role table, with a link to the bill's section in `docs/operator-guide/records.md`.
3. *The models* says that every shipped agent names `opus`, and that `sonnet` and `haiku` are aliases a project's own agent may name.
4. The example agent file in *The agent files* is either one that keeps the shared start or is followed by a sentence saying that it does not.
5. `make check` stays green.
6. docs: the operator guide (`docs/operator-guide/agent-runtime.md`), as criteria 1 to 4 say; the project guide and `docs/decisions.md` need nothing, since they already give the reason.

## Smoke test

```bash
grep -c 'cached start' docs/operator-guide/agent-runtime.md
```
Expect: a number of at least `1`.

```bash
grep -n 'factory-bill' docs/operator-guide/agent-runtime.md
```
Expect: at least one line in the section *A project's own agents*.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: none; the story changes only `docs/operator-guide/agent-runtime.md`, which is inside the documenter's write paths (`docs/*`). So the route is docs-only. The facts it relies on hold. Every file in `agents/agents/` names `model: opus` and the same tools, `[Read, Grep, Glob, Edit, Bash, Write, Skill]`. Intake, tester, coder, documenter and smoke tester run at `effort: medium`, and the reviewer and acceptance reviewer at `high`. *The models* (line 212) still says the files name `opus`, `sonnet` and `haiku`. The example file (lines 317-321) has `model: sonnet`, `tools: [Read, Write]`, `effort: low`.
   - Criteria: each of 1 to 4 can be checked against the document. 1 is the condition for sharing the cached start (shipped tools, matching model and effort) and what happens when an agent differs (a cache of its own). 2 is the place where the effect shows, with a link to the `factory-bill` section of `records.md`, which exists along with *The cache figures*. 3 is the reworded *The models*. 4 is an either/or about the example, and either side can be checked. No Interface rule needs a failing side. 5 and 6 are the closing two.
   - Smoke test: both `grep` commands run as written. The first expects a count of at least 1 and the second a line inside *A project's own agents* (lines 328-339 now), so both can be checked.
   - Docs criterion: it names what the operator must know: what keeps the shared start, what breaking it costs, where it shows and what the aliases mean. It quotes no sentences. It also says why the project guide and `docs/decisions.md` need no change.
   - Architecture: no code, no change to `factory/`, no tests, no dependency. The operator guide is the right document for operator-facing guidance.
   - Scope: within F0058. The feature's goal is that runs share one cached start, and decision 3 is the shared model and effort. The story writes down for operators what S0001 to S0003 built. It touches nothing the feature lists as out of scope.
4. factory: started docs-only as vm.
