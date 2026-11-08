# End-to-end test: demo-todo F0001 on an empty repository (2026-11-08)

The factory at `develop` 0cda2acda built demo-todo's F0001 (the to-do service) into the new, empty private repository `pkrahmer/kumpel-demo-todo-2`. It ran as a second instance, `factory@demo2` on factory-vm, set up by `operator/vm/setup.sh --instance demo2 --code-ref develop`, with the agents on the API key. A Claude Code session played the human; it wrote no product code.

## Result

F0001 is accepted. Its four stories and its acceptance were merged one after another, from 08:30 to 09:16 UTC (46 minutes of wall clock, the human's waits included). `make check` is green with 150 tests. The acceptance proposed one documents-only story, F0001-S0005 (documentation repair after acceptance), which waits in the backlog and was not started.

| Work item | Runs | Agent minutes | Cost | Pull request | What happened |
| :- | -: | -: | -: | :- | :- |
| F0001-S0001 domain model and in-memory repository | 8 | 4.8 | 1.56 USD | #1 | one review rework (a docstring) |
| F0001-S0002 service layer with filtering | 10 | 4.6 | 1.50 USD | #2 | one review rework, sent back to the tester |
| F0001-S0003 HTTP API | 13 | 8.7 | 2.39 USD | #3 | one question, then one review rework with four findings |
| F0001-S0004 SQLite repository and persistence switch | 8 | 5.6 | 1.66 USD | #4 | one review rework; the shared contract test widened to SQLite |
| F0001-A0001 acceptance | 1 | 3.9 | 1.16 USD | #5 | accepted, one story proposed |
| **Total** | **40** | **27.8** | **8.27 USD** | | |

By role: reviewer 8 runs, 2.07 USD; coder 12, 1.93 USD; tester 7, 1.68 USD; acceptance reviewer 1, 1.16 USD; smoke tester 4, 0.67 USD; documenter 4, 0.50 USD; intake 4, 0.26 USD.

## The one question

In S0003 the coder found `make types` red in a test helper: starlette 1.8's test client is typed through `httpx2`, which is not installed, so mypy sees `Any`. The coder offered three options and recommended (a), typing the helper's return value in the test. The human answered (a). The factory took the answer within three minutes, and no time was lost waiting.

## Against v1's run 4 of the same feature

| | v1 run 4 (2026-10-05) | this run |
| :- | -: | -: |
| Agent runs | 32 | 40 |
| Agent minutes | 22.6 | 27.8 |
| Cost | 9.23 USD | 8.27 USD |
| Questions to the human | 1 | 1 |
| Review reworks | 2 | 4 |

The run is about 10 % cheaper although it made eight runs more. Every story went through a second review round, where v1 needed one in two stories. The reworks were small (a docstring, test wording, an untyped helper), so the reviewer is stricter rather than the code worse.

## Health of the run

- No run ended other than `completed`, no write was denied, and 3 of 151 Bash calls failed inside the agents.
- The longest run took 21 turns.
- Every run has its transcript in `/srv/factory/demo2/transcripts/` on the VM, and each cost record names its transcript with a checksum.
- The setup script, the image build and the start worked first time on the shared ZFS pool, with no fix.

## Open points

1. **Starlette deprecation.** Starlette warns 12 times per test run that `httpx` is deprecated in favour of `httpx2`. The fix is a pinned dependency in the demo's `pyproject.toml`, so it is the human's; it belongs in `demo/todo-service/project/`.
2. **Missing directory.** With `TODO_DB` in a missing directory the server exits at start with `unable to open database file`. No criterion covers it.
3. **Disk.** The VM's root disk went from 76 % to 80 % used with the second instance's checkout and image (12 GB free). The acceptance also saw about 0.55 GB of disk growth that the feature's changes do not explain.
4. **My own slip.** I forgot `mkdir -p in-progress` once more at S0002's start; the second try worked. The watcher also ends at once while a question is still marked as open, so it needs a short pause after an answer.

## Transcript review (Haiku flags, Opus judges)

Haiku 5.5 read all 40 transcripts and flagged passages; Opus 5.5 checked the flags against excerpts and wrote [transcripts-report.md](transcripts-report.md). The data is in `transcripts-stage1.json` (the flags) and `transcripts-economics.json` (from the cost records). The review cost about 0.48 USD on the API key. A bug in the script kept the economics block out of Opus's input, so section 3 of its report is inference; the economics below are computed from the data.

Its main findings:

1. **A reviewer edited the story's acceptance criteria** (S0003, it added criterion 24). The gap was real, but the contract changed without intake or the human. The reviewer needs a way to propose a criterion instead.
2. **The tester stage does not type-check tests**, so a typing error in a test reached the coder, who may not fix tests. That cost a question and four runs (about 0.50 USD).
3. **Every role reads the whole work item and diff again**, and large outputs are paged through or read twice; worst in the acceptance run.
4. **Small findings cost full rounds:** a duplicated test constant in S0002 (four runs, about 0.51 USD), and a known `Any` conflict the S0004 coder passed on instead of solving.
5. **Four coder runs changed no code**; they only reran `make check` or routed the item on.
6. **Prompts name tools that do not exist** in the target: the `documents` target (documenters) and `factory-check-story` (acceptance).

## Token economics and caching

| | Tokens | Share of the bill at Opus 5.5 prices |
| :- | -: | -: |
| Cache writes | 1.06 M | about 60 % |
| Output | 0.14 M | about 30 % |
| Cache reads | 4.64 M | about 10 % |
| Uncached input | 396 | 0 |

The cache hit rate is 81 % over all runs (reads against reads plus writes), from 50 % for intake to 91 % for the acceptance.

The weak spot looked like the cache writes, so I checked the recorded request shapes (system prompt and tools) of 39 runs:

- **The fixed start is stable.** There is exactly one shape per role (7 roles, 7 hashes), so nothing per run, such as a date, git status or path, breaks it. My first hypothesis, that every run rewrites a changing start, is wrong.
- **The fixed start is small.** It is about 8 K tokens per role (system prompt with the role prompt, about 4–5 K; tools, about 3.5 K), while a run writes 16 K to 37 K tokens. Most of what is written is new content: the work item, the diff and the tool results, each written once when it first enters the conversation.
- **The start is rewritten each time its role comes back.** The same role recurs only every 8 to 10 minutes, after the 5-minute cache has expired, and the roles cannot share a start, because their tools come first in the request and differ. A 1-hour cache, or the same tools for every role, would save roughly 0.5–1 USD per feature (about 8–10 %).

So the real lever is the amount of text the agents pull in. Every token read is written to the cache once (5 USD per million) and then read again on every later turn (0.20 USD per million). That is Opus's finding 3: a scoped brief instead of the whole work item, a per-file diff, and no duplicate reads.

Other levers:
- a scoped brief instead of the whole work item (about 1 USD per feature, by Opus's estimate);
- no coder runs that change nothing (about 0.3 USD);
- a cheaper model or lower effort for intake and the smoke tester (about 0.4 USD).

## Speed

Of 27.8 agent minutes, 86 % is waiting for the model, 14 % is tools (almost all Bash, mainly `make check`), and the rest is negligible. The wall clock was 46 minutes. The other 18 minutes are the factory's ticks between stages and my approvals.

So speed comes from fewer runs and turns, not from faster tools. Opus's estimates:
- fewer review rounds, by fixing findings 2 and 4 (5 to 6 minutes per feature);
- no coder runs that change nothing (about 2.5 minutes);
- a brief up front instead of paging (2 to 3 minutes);
- the smoke test and the documenter in parallel (about 2 minutes).

A cheaper or faster model for intake, the documenter and the smoke tester would also shorten their runs.

## Where the factory's time goes (F0057, measured)

F0057's 12 stories took 351 minutes from each story's start to its approval, in 107 stage runs. The split comes from the journals (stage start and result) and the cost records (each run's duration, model time and tool time).

| Part | Minutes | Share |
| :- | -: | -: |
| Tests and checks run by the agents themselves (tool time, mostly `make check` and pytest) | about 107 | 30 % |
| Checks run by the factory after a stage, plus container start-up | 83 | 24 % |
| The model thinking and writing | about 91 | 26 % |
| Between stages: questions to the human, approvals, stalls | 101 | 29 % |

The shares add up to a little more than 100 %, because the cost records also hold runs that ended without a result.

- **Running tests and checks is about half of all the time.** The coder spent 57 of its 77 minutes in tools, mostly its own `make check`, and the factory then runs `make check` again after the coder (34 minutes over 26 runs). The documenter spent 23 of its 30 minutes in tools, and the docs stages' checks (`make check`, `make secrets`, `make documents`) took another 46 minutes over 17 runs, about 2.7 minutes each. The tester spent 26 minutes running tests.
- **The model itself is only about a quarter.** The reviewer and intake are almost pure model time and are fast.
- **Waits are the other big part.** F0057-S0002 alone waited 36 minutes between stages, mostly for answers.
- **Container start-up is small.** The tests stage, whose only check is `make lint`, shows 1.4 minutes over 19 runs beyond the agent's own time.

So the shared cache will lower the cost, but the time is in the checks and the waits. The biggest time levers:
1. One `make check` per state of the code instead of two: the coder runs only the tests it touched, and the factory's check is the gate.
2. A lighter check after a docs-only change.
3. Fewer questions and rework rounds, through stories that name the earlier tests they may change.
