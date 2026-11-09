---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 686
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-09T01:06:55.841407Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-09T01:06:55.848742Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-09T01:07:20.237499Z'
  stage: intake
  run: 99f1214bf2804a25a36e2f8727fbfbd3
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-09T01:07:25.437575Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-09T01:07:57.282394Z'
  stage: tests
  run: 537d4be0fd274c80a117eb520ce58961
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-09T01:08:02.525396Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-09T01:10:32.319872Z'
  stage: doing
  run: 15d18a26744042afb5404d4b941dd55d
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-09T01:10:37.654123Z'
  stage: review
- number: 9
  speaker: reviewer
  kind: result
  at: '2026-11-09T01:11:02.061726Z'
  stage: review
  run: a28a769ae27f43eeb3153e1959f10f08
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-09T01:11:07.431495Z'
  stage: docs
- number: 11
  speaker: documenter
  kind: result
  at: '2026-11-09T01:13:25.731941Z'
  stage: docs
  run: 0f13d17c2e984d66bb28547110b1c9d2
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-09T01:13:30.552820Z'
  stage: smoke-test
- number: 13
  speaker: smoke-tester
  kind: result
  at: '2026-11-09T01:15:48.395803Z'
  stage: smoke-test
  run: 7b07864154d04eb1b0743f32272baaac
- number: 14
  speaker: factory
  kind: done
  at: '2026-11-09T01:16:37.712147Z'
  stage: approval
---

# Document examples copy from the uv cache without a warning

<!-- proposed by feature acceptance of 2026-11-09; refine before starting -->

## Description

Since F0061-S0001 the document check gives its examples `UV_CACHE_DIR`, the uv cache of the process that runs the check. But the examples run under `env -i`, so they lose the `UV_LINK_MODE=copy` that the stage image sets (`operator/vm/Dockerfile`). uv then tries to hardlink from the cache. The cache (under the agent home on the dataset) and the example's copy (a temporary folder under `/tmp`) are on different filesystems, so every document's first `uv run` fails to hardlink and falls back to a full copy. uv prints a three-line `warning: Failed to hardlink files; falling back to full copy...` into the example's output, because stderr is merged into it. The documents' examples pass today only because they start with `...`. This warning was found and fixed for agent runs once before (`UV_LINK_MODE=copy`, `docs/decisions.md`, F0040). After this story, the fixed environment holds `UV_LINK_MODE=copy` whenever it holds `UV_CACHE_DIR`. So uv copies without trying a hardlink and prints no warning, and a fixture cannot change it. Without a uv cache the examples get no `UV_LINK_MODE`, as today. Nothing else in the fixed environment changes, and the examples' limit stays 60 s.

## Interface

- `src/factory/shared/adapters/document_examples.py` (`adapters`): no new signature. `ProcessExampleRunner(time_limit, uv_cache)` keeps the one from F0061-S0001.
  - With `uv_cache` given, every command's environment holds `UV_LINK_MODE=copy` beside `UV_CACHE_DIR`. Both come after the fixture's environment, so a fixture cannot change either.
  - With `uv_cache` `None`, the fixed environment holds no `UV_LINK_MODE`. A fixture's own `UV_LINK_MODE` then reaches the command, as any other fixture variable does.
- Tests: `tests/shared/adapters/test_document_examples_uv_cache.py` (F0061-S0001's module; this story adds tests to it and changes none of its tests). Its fixtures come from `tests/support/document_examples_support.py`.

## Acceptance criteria

1. A runner built with `uv_cache` runs a command that prints `[$UV_LINK_MODE]`, with a fixture that gives no variable, and the output is `[copy]`. A runner built without `uv_cache` prints `[]`. These are rows of one parametrized test.
2. A fixture whose environment holds `UV_LINK_MODE=hardlink` does not change the value the command sees when the runner has `uv_cache`: it prints `[copy]`. Without `uv_cache`, it prints `[hardlink]`. These are rows of one parametrized test.
3. `make check` stays green.
4. docs: the project guide says that the examples get `UV_LINK_MODE=copy` with the uv cache, and why: the cache and the example's folder may lie on different filesystems, and uv's hardlink warning would otherwise reach the example's output. This goes in `docs/project-guide/shared.md` (*The examples*, the fixed variables) and in the fixed environment's list in `docs/project-guide/style.md` (*Runnable examples*).

## Smoke test

```bash
uv run --quiet python - <<'EOF'
from pathlib import Path
from factory.shared.adapters.document_examples import ProcessExampleRunner
from factory.shared.application.document_examples import Fixture
from factory.shared.domain.documents import DEFAULT_FIXTURE, examples

class Empty(Fixture):
    def prepare(self, folder: Path) -> dict[str, str]:
        return {}

text = '# A guide\n\n```console\n$ echo "[$UV_LINK_MODE]"\n[copy]\n```\n'
for cache in (Path("/c"), None):
    print(cache, ProcessExampleRunner(uv_cache=cache).run_document("g.md", examples(text).runnable, {DEFAULT_FIXTURE: Empty()}))
EOF
```
Expect: two lines, `/c []` and then `None ['g.md:4: the example printed []']`.

```bash
uv run pytest tests/shared/adapters/test_document_examples_uv_cache.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-09 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names one module, `src/factory/shared/adapters/document_examples.py`, and keeps its signature (`ProcessExampleRunner(time_limit, uv_cache)`). The change is local to `_fixed_environment`, which already adds `UV_CACHE_DIR` only when `uv_cache` is given, and `_DocumentRun.environment` already puts the fixed environment after the fixture's. The tests go in the existing `tests/shared/adapters/test_document_examples_uv_cache.py`, and no existing test there changes. `EmptyFixture` and `LiftingFixture(name, value)` in `tests/support/document_examples_support.py` already cover what the tests need.
   - Criteria: each one is testable by a single parametrized test. Criterion 1 covers both sides of the uv_cache rule: with it the command gets `[copy]`, without it `[]`. Criterion 2 covers the fixture rule on both sides: with uv_cache a fixture's `UV_LINK_MODE=hardlink` does not get through, without uv_cache it does. Neither criterion leaves a decision open. "Nothing else changes" and "the limit stays 60 s" are not new behaviour, and the existing tests already pin them.
   - Smoke test: both commands can run. The first prints `/c []` (the expected `[copy]` matches) and `None ['g.md:4: the example printed []']`. The example command is on line 4 of the text, and `DEFAULT_FIXTURE` is `checkout` (`src/factory/shared/domain/documents.py:621`). The pytest command passes no `-q`, which `addopts` already sets, and its expectation is a summary line that can be checked.
   - Docs criterion: it names what the reader must know: the variable, when the examples get it, and why (different filesystems, a warning in the output). It names the two places (`shared.md` *The examples*, `style.md` *Runnable examples*), which already list the fixed variables (`shared.md:236`, `style.md:32`). It dictates no sentences.
   - Architecture: the change stays in the `shared` adapters layer, where the process-based runner already builds the fixed environment. No new interface, dependency, tool call or layer import.
   - Scope: within F0061's goal, the examples using the check's uv cache. This story fixes a side effect of S0001's cache sharing and touches nothing in "Out of scope": the limit stays 60 s and no cache is shared between instances.
   - Route: `tests`, because the Interface changes `src/` and `tests/`.
4. factory: started tests as vm.
5. tester: Wrote the tests for both behaviour criteria. I added them to F0061-S0001's module, `tests/shared/adapters/test_document_examples_uv_cache.py`, and changed none of its existing tests.
   - criterion 1: `tests/shared/adapters/test_document_examples_uv_cache.py::test_a_command_copies_from_the_uv_cache_only_when_the_runner_has_one`. Rows `with-cache` → `[copy]` and `without-cache` → `[]`. The fixture is a local `_NoVariableFixture` that returns `{}`, because the criterion says "a fixture that gives no variable" and the support `EmptyFixture` always gives `EXAMPLE_FIXTURE`. The caller's own `UV_LINK_MODE` is set to `clone` through monkeypatch, so the `[]` row also shows the caller's value does not reach the command. This matches the existing test of `UV_CACHE_DIR`.
   - criterion 2: `tests/shared/adapters/test_document_examples_uv_cache.py::test_a_fixtures_link_mode_reaches_the_command_only_without_a_uv_cache`. Rows `with-cache` → `[copy]` and `without-cache` → `[hardlink]`. The fixture is `LiftingFixture("UV_LINK_MODE", "hardlink")` from `tests/support/document_examples_support.py`.
   - criterion 3 (`make check`) and criterion 4 (docs) are for the coder and the documenter.
   Files: I created none. I added the two tests and the one private fixture class to the module above.
   Run: `uv run pytest -q` on that module. As expected, both `with-cache` rows fail on the findings assertion, because the command prints `[]` where `[copy]` is expected. The `without-cache` rows and the existing tests pass. That is the right reason: `_fixed_environment` does not add `UV_LINK_MODE` yet. Every module imported fine. `make lint` is green, after I made the local fixture check its folder, as the support fixtures do, to clear ARG002.
   Not done: I ran this module alone, not the whole `make test` that step 2 names, as `CLAUDE.md` says for the tester's run. I skipped the type check, as the stage says.

   `lint`: lint: green (0.2 s)
6. factory: started doing as vm.
7. coder: Built: `src/factory/shared/adapters/document_examples.py`, `_fixed_environment`. When `uv_cache` is given, the fixed environment now holds `UV_LINK_MODE=copy` next to `UV_CACHE_DIR`. A comment explains why: the cache and the example's folder may lie on different filesystems, and the failed hardlink would put uv's warning into the example's output. Agent runs already copy for the same reason.
   - I changed no signature. `_DocumentRun.environment` already puts the fixed environment after the fixture's, so a fixture cannot override either variable. Without a uv cache there is no `UV_LINK_MODE`, so a fixture's own value still reaches the command.
   - Main choice: I set the variable inside the existing `if uv_cache is not None` branch. The rejected alternative was setting `UV_LINK_MODE` always. The description says the examples get no `UV_LINK_MODE` without a uv cache, and criterion 2's `[hardlink]` row needs that.
   - Run: before the change, `uv run pytest -q tests/shared/adapters/test_document_examples_uv_cache.py` failed in the two `with-cache` rows, as the tester's entry says. After the change, all 16 tests in it pass.
   - `make check guides` ended with `check: green` and `guides: green`.
   - Refactor: I read the diff and found nothing to change.
   - Noticed, not touched: the docs criterion (`docs/project-guide/shared.md` *The examples*, `docs/project-guide/style.md` *Runnable examples*) is the documenter's. The journal did not change the description.

   `duplicates`: duplicates: 7 new, 39 known, 4 gone
8. factory: started review as vm.
9. reviewer: no findings

   - Criterion 1: `tests/shared/adapters/test_document_examples_uv_cache.py::test_a_command_copies_from_the_uv_cache_only_when_the_runner_has_one` covers both sides of the uv_cache rule as rows of one parametrized test. With a cache the command prints `[copy]`; without one it prints `[]`. The caller's own `UV_LINK_MODE=clone` is set through monkeypatch, so the `[]` row also shows that the caller's value does not leak through `env -i`.
     - The test uses a local `_NoVariableFixture`, which returns `{}`. It is not a copy of an existing helper: the support `EmptyFixture` always gives a variable, and no fixture in `tests/support/` returns nothing. So the local class is the right reading of "a fixture that gives no variable".
   - Criterion 2: `test_a_fixtures_link_mode_reaches_the_command_only_without_a_uv_cache` uses the support `LiftingFixture("UV_LINK_MODE", "hardlink")`. Its rows are `with-cache` → `[copy]` and `without-cache` → `[hardlink]`. Together they cover the Interface's rule on both sides: with a cache a fixture cannot change the value, and without one the fixture's value reaches the command.
   - Code: `src/factory/shared/adapters/document_examples.py:44-47` sets `UV_LINK_MODE=copy` only inside the existing `if uv_cache is not None` branch. Line 98 keeps the fixed environment after the fixture's, so the order the Interface asks for holds. No signature changed. Nothing else in the fixed environment changed, and `EXAMPLE_TIME_LIMIT` is still 60 s. The comment gives the reason (different filesystems, so uv's warning would reach the output), not a restatement of the code.
   - Architecture and security: the change stays in the `shared` adapters layer. It adds no tool call, import, dependency or suppression marker. The journal says the coder's `make check guides` was green.
   - Hygiene: the coder's entry 7 names the main choice (set the variable only with a cache) and the rejected one (always set it). The Description matches what was built. The docs criterion still names what the documenter must write and where (`docs/project-guide/shared.md` *The examples*, `docs/project-guide/style.md` *Runnable examples*).
   - Duplicates: the `7 new` in entry 7 cannot come from this diff, which adds only three lines and one small test fixture class to `src/` and the tests.

   Earlier tests:
   - `tests/shared/adapters/test_document_examples_uv_cache.py`: none needed. The diff only adds two tests and one private fixture class, and every test the file already held is unchanged.
10. factory: started docs as vm.
11. documenter: Wrote the docs criterion into the two places it names. I changed only documents, so I did not run `make check`, as the role's lessons say. `make documents` ended with `documents ok (50.8 s)`.

    Changed:
    - `docs/project-guide/shared.md` (*The examples*): added `UV_LINK_MODE` to the fixed variables that a fixture cannot replace. Added a bullet after the uv-cache bullet. It says that with the uv cache the commands also get `UV_LINK_MODE=copy`, and why: the cache and the example's temporary folder may lie on different filesystems, so the hardlink would fail and uv's `warning: Failed to hardlink files` would reach the example's output, which also holds stderr. It also says that agent runs copy for the same reason, and that without a uv cache there is no `UV_LINK_MODE`, so a fixture's own value reaches the command.
    - `docs/project-guide/style.md` (*Runnable examples*): the fixed environment's list now names `UV_LINK_MODE=copy` beside `UV_CACHE_DIR`, when the check's process has a uv cache, with the same reason in short.

    I checked both against `src/factory/shared/adapters/document_examples.py` (`_fixed_environment`, which sets the variable only inside the `uv_cache is not None` branch). I wrote no runnable example.

    Cross-read and found current:
    - `docs/operator-guide/machine.md:134`: the image's `UV_LINK_MODE` for the runtimes, unchanged.
    - `docs/decisions.md:1047`: `UV_LINK_MODE=copy` for project commands, unchanged.
    - The rest of `shared.md` *The examples*: `uv_cache_directory`, the 60 s limit, the folder and home.
    - `README.md`: says nothing about the fixed environment.

    I added no `docs/decisions.md` entry, because the docs criterion asks for none.

    Stale but not mine: nothing found.

    `guides`: guides: green (9.7 s)
    `secrets`: secrets: green (0.4 s)
    `documents`: documents ok (51.0 s)
12. factory: started smoke-test as vm.
13. smoke-tester: Ran both smoke-test commands from the repository root, exactly as written. Both met their `Expect:` lines, so there are no findings.

    Command 1 (the inline Python that runs one example with and without a uv cache):
    ```
    /c []
    None ['g.md:4: the example printed []']
    ```
    Exit 0. This met the expectation: two lines, `/c []` and then `None ['g.md:4: the example printed []']`. With a uv cache the command printed `[copy]`, as the example expects, so the runner reported nothing. Without one it printed `[]`, which the runner reported as a mismatch on line 4.

    Command 2 (`uv run pytest tests/shared/adapters/test_document_examples_uv_cache.py`):
    ```
    Bytecode compiled 4164 files in 57ms
    ................                                                         [100%]
    16 passed in 0.03s
    ```
    Exit 0. This met the expectation: the summary line says only `passed`, with no `failed` or `error`.

    Criteria, checked against what the commands showed:
    - 1 and 2: command 1 shows the `[copy]` / `[]` sides of criterion 1. The parametrized tests for criteria 1 and 2 are among the 16 that passed.
    - 3 (`make check`): the factory runs it after this stage. I did not run it.
    - 4 (docs): grep finds the text in both places the criterion names. `docs/project-guide/shared.md:236` and `:238` say the examples get `UV_LINK_MODE=copy` with the uv cache, and why. `docs/project-guide/style.md:32` names the variable in the fixed environment's list, with the reason. Nothing in either contradicts what the smoke test showed.

    Findings: none.

    `check`: check: green
14. factory: done (pull request merged); cost: 6 runs, 4.9 min, 30 turns, 100743 tokens in (621906 more from cache), 10121 out, $0.83
