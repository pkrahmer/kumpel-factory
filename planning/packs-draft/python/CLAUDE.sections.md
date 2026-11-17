## Tests
- pytest. Tests live under `tests/` and mirror the package. Plain test functions, shared fixtures in `tests/conftest.py`, parametrize for tables of cases. Never mock the code under test.
- No network, no sleeps, no files outside `tmp_path`.
- Tests pass `mypy --strict` once the code exists: never use the value of a call to a function typed `-> None`; call it as a statement.
- Fake commit ids and other hexadecimal test values are low-entropy (`"a" * 40`), so that `make secrets` stays green without a baseline entry.

## Checks
- `make check` must be green before any stage reports done. It runs `make lint` (ruff check and format check), `make types` (`mypy --strict`), `make layers` (<the layers command>), `make sast` (semgrep with the rules in `security/semgrep`, and bandit), `make secrets` (detect-secrets against `.secrets.baseline`), `make licenses` (pip-licenses against an allow list) and `make test` (pytest on every core, with coverage). Each target ends with the line `<target>: green (<seconds> s)`; `make check` ends with `check: green`.
- Run Python through `uv run`. All dependencies, runtime and development, are declared and pinned in `pyproject.toml`; the lockfile is `uv.lock`.
- Run `make check` and every other make target in the foreground and read its output.

## Review
- Everything is typed; `Any` only at a boundary that validates immediately.
- No `dict[str, Any]` crosses a function boundary: inputs and outputs are models shaped by what the code needs.
- A marker that silences a check (`noqa`, `type: ignore`, `nosec`, `nosemgrep`, a baseline entry) is a finding unless this file allows it.

## Not without asking (end the stage with `question`)
- New dependency, new top-level package, change to `pyproject.toml`, the makefile or `factory/`, change to a test another story wrote, a new entry in `.secrets.baseline`, a `nosemgrep` or `nosec` marker, a licence outside the allow list.
