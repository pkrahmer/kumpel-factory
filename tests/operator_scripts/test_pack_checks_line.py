"""Each pack's `## Checks` section carries the kit's line that names `factory/Makefile`."""

import hashlib

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

# The sha256 of each pack's `CLAUDE.sections.md` as it was before the kit's line was added.
SECTIONS_BEFORE_SHA256: dict[Pack, str] = {
    "python": "db11db87fa8e3028cc57f5db81d28a7d991b5f3428cf87817a802f53ae11971e",
    "c-host": "9fb0ec3597d149077978af59a390d5960a41392cede3768145ff1e1db8b0958c",
    "java-gradle": "46d3cc2ebc5d3cc20fa7f2f8bd9ce322f3e5afc3891121772d52b8546d009ba9",
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
    without = [line for line in text.split("\n") if line != kit_line]
    before = "\n".join(without).encode("utf-8")

    assert bullets[1] == kit_line
    assert tuple(bullet for bullet in bullets if bullet != kit_line) == OTHER_CHECKS_BULLETS[pack]
    assert hashlib.sha256(before).hexdigest() == SECTIONS_BEFORE_SHA256[pack]


def test_the_kit_holds_the_makefile_line_once_under_checks() -> None:
    kit = _kit_text()

    everywhere = [line for line in split_lines(kit) if line.startswith(LINE_START)]
    in_checks = [line for line in section_texts(kit)[CHECKS] if line.startswith(LINE_START)]

    assert len(everywhere) == 1
    assert in_checks == everywhere
