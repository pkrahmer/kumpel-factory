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
