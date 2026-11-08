---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 661
comments_read: [6721548904]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T12:32:38.033603Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T12:32:38.041290Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T12:33:11.145277Z'
  stage: intake
  run: fb2c94e9745546018327eb33585770b7
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T12:34:58.551245Z'
  stage: intake
---

# The bill shows how well the cache works

## Description

Every cost record already holds a run's tokens: input, output, cache read and cache written. The bill (`factory-bill`) shows the cost and the runs, but not these tokens, so nobody can see whether the cache works without reading the records by hand.

After this story, the bill shows for each work item, and in its total, the tokens read from the cache, the tokens written to it, and the hit rate. The hit rate is the tokens read from the cache divided by all prompt tokens (read, written and uncached input). The bill also shows the same three figures per role. This is the measure for this feature's goal, and for every later change to the prompts.

## Interface

- `factory-bill <work item>` and `factory-bill` (the work items in flight) show, beside today's lines: cache read, cache written and hit rate, for each work item and in the total.
- One line per role with the same three figures, in the work item's bill.
- The hit rate is shown as a whole percent. A work item with no prompt tokens shows `-`.
- Today's lines and their order stay as they are.
- The human's leave for earlier tests: a test that pins the bill's whole output or its models may change to hold the new figures, keeping its name and checking otherwise the same thing: `tests/entry/test_bill.py`, `tests/watching/application/test_bill_service.py`, `tests/watching/domain/test_bills.py`, `tests/watching/domain/test_bills_model_time.py` and `tests/hosting/application/test_costs.py`. The tester's entry names each one it changed.

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

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Intake questions (the format check passed). I read the feature's `feature.md`, `src/factory/watching/domain/bills.py`, `src/factory/entry/bill.py`, `src/factory/watching/domain/cost_records.py` and `docs/operator-guide/records.md` ("What a work item cost").

   1. Where do the new figures go? The Interface asks for them "beside today's lines" and says "today's lines and their order stay as they are" (criterion 4). Today the bill is a stage table (`| stage | runs | min | model min | turns | in | cached | out | USD |`), an empty line and the `Cost: ...` line. Each row already has a `cached` column, which is the cache read, and an `in` column, which is input plus cache written. New columns would change every earlier line and break criterion 4. That leaves new lines after the `Cost:` line. Options: (a) after `Cost:`, one `Cache: <read> read, <written> written, <n> % hit` line for the work item; then a second table, `| role | cache read | cache written | hit rate |`, with one row per role in the order the role first ran and a **total** row. (b) New columns in the stage table, with criterion 4 reworded to "every earlier column is unchanged". (c) Something else you name. I would pick (a). Whichever you choose, please write the exact line format and the role table into the Interface, so that criteria 1, 2 and 4 can each be pinned by one test.
   2. "In the total": with no argument the bill prints one block per work item in flight, and there is no total across them. Does "total" mean the work item's total (the **total** row or the `Cost:` line), or a new total across every work item in flight? I would pick the work item's total, with no new cross-work-item total.
   3. The other places that print the bill: `cost_table` and `cost_line` also feed the cost table posted on the pull request at the hand-over (`src/factory/pipeline/application/handlers/hand_over.py:82`) and the acceptance report (`src/factory/work/application/acceptance.py:153`, `:273`). Should the cache figures appear there too, or only in `factory-bill`? Option (a) in question 1 keeps them to `factory-bill` and leaves the posted tables unchanged, which is what I would pick. If they should appear there too, that needs its own Interface line and criterion.
   4. The hit rate's rounding: "a whole percent" can be read two ways, half up (as the bill's other figures are rounded) or down. Please name the rule and add a criterion with a value on the rounding edge (for example 2 of 3 = 66.67 % → `67 %`). I would pick half up.
   5. The smoke test runs `uv run factory-bill --help` and expects the help to name the cache figures. Today `factory-bill` has no `--help`: `run` reads `--help` as a work item id and exits 2 with `not a work item id: --help`. So the help is new behaviour that no Interface line or criterion covers. Options: (a) add an Interface line, "`factory-bill --help` prints the usage and names the cache read, cache written and hit rate figures and exits 0", plus a criterion for it; or (b) change the smoke test to run the bill on a work item with cost records, with an `Expect:` that names the new line. I would pick (a), because the smoke test cannot count on a work item having records.
   6. Per role versus per stage: cost records carry both `stage` and `role`, and today's table is per stage. Please confirm that the new lines group by `role` (the field in the record), in the order each role first ran. Please also say whether the role lines have their own **total** row; criterion 2's "add up to the work item's figures" suggests that they sum and need no total row.

   Once these are answered I expect to accept on the `tests` route: the change is in `src/factory/watching/domain/bills.py` and `src/factory/entry/bill.py`, and the human's leave for the five named test files covers the earlier tests. The scope is the feature's S0003 line and is not in its Out of scope.
4. 2026-11-08 human: As you recommend:
   1. (a) After the `Cost:` line, one line `Cache: <read> read, <written> written, <n> % hit` for the work item; then a table `| role | cache read | cache written | hit rate |` with one row per role, in the order each role first ran, and a **total** row. Treat this as the Interface's exact format.
   2. The work item's total; no new total across the work items in flight.
   3. Only `factory-bill`; the posted cost table and the acceptance report stay unchanged.
   4. Half up, as the bill's other figures; add the criterion with 2 of 3 giving `67 %`.
   5. (a) `factory-bill --help` prints the usage, names the cache read, cache written and hit rate figures, and exits 0; add the criterion.
   6. Grouped by the record's `role`, in the order each role first ran; the role table has the **total** row of answer 1, which equals the `Cache:` line.
