"""No file of the source or the tests writes the working branch's name literally."""

from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
SCOPE = ("src/factory", "tests")
LITERALS = ("origin/main", "heads/main", "-b main", "--initial-branch=main")
CACHE = "__pycache__"


def _literal_branch_names(root: Path) -> list[str]:
    """Return `path: literal` for every file in scope under `root` that holds a literal."""
    found: list[str] = []
    for folder in SCOPE:
        for path in sorted((root / folder).rglob("*")):
            if not path.is_file() or CACHE in path.parts or path == Path(__file__):
                continue
            text = path.read_bytes().decode("utf-8", errors="ignore")
            found.extend(
                f"{path.relative_to(root)}: {literal}" for literal in LITERALS if literal in text
            )
    return found


def test_no_file_in_the_source_or_the_tests_writes_the_working_branch_by_name() -> None:
    assert _literal_branch_names(ROOT) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param('BRANCH = f"{REMOTE}/{WORK_BRANCH}"\n', [], id="clean"),
        pytest.param('REF = "origin/main"\n', ["src/factory/module.py: origin/main"], id="origin"),
        pytest.param(
            'REF = "refs/heads/main"\n', ["src/factory/module.py: heads/main"], id="heads"
        ),
        pytest.param(
            'ARGS = "git init -b main"\n', ["src/factory/module.py: -b main"], id="dash-b"
        ),
        pytest.param(
            'ARGS = "--initial-branch=main"\n',
            ["src/factory/module.py: --initial-branch=main"],
            id="initial-branch",
        ),
    ],
)
def test_the_search_finds_each_literal_branch_name_in_a_file_in_scope(
    tmp_path: Path, text: str, expected: list[str]
) -> None:
    (tmp_path / "src" / "factory").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "factory" / "module.py").write_text(text, encoding="utf-8")

    assert _literal_branch_names(tmp_path) == expected
