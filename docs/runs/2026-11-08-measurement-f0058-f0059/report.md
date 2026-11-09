# Measurement run: F0058 and F0059 against the baseline

Date: 2026-11-08. The same demo, demo-todo F0001 (four stories and the acceptance, started one at a time), built twice on a fresh repository:

- **Baseline:** `pkrahmer/kumpel-demo-todo-2`, instance `demo2`, before F0058 and F0059 (eval in [../2026-11-08-e2e-demo-todo-2/eval.md](../2026-11-08-e2e-demo-todo-2/eval.md)).
- **Measured:** `pkrahmer/kumpel-demo-todo-3`, instance `demo3`, kumpel-factory `develop` at 73db6c861: F0058 (agent runs share a cached start: same tools, one system prompt, the work item first, start facts) and F0059 (each change is checked once: the coder starts from the tester's tests, the factory runs the whole `make check` once, after the smoke tester).

Both runs stop at the accepted acceptance; the three stories the measured run's acceptance proposed (S0005 to S0007) were not run. Figures come from the cost records and journals of the `done/` work items (`measure.py` in the session's scratchpad).

> **Correction (2026-11-08, later):** this report priced every role at opus. The baseline ran intake and the documenter on sonnet; priced at the models each role used, the baseline cost $8.32 and the measured run $8.40, about the same, not 7 % less. See [../2026-11-08-measurement-f0060/report.md](../2026-11-08-measurement-f0060/report.md).

## Results

| | Baseline | Measured | Change |
| :-- | --: | --: | --: |
| Agent runs | 40 | 36 | −10 % |
| Turns | 249 | 177 | **−29 %** |
| Agent minutes (run time) | 27.8 | 24.5 | −12 % |
| Model minutes | 23.9 | 21.2 | −11 % |
| Shell minutes inside runs | 3.9 | 2.9 | −26 % |
| Wall clock, first start to acceptance | 45 min | 38 min | −16 % |
| Cache written | 1.06 M | 0.96 M | −9 % |
| Cache read | 4.64 M | 4.15 M | −11 % |
| Output | 139 k | 139 k | 0 % |
| Cache hit (read ÷ all prompt tokens) | 81 % | 81 % | 0 |
| Cost as recorded | $8.27 | $11.26 | +36 % (see below) |
| Cost at one price list (Opus: input $4, write $5, read $0.20, output $20 per M) | $9.01 | $8.41 | **−7 %** |

## Reading the numbers

- **The recorded cost is not comparable.** The baseline ran on the API key; the measured run on the subscription, after the key ran out at 14:46. Claude Code on the subscription writes the cache for one hour, at twice the input price, instead of five minutes at 1.25 times. Priced that way, the measured run's tokens give its recorded $11.26; at one price list it is 7 % cheaper than the baseline. On the subscription the dollar figure is notional anyway.
- **Turns fell most (−29 %).** The coder went from 71 to 42 turns and the reviewer from 45 to 19: the start facts and the work item in the first message replace the turns the agents spent gathering facts (F0058-S0004, S0008), and the coder no longer runs the whole suite first (F0059-S0001).
- **The cache hit stayed at 81 %.** Fewer turns mean fewer re-reads of a long prefix, so cache read fell with cache written. Per role the shared start shows where a role runs once per story: intake 49 → 66 %, documenter 75 → 84 %, acceptance 91 → 93 %. The reviewer fell (75 → 60 %), because it now makes few turns after a large first message, which is written once and read little.
- **Time fell less than turns (−12 % agent minutes, −16 % wall clock).** Model time dominates, and output stayed the same. The checks moved out of the runs (shell minutes −26 %); the factory's own checks are not in these minutes.
- **One sample each.** The stories' paths differed: the measured S0003 had a question (starlette's `httpx2` type stubs) and a review round, the baseline S0002 a review round. Differences under about 10 % are within that noise.

## Per role

| Role | Runs (base → now) | Turns | Cache written (k) | Hit |
| :-- | :-- | :-- | :-- | :-- |
| intake | 4 → 4 | 17 → 13 | 85 → 68 | 49 → 66 % |
| tester | 7 → 7 | 51 → 41 | 155 → 170 | 85 → 82 % |
| coder | 12 → 10 | 71 → 42 | 234 → 218 | 83 → 75 % |
| reviewer | 8 → 6 | 45 → 19 | 249 → 187 | 75 → 60 % |
| documenter | 4 → 4 | 25 → 26 | 131 → 123 | 75 → 84 % |
| smoke tester | 4 → 4 | 19 → 14 | 100 → 80 | 69 → 70 % |
| acceptance reviewer | 1 → 1 | 21 → 22 | 108 → 110 | 91 → 93 % |

## Open points

- A second measured run on the same login as its baseline would settle the cost question; the subscription's one-hour cache may also change which start is shared across stages.
- The factory's own check minutes are not in the cost records; the journals name only some of them. A measure of the time between stages (as in the baseline's eval, *Where the factory's time goes*) would show F0059's main effect.
- The measured acceptance proposed three stories for the demo (S0005 to S0007); they stay in its backlog.
