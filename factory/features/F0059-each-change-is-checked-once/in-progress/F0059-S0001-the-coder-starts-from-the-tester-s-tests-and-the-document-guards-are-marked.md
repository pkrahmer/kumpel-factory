# The coder starts from the tester's tests, and the guards that read the documents are marked

## Description

The coder's first step today runs the whole test suite (`make test`, about three minutes on the VM) only to read which tests fail. On `develop` every test is green, so the only failing tests are the tester's new ones, and the tester's latest entry names their files. After this story the coder runs only those files first, with the project's command for single test files that `CLAUDE.md` names.

A few tests read the real documents: the guides under `docs/` and the README files the documenter keeps. Because `make test` runs them, `make check` reads the documenter's files, and the factory cannot reuse its passed check after a docs-only change. After this story each such test carries the pytest marker `documents`. The human then moves the marked tests into a project command of their own (`feature.md`, *The human's changes*); this story only marks them.

## Interface

- `agents/agents/coder.md`: the role section and step 1 say that the coder starts by running only the test files the tester's latest entry names, with the command `CLAUDE.md` names for single test files, and reads their failures. The rest of the coder's steps stay as they are, `make check` at the end included. The text stays project-neutral: it names no `make` target and no `pytest` option beyond what it names today.
- `tests/conftest.py` registers the marker `documents` with a one-line description (pytest's `pytest_configure` and `config.addinivalue_line`), so `pytest --strict-markers` accepts it.
- Every test module that reads a file under the documenter's write paths (`factory/pipeline.yml`, `roles.documenter.write_paths`) on the real checkout, not one it wrote under `tmp_path`, carries `pytestmark = pytest.mark.documents`. A starting list, from a search on 2026-11-08: the modules under `tests/guards/` named `test_area_guides.py`, `test_folder_readmes.py`, `test_test_folder_readmes.py`, `test_operator_guide_files.py`, `test_operator_guide_pointers_search.py`, `test_project_guide_files.py`, `test_guide_index_problems.py` and `test_document_tests_write_their_documents.py`. The tester checks each against what it reads, adds any it finds, and names the final list in its entry.
- A module that reads both documents and code keeps the marker: the human's `guides` command runs in the doing stage as well (`feature.md`, decision 2).
- No test changes what it checks, and none is renamed.

The human's leave for earlier tests: this story may add the marker line, and the `pytest` import it needs, to the test modules under `tests/guards/` that read the documenter's files, and change `tests/conftest.py` for the registration, and only that.

## Acceptance criteria

1. `uv run pytest --strict-markers -m documents --collect-only -q` collects every test of the marked modules and no other.
2. `uv run pytest --strict-markers -m "not documents" --collect-only -q` collects every other test, so the two selections together are the whole suite.
3. No test outside the marked modules reads a file under the documenter's write paths on the real checkout. The tester's entry names how it searched.
4. The coder's agent file says the first step runs only the tester's named test files, and still says the run ends with `make check` green.
5. `make check` stays green.
6. docs: `docs/project-guide/` names the marker `documents`: which tests carry it, and why (so that the check after the docs stage can be reused once the human's `guides` command exists). `tests/README.md` says the same in one sentence.

## Smoke test

```bash
uv run pytest --strict-markers -m documents --collect-only -q 2>&1 | tail -1
```
Expect: a line `<n> tests collected`, `<n>` greater than 0.

## Journal
