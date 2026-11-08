---
stage: doing
blocked: question
round: 1
attempts: 0
crashes: 0
pull_request: 672
comments_read: [6723592271, 6723685612]
handed_over: null
claim: null
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
- number: 11
  speaker: tester
  kind: result
  at: '2026-11-08T15:59:31.146858Z'
  stage: tests
  run: ddbb9db76b294cefb76af23a9c426a6f
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T15:59:36.927743Z'
  stage: doing
- number: 13
  speaker: coder
  kind: result
  at: '2026-11-08T16:04:03.767998Z'
  stage: doing
  run: a68e788cf1694871b14929d893796348
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-08T16:04:09.348911Z'
  stage: review
- number: 15
  speaker: reviewer
  kind: result
  at: '2026-11-08T16:05:25.021639Z'
  stage: review
  run: bf3c316599b649109e471e4a1722b3d1
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-08T16:05:29.895734Z'
  stage: doing
- number: 17
  speaker: coder
  kind: question
  at: '2026-11-08T16:05:52.306188Z'
  stage: doing
  run: 4d1a92dfa8e04620806b8fb4b97d320a
  blocked: question
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
11. tester: Carried out the human's answer (entry 9). I added `pytestmark = pytest.mark.documents` to `tests/operator_scripts/test_operator_site_check.py`, to the whole module and nothing else in it. Its `pytest` import was already there. The work from the earlier run of this stage is unchanged and committed.

    Final list of marked modules (11):
    - `tests/guards/test_area_guides.py`
    - `tests/guards/test_folder_readmes.py`
    - `tests/guards/test_test_folder_readmes.py`
    - `tests/guards/test_operator_guide_files.py`
    - `tests/guards/test_operator_guide_pointers_search.py`
    - `tests/guards/test_project_guide_files.py`
    - `tests/guards/test_license_headers.py`
    - `tests/guards/test_work_branch_search.py`
    - `tests/guards/test_root_operator_folders_removed.py`
    - `tests/guards/test_agent_folder_names.py`
    - `tests/operator_scripts/test_operator_site_check.py`

    Left unmarked, as the human confirmed: `tests/guards/test_guide_index_problems.py` and `tests/guards/test_document_tests_write_their_documents.py`.

    The marker is registered in `tests/conftest.py` (`pytest_configure`, `config.addinivalue_line`).

    Criterion → test:
    - criterion 1: tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other
    - criterion 2: tests/guards/test_documents_marker.py::test_the_tests_without_the_marker_are_the_rest_of_the_suite
    - criterion 3: no test function, by the human's answer in entry 4. The search, named in entry 8: a grep over `tests/` for paths built from the repository root (`Path(__file__).parents[...]`, `ROOT`, `REPOSITORY`, the support modules' ROOT) and for the names of the documenter's paths (`README.md`, `docs/`, `operator-guide`, `project-guide`, `checked-documents.txt`). I then read every hit to see what it opens. It also found `test_operator_site_check.py`, now marked.
    - criterion 4: tests/agent_files/test_claude_agent_texts_first_tests.py::test_the_coder_starts_with_only_the_tester_s_named_test_files (rows role, step-one), ::test_the_coder_no_longer_starts_with_the_whole_suite, ::test_the_coder_still_finishes_with_make_check_green, ::test_the_coder_file_names_no_new_make_target_and_no_pytest_option
    - criteria 5 and 6: `make check` and the docs stage.

    Files created (earlier run): `tests/guards/test_documents_marker.py`, `tests/agent_files/test_claude_agent_texts_first_tests.py`.

    Earlier test files changed:
    - Under the leave in the Interface: `tests/conftest.py` and the ten `tests/guards/` modules above.
    - Under the human's leave in entry 9: `tests/operator_scripts/test_operator_site_check.py`.

    Run of the two new files: both marker tests pass. Three criterion 4 tests fail as expected (the two rows of starts-with-only-the-named-files, and no-longer-starts-with-the-whole-suite) until `agents/agents/coder.md` changes. Every module imported. `make lint` is green.

    `lint`: lint: green (0.2 s)
12. factory: started doing as vm.
13. coder: Built: `agents/agents/coder.md`, and nothing else. The tester's marker work (the `tests/conftest.py` registration, the eleven marked modules and the two new test files) already satisfied criteria 1 and 2. It needed no code.
    - Role section: the first bullet now says to start by running only the test files the tester's latest entry names, with the command `CLAUDE.md` names for single test files, and to read their failures. "Finish with `make check` green." is unchanged.
    - Stage step 1: it still reads the named files. It now also says to run only the test files the tester's latest entry names, with the command `CLAUDE.md` names for single test files, to read their failures.
    - The text stays project-neutral. It names no new make target and no pytest option.

    Main choice: I changed the existing role bullet and step 1 in place. The alternative was a new step 0 or a separate bullet, which I rejected because it would leave two "start" instructions that disagree. I left steps 2 to 6, the Rules and the Lessons untouched.

    Run: `uv run pytest -q tests/agent_files` passes (it was 3 failed and 2 passed in the new module before the change). `make check` is green (test: green, 105.6 s, coverage 99.21 %).

    Refactor: the diff is two sentences, and nothing needed changing.

    Description: the journal (entries 4 and 9) already changed it during intake and the tests stage. Nothing in this stage changes its meaning.

    Noticed but not touched: `CLAUDE.md` does not yet name a project command for single test files in the coder's words. It names the tester's `uv run pytest -q <files>` command. Pointing it at the coder too is among the human's changes (`CLAUDE.md` is the human's file).

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
14. factory: started review as vm.
15. reviewer: Findings:

    1. `tests/guards/test_mount_program_search.py:14` (criterion 3, the Interface's "every test module that reads a file under the documenter's write paths"): `SOURCE_ROOT` is `src/`, and `rglob("*")` reads the text of every file under it. That includes `src/factory/README.md` and the area READMEs (`src/factory/<area>/README.md`), which are all in `roles.documenter.write_paths`. The module has no marker, and the tester's search in entries 8 and 11 missed it, although it marked `test_work_branch_search.py` for the same reason. Fix: the tester adds `pytestmark = pytest.mark.documents` to the module. It sits under `tests/guards/`, so the Interface's leave covers the change. Then the tester names the module in the final list.
    2. `tests/shared/domain/test_document_settings.py:178` (`test_todays_install_guide_gives_no_settings_finding`, same criterion and Interface rule): it reads `ROOT / OPERATOR_INSTALL`, which is `docs/operator-guide/install.md` on the real checkout. The module has no marker. Fix: the module needs `pytestmark = pytest.mark.documents`. It sits outside `tests/guards/`, so the leave does not cover it. As in entry 8, this needs the human's word first (mark the whole module, or move the one test). Then the tester makes the change and names the module in the final list.

    My search, beside the tester's:
    - a grep over `tests/**/test_*.py` without the marker for `rglob`, `glob`, `iterdir`, `walk` and `ls-files` on repository paths, and for the documenter path names;
    - a read of each hit that opens real files (`SRC`, `SKILL`, `ROOT`, `operator_support.ROOT`).

    Results:
    - `operator/skill/kumpel` (`SKILL`) does not hold `operator/skill/README.md`.
    - `test_working_branch_in_agent_texts.py` reads only `agents/agents` and `operator/template`.
    - `test_left_branch_removed.py` reads only `*.py` and `*.json`.
    - `test_tests_layout.py` and `test_old_layer_packages_removed.py` read only directory names.
    - I found no other gap.

    Groups 2 to 5: no findings.
    - The coder's text in `agents/agents/coder.md` (role bullet and step 1) matches the Interface. It is project-neutral, and `make check` stays at the end.
    - The criterion 1, 2 and 4 tests check what they are named after.
    - The factory's `make check` after the coder was green (entry 13).
    - The diff adds no marker that silences a check, and no secret.
    - The Description matches what was built.

    Earlier tests changed (any status but `A`):
    - `tests/conftest.py`: the Interface's leave (marker registration only).
    - `tests/guards/test_agent_folder_names.py`, `test_area_guides.py`, `test_folder_readmes.py`, `test_license_headers.py`, `test_operator_guide_files.py`, `test_operator_guide_pointers_search.py`, `test_project_guide_files.py`, `test_root_operator_folders_removed.py`, `test_test_folder_readmes.py`, `test_work_branch_search.py`: the Interface's leave (marker line and `pytest` import only).
    - `tests/operator_scripts/test_operator_site_check.py`: the human's answer, entry 9 (marker line only).
16. factory: started doing as vm.
17. coder: Round 1. Both review findings (entry 15) are test changes, and a coder never edits tests. One of them needs the human's word first. I changed no code.

    I checked both findings against the code:
    - `tests/guards/test_mount_program_search.py`: `SOURCE_ROOT = SRC.parent` (`src/`), and `rglob("*")` reads the text of every file under it. That includes `src/factory/README.md` and the area READMEs, which are under the documenter's write paths. The module has no marker. It sits under `tests/guards/`, so the Interface's leave already covers adding `pytestmark = pytest.mark.documents`. This needs no question.
    - `tests/shared/domain/test_document_settings.py:177-178`: `test_todays_install_guide_gives_no_settings_finding` reads `ROOT / OPERATOR_INSTALL` (`docs/operator-guide/install.md`) on the real checkout. It is the only test in the module that does. The others build their tables in memory or read `settings.py` from `src/`. The module is outside `tests/guards/`, so the leave does not cover it.

    Question for the human: how should `test_todays_install_guide_gives_no_settings_finding` get the `documents` marker? Options:
    - (a) Add `pytestmark = pytest.mark.documents` to the whole module `tests/shared/domain/test_document_settings.py` (its `pytest` import is already there). Criteria 1 and 2 stay per module, but about a dozen pure domain tests join the documents selection and run in the human's `guides` command instead of `make check`'s selection.
    - (b) The tester moves that one test, keeping its function name, into a new marked module (for example `tests/guards/test_install_guide_settings.py`). The rest of the module stays unmarked. The test's node id changes, though its name does not.
    - (c) Mark only that test function. This breaks criterion 1 as written ("every test of the marked modules and no other").

    I'd choose (b). The test reads a real document, which is what the guards under `tests/guards/` do, and it keeps the domain tests out of the documents selection. (a) is the smallest change if the human prefers to keep node ids, as entry 9 chose for the operator site check.

    Once the answer comes in, I end with `tests`, naming both changes: the marker on `tests/guards/test_mount_program_search.py` (under the existing leave) and the human's choice for `test_document_settings.py`. The tester then adds both modules to the final list.

    Built this round: nothing. Noticed but not touched: nothing else.
