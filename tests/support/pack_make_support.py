"""Runs of a pack's makefile in a committed project with stand-ins for the stack's tools."""

from pathlib import Path

from support.kit_support import WRITTEN_FILES, Pack, pack_project_files
from support.project_check_support import committed_repository

# The stand-ins on the PATH for each stack's tools; the Java pack's Gradle wrapper sits in the
# project, since its makefile calls `./gradlew`.
PATH_TOOLS: dict[Pack, tuple[str, ...]] = {
    "python": ("uv",),
    "c-host": ("cmake", "ctest", "clang-format", "gitleaks"),
    "java-gradle": ("gitleaks",),
}
PROJECT_TOOLS: dict[Pack, tuple[str, ...]] = {
    "python": (),
    "c-host": (),
    "java-gradle": ("gradlew",),
}
TRUST_STORE_SCRIPT = "factory/scripts/trust-store.sh"


def stand_in(path: Path, log: Path, status: int) -> None:
    """Write an executable at `path` that logs its name and arguments to `log` and ends with
    `status`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'#!/bin/sh\necho "$(basename "$0") $*" >> "{log}"\nexit {status}\n', encoding="utf-8"
    )
    path.chmod(0o755)


def stand_in_project(tmp_path: Path, pack: Pack, status: int) -> tuple[Path, dict[str, str]]:
    """A committed thin project of `pack` with its tools' stand-ins ending with `status`, logging
    to `tmp_path / "calls"`, and the variables a run of make in it needs."""
    project = committed_repository(
        tmp_path / "project", {**pack_project_files(pack, "thin"), **WRITTEN_FILES}
    )
    log = tmp_path / "calls"
    for tool in PATH_TOOLS[pack]:
        stand_in(tmp_path / "bin" / tool, log, status)
    for tool in PROJECT_TOOLS[pack]:
        stand_in(project / tool, log, status)
    # The licence check reads the file `uv export` writes; the stand-in writes none.
    reports = project / ".reports"
    reports.mkdir()
    (reports / "licenses-requirements.txt").write_text("", encoding="utf-8")
    home = tmp_path / "home"
    home.mkdir()
    variables = {"PATH": f"{tmp_path / 'bin'}:/usr/bin:/bin", "HOME": str(home)}
    return project, variables


def stand_in_trust_store(tmp_path: Path, project: Path) -> tuple[Path, Path]:
    """Replace the Java project's trust-store script with one that records its arguments and
    writes the store it is asked for; give the record's path and a certificate bundle's."""
    record = tmp_path / "trust-store-calls"
    (project / TRUST_STORE_SCRIPT).write_text(
        f'printf \'%s\\n\' "$*" >> "{record}"\nmkdir -p "$(dirname "$2")"\n: > "$2"\n',
        encoding="utf-8",
    )
    bundle = tmp_path / "bundle.pem"
    bundle.write_text("a bundle\n", encoding="utf-8")
    return record, bundle
