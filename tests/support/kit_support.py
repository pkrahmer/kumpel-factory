"""The kit under `operator/kit/`: its files, a project assembled from it, and runs of make on it."""

import os
from datetime import timedelta
from pathlib import Path
from typing import Literal

from factory.shared.adapters.process import ProcessRequest, ProcessResult, run_process
from support.shipped_agents import ROOT
from support.template_make_support import DROPPED

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

Line = Literal["thin", "full"]
LINES: tuple[Line, ...] = ("thin", "full")

# The kit's variables, which a run sets itself or not at all.
_KIT_VARIABLES = {"WORKING_BRANCH", "FACTS_LEFT_OUT"}


def kit_pipeline_text(line: Line) -> str:
    """The text of the kit's pipeline definition of `line`."""
    return (KIT / "factory" / f"pipeline.{line}.yml").read_text(encoding="utf-8")


def kit_project_files(line: Line) -> dict[str, str]:
    """The files of a project assembled from the kit alone for `line`, by their project paths.

    The files of `operator/kit/factory/` go to `factory/`, the chosen line's pipeline
    definition as `pipeline.yml` and the other line's not at all; `CLAUDE.md` goes to the root.
    """
    files: dict[str, str] = {}
    for relative in KIT_FILES:
        text = (KIT / relative).read_text(encoding="utf-8")
        if relative.startswith("factory/pipeline."):
            if relative == f"factory/pipeline.{line}.yml":
                files["factory/pipeline.yml"] = text
            continue
        files[relative] = text
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
