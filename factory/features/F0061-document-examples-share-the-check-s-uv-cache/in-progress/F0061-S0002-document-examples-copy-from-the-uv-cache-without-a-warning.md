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
