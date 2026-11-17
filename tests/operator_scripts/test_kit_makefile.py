"""Real runs of make on a makefile that includes the kit's `kit.mk`."""

import re
import shutil
from pathlib import Path

import pytest

from support.git_support import clone, commit_all, make_remote, run_git, write_files
from support.kit_make_support import green_line
from support.kit_support import KIT_MAKEFILE, run_kit_make

PROJECT_MAKEFILE = (
    "include factory/kit.mk\n"
    "lint:\n\t$(start)\n\ttrue\n\t$(green)\n"
    "broken:\n\t$(start)\n\tfalse\n\techo reached\n\t$(green)\n"
    'check: lint\n\techo "check: green"\n'
)
LEFT_OUT = ":!build.lock"
FACTS = ("facts-diff", "facts-changes", "facts-files")
BRANCH_CHANGES = {"src/a.txt": "two\n", "factory/pipeline.yml": "second\n"}


def _project(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    (project / "factory").mkdir(parents=True)
    shutil.copyfile(KIT_MAKEFILE, project / "factory" / "kit.mk")
    (project / "Makefile").write_text(PROJECT_MAKEFILE, encoding="utf-8")
    return project


def _branch_clone(tmp_path: Path, base: str, changes: dict[str, str]) -> Path:
    """A clone of a remote whose branch `base` holds the kit, on a branch committing `changes`.

    The clone also holds one untracked file, `src/new.txt`.
    """
    files = {
        "Makefile": "include factory/kit.mk\n",
        "factory/kit.mk": KIT_MAKEFILE.read_text(encoding="utf-8"),
        "factory/pipeline.yml": "first\n",
        "src/a.txt": "one\n",
        "build.lock": "lock one\n",
    }
    remote = make_remote(tmp_path / "remote", files, branch=base)
    checkout = clone(remote, tmp_path / "clone")
    run_git(checkout, "checkout", "-q", "-b", "work")
    write_files(checkout, changes)
    commit_all(checkout, "work")
    write_files(checkout, {"src/new.txt": "new\n"})
    return checkout


@pytest.mark.parametrize(
    ("args", "succeeds", "lines"),
    [
        pytest.param(
            [], True, [green_line("lint"), re.compile(r"^check: green$")], id="default-goal"
        ),
        pytest.param(["broken"], False, [], id="first-line-fails"),
    ],
)
def test_a_kit_recipe_prints_only_its_green_line_or_stops_red(
    tmp_path: Path, args: list[str], succeeds: bool, lines: list[re.Pattern[str]]
) -> None:
    result = run_kit_make(_project(tmp_path), *args)

    printed = [line for line in result.stdout.splitlines() if not line.startswith("make: ***")]
    assert (result.exit_status == 0) == succeeds
    assert len(printed) == len(lines), result.stdout
    assert all(pattern.fullmatch(line) for pattern, line in zip(lines, printed, strict=True))


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        pytest.param("facts-files", ["Makefile", "build.lock", "src/a.txt"], id="files"),
        pytest.param("facts-changes", ["M\tsrc/a.txt", "src/new.txt"], id="changes"),
    ],
)
def test_the_listing_start_facts_leave_out_the_factory_folder(
    tmp_path: Path, target: str, expected: list[str]
) -> None:
    checkout = _branch_clone(tmp_path, "develop", BRANCH_CHANGES)

    result = run_kit_make(checkout, target)

    assert result.exit_status == 0, result.stdout
    assert result.stdout.splitlines() == expected


def test_the_diff_start_fact_holds_the_branch_change_from_origin_develop(
    tmp_path: Path,
) -> None:
    checkout = _branch_clone(tmp_path, "develop", BRANCH_CHANGES)

    result = run_kit_make(checkout, "facts-diff")

    assert result.exit_status == 0, result.stdout
    assert "src/a.txt" in result.stdout
    assert {"-one", "+two"} <= set(result.stdout.splitlines())
    assert "factory" not in result.stdout
    assert "second" not in result.stdout


@pytest.mark.parametrize("target", FACTS)
@pytest.mark.parametrize(
    ("variables", "shown"),
    [
        pytest.param({}, True, id="without-left-out"),
        pytest.param({"FACTS_LEFT_OUT": LEFT_OUT}, False, id="left-out"),
    ],
)
def test_facts_left_out_leaves_its_paths_out_of_every_start_fact(
    tmp_path: Path, target: str, variables: dict[str, str], shown: bool
) -> None:
    checkout = _branch_clone(tmp_path, "develop", {"build.lock": "lock two\n"})

    result = run_kit_make(checkout, target, variables=variables)

    assert result.exit_status == 0, result.stdout
    assert ("build.lock" in result.stdout) == shown


def test_working_branch_names_the_base_of_the_diff(tmp_path: Path) -> None:
    checkout = _branch_clone(tmp_path, "main", {"src/a.txt": "two\n"})

    result = run_kit_make(checkout, "facts-diff", variables={"WORKING_BRANCH": "main"})

    assert result.exit_status == 0, result.stdout
    assert {"-one", "+two"} <= set(result.stdout.splitlines())
