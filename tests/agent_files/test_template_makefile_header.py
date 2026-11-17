"""The Python pack's makefile header calls `mutants` a sweep by hand, not a report."""

import pytest

from support.template_make_support import MAKEFILE, header_text

_NEW_HEADER_LINE = (
    "`duplicates` is a report outside `check`; `mutants` is for a sweep by hand, never a stage."
)


@pytest.mark.parametrize(
    ("text", "count", "in_header"),
    [
        pytest.param(_NEW_HEADER_LINE, 1, True, id="new-line-4"),
        pytest.param("`duplicates` and `mutants` are reports", 0, None, id="old-phrase"),
        pytest.param("for a Python project with a src layout", None, True, id="line-5"),
    ],
)
def test_template_makefile_header_calls_mutants_a_sweep_by_hand(
    text: str, count: int | None, in_header: bool | None
) -> None:
    makefile = " ".join(MAKEFILE.read_text(encoding="utf-8").replace("#", " ").split())
    if count is not None:
        assert makefile.count(text) == count
    if in_header is not None:
        assert (text in header_text()) == in_header
