# The bill shows how well the cache works

## Description

Every cost record already holds a run's tokens: input, output, cache read and cache written. The bill (`factory-bill`) shows the cost and the runs, but not these tokens, so nobody can see whether the cache works without reading the records by hand.

After this story, the bill shows for each work item, and in its total, the tokens read from the cache, the tokens written to it, and the hit rate. The hit rate is the tokens read from the cache divided by all prompt tokens (read, written and uncached input). The bill also shows the same three figures per role. This is the measure for this feature's goal, and for every later change to the prompts.

## Interface

- `factory-bill <work item>` and `factory-bill` (the work items in flight) show, beside today's lines: cache read, cache written and hit rate, for each work item and in the total.
- One line per role with the same three figures, in the work item's bill.
- The hit rate is shown as a whole percent. A work item with no prompt tokens shows `-`.
- Today's lines and their order stay as they are.

## Acceptance criteria

1. A bill over cost records with known tokens shows the right cache read, cache written and hit rate for the work item and the total (rows of one test).
2. The per-role lines add up to the work item's figures.
3. A work item with no prompt tokens shows `-` for its hit rate.
4. Every earlier line of the bill is unchanged.
5. `make check` stays green.
6. docs: the operator's documents that show the bill name the three new figures and how to read the hit rate.

## Smoke test

```bash
uv run factory-bill --help
```
Expect: the help names the cache figures and the hit rate.

## Journal
