"""Each pack's `## Checks` section carries the kit's line that names `factory/Makefile`."""

import pytest

from factory.shared.domain.sections import split_lines
from support.kit_support import (
    KIT,
    PACK_SECTIONS,
    PACKS,
    PACKS_FOLDER,
    Pack,
    pack_claude_md,
    section_texts,
)

CHECKS = "Checks"
LINE_START = "- The factory's targets are in `factory/Makefile`."

# The bullets of each pack's `## Checks` section other than the kit's line, in their order.
OTHER_CHECKS_BULLETS: dict[Pack, tuple[str, ...]] = {
    "python": (
        "- `make check` must be green before any stage reports done. It runs `make lint` (ruff "
        "check and format check), `make types` (`mypy --strict`), `make layers` (<the layers "
        "command>), `make sast` (semgrep with the rules in `security/semgrep`, and bandit), `make "
        "secrets` (detect-secrets with the reviewed findings of its baseline file), `make licenses`"
        " (pip-licenses against an allow list) and `make test` (pytest on every core, with "
        "coverage). Each target ends with the line `<target>: green (<seconds> s)`; `make check` "
        "ends with `check: green`.",
        "- Run Python through `uv run`. All dependencies, runtime and development, are declared and"
        " pinned in `pyproject.toml`; the lockfile is `uv.lock`.",
        "- Run `make check` and every other make target in the foreground and read its output.",
    ),
    "c-host": (
        "- `make check` must be green before any stage reports done. It runs `make lint` "
        "(clang-format over the C sources the project writes), `make secrets` (gitleaks over the "
        "working tree) and `make test` (the host build, then CTest). Each target ends with the "
        "line `<target>: green (<seconds> s)`; `make check` ends with `check: green`.",
        "- `make sync` configures the host build and fetches what `CMakeLists.txt` pins.",
        "- Run `make check` and every other make target in the foreground and read its output.",
    ),
    "java-gradle": (
        "- `make check` must be green before any stage reports done. It runs `make lint` (the "
        "compiler with `-Xlint:all -Werror`), `make secrets` (gitleaks over the working tree), "
        "`make test` and `make package`. Each target ends with the line `<target>: green "
        "(<seconds> s)`; `make check` ends with `check: green`.",
        "- `make sync` fetches the Gradle distribution and every dependency; every other target "
        "runs Gradle offline. A dependency that is new since the last sync fails until `make sync` "
        "ran again.",
        "- Run `make check` and every other make target in the foreground and read its output.",
    ),
}

# Each pack file's lines up to its `## Checks` heading, as before the kit's line was added.
LINES_BEFORE_CHECKS: dict[Pack, tuple[str, ...]] = {
    "python": (
        "## Tests",
        (
            "- pytest. Tests live under `tests/` and mirror the package. Plain test functions, "
            "shared fixtures in `tests/conftest.py`, parametrize for tables of cases. Never mock "
            "the code under test."
        ),
        "- No network, no sleeps, no files outside `tmp_path`.",
        (
            "- Tests pass `mypy --strict` once the code exists: never use the value of a call to a "
            "function typed `-> None`; call it as a statement."
        ),
        (
            '- Fake commit ids and other hexadecimal test values are low-entropy (`"a" * 40`), so '
            "that `make secrets` stays green without a baseline entry."
        ),
        "",
        "## Checks",
    ),
    "c-host": (
        "## Tests",
        (
            "- The tests build and run on the host, registered with CTest; no test needs a device, "
            "a network or a container runtime."
        ),
        (
            "- The logic is tested through its ports: a test gives it a hand-written fake of the "
            "port it calls and a clock it can set. No test sleeps."
        ),
        (
            "- The host build runs under the sanitizers `SANITIZERS` names; a sanitizer report is "
            "a failed test."
        ),
        "",
        "## Checks",
    ),
    "java-gradle": (
        "## Tests",
        (
            "- JUnit 5 with AssertJ. Unit tests are in `src/test/java`, mirroring the main "
            "packages; a class under test is created with `new` and a hand-written fake of the "
            "port it calls. Mockito is for types that cannot be faked by hand."
        ),
        (
            "- No test reaches the network, and none needs a container runtime: a stage has none. "
            "What a test needs from outside runs as a plain process that `make test` starts and "
            "stops."
        ),
        "",
        "## Checks",
    ),
}

# Each pack file's lines from the blank line that ends its `## Checks` section, as before.
LINES_AFTER_CHECKS: dict[Pack, tuple[str, ...]] = {
    "python": (
        "",
        "## Review",
        "- Everything is typed; `Any` only at a boundary that validates immediately.",
        (
            "- No `dict[str, Any]` crosses a function boundary: inputs and outputs are models "
            "shaped by what the code needs."
        ),
        (
            "- A marker that silences a check (`noqa`, `type: ignore`, `nosec`, `nosemgrep`, a "
            "baseline entry) is a finding unless this file allows it."
        ),
        "",
        "## Not without asking (end the stage with `question`)",
        (
            "- New dependency, new top-level package, change to `pyproject.toml`, the makefile or "
            "`factory/`, change to a test another story wrote, a new entry in `.secrets.baseline`, "
            "a `nosemgrep` or `nosec` marker, a licence outside the allow list."
        ),
        "",
    ),
    "c-host": (
        "",
        "## Review",
        (
            "- The logic names no platform header: what touches hardware, an operating system or a "
            "vendor's library sits behind a port in an adapter."
        ),
        (
            "- No dynamic allocation after start-up, no unbounded loop, no blocking call in the "
            "logic; every buffer has its size checked where it is filled."
        ),
        "- Every fixed-width quantity has its unit and range in its name or its comment.",
        "",
        "## Not without asking (end the stage with `question`)",
        (
            "- A new dependency or fetched source, a change to `CMakeLists.txt`, the makefile, the "
            "toolchain files or `factory/`, a change to a test another story wrote, a marker that "
            "silences a check."
        ),
        "",
    ),
    "java-gradle": (
        "",
        "## Review",
        "- No field injection; constructor injection only. Records for values.",
        (
            "- No secret and no host of a real environment in any file; configuration reaches a "
            "deployed service from outside."
        ),
        (
            "- A new dependency, plugin or version in the build files is a finding unless the "
            "story names it."
        ),
        (
            "- Javadoc: one sentence per public type, and per public method where its signature "
            "does not say it all."
        ),
        "",
        "## Not without asking (end the stage with `question`)",
        (
            "- A new dependency or plugin, a new version, a change to `build.gradle`, "
            "`settings.gradle`, `gradle/`, the makefile or `factory/`, a new top-level package, a "
            "change to a test another story wrote, a new entry in `factory/gitleaks.toml`."
        ),
        "",
    ),
}


def _kit_text() -> str:
    return (KIT / "CLAUDE.md").read_text(encoding="utf-8")


def _kit_line() -> str:
    matching = [line for line in split_lines(_kit_text()) if line.startswith(LINE_START)]
    assert len(matching) == 1, matching
    return matching[0]


def _pack_text(pack: Pack) -> str:
    return (PACKS_FOLDER / pack / PACK_SECTIONS).read_text(encoding="utf-8")


@pytest.mark.parametrize("pack", PACKS)
def test_each_assembled_checks_section_holds_the_kit_makefile_line_once(pack: Pack) -> None:
    checks = section_texts(pack_claude_md(pack))[CHECKS]

    lines = [line for line in checks if line.startswith(LINE_START)]

    assert lines == [_kit_line()]


@pytest.mark.parametrize("pack", PACKS)
def test_each_pack_sections_file_differs_from_before_only_by_the_kit_line(pack: Pack) -> None:
    kit_line = _kit_line()
    text = _pack_text(pack)

    checks = section_texts(text)[CHECKS]
    bullets = [line for line in checks[1:] if line.strip()]
    without = tuple(line for line in text.split("\n") if line != kit_line)
    expected = (
        *LINES_BEFORE_CHECKS[pack],
        *OTHER_CHECKS_BULLETS[pack],
        *LINES_AFTER_CHECKS[pack],
    )

    assert bullets[1] == kit_line
    assert tuple(bullet for bullet in bullets if bullet != kit_line) == OTHER_CHECKS_BULLETS[pack]
    assert without == expected


def test_the_kit_holds_the_makefile_line_once_under_checks() -> None:
    kit = _kit_text()

    everywhere = [line for line in split_lines(kit) if line.startswith(LINE_START)]
    in_checks = [line for line in section_texts(kit)[CHECKS] if line.startswith(LINE_START)]

    assert len(everywhere) == 1
    assert in_checks == everywhere
