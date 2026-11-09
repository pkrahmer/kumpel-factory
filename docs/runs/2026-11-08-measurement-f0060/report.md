# Measurement run: F0060 against the earlier demo runs

Date: 2026-11-08. The same demo, demo-todo F0001 (four stories and the acceptance, started one at a time), built on a fresh repository each time. Figures come from the cost records and journals of the `done/` work items, each role priced at the model it ran on (`measure.py` and `routes.py` in the session's scratchpad), and from the transcripts on the VM for demo3 and demo4.

| Run | Repository | Factory | Login |
| :-- | :-- | :-- | :-- |
| 1 | `pkrahmer/kumpel-demo-todo`, 2026-11-01 | before F0058 | subscription |
| 2 | `pkrahmer/kumpel-demo-todo-2` | before F0058 (the baseline) | API key |
| 3 | `pkrahmer/kumpel-demo-todo-3` | F0058 and F0059 | subscription |
| 4 | `pkrahmer/kumpel-demo-todo-4` | F0060 (at 02c044019) | subscription |

Run 1 is incomplete: three of the four stories are in `done/`, and it has no acceptance. Its totals are shown for completeness and are not compared.

## Models

The agent files set `model:` and `effort:` per role; Claude Code turns `opus` into `claude-opus-5-5` and `sonnet` into `claude-sonnet-5-5` (version 2.1.318 in the transcripts of runs 3 and 4, which name `claude-opus-5-5` for every answer). The transcripts of runs 1 and 2 are gone; their agent files say:

| Run | intake | documenter | tester, coder, smoke tester | reviewer, acceptance reviewer |
| :-- | :-- | :-- | :-- | :-- |
| 1, 2 | sonnet, low | sonnet, medium | opus, medium | opus, high |
| 3, 4 | opus, medium | opus, medium | opus, medium | opus, high |

F0058-S0001 moved intake and the documenter to opus so that every role shares one cached start. Prices per million tokens, from the Claude API reference: Opus 5.5 input 4, five-minute write 5, one-hour write 8, read 0.20, output 20; Sonnet 5.5 input 2, five-minute write 2.50, one-hour write 4, read 0.20, output 10. Run 2's recorded cost (on the API key, the real price) is $8.27; priced this way it is $8.32, so the method holds.

## Results

| | Run 2 (baseline) | Run 3 (F0058, F0059) | Run 4 (F0060) | 4 against 2 | 4 against 3 |
| :-- | --: | --: | --: | --: | --: |
| Agent runs | 40 | 36 | 31 | −23 % | −14 % |
| Turns | 249 | 177 | 165 | −34 % | −7 % |
| Agent minutes | 27.8 | 24.5 | 22.1 | −21 % | −10 % |
| Wall clock, first start to acceptance | 45 min | 38 min | 34 min | −24 % | −11 % |
| Cache written | 1.06 M | 0.96 M | 0.69 M | −35 % | −28 % |
| Cache read | 4.64 M | 4.15 M | 4.15 M | −11 % | 0 % |
| Output | 139 k | 139 k | 127 k | −9 % | −9 % |
| Cache hit | 81 % | 81 % | 86 % | +5 | +5 |
| Cost at the models used | $8.32 | $8.40 | **$6.85** | **−18 %** | **−18 %** |
| Cost as recorded | $8.27 | $11.26 | $6.85 | | |

Run 1, for completeness (three stories, no acceptance): 35 runs, 197 turns, 19.1 agent minutes, $5.40 at the models used.

## Reading the numbers

- **F0060 cut the cost by 18 %**, all of it from writing less into the cache (−28 %): every first request of run 4 reads 11,959 tokens from the cache (the tools, Claude Code's part, the shared rules and the demo's `CLAUDE.md`) against 6,683 in run 3, and writes about 13,600 tokens instead of 18,700. All of run 4's writes are five-minute ones (0.59 M, none of one hour); run 3's were all one-hour ones (0.96 M). The forecast from the replay was 11 to 14 %; run 4 beat it because the review route also saved runs.
- **The route from review to tests worked.** Run 4's reviewer sent findings to the tester twice and the coder relayed none; runs 2 and 3 each had two coder runs that only passed findings on. The coder ran 6 times against 10 in run 3.
- **Correction to the report of F0058 and F0059** (`../2026-11-08-measurement-f0058-f0059/report.md`): it priced every role at opus and found run 3 7 % cheaper than run 2. At the models used, run 2 cost $8.32 and run 3 $8.40, about the same: F0058-S0001 moved intake and the documenter from sonnet to opus, which ate the token savings. Its findings on turns and time stand.
- **Against the baseline**, F0058 to F0060 together: a third fewer turns, a fifth less time and an 18 % lower cost on the same models' prices.
- **One sample each.** The paths differ from run to run (questions, review rounds); differences under about 10 % are within that noise. Run 4's acceptance proposed three stories for the demo (S0005 to S0007); they stay in its backlog.

## Open points

- The reviewer and the acceptance reviewer run at effort `high`, the other roles at `medium`; a change of effort ends the shared cache, so the shared start is shared within each effort group. One effort for all roles would share it fully; whether the reviewer keeps its quality at `medium` is a separate question.
- The factory's own check minutes are not in the cost records; the time between stages is not measured here.
