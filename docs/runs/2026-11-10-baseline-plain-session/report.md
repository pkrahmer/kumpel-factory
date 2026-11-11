# Baseline: the demo built by plain Claude Code sessions and by a thin factory line

Date: 2026-11-10. The question: what does the todo demo (demo-todo F0001, four stories) cost when ordinary Claude Code sessions build it, without the factory, to the same quality?

## Setup

- Start: demo4's commit a067c89, the empty project (the same `CLAUDE.md`, `Makefile`, `pyproject.toml` and `make check` configuration) and the feature with its four stories as the human wrote them, before any factory stage touched them.
- `claude -p` sessions on the VM, in the stage image `factory-stage:vm`: model opus (`claude-opus-5-5`), Claude Code's default effort and cache, `--permission-mode bypassPermissions`, no factory, no reviewer, no acceptance.
- **One session** (07:36 to 07:43 UTC, cap $40): one prompt for the whole feature: build S0001 to S0004 in order; meet every criterion with tests written first; update the documents each story's docs criterion names; run the smoke tests against their `Expect:` lines; get `make check` green; one commit per story; decide open points alone and record them in `docs/decisions.md`.
- **Four sessions** (15:29 to 15:39 UTC, cap $20 each): one fresh session per story, one after the other, with the same wording for that story alone ("Build only this story"; from S0002 on, "the earlier stories are already built and committed"). Each starts with no memory of the one before.
- **Thin line** (demo5, 22:32 to 22:59 UTC): the factory on `main` 8c45669af, in a fresh repository `pkrahmer/kumpel-demo-todo-5` seeded with the same start plus one commit 761530b in the project's own `factory/`: `pipeline.yml` with the stages doing (role `builder`), review (role `reviewer`), approval and done, and two project agents. `builder.md` writes the tests first, then the code and the documents, runs the smoke test and gets `make check` green; `reviewer.md` is the shipped reviewer with `approval` as its pass. No intake, tester, documenter, smoke tester or acceptance; kumpel-factory unchanged. Stories started one at a time, each approved by the session in the human's seat after the usual checks.
- The full factory side is run 4, demo4 (F0060, `../2026-11-08-measurement-f0060/report.md`).

## Cost and time

| | One session | Four sessions | Thin line (demo5) | Factory (demo4) |
| :-- | --: | --: | --: | --: |
| Cost (list prices) | $1.70 | $3.07 | $4.48 | $6.85 |
| Agent runs | 1 | 4 | 16 | 31 |
| Turns | 28 | 58 | 103 | 165 |
| Model minutes | 5.4 | 8.2 | 15.2 | |
| Wall clock | 6.5 min | 9.3 min | 25 min | 34 min |
| Cache written | 73 k | 173 k | 400 k | 690 k |
| Cache read | 1.47 M | 2.52 M | 2.42 M | 4.15 M |
| Output | 41 k | 59 k | 99 k | 127 k |
| Questions to the human | 0 | 0 | 0 | 0 |

The four sessions per story: S0001 $0.67, S0002 $0.44, S0003 $1.12, S0004 $0.84. Sessions 2 to 4 each read their first 12,984 tokens (Claude Code's part and the project's `CLAUDE.md`) from the one-hour cache the session before had written. A user who works one story a day would write them again, about $0.10 more per session.

The thin line per story: S0001 $1.12, S0002 $0.68, S0003 $1.41, S0004 $1.27, each in four runs: the builder, a review with findings, the builder again, a review that passed. The builder's eight runs had a cache hit of 91 %, the reviewer's 73 % (it runs at effort `high` and shares no start with the builder). The wall clock includes the approvals and the start of each next story.

## Quality

| | One session | Four sessions | Thin line (demo5) | Factory (demo4) |
| :-- | --: | --: | --: | --: |
| `make check` | green | green | green | green |
| Tests | 157 | 168 | 165 | 146 |
| Coverage (lines and branches) | 100 % | 100 % | 100 % | 99 % |
| Lines in `src/`, `tests/` | 549, 998 | 504, 1,221 | 490, 1,104 | 497, 1,092 |
| Docs words: README, api, project guide, decisions | 241, 583, 718, 714 | 246, 649, 1,360, 1,057 | 236, 561, 860, 691 | 258, 1,061, 369, none |
| Mutants killed (`make mutants FEATURE=F0001`, 17 modules) | 217 of 223, 97.3 % | 213 of 219, 97.3 % | 215 of 222, 96.8 % | 233 of 242, 96.3 % |
| `make duplicates` | 0 similar, 11 dead | 0 similar, 9 dead | 0 similar, 9 dead | 0 similar, 6 dead |
| demo4's 146 tests on this code | all pass | all pass | all pass | |
| This side's tests on demo4's code | 143 pass, 3 fail, 1 module does not import | 167 pass, 1 fails | 155 pass, 1 module does not import | |

The plain tests that fail on demo4's code check the sessions' own stricter decisions: the one session refuses unknown fields in a request body, and both document the real error body in the schema; one test module of the one session imports a name demo4 does not have. Both plain runs keep a decision log; demo4 has none for the demo.

## Reading the numbers

- **The thin line keeps the factory's frame for two thirds of its cost.** At $4.48 against $6.85 (−35 %) and 25 against 34 minutes, it built the same quality, and it keeps the pull request and the human's approval per story, the journal and cost lines, `make check` after the builder, a separate reviewer, unattended work and isolation. It costs $1.41 more than four plain sessions: the reviewer's eight runs and the builder's second run per story, all sent back by review findings.
- **On this demo, plain sessions built the same quality for a quarter to a half of the factory's cost and a fifth to a quarter of its time.** By every measure here (the check, coverage, mutants, demo4's tests on their code, the documents) their results are at least as good.
- **One session against four:** splitting the feature into fresh sessions cost 1.8 times as much, because each session reads the project and the code built so far again. The factory goes further down that road: 31 fresh runs, each reading its role, the rules, the story and the code again, and stages (intake, review, smoke test, acceptance) that found little to fix on this demo.
- **What the demo does not measure:** the factory's worth lies where a plain session has no answer: the human's decisions and acceptance on a pull request per story, the written trail, review by a separate role, unattended work across many stories and days, recovery after a crash, and the agent's isolation from the host. The demo's stories are small, precise, and written in the factory's form with an Interface; the human's design work in them helps every side alike.
- **One sample each.** Differences under about 10 % are within the noise; the factors of two and four are not.

## Test first, asked or enforced

Every side was told to write the tests first: the plain prompts said so, the thin line's builder says so, and the full factory gives the tests to a separate tester before the coder starts. The plain transcripts show that the sessions mostly did it unasked-for by any role boundary. In the one session, three of the four stories went: write the tests, run them and see them fail, write the code, run them green; in the fourth it wrote tests and code before the first run. The four sessions show the same order where their writes are visible (they wrote files through shell heredocs, and one session's writes could not be read from its transcript).

So the comparison says only this: on this demo, enforcing test-first through a separate tester role gave no better quality than asking one agent for it. It does not say whether test-first itself matters. That would need a run without it (build first, then write tests until every criterion is covered), judged by the mutation sweep and by demo4's tests on its code; coverage would not tell the two apart, because `make check` demands it. On stories as precise as these, where each criterion nearly spells out its test, the difference is likely small; test-first should matter more on vaguer stories, where the test is where the agent decides what done means.

## Open points

- A plain session on a larger feature, where one context fills up, is the comparison that would show where the factory starts to pay.
- The stages that found nothing on this demo (intake's rewrite, the documenter, the smoke tester, the acceptance) are the place to look for savings; the thin line shows what dropping them costs on a demo, not on a feature where they find something.
- Every thin-line story had exactly one review round. What the reviewer found, and whether a builder at effort `high` would have needed none, would say whether the second builder run is worth its price.
