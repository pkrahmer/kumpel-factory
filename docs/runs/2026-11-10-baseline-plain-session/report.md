# Baseline: the demo built by one plain Claude Code session

Date: 2026-11-10. The question: what does the todo demo (demo-todo F0001, four stories) cost when one ordinary Claude Code session builds it, without the factory, to the same quality?

## Setup

- Start: demo4's commit a067c89, the empty project (the same `CLAUDE.md`, `Makefile`, `pyproject.toml` and `make check` configuration) and the feature with its four stories as the human wrote them, before any factory stage touched them.
- One `claude -p` session on the VM, in the stage image `factory-stage:vm`: model opus (`claude-opus-5-5`), Claude Code's default effort and cache, `--permission-mode bypassPermissions`, a budget cap of $40, no factory, no reviewer, no acceptance.
- The prompt, as a user would type it: build S0001 to S0004 in order; meet every criterion with tests written first; update the documents each story's docs criterion names; run the smoke tests against their `Expect:` lines; get `make check` green; one commit per story; decide open points alone and record them in `docs/decisions.md`.
- The factory side is run 4, demo4 (F0060, `../2026-11-08-measurement-f0060/report.md`).

## Cost and time

| | Plain session | Factory (demo4) | Factory against plain |
| :-- | --: | --: | --: |
| Cost (list prices) | $1.70 | $6.85 | 4.0 times |
| Agent runs | 1 | 31 | |
| Turns | 28 | 165 | |
| Model minutes | 5.4 | | |
| Wall clock | 6.5 min | 34 min | 5.2 times |
| Cache written | 73 k (all one-hour) | 690 k | |
| Cache read | 1.47 M | 4.15 M | |
| Output | 41 k | 127 k | |
| Questions to the human | 0 | 0 | |

## Quality

| | Plain session | Factory (demo4) |
| :-- | --: | --: |
| `make check` | green | green |
| Tests | 157 | 146 |
| Coverage (lines and branches) | 100 % | 99 % |
| Lines in `src/`, `tests/` | 549, 998 | 497, 1,092 |
| Docs words: README, api, project guide, decisions | 241, 583, 718, 714 | 258, 1,061, 369, none |
| Mutants killed (`make mutants FEATURE=F0001`, 17 modules) | 217 of 223, 97.3 % | 233 of 242, 96.3 % |
| `make duplicates` | 0 similar, 11 dead | 0 similar, 6 dead |
| The other side's tests on this side's code | demo4's 146 all pass | plain's: 143 pass, 3 fail, 1 module does not import |

The three plain tests that fail on demo4's code check the plain session's own stricter decisions: unknown fields in a request body are refused, and the schema documents the real error body. The fourth imports a name demo4 does not have. The plain session recorded 14 decisions in `docs/decisions.md`; demo4 has no decision log for the demo.

## Reading the numbers

- **On this demo, the plain session built the same quality for a quarter of the cost and a fifth of the time.** By every measure here (the check, coverage, mutants, the other side's tests, the documents) its result is at least as good.
- **Why it is cheaper:** one context reads the project once and keeps it; the factory starts 31 fresh runs, each reading its role, the rules, the story and the code again, and adds stages (intake, review, smoke test, acceptance) that found little to fix on this demo.
- **What the demo does not measure:** the factory's worth lies where a single session has no answer: the human's decisions and acceptance on a pull request per story, the written trail, review by a separate role, unattended work across many stories and days, recovery after a crash, and the agent's isolation from the host. The demo's stories are small, precise, and written in the factory's form with an Interface; the human's design work in them helps both sides alike.
- **One sample.** A second plain run would show how much the result varies; differences under about 10 % are within that noise, the factor of four is not.

## Open points

- A plain session on a larger feature, where one context fills up, is the comparison that would show where the factory starts to pay.
- The stages that found nothing on this demo (intake's rewrite, review rounds, the acceptance) are the place to look for savings.
