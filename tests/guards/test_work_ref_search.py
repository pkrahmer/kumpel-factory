"""Only the paths module of the shared domain builds the working branch's remote ref."""

from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
SOURCE = "src/factory"
CACHE = "__pycache__"
SPELLING = "{REMOTE}/{WORK_BRANCH}"
OWNER = Path("src/factory/shared/domain/paths.py")


def _spelled_work_refs(root: Path) -> list[str]:
    """Return the relative path of every source file but the owner that builds the ref."""
    found: list[str] = []
    for path in sorted((root / SOURCE).rglob("*.py")):
        relative = path.relative_to(root)
        if CACHE in path.parts or relative == OWNER:
            continue
        if SPELLING in path.read_text(encoding="utf-8"):
            found.append(str(relative))
    return found


def test_no_source_file_but_the_paths_module_builds_the_working_branch_s_remote_ref() -> None:
    assert _spelled_work_refs(ROOT) == []


@pytest.mark.parametrize(
    ("relative", "text", "expected"),
    [
        pytest.param(
            "src/factory/module.py",
            'ref = f"{REMOTE}/{WORK_BRANCH}"\n',
            ["src/factory/module.py"],
            id="inline",
        ),
        pytest.param(
            "src/factory/area/application/module.py",
            '_WORK_REF = f"{REMOTE}/{WORK_BRANCH}"\n',
            ["src/factory/area/application/module.py"],
            id="private-constant",
        ),
        pytest.param(
            "src/factory/module.py",
            "from factory.shared.domain.paths import WORK_REF\n\nref = WORK_REF\n",
            [],
            id="imports-work-ref",
        ),
        pytest.param(
            "src/factory/module.py",
            'ref = f"{REMOTE}/{snapshot.branch}"\n',
            [],
            id="work-item-branch",
        ),
        pytest.param(
            "src/factory/shared/domain/paths.py",
            'WORK_REF = f"{REMOTE}/{WORK_BRANCH}"\n',
            [],
            id="the-paths-module",
        ),
    ],
)
def test_the_search_finds_each_file_that_builds_the_working_branch_s_remote_ref(
    tmp_path: Path, relative: str, text: str, expected: list[str]
) -> None:
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")

    assert _spelled_work_refs(tmp_path) == expected
