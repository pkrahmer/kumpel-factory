"""One layout for every project: `CLAUDE.md` and the `factory/` folder, and a root makefile that
forwards to `factory/Makefile`."""

import re
import shutil
from pathlib import Path

import pytest

from factory.agents.domain.write_paths import matches_any, protected_paths
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from support.kit_make_support import green_line
from support.kit_support import (
    KIT_MAKEFILE,
    LINES,
    PACKS,
    PACKS_FOLDER,
    ROOT_MAKEFILE,
    WRITTEN_FILES,
    Line,
    Pack,
    kit_pipeline_text,
    pack_project_files,
    run_kit_make,
)
from support.project_check_support import committed_repository, project_faults, run_project_check
from support.shipped_agents import AGENT_HOME

FACTORY_MAKEFILE = "factory/Makefile"
COMMENTED_MAKE_FILE = re.compile(r"^\s*#\s*make_file\s*:")
OWN_ROOT_MAKEFILE = "# The repository's own makefile.\nbuild:\n\t@echo built\n"
FORWARDED_MAKEFILE = (
    'include factory/kit.mk\nlint:\n\t$(start)\n\t$(green)\ncheck: lint\n\techo "check: green"\n'
)
# A line of make's output that names the target `Makefile`, in either quoting make uses.
MAKEFILE_TARGET = re.compile(r"[`']Makefile'")
OLD_ROOT_PATHS = (
    re.compile(r"(?<!factory/)scripts/trust-store\.sh"),
    re.compile(r"\.gitleaks\.toml"),
)


def _write_stand_in(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"#!/bin/sh\n{body}", encoding="utf-8")
    path.chmod(0o755)


@pytest.mark.parametrize("line", LINES)
def test_each_kit_pipeline_definition_names_the_factory_makefile(line: Line) -> None:
    text = kit_pipeline_text(line)

    definition = RuamelPipelineDefinitionReader().parse(text)

    assert definition.make_file == FACTORY_MAKEFILE
    assert not [
        text_line for text_line in text.splitlines() if COMMENTED_MAKE_FILE.match(text_line)
    ]


@pytest.mark.parametrize("line", LINES)
@pytest.mark.parametrize("pack", PACKS)
def test_a_one_way_project_is_ready_with_only_claude_md_and_makefile_outside_factory(
    tmp_path: Path, pack: Pack, line: Line
) -> None:
    files = pack_project_files(pack, line)

    faults = project_faults(tmp_path, {**files, **WRITTEN_FILES})

    assert faults == {name: [] for name in faults}
    outside = {path for path in files if not path.startswith("factory/")}
    assert outside == {"CLAUDE.md", "Makefile"}
    assert files["Makefile"] == ROOT_MAKEFILE.read_text(encoding="utf-8")


@pytest.mark.parametrize("line", LINES)
@pytest.mark.parametrize("pack", PACKS)
def test_an_own_root_makefile_is_kept_byte_for_byte(tmp_path: Path, pack: Pack, line: Line) -> None:
    files = pack_project_files(pack, line, own_root_makefile=OWN_ROOT_MAKEFILE)
    repository = committed_repository(tmp_path / "project", {**files, **WRITTEN_FILES})

    points = run_project_check(repository, AGENT_HOME)

    assert (repository / "Makefile").read_bytes() == OWN_ROOT_MAKEFILE.encode("utf-8")
    assert {point.name: point.faults for point in points} == {point.name: [] for point in points}


@pytest.mark.parametrize(
    ("args", "succeeds", "expected", "unexpected"),
    [
        pytest.param(
            [],
            True,
            [green_line("lint"), re.compile(r"^check: green$")],
            [],
            id="default-goal-is-check",
        ),
        pytest.param(
            ["lint"], True, [green_line("lint")], [re.compile(r"^check: green$")], id="lint"
        ),
        pytest.param(["nosuch"], False, [], [re.compile(r"^check: green$")], id="unknown-target"),
    ],
)
def test_the_root_makefile_forwards_every_target_to_the_factory_makefile(
    tmp_path: Path,
    args: list[str],
    succeeds: bool,
    expected: list[re.Pattern[str]],
    unexpected: list[re.Pattern[str]],
) -> None:
    project = tmp_path / "project"
    (project / "factory").mkdir(parents=True)
    shutil.copyfile(KIT_MAKEFILE, project / "factory" / "kit.mk")
    shutil.copyfile(ROOT_MAKEFILE, project / "Makefile")
    (project / FACTORY_MAKEFILE).write_text(FORWARDED_MAKEFILE, encoding="utf-8")

    result = run_kit_make(project, *args)

    lines = result.stdout.splitlines()
    assert (result.exit_status == 0) == succeeds, result.stdout
    for pattern in expected:
        assert sum(1 for line in lines if pattern.match(line)) == 1, (pattern, result.stdout)
    for pattern in unexpected:
        assert not [line for line in lines if pattern.match(line)], result.stdout
    if expected:
        assert expected[-1].match(lines[-1]), result.stdout
    assert not [line for line in lines if MAKEFILE_TARGET.search(line)], result.stdout


def test_the_java_pack_calls_its_files_under_factory(tmp_path: Path) -> None:
    files = pack_project_files("java-gradle", "thin")
    project = committed_repository(tmp_path / "project", {**files, **WRITTEN_FILES})
    calls = tmp_path / "calls"
    stand_in = f'echo "$(basename "$0") $*" >> "{calls}"\n'
    _write_stand_in(tmp_path / "bin" / "gitleaks", stand_in)
    _write_stand_in(project / "gradlew", stand_in)
    trust_calls = tmp_path / "trust-store-calls"
    (project / "factory" / "scripts" / "trust-store.sh").write_text(
        f'printf \'%s\\n\' "$*" >> "{trust_calls}"\nmkdir -p "$(dirname "$2")"\n: > "$2"\n',
        encoding="utf-8",
    )
    bundle = tmp_path / "bundle.pem"
    bundle.write_text("a bundle\n", encoding="utf-8")
    home = tmp_path / "home"
    home.mkdir()
    variables = {
        "PATH": f"{tmp_path / 'bin'}:/usr/bin:/bin",
        "HOME": str(home),
        "SSL_CERT_FILE": str(bundle),
    }

    sync = run_kit_make(project, "sync", variables=variables)
    secrets = run_kit_make(project, "secrets", variables=variables)

    assert sync.exit_status == 0, sync.stdout
    assert trust_calls.read_text(encoding="utf-8").splitlines()
    assert secrets.exit_status == 0, secrets.stdout
    gitleaks = [
        call
        for call in calls.read_text(encoding="utf-8").splitlines()
        if call.startswith("gitleaks ")
    ]
    assert gitleaks
    assert all("--config factory/gitleaks.toml" in call for call in gitleaks), gitleaks
    pack_texts = {
        path.relative_to(PACKS_FOLDER).as_posix(): path.read_text(encoding="utf-8")
        for pack in PACKS
        for path in sorted((PACKS_FOLDER / pack).rglob("*"))
        if path.is_file()
    }
    named = [
        (relative, pattern.pattern)
        for relative, text in pack_texts.items()
        for pattern in OLD_ROOT_PATHS
        if pattern.search(text)
    ]
    assert named == []


@pytest.mark.parametrize("path", [FACTORY_MAKEFILE, "factory/kit.mk"])
@pytest.mark.parametrize("line", LINES)
def test_the_factory_makefiles_are_protected_for_every_role(line: Line, path: str) -> None:
    definition = RuamelPipelineDefinitionReader().parse(kit_pipeline_text(line))

    protected = protected_paths(definition.make_file)

    assert definition.roles
    assert matches_any(path, protected)
