# Baseline: the demo built by plain Claude Code sessions

Date: 2026-11-10. The question: what does the todo demo (demo-todo F0001, four stories) cost when ordinary Claude Code sessions build it, without the factory, to the same quality?

## Setup

- Start: demo4's commit a067c89, the empty project (the same `CLAUDE.md`, `Makefile`, `pyproject.toml` and `make check` configuration) and the feature with its four stories as the human wrote them, before any factory stage touched them.
- `claude -p` sessions on the VM, in the stage image `factory-stage:vm`: model opus (`claude-opus-5-5`), Claude Code's default effort and cache, `--permission-mode bypassPermissions`, no factory, no reviewer, no acceptance.
- **One session** (07:36 to 07:43 UTC, cap $40): one prompt for the whole feature: build S0001 to S0004 in order; meet every criterion with tests written first; update the documents each story's docs criterion names; run the smoke tests against their `Expect:` lines; get `make check` green; one commit per story; decide open points alone and record them in `docs/decisions.md`.
- **Four sessions** (15:29 to 15:39 UTC, cap $20 each): one fresh session per story, one after the other, with the same wording for that story alone ("Build only this story"; from S0002 on, "the earlier stories are already built and committed"). Each starts with no memory of the one before.
- The factory side is run 4, demo4 (F0060, `../2026-11-08-measurement-f0060/report.md`).

## Cost and time

| | One session | Four sessions | Factory (demo4) |
| :-- | --: | --: | --: |
| Cost (list prices) | $1.70 | $3.07 | $6.85 |
| Agent runs | 1 | 4 | 31 |
| Turns | 28 | 58 | 165 |
| Model minutes | 5.4 | 8.2 | |
| Wall clock | 6.5 min | 9.3 min | 34 min |
| Cache written | 73 k | 173 k | 690 k |
| Cache read | 1.47 M | 2.52 M | 4.15 M |
| Output | 41 k | 59 k | 127 k |
| Questions to the human | 0 | 0 | 0 |

The four sessions per story: S0001 $0.67, S0002 $0.44, S0003 $1.12, S0004 $0.84. Sessions 2 to 4 each read their first 12,984 tokens (Claude Code's part and the project's `CLAUDE.md`) from the one-hour cache the session before had written. A user who works one story a day would write them again, about $0.10 more per session.

## Quality

| | One session | Four sessions | Factory (demo4) |
| :-- | --: | --: | --: |
| `make check` | green | green | green |
| Tests | 157 | 168 | 146 |
| Coverage (lines and branches) | 100 % | 100 % | 99 % |
| Lines in `src/`, `tests/` | 549, 998 | 504, 1,221 | 497, 1,092 |
| Docs words: README, api, project guide, decisions | 241, 583, 718, 714 | 246, 649, 1,360, 1,057 | 258, 1,061, 369, none |
| Mutants killed (`make mutants FEATURE=F0001`, 17 modules) | 217 of 223, 97.3 % | 213 of 219, 97.3 % | 233 of 242, 96.3 % |
| `make duplicates` | 0 similar, 11 dead | 0 similar, 9 dead | 0 similar, 6 dead |
| demo4's 146 tests on this code | all pass | all pass | |
| This side's tests on demo4's code | 143 pass, 3 fail, 1 module does not import | 167 pass, 1 fails | |

The plain tests that fail on demo4's code check the sessions' own stricter decisions: the one session refuses unknown fields in a request body, and both document the real error body in the schema; one test module of the one session imports a name demo4 does not have. Both plain runs keep a decision log; demo4 has none for the demo.

## Reading the numbers

- **On this demo, plain sessions built the same quality for a quarter to a half of the factory's cost and a fifth to a quarter of its time.** By every measure here (the check, coverage, mutants, demo4's tests on their code, the documents) their results are at least as good.
- **One session against four:** splitting the feature into fresh sessions cost 1.8 times as much, because each session reads the project and the code built so far again. The factory goes further down that road: 31 fresh runs, each reading its role, the rules, the story and the code again, and stages (intake, review, smoke test, acceptance) that found little to fix on this demo.
- **What the demo does not measure:** the factory's worth lies where a plain session has no answer: the human's decisions and acceptance on a pull request per story, the written trail, review by a separate role, unattended work across many stories and days, recovery after a crash, and the agent's isolation from the host. The demo's stories are small, precise, and written in the factory's form with an Interface; the human's design work in them helps every side alike.
- **One sample each.** Differences under about 10 % are within the noise; the factors of two and four are not.

## Open points

- A plain session on a larger feature, where one context fills up, is the comparison that would show where the factory starts to pay.
- The stages that found nothing on this demo (intake's rewrite, review rounds, the acceptance) are the place to look for savings.
