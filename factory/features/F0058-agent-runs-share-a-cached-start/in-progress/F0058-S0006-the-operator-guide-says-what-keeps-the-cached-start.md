---
stage: docs-only
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 665
comments_read: []
handed_over: null
claim: null
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
- number: 5
  speaker: documenter
  kind: result
  at: '2026-11-08T14:43:57.183542Z'
  stage: docs-only
  run: dc3fa3de23c14f69831bbd2307fdecc1
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T14:44:02.554853Z'
  stage: docs-review
- number: 7
  speaker: reviewer
  kind: result
  at: '2026-11-08T14:44:57.743272Z'
  stage: docs-review
  run: 5c91770383024551bdf0a81f1762d64c
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
5. documenter: Changed `docs/operator-guide/agent-runtime.md` only (the docs route):
   - *A project's own agents*: a new paragraph block **The cached start** above the bullet list. It says that runs share a cached start only where tools, model and effort agree, gives the shipped values (tools `[Read, Grep, Glob, Edit, Bash, Write, Skill]`, `opus`, `medium` for intake, tester, coder, documenter and smoke tester, `high` for the two reviewers), says that a project's agent shares the start only with the shipped tools and a matching model and effort, and that one that differs starts a cache of its own and writes the cache again (criterion 1). It also says that a smaller tool list does not limit writes, because the write paths do. It names where the effect shows, the hit rate per role in `factory-bill`'s role table, and links `records.md#what-a-work-item-cost-factory-bill` and its *The cache figures* part (criterion 2).
   - *The models*: now says that every shipped agent file names `opus` and that `sonnet` and `haiku` are aliases a project's own agent may name. It still says that `FACTORY_OPENCODE_MODELS` maps all three (criterion 3).
   - *The agent files*: the example now keeps the shared start (`model: opus`, the shipped tool list, `effort: medium`, `budget_usd: 1`), followed by a sentence saying so (criterion 4).

   Checked against: every `agents/agents/*.md` front matter (model, effort, tools), the cache paragraph in `docs/project-guide/agents.md` (*The seven agents*), and `docs/operator-guide/records.md` (*The cost table*, *The cache figures*: both the anchor and the role table it describes exist).

   Ran: both smoke-test greps. `cached start` counts 3, and `factory-bill` matches line 342, inside *A project's own agents*. `make documents` ended `documents ok (59.5 s)`. I did not run `make check` because only a document changed; the factory runs the gate.

   Documents I cross-read and found current: `docs/project-guide/agents.md` (agent table and cache reasoning) and `docs/operator-guide/records.md`. I saw nothing stale outside this story.

   Not from the story: the sentence that cache writes cost more than plain input is general Anthropic pricing knowledge, not something the story or the project guide states. The reviewer may drop it.

   `check`: check: green
   `secrets`: secrets: green (0.4 s)
   `documents`: documents ok (60.4 s)
6. factory: started docs-review as vm.
7. reviewer: I checked the diff of `docs/operator-guide/agent-runtime.md` against `agents/agents/*.md` (every file has `model: opus` and the tools `[Read, Grep, Glob, Edit, Bash, Write, Skill]`; intake, tester, coder, documenter and smoke tester use `effort: medium`, the two reviewers `high`), the cache paragraph in `docs/project-guide/agents.md` (line 266), F0058 decision 1 in `docs/decisions.md`, `docs/operator-guide/records.md` (*What a work item cost: `factory-bill`*, *The cache figures*, the hit-rate row) and `docs/project-guide/style.md`. Criteria 1 to 4 are met in substance: the condition and what breaking it costs, where the effect shows, the reworded *The models*, and an example that keeps the shared start with a sentence saying so. The sentence "cache writes cost more than plain input" is Anthropic's pricing, not a claim about the factory's code. It is true, so I kept it. Four findings remain:

   1. `docs/operator-guide/agent-runtime.md:342`: the link to the bill's section is an anchor link, `[What a work item cost: ...](records.md#what-a-work-item-cost-factory-bill)`. Style rule 8 asks for the heading in italics, then `in` and a link to the page. The document check also drops a link's fragment (`src/factory/shared/domain/documents.py`, `_FRAGMENT`), so a renamed heading would go unnoticed. Fix: write `see *What a work item cost: factory-bill* in [records.md](records.md)`, and name its part *The cache figures* the same way. That still meets criterion 2.
   2. `docs/operator-guide/agent-runtime.md:340`: "write paths" is a glossary word (`docs/project-guide/glossary.md`, **write paths**), and this is its first use in the file, but it has no link (style rule 3). Fix: link it as `[write paths](../project-guide/glossary.md)`.
   3. `docs/operator-guide/agent-runtime.md:340`: "A smaller tool list does not make a role safer either" claims more than the code and the project guide back. `docs/project-guide/agents.md:266` says only that the tool list does not limit what a role writes, because the write paths do this through the take. Fix: "A smaller tool list does not limit what a role writes: its write paths do."
   4. `docs/operator-guide/agent-runtime.md:338`, `:340`, `:342`: several new sentences run to about 30 to 40 words, against style rule 2 (split a sentence of more than about 25 words). They are the one that starts "Every shipped agent has the tools …; intake, the tester, …", "A project's agent shares the cached start … should share with", "A project's agent that differs … than plain input", and "The effect shows in `factory-bill`: … than the others". Fix: split each, for example the shipped values into one sentence on the tools and model and one on the efforts, and the cost sentence at its colon.
