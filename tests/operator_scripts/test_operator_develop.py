"""Kumpel on `develop`: its scripts read and write `develop`; only a promotion reaches `main`."""

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from support.git_support import clone, commit_all, run_git, write_files
from support.operator_skill_support import (
    DEFAULT_BRANCH,
    KUMPEL,
    PREFIX,
    SCRIPTS_BRANCH,
    SKILL,
    Operator,
    Request,
    make_bare_remote,
    recorded_requests,
)
from support.operator_support import ROOT

FEATURE_FOLDER = "F0001-example"
FEATURE = f"factory/features/{FEATURE_FOLDER}"
ARCHIVED = f"factory/archive/{FEATURE_FOLDER}"
OTHER = "factory/features/F0002-other"
FEATURE_TEXT = "# Example feature\n\n## Stories\n\n- S0001: first\n- S0002: second\n"
FIRST = "# First story\n\n## Journal\n\n1. human: created.\n"
SECOND = "# Second story\n\n## Journal\n\n1. human: created.\n"
THIRD = "# Third story\n\n## Journal\n\n1. human: created.\n"
ACCEPTANCE = "# Acceptance of F0001\n\n## Journal\n\n1. factory: created.\n"
LOG_FORMAT = "%s%n%an <%ae>%n%cn <%ce>"
PULL_NUMBER = 4711


def finished_feature(folder: str) -> dict[str, str]:
    """A feature in `folder` whose two stories and whose acceptance are done."""
    return {
        f"{folder}/feature.md": FEATURE_TEXT,
        f"{folder}/done/F0001-S0001-first.md": FIRST,
        f"{folder}/done/F0001-S0002-second.md": SECOND,
        f"{folder}/done/F0001-A0001-acceptance.md": ACCEPTANCE,
    }


def tree(remote: Path, branch: str) -> list[str]:
    """The files `branch` of `remote` holds."""
    return run_git(remote, "ls-tree", "-r", "--name-only", branch).splitlines()


def head(remote: Path, branch: str) -> str:
    """The commit `branch` of `remote` names."""
    return run_git(remote, "rev-parse", branch).strip()


def test_start_story_commits_on_develop_as_kumpel(operator: Operator) -> None:
    files = {
        "README.md": "# Project\n",
        f"{FEATURE}/feature.md": FEATURE_TEXT,
        f"{FEATURE}/backlog/F0001-S0001-first.md": FIRST,
    }
    bare, _seed = make_bare_remote(operator.tmp_path / "hosting", files)
    clone(bare, operator.checkout)
    main_before = head(bare, DEFAULT_BRANCH)

    result = operator.run("start-story.sh", "F0001-S0001")

    assert result.exit_status == 0, result.stderr
    pushed = run_git(bare, "log", "-1", f"--format={LOG_FORMAT}", SCRIPTS_BRANCH)
    assert pushed.splitlines() == ["F0001-S0001: start", KUMPEL, KUMPEL]
    assert f"{FEATURE}/in-progress/F0001-S0001-first.md" in tree(bare, SCRIPTS_BRANCH)
    assert head(bare, DEFAULT_BRANCH) == main_before


@pytest.mark.parametrize(
    ("change", "archived"),
    [
        pytest.param({}, True, id="finished"),
        pytest.param(
            {f"{FEATURE}/backlog/F0001-S0003-third.md": THIRD}, False, id="story-in-backlog"
        ),
        pytest.param(
            {f"{FEATURE}/in-progress/F0001-S0003-third.md": THIRD}, False, id="story-in-progress"
        ),
        pytest.param(
            {f"{FEATURE}/done/F0001-A0001-acceptance.md": None}, False, id="no-acceptance"
        ),
        pytest.param(
            {
                f"{FEATURE}/done/F0001-A0001-acceptance.md": None,
                f"{FEATURE}/in-progress/F0001-A0001-acceptance.md": ACCEPTANCE,
            },
            False,
            id="acceptance-in-progress",
        ),
        pytest.param(
            {f"{FEATURE}/in-progress/F0001-A0002-acceptance.md": ACCEPTANCE},
            False,
            id="last-acceptance-in-progress",
        ),
    ],
)
def test_archive_feature_moves_only_a_finished_feature_to_the_archive_on_develop(
    operator: Operator, change: dict[str, str | None], archived: bool
) -> None:
    files: dict[str, str | None] = {
        "README.md": "# Project\n",
        **finished_feature(FEATURE),
        f"{OTHER}/feature.md": "# Other feature\n",
        f"{OTHER}/backlog/F0002-S0001-first.md": FIRST,
        **change,
    }
    bare, _seed = make_bare_remote(
        operator.tmp_path / "hosting",
        {name: text for name, text in files.items() if text is not None},
    )
    clone(bare, operator.checkout)
    develop_before = head(bare, SCRIPTS_BRANCH)
    main_before = head(bare, DEFAULT_BRANCH)

    result = operator.run("archive-feature.sh", "F0001")

    assert head(bare, DEFAULT_BRANCH) == main_before
    if not archived:
        assert result.exit_status != 0, result.stdout
        assert head(bare, SCRIPTS_BRANCH) == develop_before
        return
    assert result.exit_status == 0, result.stderr
    pushed = run_git(bare, "log", "-1", f"--format={LOG_FORMAT}", SCRIPTS_BRANCH)
    assert pushed.splitlines() == ["F0001: archived", KUMPEL, KUMPEL]
    files_after = tree(bare, SCRIPTS_BRANCH)
    assert sorted(name for name in files_after if name.startswith(f"{ARCHIVED}/")) == sorted(
        finished_feature(ARCHIVED)
    )
    assert [name for name in files_after if name.startswith(f"{FEATURE}/")] == []
    assert f"{OTHER}/backlog/F0002-S0001-first.md" in files_after


def write_switches(operator: Operator, promote: bool) -> None:
    """A settings file with the four switches, `promote` as given."""
    operator.settings_file.parent.mkdir(parents=True)
    switches = {"merge": False, "answer": True, "start_next": True, "promote": promote}
    operator.settings_file.write_text(json.dumps({"switches": switches}), encoding="utf-8")


def requests_that_change(operator: Operator) -> list[Request]:
    """The recorded requests other than reads, in order."""
    return [request for request in recorded_requests(operator.records) if request.method != "GET"]


@pytest.mark.parametrize(
    ("folder", "promote", "merged"),
    [
        pytest.param(FEATURE, True, None, id="not-archived"),
        pytest.param(ARCHIVED, False, False, id="archived-switch-off"),
        pytest.param(ARCHIVED, True, True, id="archived-switch-on"),
    ],
)
def test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on(
    operator: Operator, folder: str, promote: bool, merged: bool | None
) -> None:
    files = {"README.md": "# Project\n", **finished_feature(folder)}
    bare, _seed = make_bare_remote(operator.tmp_path / "hosting", files)
    clone(bare, operator.checkout)
    write_switches(operator, promote)
    operator.answer(
        {
            f"{PREFIX}/pulls": {"number": PULL_NUMBER, "state": "open"},
            f"{PREFIX}/pulls/{PULL_NUMBER}/merge": {"merged": True, "sha": "f" * 40},
        }
    )

    result = operator.run("promote.sh", "F0001")

    changes = requests_that_change(operator)
    if merged is None:
        assert result.exit_status != 0, result.stdout
        assert changes == []
        return
    assert result.exit_status == 0, result.stderr
    opened = [request for request in changes if request.method == "POST"]
    assert [request.route for request in opened] == ["/pulls"]
    body = opened[0].body
    assert isinstance(body, dict)
    assert (body["head"], body["base"], body["title"]) == (
        "develop",
        "main",
        "F0001: promoted to main",
    )
    for text in ("F0001-S0001", "First story", "F0001-S0002", "Second story"):
        assert text in body["body"], body["body"]
    merges = [request for request in changes if request.method == "PUT"]
    if not merged:
        assert merges == []
        assert str(PULL_NUMBER) in result.stdout
        return
    assert [request.route for request in merges] == [f"/pulls/{PULL_NUMBER}/merge"]
    merge = merges[0].body
    assert isinstance(merge, dict)
    assert merge["merge_method"] == "merge"
    assert merge["commit_message"] == "Promoted by Kumpel after F0001's acceptance."


STORY = "# Second story\n\n## Smoke test\n\nExpect: `0`.\n\n## Journal\n\n1. human: created.\n"
BASE_FILES = {
    "README.md": "# Project\n",
    f"{FEATURE}/feature.md": FEATURE_TEXT,
    f"{FEATURE}/backlog/F0001-S0001-first.md": FIRST,
    f"{FEATURE}/backlog/F0001-S0002-second.md": STORY,
}
DEVELOP_ARCHIVE = "work item F0001-S0001: merged, archived"
MAIN_ARCHIVE = "work item F0001-S0000: merged, archived"


@pytest.fixture
def diverged(operator: Operator) -> Path:
    """A remote whose `develop` is one commit ahead of `main`, a work item branch from `develop`.

    On `develop` the first story is done and a test was added; the branch starts the second story
    and adds another test. The checkout is a fresh clone, on `main`.
    """
    bare, seed = make_bare_remote(operator.tmp_path / "hosting", BASE_FILES)
    (seed / FEATURE / "done").mkdir()
    run_git(
        seed,
        "mv",
        f"{FEATURE}/backlog/F0001-S0001-first.md",
        f"{FEATURE}/done/F0001-S0001-first.md",
    )
    write_files(seed, {"tests/test_develop.py": "def test_develop() -> None:\n    pass\n"})
    commit_all(seed, "work item F0001-S0001: merged, archived")
    run_git(seed, "push", "-q", "origin", SCRIPTS_BRANCH)
    run_git(seed, "checkout", "-q", "-b", "work-item/F0001-S0002")
    (seed / FEATURE / "in-progress").mkdir()
    run_git(
        seed,
        "mv",
        f"{FEATURE}/backlog/F0001-S0002-second.md",
        f"{FEATURE}/in-progress/F0001-S0002-second.md",
    )
    write_files(seed, {"tests/test_new.py": "def test_new() -> None:\n    pass\n"})
    commit_all(seed, "F0001-S0002: work")
    run_git(seed, "push", "-q", "origin", "work-item/F0001-S0002")
    clone(bare, operator.checkout)
    operator.answer(
        {
            f"{PREFIX}/pulls/4/files?per_page=100": [{"filename": "tests/test_new.py"}],
            f"{PREFIX}/issues/4/comments": [],
            f"{PREFIX}/pulls?state=open&per_page=50": [],
            f"{PREFIX}/commits?sha=develop&per_page=20": [{"commit": {"message": DEVELOP_ARCHIVE}}],
            f"{PREFIX}/commits?per_page=20": [{"commit": {"message": MAIN_ARCHIVE}}],
        }
    )
    return bare


def lines_under(header: str) -> Callable[[str], list[str]]:
    """The lines of a run's output under the header that starts with `header`, to the next one."""

    def read(stdout: str) -> list[str]:
        lines = stdout.splitlines()
        start = next(index for index, line in enumerate(lines) if line.startswith(header))
        rest = lines[start + 1 :]
        end = next((index for index, line in enumerate(rest) if line.startswith("== ")), len(rest))
        return rest[:end]

    return read


def all_lines(stdout: str) -> list[str]:
    """Every line of a run's output."""
    return stdout.splitlines()


@pytest.mark.parametrize(
    ("script", "arguments", "read", "expected"),
    [
        pytest.param("next-story.sh", (), all_lines, ["next: F0001-S0002"], id="next-story"),
        pytest.param(
            "approval.sh",
            ("4", "F0001-S0002"),
            lines_under("== tests changed"),
            ["A\ttests/test_new.py"],
            id="approval",
        ),
        pytest.param("status.sh", (), all_lines, [f"last archive: {DEVELOP_ARCHIVE}"], id="status"),
    ],
)
@pytest.mark.usefixtures("diverged")
def test_next_story_approval_and_status_read_develop_not_main(
    operator: Operator,
    script: str,
    arguments: tuple[str, ...],
    read: Callable[[str], list[str]],
    expected: list[str],
) -> None:
    result = operator.run(script, *arguments)
    assert result.exit_status == 0, result.stderr
    assert read(result.stdout) == expected


@pytest.mark.parametrize(
    ("changes", "refusal", "value"),
    [
        pytest.param([], None, "off", id="new-file"),
        pytest.param([["on"]], None, "on", id="set-on"),
        pytest.param([["on"], ["off"]], None, "off", id="set-off-again"),
        pytest.param(
            [["yes"]], "settings.sh: yes is neither on nor off\n", "off", id="another-value"
        ),
    ],
)
def test_the_promote_switch_is_off_in_a_new_file_and_set_like_the_others(
    operator: Operator, changes: list[list[str]], refusal: str | None, value: str
) -> None:
    written = operator.run("settings.sh", "init", "owner/name", str(operator.checkout))
    assert written.exit_status == 0, written.stderr
    for words in changes:
        result = operator.run("settings.sh", "set", "promote", *words)
        if refusal is None:
            assert result.exit_status == 0, result.stderr
        else:
            assert (result.exit_status, result.stderr) == (2, refusal)
    answer = operator.run("settings.sh", "get", "promote")
    assert (answer.exit_status, answer.stdout) == (0, f"{value}\n"), answer.stderr


def test_a_settings_file_without_the_promote_switch_reads_it_as_off(operator: Operator) -> None:
    operator.settings_file.parent.mkdir(parents=True)
    switches = {"merge": False, "answer": True, "start_next": True}
    operator.settings_file.write_text(json.dumps({"switches": switches}), encoding="utf-8")
    answer = operator.run("settings.sh", "get", "promote")
    assert (answer.exit_status, answer.stdout) == (0, "off\n"), answer.stderr


@pytest.mark.parametrize(
    ("path", "phrase"),
    [
        pytest.param(ROOT / "operator/claude/commands/kumpel.md", "promote", id="claude-command"),
        pytest.param(
            ROOT / "operator/opencode/command/kumpel.md", "promote", id="opencode-command"
        ),
        pytest.param(
            SKILL / "references/standing-orders.md", "never push to main", id="never-push-to-main"
        ),
        pytest.param(
            SKILL / "references/standing-orders.md", "a fix goes to develop", id="fix-on-develop"
        ),
    ],
)
def test_the_texts_name_the_promote_switch_and_keep_kumpel_off_main(
    path: Path, phrase: str
) -> None:
    text = " ".join(path.read_text(encoding="utf-8").replace("`", "").lower().split())
    assert phrase in text
