---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 684
comments_read: [6729441197]
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-09T00:36:00.302295Z'
  lease_duration: 60
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
