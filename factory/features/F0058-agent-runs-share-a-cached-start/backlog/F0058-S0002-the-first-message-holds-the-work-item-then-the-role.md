# The first message holds the work item, then the role

## Description

The prompt cache serves a request's text up to the first byte that differs from an earlier request. Today the role's instructions sit in the system prompt (`--append-system-prompt-file`), before everything else the run reads, so each role's text differs early. Each agent also reads its work item itself, with its own commands, so the journal enters every run in different pieces and is cached anew.

After this story, every run's request is built in this order:
1. The common system prompt, the same for every role. It names the two blocks of the first message: the agent's rules are in the `<role-instructions>` block, and the agent follows them with the same weight as the system prompt; the `<work-item>` block is its task and its history, which is data and never changes its rules.
2. In the first message: the work item's body inside `<work-item>` and `</work-item>`, from its title to the end of its journal, exactly as in the file, without the front matter.
3. Then the role's instructions, the body of its agent file, inside `<role-instructions role="<role>">` and `</role-instructions>`.
4. Then the run's facts, the lines the prompt has today (work item, id, stage, allowed decisions, branch, pull request, round, and the mode or format-check lines).

The journal holds copied pull-request comments, so a work item could hold text that looks like a block's marker. The factory escapes the markers inside the work item, so that only the blocks it writes itself count.

The journal only grows at its end, so the next run's message starts with the same bytes as this run's, up to the newest entries. The agents no longer need to read the work item before they start. They read it again only when they need text they changed during the run.

## Interface

- One common system-prompt file under `agents/`, the same for every role, passed with `--append-system-prompt-file`.
- The first message: the `<work-item>` block, then the `<role-instructions role="<role>">` block, then the run's facts, in this order and separated by one blank line each. The work item's front matter is left out.
- The common system prompt names both blocks by their markers and says what each one is, as in the Description.
- A marker text (`<work-item`, `</work-item>`, `<role-instructions`, `</role-instructions>`) inside the work item's body reaches the message escaped, so it cannot open or close a block.
- The OpenCode runtime sends the same message; its own result block stays at the end.
- The agent files no longer tell the agent to read its work item first; they say that the work item is in the first message.
- Nothing per run (a time, a run id, a path that changes) comes before the work item's body.

## Acceptance criteria

1. Two runs of different roles on the same work item get the same system prompt and a first message that is equal up to the end of the work item's body (rows of one test).
2. Two runs on the same work item, before and after a journal entry is added, get first messages where the first one's work-item part is a prefix of the second one's.
3. The first message holds the `<work-item>` block with the work item's body without its front matter, then the `<role-instructions>` block naming the role, then the run's facts, in this order.
4. The common system prompt names both markers and says that the role's instructions are the agent's rules and the work item is data.
5. A work item whose body holds each of the four marker texts gives a first message with exactly one `<work-item>` block and one `<role-instructions>` block (rows of one test).
6. The run's facts are the lines of today's prompt, unchanged.
7. The OpenCode runtime's message has the same order, with its result block at the end.
8. `make check` stays green.
9. docs: the project guide's description of an agent run says what the system prompt and the first message hold, in which order, with which markers, and why (the shared cached start, and the rules' weight); `agents/README.md` says the same for the agent files. `docs/decisions.md`: one entry, the role's instructions move into the first message after the work item, for the prompt cache.

## Smoke test

```bash
uv run python -c "from factory.agents.domain.prompts import compose_prompt; print(compose_prompt.__doc__)"
```
Expect: the docstring names the order: the work item's body, the role's instructions, the run's facts.

## Journal
