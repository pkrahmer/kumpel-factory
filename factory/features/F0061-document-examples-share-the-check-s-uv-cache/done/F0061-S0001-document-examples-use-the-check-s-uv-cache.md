---
stage: done
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 684
comments_read: [6729441197]
handed_over: approval
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-09T00:34:17.945661Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-09T00:34:17.952891Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-09T00:34:42.821295Z'
  stage: intake
  run: 82101504913b4ccc87e9a80c5a31cb42
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-09T00:35:27.750198Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-09T00:35:32.377252Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-09T00:35:52.422231Z'
  stage: intake
  run: 8e99f99d4fb24662bf9dbea11cf357bd
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-09T00:36:00.302295Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-09T00:38:50.709013Z'
  stage: tests
  run: d5bd67b8e77f4f58848ec2d28a9ff47a
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-09T00:38:55.648389Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-09T00:41:32.673056Z'
  stage: doing
  run: 091c8c96147d4696b55fa86f06a8889e
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-09T00:41:37.605525Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-09T00:42:14.649458Z'
  stage: review
  run: cbb04a0404e146f69f5b014b39029267
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-09T00:42:19.599955Z'
  stage: tests
- number: 14
  speaker: tester
  kind: result
  at: '2026-11-09T00:47:22.925428Z'
  stage: tests
  run: 5bec26d3d96f433c93020848ff8937c7
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-09T00:47:27.911021Z'
  stage: doing
- number: 16
  speaker: coder
  kind: result
  at: '2026-11-09T00:50:07.605174Z'
  stage: doing
  run: 40ac0a92fdc341408ac521e92c75e151
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-09T00:50:12.880226Z'
  stage: review
- number: 18
  speaker: reviewer
  kind: result
  at: '2026-11-09T00:50:35.585163Z'
  stage: review
  run: 97c708c68cea4225a88d44918d87096a
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-09T00:50:40.383633Z'
  stage: docs
- number: 20
  speaker: documenter
  kind: result
  at: '2026-11-09T00:54:16.245585Z'
  stage: docs
  run: fce311af2c654382aac7229675ed4ffb
- number: 21
  speaker: factory
  kind: started
  at: '2026-11-09T00:54:21.416577Z'
  stage: smoke-test
- number: 22
  speaker: smoke-tester
  kind: result
  at: '2026-11-09T00:56:28.945725Z'
  stage: smoke-test
  run: 4fbd6856b29f495aa79c83d1bb129f51
- number: 23
  speaker: factory
  kind: done
  at: '2026-11-09T00:58:20.519233Z'
  stage: approval
---

# Document examples use the check's uv cache

## Description

The document check runs a document's examples under `env -i` with a fixed environment (`PATH`, `HOME` set to the document's own empty home, `TZ`, `LANG`), so uv finds no cache and every document's first `uv run` downloads every package, which can take longer than the examples' 60 s limit. After this story the fixed environment also holds `UV_CACHE_DIR`, set to the uv cache that the process running the check uses: its own `UV_CACHE_DIR` when set, otherwise `$XDG_CACHE_HOME/uv` when `XDG_CACHE_HOME` is set, otherwise `$HOME/.cache/uv`. When the check's process has none of the three, the examples get no `UV_CACHE_DIR`, as today. `HOME` stays the document's own empty home, each document keeps its own copy, and no fixture can change `UV_CACHE_DIR`, as no fixture can change the rest of the fixed environment.

## Interface

- `src/factory/shared/adapters/document_examples.py` (`adapters`):

```python
class ProcessExampleRunner(ExampleRunner):
    def __init__(self, time_limit: timedelta = EXAMPLE_TIME_LIMIT, uv_cache: Path | None = None) -> None: ...

def uv_cache_directory(environment: Mapping[str, str]) -> Path | None: ...
```

  - `uv_cache_directory`: `UV_CACHE_DIR` when it is set and not empty; otherwise `XDG_CACHE_HOME` + `/uv` when that is set and not empty; otherwise `HOME` + `/.cache/uv` when that is set and not empty; otherwise `None`.
  - With `uv_cache` given, every command's environment holds `UV_CACHE_DIR` with that path, after the fixture's environment, so a fixture cannot change it; with `None`, no command's environment holds `UV_CACHE_DIR`.
  - `HOME` stays the document's own home folder.
- `src/factory/entry/check_documents.py` (`entry`): builds the runner with `uv_cache=uv_cache_directory(os.environ)`.
- Tests: `tests/shared/adapters/test_document_examples_uv_cache.py` and `tests/entry/test_check_documents_uv_cache.py`.

## Acceptance criteria

1. `uv_cache_directory` returns `UV_CACHE_DIR`'s value when it is set; `XDG_CACHE_HOME/uv` when only `XDG_CACHE_HOME` and `HOME` are set; `HOME/.cache/uv` when only `HOME` is set; `None` when none is set; and an empty value counts as not set, for each of the three: rows of one parametrized test.
2. A runner built with `uv_cache` runs a command that prints `$UV_CACHE_DIR`, and the output is that path; a runner built without it prints an empty line: rows of one parametrized test.
3. A fixture whose environment holds `UV_CACHE_DIR` does not change the value the command sees when the runner has `uv_cache`.
4. With `uv_cache` given, the command's `$HOME` is still the document's own home folder, not the cache's parent.
5. The document check, run with `UV_CACHE_DIR` set in its own environment (monkeypatched) on a written document (`tests/support/minimal_documents_support.py`) whose example prints `$UV_CACHE_DIR` and expects that path, reports no finding.
6. `make check` stays green.
7. docs: the project guide (`docs/project-guide/shared.md`, the document examples) says that the examples share the uv cache of the process that runs the check, how that cache is found, and why (a fresh copy's first `uv run` would otherwise download every package and could pass the examples' limit).

## Smoke test

```bash
uv run python -c "from factory.shared.adapters.document_examples import uv_cache_directory as u; print(u({'UV_CACHE_DIR': '/c', 'HOME': '/h'}), u({'HOME': '/h'}), u({}))"
```
Expect: `/c /h/.cache/uv None`

```bash
uv run pytest tests/shared/adapters/test_document_examples_uv_cache.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-09 human: created.
2. factory: started intake as vm.
3. intake: Intake: one question before the story can go to tests. The other checks passed: the form check passed; the Interface names concrete modules and signatures; criteria 1–4 cover each branch of `uv_cache_directory` (including empty values and the order of precedence), both sides of `uv_cache`, the fixture that cannot override it, and `HOME`; the smoke test commands can run (pyproject's `addopts` already sets `-q`, so the summary line is printed) and their expectations can be checked; the docs criterion says what the reader must know without dictating sentences; the change belongs in the shared adapters plus the entry wiring; and the story fits F0061's scope, with the 60 s limit untouched.

   1. The Interface says `src/factory/entry/check_documents.py` builds the runner with `uv_cache=uv_cache_directory(os.environ)` (it now calls `ProcessExampleRunner()`, line 203). No criterion tests this line, and it is what makes the feature work at all: a coder who leaves it out passes criteria 1–4 and the smoke test, yet the examples would still get no `UV_CACHE_DIR`. The options I see:
      (a) Add a criterion before the two closing ones, for example: "The document check, run with `UV_CACHE_DIR` set in its own environment (monkeypatched) on a written document whose example prints `$UV_CACHE_DIR` and expects that path, reports no finding." Its test would go under `tests/entry/` beside the existing check_documents tests, using `tests/support/minimal_documents_support.py`, and the Interface's Tests line would name that file too.
      (b) Leave the wiring untested and let the reviewer check it.
      I would choose (a).
4. 2026-11-09 human: (a). Add the criterion for the document check's own wiring, with its test under tests/entry/ as you describe, and name that file in the Interface's Tests line.
5. factory: started intake as vm.
6. intake: accepted
   - Human's answer carried in (journal entry 4, option (a)): I added criterion 5, which runs the document check with `UV_CACHE_DIR` monkeypatched, on a document written through `tests/support/minimal_documents_support.py` whose example prints `$UV_CACHE_DIR`, and expects no finding. It sits before the two closing criteria, which are now 6 and 7. The Interface's Tests line now also names `tests/entry/test_check_documents_uv_cache.py`.
   - Interface: it names concrete modules and signatures. These are `ProcessExampleRunner.__init__(time_limit, uv_cache: Path | None = None)` and `uv_cache_directory(Mapping[str, str]) -> Path | None` in `src/factory/shared/adapters/document_examples.py`, plus the wiring in `src/factory/entry/check_documents.py` (it now calls `ProcessExampleRunner()` at line 203).
   - Criteria: each one can be tested by one test function.
     - Criterion 1 covers the precedence order, each fallback, `None`, and an empty value counting as not set for each of the three variables.
     - Criterion 2 covers both sides of `uv_cache`.
     - Criterion 3 checks that a fixture cannot override it, and criterion 4 that `HOME` is still the document's own home.
     - Criterion 5 covers the entry wiring.
   - Smoke test: both commands can run. pyproject's `addopts` already sets `-q`, so the pytest command passes no `-q` and still prints its summary line. Each `Expect:` can be checked: an exact printed line, and a summary with only `passed`.
   - Docs criterion: it names what the reader must know (that the examples share the check's uv cache, how that cache is found, and why) and dictates no sentences.
   - Architecture: the pure lookup and the runner sit in the shared adapters, which already hold `ProcessExampleRunner`. The `os.environ` read sits in `entry`, where wiring belongs. No new dependency, no change to `factory/` or to another story's tests.
   - Scope: the story is within F0061's one scope line. The 60 s limit stays and no cache is shared between instances, as the Out of scope section requires.
7. factory: started tests as vm.
8. tester: Tests written for every criterion. They are red on purpose and are the coder's specification.

   - criterion 1: tests/shared/adapters/test_document_examples_uv_cache.py::test_the_uv_cache_is_found_in_the_order_of_its_variables. It is parametrized with these rows:
     - `UV_CACHE_DIR` wins over `XDG_CACHE_HOME` and `HOME`
     - `XDG_CACHE_HOME` + `HOME` gives `XDG/uv`
     - `HOME` only gives `HOME/.cache/uv`
     - none set gives `None`
     - an empty value counts as not set, one row for each of the three variables, plus a row where all three are empty
   - criterion 2: tests/shared/adapters/test_document_examples_uv_cache.py::test_a_command_sees_the_runners_uv_cache_or_none. Rows `with-cache` and `without-cache`. The command is `echo "[$UV_CACHE_DIR]"` and expects `[path]` or `[]`; the brackets make the empty line visible. The caller's own `UV_CACHE_DIR` is monkeypatched so that its value cannot leak through.
   - criterion 3: tests/shared/adapters/test_document_examples_uv_cache.py::test_a_fixtures_uv_cache_does_not_replace_the_runners. A fixture gives `UV_CACHE_DIR=/from/the/fixture`, and the command still sees the runner's path.
   - criterion 4: tests/shared/adapters/test_document_examples_uv_cache.py::test_with_a_uv_cache_home_stays_the_documents_own_folder. The cache is `<tmp>/callers-home/.cache/uv`. The test checks three things: `$HOME` is not `callers-home`, it exists, and it is empty.
   - criterion 5: tests/entry/test_check_documents_uv_cache.py::test_the_check_gives_its_examples_its_own_uv_cache. It uses the `minimal` fixture (built with `minimal_documents_support`) and monkeypatches `UV_CACHE_DIR`. It appends a `console` block to `docs/project-guide/shared.md` that prints `$UV_CACHE_DIR` and expects the path, and lists that file in `docs/checked-documents.txt` so that a finding would block. The check must print only the time line and exit 0.
   - criteria 6–7 (`make check` green, docs): not test criteria.

   Files created:
   - tests/shared/adapters/test_document_examples_uv_cache.py
   - tests/entry/test_check_documents_uv_cache.py

   No earlier test files were changed. The new module defines two small fixtures of its own (`CacheFixture`, `PlainFixture`) instead of importing `LiftingFixture` from another test module, because test modules must not import each other.

   Run of `make test`:
   - It is red as expected. `tests/shared/adapters/test_document_examples_uv_cache.py` could not be imported: `ImportError: cannot import name 'uv_cache_directory' from 'factory.shared.adapters.document_examples'`.
   - The entry test fails on `assert re.fullmatch(TIME_LINE, lines[0])`. The check does not yet pass the cache to its examples, so the example prints an empty line and gives a finding.
   - The two `tests/guards/test_documents_marker.py` errors in the same run follow from that collection error. They should clear once the module imports.

   `make lint` is green.

   `lint`: lint: green (0.1 s)
9. factory: started doing as vm.
10. coder: Built the uv cache passthrough for document examples. The tester's two files pass, and `make check guides` is green (check: green, test 103.9 s; guides: green).

    - `src/factory/shared/adapters/document_examples.py`:
      - New public `uv_cache_directory(environment)`. It returns `UV_CACHE_DIR`, else `XDG_CACHE_HOME/uv`, else `HOME/.cache/uv`, else `None`. An empty value counts as not set.
      - `ProcessExampleRunner.__init__` takes `uv_cache: Path | None = None` and hands it to `_DocumentRun`.
      - `_fixed_environment(home, uv_cache)` adds `UV_CACHE_DIR` only when a cache is given. It is still merged after the fixture's environment, so no fixture can change it. `HOME` stays the document's own home folder. A comment there gives the reason: a fresh home's first `uv run` would download every package within the examples' limit.
    - `src/factory/entry/check_documents.py`: imports `os` and builds `ProcessExampleRunner(uv_cache=uv_cache_directory(os.environ))`.

    Main choice: the cache goes into the fixed environment, which stays the one place every command's environment comes from. That also gives the "fixture cannot override" rule for free. I rejected two alternatives:
    - adding the variable inside `run_document`, or letting it through `env -i`, which would split the fixed environment across two places;
    - reading `os.environ` inside the adapter, which the Interface places in `entry`.

    Refactor pass: I read the diff and nothing needed changing.

    The journal changed only the criteria (criterion 5 added at intake), not the meaning of the task, so the Description stays as written. Noticed but not touched: `_fixed_environment` still reads `PATH` from `os.environ` directly in the adapter, as before. The docs criterion (`docs/project-guide/shared.md`) is the documenter's.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
11. factory: started review as vm.
12. reviewer: Review, round 0. I read the diff against the criteria and the Interface. I checked groups 1 to 5 and item 6.

    Group 1, acceptance criteria:
    - Criterion 1 has one parametrized test. It has rows for the order of precedence, each fallback, `None`, an empty value for each of the three variables, and all three empty.
    - Criterion 2 has `with-cache` and `without-cache` rows. The brackets make the empty value visible, and the caller's own `UV_CACHE_DIR` is monkeypatched so it cannot leak through.
    - Criterion 3 runs a fixture that gives `UV_CACHE_DIR`, and the runner's value still wins.
    - Criterion 4 checks that `$HOME` is not the caller's home, that it exists and that it is empty. The cache's folder is not empty, so this rules it out as `HOME`.
    - Criterion 5 is in `tests/entry/`. It is a real end-to-end test of the `os.environ` wiring, and it would block if the wiring were missing. The tester's entry says it was red before the coder.
    - The journal says `make check guides` was green after the coder.
    - Group 1 has no gaps.

    Group 2, architecture: `uv_cache_directory` is pure and sits where the Interface puts it. The `os.environ` read is in `entry`. The cache goes into `_fixed_environment`, which is still merged last, so no fixture can lift it. No wrapper or layer rule is broken.

    Group 3, security: there are no markers. Commands get the cache only through `env -i` arguments, and no shell string is built from it beyond what was there before.

    Group 4, quality: the names, docstrings and why-comment in `src/` are fine.

    Group 5, work item hygiene: the Description matches what was built, and the docs criterion is still accurate.

    Findings:
    1. `tests/shared/adapters/test_document_examples_uv_cache.py:18-37` copies helpers that `tests/shared/adapters/test_document_examples.py` already holds:
       - `PlainFixture` copies `EmptyFixture` (line 28), except for its one variable.
       - `CacheFixture` is `LiftingFixture("UV_CACHE_DIR")` (line 238) with a different value.
       - `_document` copies `_block`/`_document` (lines 45-50).
       
       The fix: under the standing leave in CLAUDE.md *Tests*, move `EmptyFixture`, `LiftingFixture`, `_block` and `_document` (with `LIFTED_VALUE` and `FIXTURE_VARIABLE`) into a support module in `tests/support/`, for example `document_examples_support.py`. Then make both modules use them, with every earlier test keeping its name and what it checks, and name `tests/shared/adapters/test_document_examples.py` in the entry as changed. The test files are the only thing to change, so this goes to the tester.

    Earlier tests: none. The diff changes no test file that `develop` already holds; both test files are new (status `A`).
13. factory: started tests as vm.
14. tester: Round 1: I answered the reviewer's one finding by moving test helpers only. No product code changed and no criterion test changed what it checks.

    Finding 1 (copied helpers in `tests/shared/adapters/test_document_examples_uv_cache.py`) is answered with a move under the standing leave in CLAUDE.md *Tests* (moving a shared test helper):
    - New `tests/support/document_examples_support.py` holds `FIXTURE_VARIABLE`, `LIFTED_VALUE`, `EmptyFixture`, `LiftingFixture`, `block` and `document`. These are the former `_block`/`_document`, made public because a support module shares them. `EmptyFixture(variable=FIXTURE_VARIABLE)` and `LiftingFixture(name, value=LIFTED_VALUE)` take optional arguments, and their defaults keep the earlier behaviour exactly.
    - Earlier test file changed: `tests/shared/adapters/test_document_examples.py`. It now imports these helpers instead of defining them. Every test keeps its name and checks the same thing; only the helper names `_block`/`_document` became `block`/`document`.
    - `tests/shared/adapters/test_document_examples_uv_cache.py`: I dropped `PlainFixture`, `CacheFixture` and `_document`.
      - The tests for criteria 2 and 4 use `EmptyFixture()`.
      - The test for criterion 3 uses `LiftingFixture("UV_CACHE_DIR", FIXTURE_CACHE)`.
      - Every document is built with `document(block(...))`.
      - The test names and the criterion mapping from entry 8 are unchanged.

    Run, with the command CLAUDE.md gives for single test files: `uv run pytest -q tests/shared/adapters/test_document_examples.py tests/shared/adapters/test_document_examples_uv_cache.py tests/entry/test_check_documents_uv_cache.py` passed, and so did a run of those two adapter files with `tests/guards`. `make lint` and `make types` are green. Every module imported.

    `lint`: lint: green (0.1 s)
15. factory: started doing as vm.
16. coder: Round 1: no code change was needed. The reviewer's one finding (copied test helpers) was a change to the tests, and the tester answered it in entry 14 by moving the helpers to `tests/support/document_examples_support.py`. The product code from entry 10 stays as it was:
    - `src/factory/shared/adapters/document_examples.py`: `uv_cache_directory`, and `ProcessExampleRunner(uv_cache=...)` feeding `_fixed_environment`.
    - `src/factory/entry/check_documents.py`: the wiring with `os.environ`.

    Checks:
    - The three test files the tester's latest entry names pass: `tests/shared/adapters/test_document_examples.py`, `tests/shared/adapters/test_document_examples_uv_cache.py` and `tests/entry/test_check_documents_uv_cache.py`.
    - `make check guides` is green: check: green (test 110.7 s, coverage 99.21 %), and guides: green.

    Main choice and rejected alternative: unchanged from entry 10. The cache goes into the one fixed environment, which is merged after the fixture's environment. I rejected adding it separately inside `run_document`.

    Refactor pass: the source diff is the same as in round 0 and nothing needed changing.

    Description: the journal changed no meaning of the task, so it stays as written.

    Noticed but not touched: as before, `_fixed_environment` reads `PATH` from `os.environ` inside the adapter. The docs criterion (`docs/project-guide/shared.md`) is the documenter's.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
17. factory: started review as vm.
18. reviewer: Review, round 1. I read `git diff develop...HEAD -- . ':!factory'` against the criteria and the Interface, and checked groups 1 to 5 and item 6.

    no findings

    - Round 0's one finding (copied helpers) is answered. The new `tests/support/document_examples_support.py` holds `EmptyFixture`, `LiftingFixture`, `block` and `document`. Both adapter test modules use these and no longer define their own copies. The new constructor arguments have defaults that keep the earlier behaviour (`EmptyFixture()` still gives `EXAMPLE_FIXTURE=set`, and `LiftingFixture(name)` still gives `from-the-fixture`).
    - Group 1: each of criteria 1–5 has a test that checks what the criterion says.
      - Criterion 1 is one parametrized test. It covers the order, each fallback, `None`, an empty value for each of the three variables, and all three empty.
      - Criterion 2 has rows for with and without a cache, and the caller's own `UV_CACHE_DIR` is monkeypatched so a leak would fail.
      - Criteria 3 and 4 check that a fixture cannot override the cache and that `HOME` is still the document's own empty folder.
      - Criterion 5 runs `main` end to end with a document that is listed for checking, so it would block if the wiring were missing.
      - Entry 16 records that `make check guides` was green after the coder.
    - Group 2: `uv_cache_directory` is a pure lookup in the shared adapters. `os.environ` is read in `entry`, at `src/factory/entry/check_documents.py:205`. The cache goes into the one fixed environment, which is still merged after the fixture's environment. No layer or wrapper rule is broken.
    - Group 3: there are no markers and no new shell strings; the value reaches the command only through `env -i` arguments.
    - Group 4: the names, the docstrings and the why-comment in `_fixed_environment` are fine. No second copy of an existing helper turns up: `src/factory` had no other lookup of `UV_CACHE_DIR` or `XDG_CACHE_HOME`.
    - Group 5: the Description matches what was built. Entries 10 and 16 give the main choice and the alternatives that were rejected. The docs criterion (criterion 7) still says what the reader needs.

    Earlier tests:
    - `tests/shared/adapters/test_document_examples.py`: changed under the standing leave to move a shared test helper (CLAUDE.md *Tests*). The change only moves `FIXTURE_VARIABLE`, `LIFTED_VALUE`, `EmptyFixture`, `LiftingFixture` and `_block`/`_document` (now `block`/`document`) to `tests/support/document_examples_support.py`. Every test keeps its name and checks the same thing.
19. factory: started docs as vm.
20. documenter: Docs for the uv cache passthrough. I changed only documents, so I did not run `make check`. `make documents` ended `documents ok (50.4 s)` and `make guides` was green.

    Files changed:
    - `docs/project-guide/shared.md` (*The examples*): the fixed-variables bullet now names `UV_CACHE_DIR` among the variables a fixture cannot replace. A new bullet says the examples share the uv cache of the process that runs the check, and why: the home is empty, so a fresh copy's first `uv run` would download every package and could pass the 60 s limit. It also says each document still has its own folder and home. Another bullet says how `check_documents.py` wires `uv_cache_directory(os.environ)`, the lookup order (`UV_CACHE_DIR`, then `XDG_CACHE_HOME/uv`, then `HOME/.cache/uv`), that an empty value counts as not set, and that `None` means no `UV_CACHE_DIR`. This is criterion 7.
    - `docs/project-guide/style.md` (*Runnable examples*): the list of the fixed environment said "and nothing else" without `UV_CACHE_DIR`, so it was stale. It now names `UV_CACHE_DIR` when the check's process has a uv cache.
    - `docs/project-guide/README.md`: added the new support module `tests/support/document_examples_support.py` (from the tester's round 1 move) to the list of support modules.

    I checked the smoke test's lookup against the code by running `uv run python -c "...uv_cache_directory..."`, which printed `/c /h/.cache/uv None`.

    Cross-read and found current: the rest of `docs/project-guide/shared.md` (the document check, its report, its tests and *Reference*), `docs/decisions.md` (the `.cache/uv` kept in the agent home is a different mechanism and is still true), the operator guide (no mention of the example environment) and `README.md`.

    Stale text not mine to fix: none seen.

    No findings.

    `guides`: guides: green (9.6 s)
    `secrets`: secrets: green (0.7 s)
    `documents`: documents ok (51.0 s)
21. factory: started smoke-test as vm.
22. smoke-tester: Smoke test, round 1. I ran both commands from the repository root, exactly as written and in order. Both met their `Expect:` lines.

    1. `uv run python -c "from factory.shared.adapters.document_examples import uv_cache_directory as u; print(u({'UV_CACHE_DIR': '/c', 'HOME': '/h'}), u({'HOME': '/h'}), u({}))"`
       ```
       Bytecode compiled 4164 files in 86ms
       /c /h/.cache/uv None
       ```
       Met: the printed line is `/c /h/.cache/uv None`. The line before it is uv's own bytecode note.

    2. `uv run pytest tests/shared/adapters/test_document_examples_uv_cache.py`
       ```
       Bytecode compiled 4164 files in 54ms
       ............                                                             [100%]
       12 passed in 0.03s
       ```
       Met: the summary line says only `passed`, with no `failed` or `error`.

    Criteria: neither command contradicts any acceptance criterion. Command 1 shows the lookup order and the `None` case (criterion 1). Command 2 passes the tests for criteria 1–4. Criterion 5 is in `tests/entry/test_check_documents_uv_cache.py`, which these commands do not run. Entries 16 and 20 record it green under `make check guides`. The factory's `make check` comes after this stage and covers criterion 6.

    No findings.

    `check`: check: green
23. factory: done (pull request merged); cost: 10 runs, 16.8 min, 61 turns, 228242 tokens in (1973145 more from cache), 26234 out, $2.06
