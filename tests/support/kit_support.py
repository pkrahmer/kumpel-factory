"""The kit under `operator/kit/` and the packs under `operator/packs/`: their files, a project
assembled from them, and runs of make on it."""

import os
from datetime import timedelta
from pathlib import Path
from typing import Literal

from factory.shared.adapters.process import ProcessRequest, ProcessResult, run_process
from factory.shared.domain.sections import sections, split_lines
from support.kit_make_support import DROPPED
from support.shipped_agents import ROOT

KIT = ROOT / "operator" / "kit"
KIT_FILES = (
    "CLAUDE.md",
    "factory/kit.mk",
    "factory/pipeline.thin.yml",
    "factory/pipeline.full.yml",
    "factory/story-form.md",
    "factory/feature-form.md",
    "factory/README.md",
)
KIT_MAKEFILE = KIT / "factory" / "kit.mk"
# The root makefile that forwards every target to `factory/Makefile`.
ROOT_MAKEFILE = KIT / "root.Makefile"

Line = Literal["thin", "full"]
LINES: tuple[Line, ...] = ("thin", "full")

PACKS_FOLDER = ROOT / "operator" / "packs"
Pack = Literal["python", "c-host", "java-gradle"]
PACKS: tuple[Pack, ...] = ("python", "c-host", "java-gradle")
PACK_STAGE_FILE = "stage.Containerfile"
PACK_SECTIONS = "CLAUDE.sections.md"
# The pack's pages a person reads, which do not go into the project's `factory/`.
PACK_PAGES = {PACK_SECTIONS, "TRAPS.md"}

# One file under every write path of both kit lines.
WRITTEN_FILES = {"src/a": "", "tests/a": "", "docs/a": "", "README.md": "# R\n"}

# The kit's variables, which a run sets itself or not at all.
_KIT_VARIABLES = {"WORKING_BRANCH", "FACTS_LEFT_OUT"}


def kit_pipeline_text(line: Line) -> str:
    """The text of the kit's pipeline definition of `line`."""
    return (KIT / "factory" / f"pipeline.{line}.yml").read_text(encoding="utf-8")


def kit_project_files(line: Line) -> dict[str, str]:
    """The files of a project assembled from the kit alone for `line`, by their project paths.

    The files of `operator/kit/factory/` go to `factory/`, the chosen line's pipeline
    definition as `pipeline.yml` and the other line's not at all; `CLAUDE.md` goes to the root,
    and `root.Makefile` to the root as `Makefile`.
    """
    files: dict[str, str] = {}
    for relative in KIT_FILES:
        text = (KIT / relative).read_text(encoding="utf-8")
        if relative.startswith("factory/pipeline."):
            if relative == f"factory/pipeline.{line}.yml":
                files["factory/pipeline.yml"] = text
            continue
        files[relative] = text
    files["Makefile"] = ROOT_MAKEFILE.read_text(encoding="utf-8")
    return files


def without_trailing_blanks(lines: list[str]) -> list[str]:
    """`lines` without the blank lines at their end."""
    end = len(lines)
    while end and not lines[end - 1].strip():
        end -= 1
    return lines[:end]


def section_texts(body: str) -> dict[str, list[str]]:
    """The lines of each `## ` section of `body`, heading line included, by heading, without the
    blank lines at their end."""
    lines = split_lines(body)
    return {
        section.heading: without_trailing_blanks(lines[section.start : section.end])
        for section in sections(body)
    }


def pack_claude_md(pack: Pack) -> str:
    """The kit's `CLAUDE.md` with each section of the pack's `CLAUDE.sections.md` in place of the
    kit's section of the same heading."""
    kit = (KIT / "CLAUDE.md").read_text(encoding="utf-8")
    pack_text = (PACKS_FOLDER / pack / PACK_SECTIONS).read_text(encoding="utf-8")
    replacements = section_texts(pack_text)
    kit_lines = split_lines(kit)
    kit_sections = sections(kit)
    assembled = kit_lines[: kit_sections[0].start] if kit_sections else list(kit_lines)
    for section in kit_sections:
        own = kit_lines[section.start : section.end]
        if section.heading in replacements:
            trailing = own[len(without_trailing_blanks(own)) :]
            own = [*replacements[section.heading], *trailing]
        assembled.extend(own)
    return "\n".join(assembled) + "\n"


def pack_project_files(
    pack: Pack, line: Line, *, own_root_makefile: str | None = None
) -> dict[str, str]:
    """The files of a project assembled from the kit's `line` and `pack`, by their project paths.

    Every file of the pack but its two pages goes to `factory/` at the same path; its sections
    go into the kit's `CLAUDE.md`. The root `Makefile` is the kit's forwarding one, or
    `own_root_makefile`, the repository's own, when it has one.
    """
    folder = PACKS_FOLDER / pack
    files = kit_project_files(line)
    files["CLAUDE.md"] = pack_claude_md(pack)
    if own_root_makefile is not None:
        files["Makefile"] = own_root_makefile
    for path in sorted(folder.rglob("*")):
        relative = path.relative_to(folder).as_posix()
        if path.is_file() and relative not in PACK_PAGES:
            files[f"factory/{relative}"] = path.read_text(encoding="utf-8")
    return files


def run_kit_make(
    project: Path, *args: str, variables: dict[str, str] | None = None
) -> ProcessResult:
    """Runs `make` with `args` in `project`, `variables` in its environment, no outer make's."""
    left_out = DROPPED | _KIT_VARIABLES
    environment = {key: value for key, value in os.environ.items() if key not in left_out}
    environment.update(variables or {})
    return run_process(
        ProcessRequest(
            argv=["make", "--no-print-directory", *args],
            cwd=project,
            env=environment,
            time_limit=timedelta(seconds=120),
            merge_stderr=True,
        )
    )
