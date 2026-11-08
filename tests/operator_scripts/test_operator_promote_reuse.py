"""`promote.sh` reuses a promotion still open instead of opening a second one."""

import re
from urllib.parse import parse_qs, urlsplit

import pytest

from support.archive_feature_support import (
    ACCEPTANCE,
    ARCHIVED,
    DONE_FRONT_MATTER,
    FEATURE_TEXT,
    FIRST,
    SECOND,
    finished_feature,
)
from support.git_support import clone
from support.operator_skill_support import (
    OLD_SWITCHES,
    OPEN_PROMOTION,
    PREFIX,
    PULL_NUMBER,
    Operator,
    make_bare_remote,
    recorded_requests,
    requests_that_change,
    write_switches,
)

SECOND_ARCHIVED = "factory/archive/F0002-other"
FIRST_BLOCK = "The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story"
SECOND_BLOCK = "The stories of F0002:\n\n- F0002-S0001: First story\n- F0002-S0002: Second story"
OPEN_TITLE = "F0001: promoted to main"


def second_feature() -> dict[str, str]:
    """F0002, archived, with two done stories and its accepted acceptance."""
    return {
        f"{SECOND_ARCHIVED}/feature.md": FEATURE_TEXT,
        f"{SECOND_ARCHIVED}/done/F0002-S0001-first.md": DONE_FRONT_MATTER + FIRST,
        f"{SECOND_ARCHIVED}/done/F0002-S0002-second.md": DONE_FRONT_MATTER + SECOND,
        f"{SECOND_ARCHIVED}/done/F0002-A0001-acceptance.md": ACCEPTANCE,
    }


@pytest.fixture
def archived(operator: Operator) -> Operator:
    """The operator's checkout of a remote on whose `develop` F0001 and F0002 are archived."""
    files = {"README.md": "# Project\n", **finished_feature(ARCHIVED), **second_feature()}
    bare, _seed = make_bare_remote(operator.tmp_path / "hosting", files)
    clone(bare, operator.checkout)
    return operator


def open_promotion(body: str) -> dict[str, object]:
    """The open promotion #4711 as the list of open pull requests shows it."""
    return {
        "number": PULL_NUMBER,
        "state": "open",
        "title": OPEN_TITLE,
        "body": body,
        "head": {"ref": "develop"},
        "base": {"ref": "main"},
    }


def answer_promotion(operator: Operator, open_pulls: list[dict[str, object]]) -> None:
    """Answer the query for the open promotion with `open_pulls`, and every change it may send."""
    operator.answer(
        {
            OPEN_PROMOTION: open_pulls,
            f"{PREFIX}/pulls": {"number": PULL_NUMBER, "state": "open"},
            f"{PREFIX}/pulls/{PULL_NUMBER}": {"number": PULL_NUMBER, "state": "open"},
            f"{PREFIX}/pulls/{PULL_NUMBER}/merge": {"merged": True, "sha": "f" * 40},
        }
    )


def test_promote_without_an_open_promotion_asks_for_it_and_opens_one(
    archived: Operator,
) -> None:
    write_switches(archived, {**OLD_SWITCHES, "promote": False})
    answer_promotion(archived, [])

    result = archived.run("promote.sh", "F0001")

    assert result.exit_status == 0, result.stderr
    reads = [
        urlsplit(request.route)
        for request in recorded_requests(archived.records)
        if request.method == "GET" and urlsplit(request.route).path == "/pulls"
    ]
    assert [parse_qs(read.query) for read in reads] == [
        {
            "state": ["open"],
            "base": ["main"],
            "head": ["owner:develop"],
            "per_page": ["1"],
        }
    ]
    changes = requests_that_change(archived)
    assert [(request.method, request.route) for request in changes] == [("POST", "/pulls")]
    body = changes[0].body
    assert isinstance(body, dict)
    assert body == {"head": "develop", "base": "main", "title": OPEN_TITLE, "body": FIRST_BLOCK}
    assert "promotion opened: #4711, for the human to merge" in result.stdout


@pytest.mark.parametrize(
    "promote",
    [pytest.param(False, id="switch-off"), pytest.param(True, id="switch-on")],
)
def test_promote_adds_the_next_feature_to_the_open_promotion(
    archived: Operator, promote: bool
) -> None:
    write_switches(archived, {**OLD_SWITCHES, "promote": promote})
    answer_promotion(archived, [open_promotion(FIRST_BLOCK)])

    result = archived.run("promote.sh", "F0002")

    assert result.exit_status == 0, result.stderr
    changes = requests_that_change(archived)
    assert [request.method for request in changes if request.method == "POST"] == []
    patches = [request for request in changes if request.method == "PATCH"]
    assert [request.route for request in patches] == [f"/pulls/{PULL_NUMBER}"]
    patch = patches[0].body
    assert isinstance(patch, dict)
    assert patch["body"] == FIRST_BLOCK + "\n\n" + SECOND_BLOCK
    assert "title" not in patch
    merges = [request for request in changes if request.method == "PUT"]
    if not promote:
        assert merges == []
        assert "promotion open: #4711, for the human to merge" in result.stdout
        return
    assert [request.route for request in merges] == [f"/pulls/{PULL_NUMBER}/merge"]
    merge = merges[0].body
    assert isinstance(merge, dict)
    assert merge["merge_method"] == "merge"
    assert merge["commit_message"] == "Promoted by Kumpel after F0002's acceptance."


def test_promote_again_for_a_feature_already_in_the_open_promotion_changes_nothing(
    archived: Operator,
) -> None:
    write_switches(archived, {**OLD_SWITCHES, "promote": False})
    answer_promotion(archived, [open_promotion(FIRST_BLOCK)])

    result = archived.run("promote.sh", "F0001")

    assert result.exit_status == 0, result.stderr
    changes = requests_that_change(archived)
    assert [request.method for request in changes if request.method in ("POST", "PATCH")] == []
    assert "promotion open: #4711, for the human to merge" in result.stdout


def test_promote_stops_when_the_query_for_the_open_promotion_fails(
    archived: Operator,
) -> None:
    write_switches(archived, {**OLD_SWITCHES, "promote": True})
    answer_promotion(archived, [])
    archived.fail(OPEN_PROMOTION, "500", "Server Error")

    result = archived.run("promote.sh", "F0001")

    assert result.exit_status == 22, result.stdout
    assert re.search(r"hosting: GET \S+: 500 ", result.stderr), result.stderr
    assert requests_that_change(archived) == []
