"""The marker `documents` splits the suite into the tests that read the documents and the rest."""

import os
import re
import sys
from datetime import timedelta
from pathlib import Path

import pytest

from factory.shared.adapters.process import ProcessRequest, run_process

ROOT = Path(__file__).parents[2]
TESTS = ROOT / "tests"
MARK = re.compile(r"^pytestmark = pytest\.mark\.documents$", re.MULTILINE)
SELECTIONS = ("", "documents", "not documents")


def _collected(selection: str) -> frozenset[str]:
    """The node ids that `pytest --strict-markers --collect-only` collects for `selection`."""
    env = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith(("PYTEST_", "COV_CORE_"))
    }
    chosen = ["-m", selection] if selection else []
    result = run_process(
        ProcessRequest(
            argv=[sys.executable, "-m", "pytest", "--strict-markers", *chosen, "--collect-only"],
            cwd=ROOT,
            env=env,
            time_limit=timedelta(seconds=300),
        )
    )
    assert result.exit_status == 0, result.stdout + result.stderr
    return frozenset(line for line in result.stdout.splitlines() if "::" in line)


@pytest.fixture(scope="module")
def collections() -> dict[str, frozenset[str]]:
    """The node ids of the whole suite and of each side of the marker."""
    return {selection: _collected(selection) for selection in SELECTIONS}


def _marked_modules() -> frozenset[str]:
    return frozenset(
        path.relative_to(ROOT).as_posix()
        for path in TESTS.rglob("test_*.py")
        if MARK.search(path.read_text(encoding="utf-8"))
    )


def test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other(
    collections: dict[str, frozenset[str]],
) -> None:
    marked = _marked_modules()
    expected = {node for node in collections[""] if node.split("::")[0] in marked}

    assert marked
    assert collections["documents"] == expected


def test_the_tests_without_the_marker_are_the_rest_of_the_suite(
    collections: dict[str, frozenset[str]],
) -> None:
    assert collections["not documents"]
    assert collections["not documents"] == collections[""] - collections["documents"]
