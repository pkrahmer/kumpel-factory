"""The stack packs under `operator/packs/`, and projects assembled from the kit and a pack."""

import re
from collections import Counter
from datetime import timedelta
from pathlib import Path

import pytest

from factory.machine.domain.stage_layer import stage_layer
from factory.pipeline.domain.project_check import makefile_targets
from factory.shared.adapters.process import ProcessRequest, run_process
from factory.shared.domain.sections import sections, split_lines
from support.kit_support import (
    KIT,
    LINES,
    PACK_SECTIONS,
    PACK_STAGE_FILE,
    PACKS,
    PACKS_FOLDER,
    WRITTEN_FILES,
    Line,
    Pack,
    pack_claude_md,
    pack_project_files,
    run_kit_make,
)
from support.project_check_support import committed_repository, run_project_check
from support.shipped_agents import AGENT_HOME
from support.template_make_support import green_line

STACK_TARGETS = ("sync", "lint", "test", "check")
KIT_TARGETS = ("facts-diff", "facts-changes", "facts-files")
PACK_HEADINGS = ("Tests", "Checks", "Review", "Not without asking (end the stage with `question`)")
KIT_KEPT_HEADINGS = ("Language", "Architecture")
STAGE_FILE_PACKS: tuple[Pack, ...] = ("c-host", "java-gradle")
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
# The Python pack's placeholders, which the project sets.
MAKE_VARIABLES: dict[Pack, tuple[str, ...]] = {
    "python": ("SOURCE=src/app", "LAYERS=uv run lint-imports"),
    "c-host": (),
    "java-gradle": (),
}
TRUST_STORE = ".cache/java-trust-store.p12"


def _faults(tmp_path: Path, files: dict[str, str]) -> dict[str, list[str]]:
    repository = committed_repository(tmp_path / "project", {**files, **WRITTEN_FILES})
    return {point.name: point.faults for point in run_project_check(repository, AGENT_HOME)}


def _stand_in(path: Path, log: Path, status: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'#!/bin/sh\necho "$(basename "$0") $*" >> "{log}"\nexit {status}\n', encoding="utf-8"
    )
    path.chmod(0o755)


def _stand_in_project(tmp_path: Path, pack: Pack, status: int) -> tuple[Path, dict[str, str]]:
    """A committed project of `pack` with its tools' stand-ins ending with `status`, and the
    variables a run of make in it needs."""
    project = committed_repository(
        tmp_path / "project", {**pack_project_files(pack, "thin"), **WRITTEN_FILES}
    )
    log = tmp_path / "calls"
    for tool in PATH_TOOLS[pack]:
        _stand_in(tmp_path / "bin" / tool, log, status)
    for tool in PROJECT_TOOLS[pack]:
        _stand_in(project / tool, log, status)
    # The licence check reads the file `uv export` writes; the stand-in writes none.
    reports = project / ".reports"
    reports.mkdir()
    (reports / "licenses-requirements.txt").write_text("", encoding="utf-8")
    home = tmp_path / "home"
    home.mkdir()
    variables = {"PATH": f"{tmp_path / 'bin'}:/usr/bin:/bin", "HOME": str(home)}
    return project, variables


def _check_prerequisites(pack: Pack) -> list[str]:
    text = (PACKS_FOLDER / pack / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^check:(.*)$", text, re.MULTILINE)
    assert match is not None
    return match.group(1).split()


def _instructions(text: str) -> list[str]:
    instructions: list[str] = []
    current = ""
    for line in text.splitlines():
        if not current and (not line.strip() or line.lstrip().startswith("#")):
            continue
        current += line.rstrip().removesuffix("\\") + " "
        if not line.rstrip().endswith("\\"):
            instructions.append(current)
            current = ""
    if current:
        instructions.append(current)
    return instructions


def _section_texts(body: str) -> dict[str, list[str]]:
    lines = split_lines(body)
    texts: dict[str, list[str]] = {}
    for section in sections(body):
        own = lines[section.start : section.end]
        while own and not own[-1].strip():
            own.pop()
        texts[section.heading] = own
    return texts


@pytest.mark.parametrize("line", LINES)
@pytest.mark.parametrize("pack", PACKS)
def test_a_project_from_the_kit_and_a_pack_is_ready(tmp_path: Path, pack: Pack, line: Line) -> None:
    faults = _faults(tmp_path, pack_project_files(pack, line))

    assert faults == {name: [] for name in faults}


@pytest.mark.parametrize("line", LINES)
@pytest.mark.parametrize("pack", PACKS)
def test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready(
    tmp_path: Path, pack: Pack, line: Line
) -> None:
    files = pack_project_files(pack, line, brownfield=True)

    faults = _faults(tmp_path, files)

    assert "Makefile" not in files
    assert "make_file: factory/Makefile" in files["factory/pipeline.yml"].splitlines()
    assert faults == {name: [] for name in faults}


@pytest.mark.parametrize("pack", PACKS)
def test_each_pack_makefile_includes_the_kit_first_and_defines_only_the_stack_targets(
    pack: Pack,
) -> None:
    text = (PACKS_FOLDER / pack / "Makefile").read_text(encoding="utf-8")
    lines = text.splitlines()

    targets = makefile_targets(text)

    include = lines.index("include factory/kit.mk")
    first_rule = min(index for index, line in enumerate(lines) if makefile_targets(line))
    assert include < first_rule
    assert set(STACK_TARGETS) <= targets
    assert targets.isdisjoint(KIT_TARGETS)


@pytest.mark.parametrize("pack", STAGE_FILE_PACKS)
def test_each_stage_file_keeps_the_layer_rule_and_checks_every_download(pack: Pack) -> None:
    text = (PACKS_FOLDER / pack / PACK_STAGE_FILE).read_text(encoding="utf-8")

    stage_layer(text, "base")

    for instruction in _instructions(text):
        for after_download in instruction.split("curl ")[1:]:
            assert "sha256sum -c" in after_download, instruction


@pytest.mark.parametrize("pack", PACKS)
def test_each_pack_sections_replace_the_kit_sections_of_the_same_heading(pack: Pack) -> None:
    kit = (KIT / "CLAUDE.md").read_text(encoding="utf-8")
    pack_text = (PACKS_FOLDER / pack / PACK_SECTIONS).read_text(encoding="utf-8")
    kit_headings = [section.heading for section in sections(kit)]
    pack_sections = _section_texts(pack_text)

    assembled = pack_claude_md(pack)

    assert set(PACK_HEADINGS) <= set(pack_sections)
    assert set(pack_sections) <= set(kit_headings)
    headings = Counter(section.heading for section in sections(assembled))
    assert headings == Counter(kit_headings)
    assembled_sections = _section_texts(assembled)
    for heading, text in pack_sections.items():
        assert assembled_sections[heading] == text
    kit_sections = _section_texts(kit)
    for heading in KIT_KEPT_HEADINGS:
        assert assembled_sections[heading] == kit_sections[heading]


@pytest.mark.parametrize(
    ("status", "green"),
    [pytest.param(0, True, id="tools-pass"), pytest.param(1, False, id="tool-fails")],
)
@pytest.mark.parametrize("pack", PACKS)
def test_make_check_of_a_pack_is_green_only_when_its_tools_pass(
    tmp_path: Path, pack: Pack, status: int, green: bool
) -> None:
    project, variables = _stand_in_project(tmp_path, pack, status)

    result = run_kit_make(project, "check", *MAKE_VARIABLES[pack], variables=variables)

    lines = result.stdout.splitlines()
    assert (tmp_path / "calls").read_text(encoding="utf-8")
    if green:
        assert result.exit_status == 0, result.stdout
        assert lines[-1] == "check: green"
        for target in _check_prerequisites(pack):
            pattern = green_line(target)
            assert sum(1 for line in lines if pattern.match(line)) == 1, target
    else:
        assert result.exit_status != 0
        assert "check: green" not in lines


def test_the_java_trust_store_script_is_a_posix_shell_script(tmp_path: Path) -> None:
    script = PACKS_FOLDER / "java-gradle" / "scripts" / "trust-store.sh"

    result = run_process(
        ProcessRequest(
            argv=["sh", "-n", str(script)], cwd=tmp_path, time_limit=timedelta(seconds=30)
        )
    )

    assert script.read_text(encoding="utf-8").splitlines()[0] == "#!/bin/sh"
    assert result.exit_status == 0, result.stderr


def test_the_java_sync_builds_the_trust_store_once_per_bundle(tmp_path: Path) -> None:
    project, variables = _stand_in_project(tmp_path, "java-gradle", 0)
    record = tmp_path / "trust-store-calls"
    (project / "scripts" / "trust-store.sh").write_text(
        f'printf \'%s\\n\' "$*" >> "{record}"\nmkdir -p "$(dirname "$2")"\n: > "$2"\n',
        encoding="utf-8",
    )
    bundle = tmp_path / "bundle.pem"
    bundle.write_text("a bundle\n", encoding="utf-8")
    variables["SSL_CERT_FILE"] = str(bundle)

    first = run_kit_make(project, "sync", variables=variables)
    second = run_kit_make(project, "sync", variables=variables)

    assert first.exit_status == 0, first.stdout
    assert second.exit_status == 0, second.stdout
    assert record.read_text(encoding="utf-8").splitlines() == [
        f"{bundle} {variables['HOME']}/{TRUST_STORE}"
    ]
