---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-09T00:34:17.952891Z'
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
- Tests: `tests/shared/adapters/test_document_examples_uv_cache.py`.

## Acceptance criteria

1. `uv_cache_directory` returns `UV_CACHE_DIR`'s value when it is set; `XDG_CACHE_HOME/uv` when only `XDG_CACHE_HOME` and `HOME` are set; `HOME/.cache/uv` when only `HOME` is set; `None` when none is set; and an empty value counts as not set, for each of the three: rows of one parametrized test.
2. A runner built with `uv_cache` runs a command that prints `$UV_CACHE_DIR`, and the output is that path; a runner built without it prints an empty line: rows of one parametrized test.
3. A fixture whose environment holds `UV_CACHE_DIR` does not change the value the command sees when the runner has `uv_cache`.
4. With `uv_cache` given, the command's `$HOME` is still the document's own home folder, not the cache's parent.
5. `make check` stays green.
6. docs: the project guide (`docs/project-guide/shared.md`, the document examples) says that the examples share the uv cache of the process that runs the check, how that cache is found, and why (a fresh copy's first `uv run` would otherwise download every package and could pass the examples' limit).

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
