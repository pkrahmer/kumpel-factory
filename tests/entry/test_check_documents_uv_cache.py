"""The document check gives its examples the uv cache of its own process."""

import re
from pathlib import Path

import pytest

from factory.entry.check_documents import main
from factory.shared.domain.documents import CHECKED_DOCUMENTS
from support.check_documents_support import TIME_LINE
from support.document_texts import FENCE
from support.minimal_documents_support import add_and_commit

SHARED = "docs/project-guide/shared.md"


def test_the_check_gives_its_examples_its_own_uv_cache(
    minimal: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    cache = minimal.parent / "uv-cache"
    monkeypatch.setenv("UV_CACHE_DIR", str(cache))
    text = (minimal / SHARED).read_text(encoding="utf-8")
    block = ["", f"{FENCE}console", '$ echo "$UV_CACHE_DIR"', str(cache), FENCE, ""]
    add_and_commit(
        minimal,
        {SHARED: text.rstrip("\n") + "\n" + "\n".join(block), CHECKED_DOCUMENTS: f"{SHARED}\n"},
    )

    status = main(["--root", str(minimal)])

    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == 1
    assert re.fullmatch(TIME_LINE, lines[0])
    assert status == 0
