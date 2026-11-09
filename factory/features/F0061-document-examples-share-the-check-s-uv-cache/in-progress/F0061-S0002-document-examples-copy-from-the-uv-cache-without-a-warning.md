---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 686
comments_read: []
handed_over: null
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
