---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 672
comments_read: [6723592271, 6723685612]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-08T15:58:45.829234Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T15:47:36.718969Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T15:47:36.726619Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T15:48:00.787373Z'
  stage: intake
  run: ec0d83c5cc7d4b0facd477111eeeab91
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T15:51:49.885706Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T15:51:52.194556Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T15:52:15.383377Z'
  stage: intake
  run: e5818b9b2d1641d2aba40f1ecb061f45
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T15:52:20.464760Z'
  stage: tests
- number: 8
  speaker: tester
  kind: question
  at: '2026-11-08T15:56:56.629309Z'
  stage: tests
  run: ed4bb79b52904c8dbfad8cf8dbbfd356
  blocked: question
- number: 9
  speaker: human
  kind: comment
  at: '2026-11-08T15:58:43.455872Z'
  stage: tests
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T15:58:45.829234Z'
  stage: tests
---

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

1. `uv run pytest --strict-markers -m documents --collect-only` collects every test of the marked modules and no other.
2. `uv run pytest --strict-markers -m "not documents" --collect-only` collects every other test, so the two selections together are the whole suite.
3. No test outside the marked modules reads a file under the documenter's write paths on the real checkout. The tester meets this with its search, named in its entry; no test function is needed for it.
4. The coder's agent file says the first step runs only the tester's named test files, and still says the run ends with `make check` green.
5. `make check` stays green.
6. docs: `docs/project-guide/` names the marker `documents`: which tests carry it, and why (so that the check after the docs stage can be reused once the human's `guides` command exists). `tests/README.md` says the same in one sentence.

## Smoke test

```bash
uv run pytest --strict-markers -m documents --collect-only 2>&1 | tail -1
```
Expect: a line `<n> tests collected`, `<n>` greater than 0.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Questions (format check: passed):

   1. The smoke test can't be met. `pyproject.toml` sets `addopts = "-q --strict-markers -p no:cacheprovider"`. Adding `-q` on the command line puts pytest at `-qq`, and at `-qq` `--collect-only` prints a count per file (`tests/guards/test_area_guides.py: 11`) with no `<n> tests collected` line. I checked this on one module: with the extra `-q` the last line is the per-file count, and without it the last line is `11 tests collected in 0.01s`. Options: (a) drop `-q` from the smoke test command: `uv run pytest --strict-markers -m documents --collect-only 2>&1 | tail -1`, and keep the Expect line as it is; (b) keep `-q` and change the Expect line to per-file count lines, one per marked module. I'd choose (a).
   2. Criteria 1 and 2 pass the same extra `-q`. Their output is then per-file counts, not node ids. That can still be checked per module, but a test that compares the two selections test by test would want node ids. Should both drop `-q`, like the smoke test? I'd say yes. `--strict-markers` is also in `addopts` already, so it can stay or go without changing anything.
   3. Criterion 3 says "the tester's entry names how it searched". That part is a journal requirement, not something a test function can check. I read the testable part as: a test (or the tester's search) shows that no unmarked module under `tests/` opens a path under the documenter's write paths on the real checkout. Is it fine for the tester to meet that with the entry alone, with no test function for criterion 3? I'd accept that.

   What I found so far, for when the answers come back: the Interface names concrete files (`agents/agents/coder.md`, `tests/conftest.py`, the guard modules) and the human's leave for earlier tests. The scope fits `feature.md` (S0001's two scope lines; the Makefile and pipeline changes stay the human's). The architecture is fine (the marker is the project's, decision 3). The docs criterion names what the reader must know without dictating sentences. Route: `tests`, because `agents/` and `tests/` are outside the documenter's write paths.
4. 2026-11-08 human: Answers from the human:

   1. (a). Drop `-q` from the smoke test command: `uv run pytest --strict-markers -m documents --collect-only 2>&1 | tail -1`; the Expect line stays.
   2. Yes: criteria 1 and 2 drop `-q` too, so the output lists node ids; `--strict-markers` may stay.
   3. Yes: the tester meets criterion 3 with its search, named in its entry; no test function is needed for it.
5. factory: started intake as vm.
6. intake: accepted
   - Answers carried in: journal entry 4, the human's answers. Criteria 1 and 2 and the smoke test command now drop `-q`, because `addopts` already sets `-q`. `--strict-markers` stays. Criterion 3 now says the tester meets it with its search, named in its entry, and needs no test function. The Description's meaning did not change.
   - Interface: it names concrete files. These are `agents/agents/coder.md` (the role section and step 1), `tests/conftest.py` (the marker registered through `pytest_configure` and `config.addinivalue_line`) and the guard modules under `tests/guards/` that get `pytestmark = pytest.mark.documents`. It has the starting list of eight modules and the human's leave for earlier tests, limited to the marker line, its import and the conftest registration.
   - Criteria: each one is testable. Criteria 1 and 2 are the two sides of the marker selection: the marked modules and nothing else, then the rest, which together make the whole suite. Criterion 3 is met by the tester's search, by the human's answer. Criterion 4 is a check of the agent file's text. Criterion 5 is `make check` and criterion 6 is docs, the last two.
   - Smoke test: runnable now that `-q` is gone. With `addopts` `-q` and a `-m` selection, pytest's last line is `<n>/<total> tests collected (<k> deselected) in …`, so the `<n> tests collected`, n > 0 expectation can be checked.
   - Docs criterion: it names what the reader must know (which tests carry `documents` and why, plus one sentence in `tests/README.md`) and dictates no sentences.
   - Architecture: the marker is the project's and lives in `tests/` and conftest (feature decision 3). The factory code and `factory/` are untouched. The coder's agent file stays project-neutral and names no new make target or pytest option.
   - Scope: this matches the S0001 scope lines in `feature.md`. The Makefile, `factory/pipeline.yml` and `CLAUDE.md` changes stay among the human's changes. Nothing touches the out-of-scope items.
   - Route: `tests`, because `agents/` and `tests/` are outside the documenter's write paths.
7. factory: started tests as vm.
8. tester: Question: one more test module reads files the documenter keeps, but it is outside the human's leave, which covers only `tests/guards/`. `tests/operator_scripts/test_operator_site_check.py` reads `operator/README.md` on the real checkout (`test_the_operator_readme_names_every_script_and_library`, line 350) and `docs/operator-guide/site.md` (`test_the_guide_names_every_key_of_the_example_site_file`, line 510). The Interface says every such module carries the marker, so I need the human's word to change it. Options: (a) add `pytestmark = pytest.mark.documents` to the whole module. This keeps criteria 1 and 2 per module, but the module's many other operator-script tests then join the documents selection. (b) The tester moves the two tests into a new marked module under `tests/guards/`, keeping their function names. The rest of the module stays unmarked, but the two tests' node ids change, which comes close to "none is renamed". (c) Mark only those two test functions. This breaks criterion 1 as written ("every test of the marked modules and no other"). I'd choose (a).

   Also for the human to confirm: I took two modules from the starting list out of the marked list, because neither reads a document on the real checkout. `tests/guards/test_guide_index_problems.py` works only on files it writes under `tmp_path`. `tests/guards/test_document_tests_write_their_documents.py` reads only `tests/entry/*.py`. If the human wants them marked anyway, that's one line in each.

   Done so far (kept in the working tree):
   - Marker registered in `tests/conftest.py` (`pytest_configure`, `config.addinivalue_line`), under the leave.
   - `pytestmark = pytest.mark.documents` (plus the `pytest` import where it was missing), under the leave, in these tests/guards modules: `test_area_guides.py`, `test_folder_readmes.py`, `test_test_folder_readmes.py`, `test_operator_guide_files.py`, `test_operator_guide_pointers_search.py`, `test_project_guide_files.py`, and four that the search found: `test_license_headers.py` (reads every tracked file), `test_work_branch_search.py` (reads every file under `src/factory` and `tests`, their READMEs included), `test_root_operator_folders_removed.py` and `test_agent_folder_names.py` (both search `docs/` and `README.md`).
   - Search for criterion 3: grep over `tests/` for paths built from the repository root (`Path(__file__).parents[...]`, `ROOT`, `REPOSITORY`, and the support modules' ROOT) and for documenter path names (`README.md`, `docs/`, `operator-guide`, `project-guide`, `checked-documents.txt`). Then I read each hit to see what it opens. Left out: modules that read only files they wrote under `tmp_path` (all the `test_check_documents_*` tests, through the minimal documents), and modules that read only `agents/agents`, `operator/template`, `operator/vm` scripts, `demo/` or `factory/pipeline.yml`. `test_tests_layout.py` and `test_old_layer_packages_removed.py` only list directory entry names (they check that `README.md` exists, not its text), so I left them unmarked.

   Criterion → test:
   - criterion 1: tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other
   - criterion 2: tests/guards/test_documents_marker.py::test_the_tests_without_the_marker_are_the_rest_of_the_suite
   - criterion 3: the search above, no test function (the human's answer, entry 4)
   - criterion 4: tests/agent_files/test_claude_agent_texts_first_tests.py::test_the_coder_starts_with_only_the_tester_s_named_test_files (rows role, step-one), ::test_the_coder_no_longer_starts_with_the_whole_suite, ::test_the_coder_still_finishes_with_make_check_green, ::test_the_coder_file_names_no_new_make_target_and_no_pytest_option
   - criteria 5 and 6: `make check` and the docs stage

   Files created: `tests/guards/test_documents_marker.py`, `tests/agent_files/test_claude_agent_texts_first_tests.py`. Earlier test files changed under the leave: the ten modules above and `tests/conftest.py`. Every module imported. In the one run (`uv run pytest -q` on the new files and `tests/guards`), the marker tests pass, because the markers are this stage's work. The three role/step-one checks of criterion 4 fail, as they should until `agents/agents/coder.md` changes. `make lint` is green.
9. 2026-11-08 human: Answers from the human:

   (a). Leave to add `pytestmark = pytest.mark.documents` (and the `pytest` import if missing) to `tests/operator_scripts/test_operator_site_check.py`, the whole module, and nothing else in it.

   Confirmed: `tests/guards/test_guide_index_problems.py` and `tests/guards/test_document_tests_write_their_documents.py` stay unmarked, since they read no document on the real checkout. The four modules your search added stay marked.
10. factory: started tests as vm.
