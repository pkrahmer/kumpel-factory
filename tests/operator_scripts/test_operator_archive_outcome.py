"""`archive-feature.sh` archives a feature only when its last acceptance in `done/` was accepted."""

from pathlib import Path

import pytest

from support.archive_feature_support import (
    ACCEPTANCE,
    ACCEPTANCE_BODY,
    ARCHIVED,
    FEATURE,
    THIRD,
    finished_feature,
    tree,
)
from support.git_support import clone, remote_commit, run_git
from support.operator_skill_support import SCRIPTS_BRANCH, SKILL, Operator, make_bare_remote

DONE = f"{FEATURE}/done"
FIRST_ACCEPTANCE = f"{DONE}/F0001-A0001-acceptance.md"
SECOND_ACCEPTANCE = f"{DONE}/F0001-A0002-acceptance.md"
REFUSED = "---\nstage: done\noutcome: refused\n---\n" + ACCEPTANCE_BODY
NO_OUTCOME = "---\nstage: done\n---\n" + ACCEPTANCE_BODY
UNCLOSED = "---\nstage: done\noutcome: accepted\n" + ACCEPTANCE_BODY
IN_BODY = "---\nstage: done\n---\n" + ACCEPTANCE_BODY + "\noutcome: accepted\n"
APPROVING = SKILL / "references" / "approving.md"


def not_accepted(path: str) -> str:
    """The refusal of a feature whose last acceptance at `path` is not accepted."""
    return f"archive-feature.sh: F0001 is not finished: its last acceptance {path} is not accepted"


def publish(operator: Operator, change: dict[str, str | None]) -> Path:
    """A remote whose `develop` holds the finished feature with `change`, and a clone of it."""
    files: dict[str, str | None] = {
        "README.md": "# Project\n",
        **finished_feature(FEATURE),
        **change,
    }
    bare, _seed = make_bare_remote(
        operator.tmp_path / "hosting",
        {name: text for name, text in files.items() if text is not None},
    )
    clone(bare, operator.checkout)
    return bare


@pytest.mark.parametrize(
    ("change", "refused"),
    [
        pytest.param({}, None, id="accepted"),
        pytest.param({FIRST_ACCEPTANCE: REFUSED}, FIRST_ACCEPTANCE, id="refused"),
        pytest.param({FIRST_ACCEPTANCE: NO_OUTCOME}, FIRST_ACCEPTANCE, id="no-outcome-line"),
        pytest.param({FIRST_ACCEPTANCE: ACCEPTANCE_BODY}, FIRST_ACCEPTANCE, id="no-front-matter"),
        pytest.param({FIRST_ACCEPTANCE: UNCLOSED}, FIRST_ACCEPTANCE, id="no-closing-line"),
        pytest.param({FIRST_ACCEPTANCE: IN_BODY}, FIRST_ACCEPTANCE, id="accepted-only-in-body"),
        pytest.param(
            {FIRST_ACCEPTANCE: REFUSED, SECOND_ACCEPTANCE: ACCEPTANCE},
            None,
            id="refused-then-accepted",
        ),
    ],
)
def test_archive_feature_archives_only_a_feature_whose_last_acceptance_was_accepted(
    operator: Operator, change: dict[str, str | None], refused: str | None
) -> None:
    bare = publish(operator, change)
    develop_before = remote_commit(bare, SCRIPTS_BRANCH)

    result = operator.run("archive-feature.sh", "F0001")

    if refused is not None:
        assert result.exit_status == 1, result.stdout
        assert remote_commit(bare, SCRIPTS_BRANCH) == develop_before
        assert run_git(operator.checkout, "rev-parse", "--abbrev-ref", "HEAD").strip() == "develop"
        assert run_git(operator.checkout, "status", "--porcelain").strip() == ""
        assert not_accepted(refused) in result.stderr.splitlines()
        return
    assert result.exit_status == 0, result.stderr
    files_after = tree(bare, SCRIPTS_BRANCH)
    assert [name for name in files_after if name.startswith(f"{FEATURE}/")] == []
    assert f"{ARCHIVED}/feature.md" in files_after


@pytest.mark.parametrize(
    ("change", "refusal"),
    [
        pytest.param(
            {f"{FEATURE}/backlog/F0001-S0003-third.md": THIRD},
            f"{FEATURE}/backlog/F0001-S0003-third.md is in backlog/",
            id="story-in-backlog",
        ),
        pytest.param(
            {f"{FEATURE}/in-progress/F0001-S0003-third.md": THIRD},
            f"{FEATURE}/in-progress/F0001-S0003-third.md is in in-progress/",
            id="story-in-progress",
        ),
        pytest.param({FIRST_ACCEPTANCE: None}, "it has no acceptance", id="no-acceptance"),
        pytest.param(
            {f"{FEATURE}/in-progress/F0001-A0002-acceptance.md": ACCEPTANCE},
            f"its last acceptance {FEATURE}/in-progress/F0001-A0002-acceptance.md is not in done/",
            id="last-acceptance-outside-done",
        ),
    ],
)
def test_archive_feature_keeps_its_earlier_refusals_and_their_texts(
    operator: Operator, change: dict[str, str | None], refusal: str
) -> None:
    bare = publish(operator, change)
    develop_before = remote_commit(bare, SCRIPTS_BRANCH)

    result = operator.run("archive-feature.sh", "F0001")

    assert result.exit_status == 1, result.stdout
    assert f"archive-feature.sh: F0001 is not finished: {refusal}" in result.stderr.splitlines()
    assert remote_commit(bare, SCRIPTS_BRANCH) == develop_before


def test_approving_names_the_refusal_of_a_feature_whose_acceptance_was_not_accepted() -> None:
    lines = APPROVING.read_text(encoding="utf-8").splitlines()
    start = lines.index("## After a feature's acceptance")
    section = lines[start + 1 :]
    end = next((i for i, line in enumerate(section) if line.startswith("## ")), len(section))
    step = next(line for line in section[:end] if line.startswith("1. "))
    assert "is not finished: its last acceptance" in step
