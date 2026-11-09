# The decision log records the shared rules in the system prompt

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

F0060-S0001 moved the rules every role shares (the opening paragraphs and R1 to R15) out of the seven shipped agent files into `agents/system-prompt.md`, so that every run reads them from the prompt cache instead of writing them anew in its first message. The decision log holds no entry for it: S0001's documenter changed only the log's introduction, and the entry of S0002 (*Claude runs carry the project's `CLAUDE.md` in the system prompt*) speaks of `CLAUDE.md` alone. The F0058 entry *The role's instructions follow the work item in the first message* still says "The system prompt says that the role's instructions are the agent's rules", which is no longer what the system prompt says: it now holds the rules itself, and the role's instructions add to them. A later story that wanted to put a rule back into an agent file would find no reason not to. After this story the log has an entry for the move, newest last, that names what it changes in the F0058 entry; the F0058 entry itself stays as it was written. Only `docs/decisions.md` changes: a story of the docs route.

## Interface

- No code changes: `docs/decisions.md` only, on the docs route.
- The new entry, after the last entry of the log: its title says that the rules every role shares stand in the system prompt; it has the line `Date: 2026-11-08 (F0060-S0001).`, as the S0002 entry dates itself, and the lines `Decision`, `Why` and `Rejected`, as the log's other entries have them.

## Acceptance criteria

1. `docs/decisions.md` holds one new entry, the last of the log, whose `Decision` line says that the opening paragraphs and R1 to R15 stand once, in `agents/system-prompt.md` and in the built-in fallback `SYSTEM_PROMPT`, which stay equal, that an agent file holds only its role's own instructions, and that the role's instructions add to the rules with the same weight.
2. Its `Why` line gives the reason: about 1,600 tokens the same in all seven agent files were written to the cache anew in every run's first message, while the system prompt is read from the cache by every run within the cache's time; it cites `planning/later-topics.md`, topic 2, or the measurement in `docs/runs/2026-11-05-f0052/log.md`, as the entry of S0002 does.
3. Its `Rejected` line names the story text in the system prompt (one cache point in the system prompt, so every change of the story text would miss `CLAUDE.md` too), as `feature.md` of F0060 gives it under *Out of scope*.
4. The entry says that it replaces the F0058 entry's sentence on what the system prompt says about the role's instructions, and that F0058 entry is unchanged.
5. `make check` stays green.
6. docs: `docs/decisions.md` as criteria 1 to 4 say; no other document.

## Smoke test

```bash
grep -c '^Date: 2026-11-08 (F0060-S0001)\.$' docs/decisions.md
```
Expect: `1`

```bash
awk '/^## /{title=$0} END{print title}' docs/decisions.md | grep -c 'rules.*system prompt'
```
Expect: `1`

## Journal
