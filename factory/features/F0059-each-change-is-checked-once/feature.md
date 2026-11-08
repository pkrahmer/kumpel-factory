# Each change is checked once

## Goal

Checks take more than half of the factory's time (`docs/runs/2026-11-08-e2e-demo-todo-2/eval.md`, *Where the factory's time goes*). The full suite runs about three minutes on the VM, and a story runs it up to five times, three of them without a new fact:
- The coder starts with `make test` only to see which tests fail. The tester's latest entry already names the failing test files, and every other test is green on `develop`.
- The factory runs `make check` after every round of the coder, although the coder ran it itself before it handed forward. In the journals of F0053 to F0058 the factory's check after the coder was red once in 113 coder results.
- The factory runs `make check` again after every round of the documenter, although the documenter can write only Markdown files. It runs the whole suite only because a few guards in `tests/guards/` read the real documents.

After this feature the coder starts from the tester's test files alone. The factory runs the whole `make check` once per story, after the smoke tester, on the tree that goes to the human's approval; when it is red, the smoke tester sends the work item to the coder or the documenter, whichever can fix the failure. The guards that read the documents move into a fast project command of their own, `guides`, which the docs stages run beside `secrets` and `documents`, so a broken document is still found where the documenter can fix it. Done when both stories are merged, the human's changes are made, `make check` and `make guides` are green on `develop`, and the human's measurement run has been compared with F0058's.

## Before it starts

F0058 is archived and promoted, and its measurement run is done, so the measurement of this feature stands on its own.

## Scope

- The coder's first step runs only the test files the tester's latest entry names, not the whole suite (S0001).
- Every test that reads a file the documenter may write carries the pytest marker `documents`, registered in `tests/conftest.py` (S0001).
- After a red check at the smoke-test stage, the smoke tester decides `doing` or `docs` by what failed and names the failure (S0002).

## Out of scope

- The coder's own `make check` at the end of its run stays; whether it may run a lighter check is a later decision, measured on this feature's numbers.
- A new factory rule that sends a work item back on a red check: the smoke tester's existing decisions do it (decision 4).
- Parallel stages, a warm index and the warning hook for the time left: later features.

## Stories

- S0001: The coder starts from the tester's tests, and the guards that read the documents are marked.
- S0002: The smoke tester routes a red check.

## The human's changes

After both stories are merged, in one commit on `develop` (Claude prepares them):
- `Makefile`: `test` runs `pytest -m "not documents"`; a new target `guides` runs `pytest -m documents` without coverage and ends with `guides: green (<seconds> s)`; `check` stays as it is.
- `factory/pipeline.yml`: a project command `guides: {time_limit: 2}`; `doing` has no `checks` (its `reports: [duplicates]` stays); `docs` checks `[guides, secrets, documents]`; `smoke-test` checks `[check]`; `docs-only` keeps `[check, secrets, documents]` and gains `guides`; `check`'s `not_read` gains the documenter's write paths, so the docs-only route reuses a passed check. The leases still fit: the smoke tester's 40 + 8 and the documenter's 40 + 2 + 3 + 2 (docs-only: + 8) minutes are within 60.
- `CLAUDE.md`: under *Checks*, the coder starts with `uv run pytest -q <the tester's test files>` and finishes with `make check guides`; the factory's check runs after the smoke tester; `make guides` joins the list of targets the pipeline knows.
- `demo/todo-service/project` and `operator/template`: the same stage checks in their `factory/pipeline.yml`, without `guides`, since their projects have no guards that read documents.

Then the measurement run: demo-todo F0001 on a fresh repository, compared with F0058's run.

## Decisions taken for the human

1. S0001 lands before the human's `Makefile` change; until then the marked tests still run in `make test`, so nothing goes unchecked in between.
2. The marked guards run in the docs stages, where the documenter can fix what they find, and in the coder's own `make check guides`.
3. The marker is the project's, not the factory's: the factory knows only the project command `guides` and the `not_read` patterns.
4. An abnormal end of the coder's run (time limit, death, no decision) is a stall and never moves the work item forward, so the factory needs no check after the coder for that case. A red check after the smoke tester is a `check_red` stall; the smoke tester runs again, reads the failing lines and decides `doing` or `docs` with the routes its stage already has (the human, 2026-11-08).
