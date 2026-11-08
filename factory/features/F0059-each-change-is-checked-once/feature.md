# Each change is checked once

## Goal

Checks take more than half of the factory's time (`docs/runs/2026-11-08-e2e-demo-todo-2/eval.md`, *Where the factory's time goes*). The full suite runs about three minutes on the VM, and a story runs it up to five times, of which two give no new fact:
- The coder starts with `make test` only to see which tests fail. The tester's latest entry already names the failing test files, and every other test is green on `develop`.
- After the docs stage the factory runs `make check` again, although the documenter can write only Markdown files. It cannot reuse the check it passed after the coder, because a few guards in `tests/guards/` read the real documents, so `check` reads them too.

This feature drops those two runs. The coder starts from the tester's test files alone. The guards that read the documents move into a project command of their own, `guides`, which the doing and docs stages run beside `check`. `check` then no longer reads the documenter's paths, and the factory reuses its passed result after a docs-only change. The gate stays the same: every test still runs after the coder, and every guard still runs after the documenter. Done when the story below is merged, the human's changes are made, `make check` and `make guides` are green on `develop`, and the human's measurement run has been compared with F0058's.

## Before it starts

F0058 is archived and promoted, and its measurement run is done, so the measurement of this feature stands on its own.

## Scope

- The coder's first step runs only the test files the tester's latest entry names, not the whole suite (S0001).
- Every test that reads a file the documenter may write carries the pytest marker `documents`, registered in `tests/conftest.py` (S0001).

## Out of scope

- The coder's own `make check` at the end of its run stays. The journals of F0053 to F0058 hold 113 coder results and one stall of the factory's check after the coder, so the factory's check rarely catches anything; whether the coder may run a lighter check is a later decision, measured on this feature's numbers.
- The secrets and document checks of the docs stages: they stay as they are.
- Parallel stages, a warm index and the warning hook for the time left: later features.

## Stories

- S0001: The coder starts from the tester's tests, and the guards that read the documents are marked.

## The human's changes

After S0001 is merged, in one commit on `develop` (Claude prepares them):
- `Makefile`: `test` runs `pytest -m "not documents"`; a new target `guides` runs `pytest -m documents` without coverage and ends with `guides: green (<seconds> s)`; `check` stays as it is.
- `factory/pipeline.yml`: a project command `guides: {time_limit: 2}`; `doing` checks `[check, guides]`; `docs` and `docs-only` check `[check, guides, secrets, documents]`; `check`'s `not_read` gains the documenter's write paths. The leases still fit: the coder's 40 + 8 + 2 and the documenter's 40 + 8 + 2 + 3 + 2 minutes are within 60.
- `CLAUDE.md`: under *Checks*, the coder starts with `uv run pytest -q <the tester's test files>` and finishes with `make check guides`; `make guides` joins the list of targets the pipeline knows.
- `demo/todo-service/project` and `operator/template`: no change; their projects have no guards that read documents.

Then the measurement run: demo-todo F0001 on a fresh repository, compared with F0058's run.

## Decisions taken for the human

1. One story: the coder's step and the marker land together, and the human's changes follow them at once. Until the human's `Makefile` change, the marked tests still run in `make test`, so nothing goes unchecked in between.
2. The marked guards run in the doing stage too, as they do today inside `make check`: a code change that breaks a guard (a new folder without its README) is still seen after the coder, not first after the documenter.
3. The marker is the project's, not the factory's: the factory knows only the project command `guides` and the `not_read` patterns.
