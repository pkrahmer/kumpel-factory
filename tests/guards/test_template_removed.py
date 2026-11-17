"""The operator's old project template is gone, and no shipped file or test names its folder."""

from pathlib import Path

import pytest

from support.git_support import run_git

pytestmark = pytest.mark.documents

ROOT = Path(__file__).parents[2]
# Built from its parts, so that the search below does not find this file by its constant alone.
OLD_FOLDER = "operator" + "/" + "template"
SEARCHED = ("src", "agents", "operator", "tests")
# The guards that may name the folder as one that must not exist.
LEFT_OUT = {
    "tests/guards/test_template_removed.py",
    "tests/guards/test_root_operator_folders_removed.py",
}


def test_the_template_folder_does_not_exist() -> None:
    assert not (ROOT / OLD_FOLDER).exists()


def test_no_shipped_file_or_test_names_the_template_folder() -> None:
    tracked = run_git(ROOT, "ls-files", "--", *SEARCHED).splitlines()

    found = [
        path
        for path in tracked
        if path not in LEFT_OUT
        and (ROOT / path).is_file()
        and OLD_FOLDER in (ROOT / path).read_bytes().decode("utf-8", errors="ignore")
    ]

    assert found == []
