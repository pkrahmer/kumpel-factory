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
