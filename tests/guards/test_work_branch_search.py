"""No file of the source or the tests writes the working branch's name literally."""

import io
import tokenize
from pathlib import Path

import pytest

pytestmark = pytest.mark.documents

ROOT = Path(__file__).parents[2]
SCOPE = ("src/factory", "tests")
LITERALS = ("origin/main", "heads/main", "-b main", "--initial-branch=main")
CACHE = "__pycache__"
SOURCE = "src/factory"
KEPT_NAMES = frozenset({"main_branch_failing", "_MAIN_FAILING", "main_failed", "main_probed"})
SPELLED_REMOTE = "origin/{WORK_BRANCH}"


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


def _names_by_the_old_branch(root: Path) -> list[str]:
    """Return `path: name` for every identifier under the source that holds `main` as a word part.

    A file that spells the remote out before the working branch is found as `path: origin/...`.
    """
    found: list[str] = []
    for path in sorted((root / SOURCE).rglob("*.py")):
        if CACHE in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        names = {
            token.string
            for token in tokenize.generate_tokens(io.StringIO(text).readline)
            if token.type == tokenize.NAME
        }
        found.extend(f"{relative}: {name}" for name in sorted(names) if _says_main(name))
        if SPELLED_REMOTE in text:
            found.append(f"{relative}: {SPELLED_REMOTE}")
    return found


def _says_main(name: str) -> bool:
    if name in KEPT_NAMES or (name.startswith("__") and name.endswith("__")):
        return False
    parts = name.split("_")
    return len(parts) > 1 and "main" in (part.lower() for part in parts)


def test_no_identifier_in_the_source_names_the_working_branch_main() -> None:
    assert _names_by_the_old_branch(ROOT) == []


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        pytest.param(
            "stage_file_on_main(git)\n",
            ["src/factory/module.py: stage_file_on_main"],
            id="public-function",
        ),
        pytest.param(
            "commit = x.main_commit\n", ["src/factory/module.py: main_commit"], id="field"
        ),
        pytest.param(
            "reports = _main_reports(git)\n",
            ["src/factory/module.py: _main_reports"],
            id="private-helper",
        ),
        pytest.param("stop = main_branch_failing\n", [], id="kept-stop"),
        pytest.param("failed = stamp.main_failed\n", [], id="kept-stamp-failed"),
        pytest.param("probed = stamp.main_probed\n", [], id="kept-stamp-probed"),
        pytest.param("def main() -> None:\n    pass\n", [], id="entry-point"),
        pytest.param(
            'ref = f"origin/{WORK_BRANCH}"\n',
            ["src/factory/module.py: origin/{WORK_BRANCH}"],
            id="remote-spelled-out",
        ),
        pytest.param('ref = f"{REMOTE}/{WORK_BRANCH}"\n', [], id="remote-from-constant"),
    ],
)
def test_the_search_finds_each_name_that_says_main_for_the_working_branch(
    tmp_path: Path, text: str, expected: list[str]
) -> None:
    (tmp_path / "src" / "factory").mkdir(parents=True)
    (tmp_path / "src" / "factory" / "module.py").write_text(text, encoding="utf-8")

    assert _names_by_the_old_branch(tmp_path) == expected
