"""The shipped agent files and the project template name `develop` as the working branch."""

import re
from pathlib import Path

import pytest

from factory.shared.domain.paths import REMOTE

ROOT = Path(__file__).parents[2]
FOLDERS = ("agents/agents", "operator/template")
CACHE = "__pycache__"


def _texts() -> dict[str, str]:
    """Return the text of every file under the two folders, by its path from the root."""
    texts: dict[str, str] = {}
    for folder in FOLDERS:
        for path in sorted((ROOT / folder).rglob("*")):
            if path.is_file() and CACHE not in path.parts:
                text = path.read_bytes().decode("utf-8", errors="ignore")
                texts[str(path.relative_to(ROOT))] = text
    return texts


@pytest.mark.parametrize(
    "form",
    [
        pytest.param(re.escape(f"{REMOTE}/main"), id="remote-ref"),
        pytest.param(re.escape("main...HEAD"), id="three-dot-diff"),
        pytest.param(r"git diff main\b", id="git-diff"),
        pytest.param(r"reaches\s+`main`\s+only\s+through", id="human-merge"),
        pytest.param(r"report\s+to\s+`main`", id="acceptance-report"),
        pytest.param(r"that\s+`main`\s+already\s+holds", id="already-holds"),
        pytest.param(r"on\s+`?main`?\s+itself", id="on-itself"),
    ],
)
def test_no_agent_or_template_file_names_main_as_the_working_branch(form: str) -> None:
    found = [path for path, text in _texts().items() if re.search(form, text)]

    assert found == []


def test_main_as_an_ordinary_word_stays_in_the_agent_files() -> None:
    assert "the main choice" in _texts()["agents/agents/coder.md"]
