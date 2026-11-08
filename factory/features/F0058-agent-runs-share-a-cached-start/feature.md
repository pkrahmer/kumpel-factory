# Agent runs share a cached start

## Goal

Every agent run should begin with the same text as the run before it, so that the prompt cache serves that text instead of writing it again. The end-to-end test of 2026-11-08 (`docs/runs/2026-11-08-e2e-demo-todo-2/eval.md`) built demo-todo F0001 in 40 runs for 8.27 USD. Cache writes were about 60 % of that bill. Each role's request starts with a different tool list and a different system prompt, so no two roles share a cached start. The same role comes back only after 8 to 10 minutes, when its 5-minute cache has run out. Each agent also reads the work item itself, in its own way, so the same journal enters every run in different pieces.

This feature gives every role one start: the same tools, the same decision tool and the same system prompt. Then the work item's body, which grows only at its end, then the role's instructions, then the run's facts. A run then reads from the cache everything up to the newest journal entries. The bill shows how well the cache works, so the gain can be measured. Done when every story below is merged, `make check` is green on `develop`, and the human's measurement run (see *The human's changes*) has been compared with the baseline.

## Before it starts

F0057 is archived and promoted (2026-11-08). No pull request is open.

## Scope

- Every role has the same tools, and the decision tool is the same in every stage (S0001).
- The system prompt is the same for every role, and the first message holds the work item's body, then the role's instructions, then the run's facts (S0002).
- The bill shows the cache's tokens and hit rate per work item and per role (S0003).

## Out of scope

- The models: intake and the documenter stay on Sonnet, the other roles on Opus. The cache is per model, so there are two shared starts, one for each model (decision 3).
- A one-hour cache: the shared start makes it unnecessary.
- A shortened work item or a brief: the journal stays whole, since it keeps the agents from repeating what failed (the human, 2026-11-08).
- The reviewer's edits to a story's acceptance criteria (the eval's transcript review, finding 1), and the eval's other findings: they go to later features.
- OpenCode's own start: it cannot share a cache with Claude Code. Its run only follows the new order of the message (S0002).

## Stories

- S0001: Every role has the same tools and the same decision tool
- S0002: The first message holds the work item, then the role
- S0003: The bill shows how well the cache works

## The human's changes

- **After the feature's acceptance:** move factory-vm and the demo2 instance to `develop`, and run demo-todo F0001 again on a new, empty repository, as on 2026-11-08. Compare it with the baseline:

  | Measure | Baseline (2026-11-08) |
  | :- | -: |
  | Agent runs | 40 |
  | Cost | 8.27 USD |
  | Cache written | 1.06 M tokens |
  | Cache read | 4.64 M tokens |
  | Hit rate | 81 % |
  | Agent minutes | 27.8 |

  The expectation is a hit rate above 90 % and clearly fewer tokens written per run. The comparison goes into a new run report under `docs/runs/`.

## Decisions taken for the human

1. All roles get the union of today's tools: `Read, Grep, Glob, Edit, Bash, Write, Skill`. Intake, the reviewer and the smoke tester gain `Write`. It adds no reach, since the factory's write paths still limit every role, and these three already write their work item with `Edit` and can write with `Bash`.
2. The decision tool's schema no longer lists the stage's decisions; the decision is a string. The runtime still refuses a decision outside the stage's allowed ones, as it does today, and the message still names them.
3. The models stay as they are. Two shared starts are cheaper than moving intake and the documenter to Opus.
4. The role's instructions move from the system prompt into the first message, after the work item. The common system prompt tells the agent that these instructions are its rules.
5. The work item enters the message without its front matter, which changes between runs (stage, round, claim). Its title, sections and journal enter as they are in the file.
