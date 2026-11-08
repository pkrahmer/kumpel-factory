---
stage: docs
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 661
comments_read: [6721548904]
handed_over: null
claim:
  instance: vm
  stage: docs
  started_at: '2026-11-08T12:52:44.682147Z'
  lease_duration: 60
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
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T12:35:01.598179Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T12:35:33.502332Z'
  stage: intake
  run: b6614815e06744afa492fbcbf9417f85
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T12:35:38.732102Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T12:39:52.910706Z'
  stage: tests
  run: fc19fb322b7a4a6c8be5e7da9a9b5456
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T12:39:58.144958Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-08T12:45:46.868689Z'
  stage: doing
  run: e437e0e5728041f7a58d44119236f9b9
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-08T12:45:52.218863Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-08T12:46:59.845121Z'
  stage: review
  run: 014e836c85e44d829a430a90e32194ac
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-08T12:47:04.951407Z'
  stage: doing
- number: 14
  speaker: coder
  kind: result
  at: '2026-11-08T12:47:15.028460Z'
  stage: doing
  run: 308313753839450db9a5c3f5fdcb0cae
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-08T12:47:20.615120Z'
  stage: tests
- number: 16
  speaker: tester
  kind: result
  at: '2026-11-08T12:47:52.372479Z'
  stage: tests
  run: 99a9bea632304b4eae5c3ab9ba823c8b
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-08T12:47:57.677225Z'
  stage: doing
- number: 18
  speaker: coder
  kind: result
  at: '2026-11-08T12:52:09.314924Z'
  stage: doing
  run: 7732de6b3e584021b438007899491f3e
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-08T12:52:14.684793Z'
  stage: review
- number: 20
  speaker: reviewer
  kind: result
  at: '2026-11-08T12:52:39.452438Z'
  stage: review
  run: b07dcf28f7cb4b79b9b4ba337b20ceb6
- number: 21
  speaker: factory
  kind: started
  at: '2026-11-08T12:52:44.682147Z'
  stage: docs
---

# The bill shows how well the cache works

## Description

Every cost record already holds a run's tokens: input, output, cache read and cache written. The bill (`factory-bill`) shows the cost and the runs, but not these tokens, so nobody can see whether the cache works without reading the records by hand.

After this story, the bill shows for each work item, and in its total, the tokens read from the cache, the tokens written to it, and the hit rate. The hit rate is the tokens read from the cache divided by all prompt tokens (read, written and uncached input). The bill also shows the same three figures per role. This is the measure for this feature's goal, and for every later change to the prompts.

## Interface

As answered by the human in journal entry 4:

- `factory-bill <work item>` and `factory-bill` (each work item in flight, one block each) print, after each work item's `Cost: ...` line and nothing else changed before it: one line `Cache: <read> read, <written> written, <n> % hit` for the work item; then a table `| role | cache read | cache written | hit rate |` with one row per role (the cost record's `role` field), in the order each role first ran, and a **total** row whose three figures equal the `Cache:` line. There is no total across the work items in flight.
- The hit rate is the tokens read from the cache divided by all prompt tokens (cache read + cache written + uncached input), shown as a whole percent rounded half up, as the bill's other figures are (2 of 3 gives `67 %`). A work item or role with no prompt tokens shows `-` in place of `<n> %`.
- `factory-bill --help` prints the usage, names the cache read, cache written and hit rate figures, and exits 0.
- Only `factory-bill` changes: the cost table posted on the pull request at the hand-over and the acceptance report stay unchanged. The change lies in `src/factory/watching/domain/bills.py` and `src/factory/entry/bill.py`.
- Today's lines and their order stay as they are.
- The human's leave for earlier tests: a test that pins the bill's whole output or its models may change to hold the new figures, keeping its name and checking otherwise the same thing: `tests/entry/test_bill.py`, `tests/watching/application/test_bill_service.py`, `tests/watching/domain/test_bills.py`, `tests/watching/domain/test_bills_model_time.py` and `tests/hosting/application/test_costs.py`. The tester's entry names each one it changed.

## Acceptance criteria

1. A bill over cost records with known tokens shows the right `Cache:` line (cache read, cache written and hit rate) after the `Cost:` line, for one work item and for each of several work items in flight (rows of one test).
2. The role table has one row per role in the order each role first ran, and its rows add up to the **total** row, which equals the `Cache:` line.
3. The hit rate rounds half up to a whole percent: 2 of 3 prompt tokens read from the cache shows `67 %`, and 1 of 3 shows `33 %` (rows of one test).
4. A work item with no prompt tokens shows `-` for its hit rate.
5. Every earlier line of the bill is unchanged, and the posted cost table and the acceptance report are unchanged.
6. `factory-bill --help` prints the usage naming cache read, cache written and hit rate, and exits 0.
7. `factory-bill -h` prints the same help as `factory-bill --help` and exits 0.
8. `make check` stays green.
9. docs: the operator's documents that show the bill name the three new figures and how to read the hit rate.

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
5. factory: started intake as vm.
6. intake: accepted (route `tests`). I carried the human's answers from journal entry 4 into the story: I rewrote `## Interface` and `## Acceptance criteria` in the work item file. The description still holds as written.
   - Interface: it now gives the exact format. After each work item's `Cost:` line comes `Cache: <read> read, <written> written, <n> % hit`, then the table `| role | cache read | cache written | hit rate |`, with one row per record `role` in the order each role first ran, and a **total** row equal to the `Cache:` line. There is no total across the work items in flight. The hit rate is read / (read + written + uncached input), rounded half up to a whole percent, and `-` when there are no prompt tokens. `factory-bill --help` prints the usage naming the three figures and exits 0. The posted cost table (`hand_over.py`) and the acceptance report stay unchanged. The earlier-test leave is kept as the human wrote it.
   - Criteria: there are now eight; the old 1 to 6 became 1, 2, 4, 5, 7 and 8. Answer 4 brought the rounding criterion (3, `67 %` and `33 %` as rows), and answer 5 brought the `--help` criterion (6). Both go before `make check` and `docs:`, which stay last. I widened criterion 1 to cover one work item and several in flight. Criterion 2 covers the role order and the total row. Criterion 5 now also says that the posted table and the acceptance report are unchanged. Each criterion can be tested by one test function. The refused or edge sides are covered by 3 (rounding), 4 (`-`) and 5 (unchanged lines).
   - Smoke test: `uv run factory-bill --help` can be run once criterion 6 is built (today `--help` is read as an id and exits 2). Its `Expect:` line can be checked against the help text.
   - Docs criterion: it names what the operator must know (the three figures and how to read the hit rate) and dictates no sentences.
   - Architecture: the change lies in `src/factory/watching/domain/bills.py` (the domain's figures and table) and `src/factory/entry/bill.py` (the command line and `--help`). It needs no new interface, dependency or change under `factory/`.
   - Scope: this is the feature's S0003 line, and none of it falls under the feature's Out of scope.
7. factory: started tests as vm.
8. tester: Wrote the tests for the bill's cache figures. They test the command through `factory.entry.bill.run`, using a real `BillService` on a local bare remote with pushed sidecars, and assume no domain names the Interface does not give.

   - criterion 1: tests/entry/test_bill_cache.py::test_the_cache_line_follows_each_cost_line_with_read_written_and_hit_rate (rows `one-work-item` and `every-work-item-in-flight`; known tokens give `Cache: 490 read, 88 written, 82 % hit` and `Cache: 2 read, 0 written, 67 % hit`)
   - criterion 2: tests/entry/test_bill_cache.py::test_the_role_table_has_a_row_per_role_in_first_run_order_adding_up_to_the_total_row. The records run tester, coder, reviewer, then coder again under another stage, so grouping by stage instead of by role fails the test.
   - criterion 3: tests/entry/test_bill_cache.py::test_the_hit_rate_rounds_half_up_to_a_whole_percent (2/3 gives `67 %` and 1/3 gives `33 %`, plus the exact halves 1/8 gives `13 %` and 1/200 gives `1 %`, which rounding half to even would get wrong)
   - criterion 4: tests/entry/test_bill_cache.py::test_no_prompt_tokens_shows_a_dash_for_the_hit_rate (rows `work-item` and `role`, where one role with no prompt tokens shows `-`)
   - criterion 5: tests/entry/test_bill_cache.py::test_every_earlier_line_of_the_bill_is_unchanged (rows for one work item and for every work item in flight: with the cache section taken out, the output equals `cost_table`, an empty line and `Cost: cost_line`, the same functions the hand-over and acceptance report use). The posted table and the report stay pinned by the existing, unchanged tests: tests/watching/domain/test_bills.py::test_the_cost_table_of_the_demo_stage_bills, ::test_the_cost_line_of_the_demo_bill, and tests/pipeline/application/handlers/test_hand_over.py.
   - criterion 6: tests/entry/test_bill_cache.py::test_the_help_prints_the_usage_naming_the_cache_figures (`run(["--help"], ...)`: the text starts with `usage: factory-bill`, names `cache read`, `cache written` and `hit rate`, and returns 0)
   - criterion 7: no test of its own; it is `make check`.
   - criterion 8: docs, for the docs stage.

   The Interface does not say where blank lines go around the new section, or what the table's alignment row looks like. The helpers in `tests/support/bill_cache_support.py` therefore accept blank lines between the `Cost:` line, the `Cache:` line and the table, and skip the header and the alignment row. They require the header `| role | cache read | cache written | hit rate |`, the role in the first cell, plain integers, `<n> %` or `-`, and `**total**` as the last row's first cell (as the stage table writes it).

   Files created: tests/entry/test_bill_cache.py and tests/support/bill_cache_support.py.

   Earlier test changed under the human's leave in the Interface: tests/entry/test_bill.py. Its four exact-output assertions now compare the output with the cache section removed (`without_cache`, `without_cache_in_flight`). Test names and what they check are unchanged. I did not change the other four files the leave names.

   Run: `make test` fails only in tests/entry/test_bill_cache.py (all tests) and the four changed tests in tests/entry/test_bill.py. Each failure has the right cause: no `Cache:` line yet ("expected one cache line"), or `--help` is still read as an id. Every module imported; nothing failed to collect. `make lint` is green; I skipped the type check as the stage says.

   `lint`: lint: green (0.2 s)
9. factory: started doing as vm.
10. coder: I built the bill's cache figures. All of the tester's tests pass unchanged, and `make check` is green (lint, types, layers, sast, secrets, licenses, test).

    - `src/factory/watching/domain/bills.py`:
      - New model `RoleBill` and function `bills_by_role`. They group the records by `role` in the order each role first ran. `bills_by_stage` now uses the same private `_groups` helper, so the grouping is not written twice.
      - `hit_rate(tokens)`: the cache read divided by (read + written + uncached input), as a whole percent rounded half up with `Decimal`, or `-` when there are no prompt tokens.
      - `cache_line(bill)`: `<read> read, <written> written, <n> % hit`.
      - `cache_table(role_bills)`: the header `| role | cache read | cache written | hit rate |`, one row per role, and a `**total**` row summed with the existing `_sum`.
      - `cost_table` and `cost_line` are untouched, so the posted cost table (`hand_over.py`) and the acceptance report are unchanged.
    - `src/factory/watching/application/costs.py`: `WorkItemBill` has two new text fields, `cache` and `cache_by_role`, which `BillService.for_work_item` fills from the same records. This file lies outside the two files the Interface names. It is the only way the entry can get the per-role figures, because `WorkItemBill` carries no records. No contract model changed.
    - `src/factory/entry/bill.py`:
      - Each block is now the stage table, an empty line, `Cost: ...`, `Cache: ...`, an empty line and the role table.
      - `--help` (and `-h`) prints the usage and a short text that names cache read, cache written and hit rate and says how the hit rate is computed. It exits 0.

    Main choice: the entry gets finished texts (`cache`, `cache_by_role`) in `WorkItemBill`, the same way it already gets `line` and `table`. I rejected two alternatives:
    - putting the raw records into `WorkItemBill` and grouping them in the entry, which would put domain work into the command line;
    - a separate service call for the cache figures, which would read the sidecar twice.

    Refactor pass: one `ruff format` fix in `cache_line`; nothing else needed changing.

    Not touched: the `Cache:` line sits directly under `Cost:`, with no empty line between them. The Interface does not say where empty lines go, and the tests accept either.

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
11. factory: started review as vm.
12. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'`: `src/factory/entry/bill.py`, `src/factory/watching/application/costs.py`, `src/factory/watching/domain/bills.py`, `tests/entry/test_bill.py`, `tests/entry/test_bill_cache.py` and `tests/support/bill_cache_support.py`.

    Findings:

    1. criterion 7 added: it needs its test. `src/factory/entry/bill.py` `_HELP_FLAGS = ("-h", "--help")` builds a behaviour that no criterion names: `factory-bill -h` used to exit 2 with `not a work item id: -h`, and now it prints the help and exits 0. No test covers it, since `tests/entry/test_bill_cache.py::test_the_help_prints_the_usage_naming_the_cache_figures` runs only `--help`. I added criterion 7 to the work item: "`factory-bill -h` prints the same help as `factory-bill --help` and exits 0". The closing criteria are now 8 (`make check`) and 9 (docs). Fix: the coder ends with `tests`, and the tester pins `-h`. The two flags are sides of one rule, so the best fit is a parametrized row beside `--help` in the help test.

    What I checked and found sound:
    - Group 1: criteria 1 to 6 each have a test that checks what the criterion says. The figures in the mixed case come out right: tester 60 %, coder 340/400 = 85 %, reviewer 90 %, total 490/600 = 82 %. Rounding half up is pinned at the exact halves (1/8 and 1/200). The `-` side and the non-zero side of the hit rate are both tested. Criterion 5 compares the output, with the cache section removed, against `cost_table` and `cost_line`; the hand-over and the acceptance report use the same functions, and their existing tests are unchanged. The journal records `make check` green after the coder.
    - Group 2: the domain stays pure. `hit_rate`, `cache_line`, `cache_table`, `RoleBill` and `bills_by_role` live in `factory.watching.domain.bills`, and the new `_groups` is shared with `bills_by_stage` rather than copied. The change to `WorkItemBill` in `costs.py` lies outside the two files the Interface names. That is not a finding: `WorkItemBill` is used only by `factory.entry.bill`, so the posted cost table and the acceptance report stay unchanged, and no contract model changed.
    - Group 3: no markers, no secrets, no command built from strings.
    - Group 4: the new public names have docstrings. Rounding uses `Decimal` with `ROUND_HALF_UP`, like `one_decimal` and `_dollars`.
    - Group 5: the journal names the main choice (finished texts in `WorkItemBill`) and the two alternatives it rejected, and the Description still matches what was built.

    Earlier tests:
    - `tests/entry/test_bill.py`: changed under the human's leave in the Interface (journal entry 4, carried in by intake in entry 6). Its four tests keep their names, and each still checks the same output with the cache section removed.
13. factory: started doing as vm.
14. coder: Round 1: the reviewer's only finding adds criterion 7: "`factory-bill -h` prints the same help as `factory-bill --help` and exits 0". The code already does this, because `_HELP_FLAGS = ("-h", "--help")` in `src/factory/entry/bill.py` covers both flags. The criterion only needs its test, so I changed no code and am sending the work item to the tester.

    For the tester: pin `-h` as a parametrized row beside `--help` in `tests/entry/test_bill_cache.py::test_the_help_prints_the_usage_naming_the_cache_figures`, as the reviewer suggested.

    The journal did not change the meaning of the task, so the Description stays as written. I did not run `make check` this round because nothing changed since round 0, when it was green.
15. factory: started tests as vm.
16. tester: Round 1: I pinned the reviewer's criterion 7 (`factory-bill -h` prints the same help as `factory-bill --help` and exits 0), as the coder's entry 14 asked. No code needed to change.

    - criterion 6 and criterion 7: tests/entry/test_bill_cache.py::test_the_help_prints_the_usage_naming_the_cache_figures. It is now parametrized over `flag`, with the rows `--help` and `-h`. Each row checks that the text starts with `usage: factory-bill`, names `cache read`, `cache written` and `hit rate`, equals the output of `run(["--help"], ...)`, and that the call returns 0.
    - The other criteria keep the mapping in entry 8, with the numbers moved: `make check` is now criterion 8 and docs is criterion 9.

    Files changed: tests/entry/test_bill_cache.py (this round's own test; I changed no earlier test of another story). I created no new files.

    Run: `uv run pytest -q tests/entry/test_bill_cache.py`: all 13 passed. Both rows pass because the coder's `_HELP_FLAGS` already covers `-h`. Every module imported.

    `lint`: lint: green (0.1 s)

    `lint`: lint: green (0.2 s)
17. factory: started doing as vm.
18. coder: Round 1: The tester pinned criterion 7 in entry 16. It is now a `-h` row beside `--help` in `tests/entry/test_bill_cache.py::test_the_help_prints_the_usage_naming_the_cache_figures`. That was the reviewer's only finding, and the code already met it: `_HELP_FLAGS = ("-h", "--help")` in `src/factory/entry/bill.py` covers both flags. I changed no code this round, so there is nothing new for the refactor pass.

    - Built (round 0, unchanged): `src/factory/watching/domain/bills.py`, `src/factory/watching/application/costs.py` and `src/factory/entry/bill.py`. Entry 10 gives the main choice (finished texts in `WorkItemBill`) and the alternatives I rejected.
    - Description: the journal added criterion 7 but did not change the meaning of the task, so the Description stays as written.
    - Noticed, not touched: nothing new.

    `check`: check: green

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
19. factory: started review as vm.
20. reviewer: Round 1: I reviewed `git diff develop...HEAD -- . ':!factory'`. It changes `src/factory/entry/bill.py`, `src/factory/watching/application/costs.py`, `src/factory/watching/domain/bills.py`, `tests/entry/test_bill.py`, `tests/entry/test_bill_cache.py` and `tests/support/bill_cache_support.py`.

    no findings

    What I checked:
    - Group 1:
      - Criterion 7 (my round 0 finding) is now pinned. `tests/entry/test_bill_cache.py::test_the_help_prints_the_usage_naming_the_cache_figures` is parametrized over `--help` and `-h`. Each row checks that the text starts with `usage: factory-bill`, that it names cache read, cache written and hit rate, that it equals the `--help` output, and that the call returns 0. `_HELP_FLAGS` in `src/factory/entry/bill.py` covers both flags, and the help check sits after the `len(argv) > 1` check.
      - Criteria 1 to 6 keep the tests named in entry 8, and each test checks what its criterion says. I recomputed the mixed case: tester 60/100 = 60 %, coder 340/400 = 85 %, reviewer 90/100 = 90 %, total 490/578 = 84.8 %. The total row's 82 % comes from this as well: 490/(490+88+22) = 490/600 = 81.7 %, which rounds to 82 %. Both are right.
      - Half up is pinned at 2/3, 1/3 and the exact halves 1/8 and 1/200. The `-` side is tested for the work item and for one role.
      - Criterion 5: `cost_table` and `cost_line` are untouched, so the hand-over table and the acceptance report stay unchanged.
      - Entry 18 records `make check` green after the coder.
    - Group 2: the domain stays pure. `bills_by_role`, `hit_rate`, `cache_line` and `cache_table` live in `factory.watching.domain.bills`, and `_groups` is shared with `bills_by_stage` rather than copied. `WorkItemBill` gains two text fields. Only `factory.entry.bill` reads them, and they are not part of the records contract.
    - Group 3: no markers, secrets or command strings. An unknown argument still goes through the work item id check.
    - Group 4: the new public names have docstrings. Rounding uses `Decimal` with `ROUND_HALF_UP`, like the bill's other figures. There is no dead code.
    - Group 5: entry 10 gives the main choice and the two alternatives it rejected. The Description matches what was built. Criterion 9 (docs) still says what the operator must know.

    Earlier tests:
    - `tests/entry/test_bill.py`: changed under the human's leave in the story's Interface, which names this file. The human's answers are in journal entry 4, and intake carried the leave into the story in entry 6. Its four tests keep their names and check the same output with the cache section removed.
21. factory: started docs as vm.
