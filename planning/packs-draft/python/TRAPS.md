# The Python pack's traps

What cost time in the Python projects the factory built (the factory itself and the todo demo; October and November 2026), and what the pack does about each.

- **No stage file is needed.** The factory's stage image holds uv, and uv fetches the Python the project pins; the pack has no `stage.Containerfile`.
- **Every tool is a pinned development dependency.** The makefile calls each through `uv run`; a tool that is not in `pyproject.toml` and `uv.lock` fails the first check. `make sync` is `uv sync --frozen`: a lockfile that does not match fails it.
- **The tests stage runs `lint` and not the type check.** The tests are written before the code, so mypy over them would fail on modules that do not exist yet.
- **The secrets check reads the changed files only.** On a work item's branch it scans what differs from the working branch; on the working branch itself every tracked file. A fake commit id or key in a test must be low-entropy (`"a" * 40`).
- **The tests run on every core.** A test must pass when its module runs on a worker of its own; a test that waits for a child gives it seconds, not tenths.
- **`SOURCE` and `LAYERS` are the project's.** The makefile's first lines name the package folder and the command that checks the layers; both carry a placeholder until the project sets them.
- **The start facts leave the lockfile out** (`FACTS_LEFT_OUT`), since no agent needs to read it.
