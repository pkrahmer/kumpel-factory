"""The kit's root makefile forwards a target to `factory/Makefile` also when a file or a folder at
the root has the target's name."""

import re
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest

from support.kit_make_support import green_line
from support.kit_support import KIT_MAKEFILE, ROOT_MAKEFILE, run_kit_make

GREEN_RECIPE = "\t$(start)\n\t$(green)\n"
RED_RECIPE = "\t$(start)\n\texit 3\n"
CHECK_GREEN = re.compile(r"^check: green$")
FORWARDED = re.compile(r"^forwarded$")
# A line of make's output that names the target `Makefile`, in either quoting make uses.
MAKEFILE_TARGET = re.compile(r"[`']Makefile'")


def factory_makefile(test_recipe: str) -> str:
    """A `factory/Makefile` with `lint`, `test` (of `test_recipe`), `check` on both, and a target
    `factory-forward` that prints `forwarded`."""
    return (
        "include factory/kit.mk\n"
        ".PHONY: lint test check factory-forward\n"
        f"lint:\n{GREEN_RECIPE}"
        f"test:\n{test_recipe}"
        'check: lint test\n\techo "check: green"\n'
        "factory-forward:\n\techo forwarded\n"
    )


def forwarding_project(tmp_path: Path, test_recipe: str = GREEN_RECIPE) -> Path:
    """A project in `tmp_path` with the kit's root makefile as `Makefile` and a `factory/Makefile`
    that includes the kit's `factory/kit.mk`."""
    project = tmp_path / "project"
    (project / "factory").mkdir(parents=True)
    shutil.copyfile(KIT_MAKEFILE, project / "factory" / "kit.mk")
    shutil.copyfile(ROOT_MAKEFILE, project / "Makefile")
    (project / "factory" / "Makefile").write_text(factory_makefile(test_recipe), encoding="utf-8")
    return project


def with_nothing(project: Path) -> None:
    """Leaves the root as it is."""


def with_test_folder(project: Path) -> None:
    """Puts a folder `test/` at the root."""
    (project / "test").mkdir()


def with_test_file(project: Path) -> None:
    """Puts an empty file `test` at the root."""
    (project / "test").write_text("", encoding="utf-8")


def with_check_folder(project: Path) -> None:
    """Puts a folder `check/` at the root."""
    (project / "check").mkdir()


Setup = Callable[[Path], None]


def matching(pattern: re.Pattern[str], lines: list[str]) -> int:
    """How many of `lines` match `pattern`."""
    return sum(1 for line in lines if pattern.match(line))


@pytest.mark.parametrize(
    "setup",
    [
        pytest.param(with_nothing, id="nothing-named-test"),
        pytest.param(with_test_folder, id="test-folder"),
        pytest.param(with_test_file, id="test-file"),
    ],
)
def test_a_target_is_forwarded_past_a_file_or_folder_of_its_name(
    tmp_path: Path, setup: Setup
) -> None:
    project = forwarding_project(tmp_path)
    setup(project)

    result = run_kit_make(project, "test")

    lines = result.stdout.splitlines()
    assert result.exit_status == 0, result.stdout
    assert matching(green_line("test"), lines) == 1, result.stdout
    assert "up to date" not in result.stdout


def test_the_default_goal_runs_check_past_a_check_folder(tmp_path: Path) -> None:
    project = forwarding_project(tmp_path)
    with_check_folder(project)

    result = run_kit_make(project)

    lines = result.stdout.splitlines()
    assert result.exit_status == 0, result.stdout
    assert matching(green_line("lint"), lines) == 1, result.stdout
    assert matching(green_line("test"), lines) == 1, result.stdout
    assert lines, result.stdout
    assert CHECK_GREEN.match(lines[-1]), result.stdout


def test_a_red_target_is_not_hidden_by_a_folder_of_its_name(tmp_path: Path) -> None:
    project = forwarding_project(tmp_path, RED_RECIPE)
    with_test_folder(project)

    result = run_kit_make(project, "test")

    assert result.exit_status != 0, result.stdout


@pytest.mark.parametrize(
    ("test_recipe", "setup", "args", "succeeds"),
    [
        pytest.param(GREEN_RECIPE, with_nothing, ["test"], True, id="nothing-named-test"),
        pytest.param(GREEN_RECIPE, with_test_folder, ["test"], True, id="test-folder"),
        pytest.param(GREEN_RECIPE, with_test_file, ["test"], True, id="test-file"),
        pytest.param(GREEN_RECIPE, with_check_folder, [], True, id="default-goal-check-folder"),
        pytest.param(RED_RECIPE, with_test_folder, ["test"], False, id="red-test-folder"),
        pytest.param(GREEN_RECIPE, with_nothing, ["nosuch"], False, id="unknown-target"),
    ],
)
def test_an_unknown_target_ends_red_and_no_run_remakes_the_makefile(
    tmp_path: Path, test_recipe: str, setup: Setup, args: list[str], succeeds: bool
) -> None:
    project = forwarding_project(tmp_path, test_recipe)
    setup(project)

    result = run_kit_make(project, *args)

    assert (result.exit_status == 0) == succeeds, result.stdout
    assert not [line for line in result.stdout.splitlines() if MAKEFILE_TARGET.search(line)], (
        result.stdout
    )


def test_the_forwarding_target_name_is_not_forwarded(tmp_path: Path) -> None:
    project = forwarding_project(tmp_path)

    result = run_kit_make(project, "factory-forward")

    assert result.exit_status == 0, result.stdout
    assert matching(FORWARDED, result.stdout.splitlines()) == 0, result.stdout
