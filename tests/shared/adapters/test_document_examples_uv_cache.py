"""The uv cache the examples share: how it is found and what the commands see of it."""

from collections.abc import Mapping
from pathlib import Path

import pytest

from factory.shared.adapters.document_examples import ProcessExampleRunner, uv_cache_directory
from factory.shared.application.document_examples import Fixture
from factory.shared.domain.documents import examples
from support.document_examples_support import EmptyFixture, LiftingFixture, block, document
from support.time_limits import ROOMY_LIMIT

DOCUMENT = "docs/project-guide/shared.md"
FIXTURE_CACHE = "/from/the/fixture"


def _findings(runner: ProcessExampleRunner, text: str, fixture: Fixture) -> list[str]:
    return runner.run_document(DOCUMENT, examples(text).runnable, {"checkout": fixture})


@pytest.mark.parametrize(
    ("environment", "expected"),
    [
        pytest.param(
            {"UV_CACHE_DIR": "/c", "XDG_CACHE_HOME": "/x", "HOME": "/h"},
            Path("/c"),
            id="uv-cache-dir",
        ),
        pytest.param({"XDG_CACHE_HOME": "/x", "HOME": "/h"}, Path("/x/uv"), id="xdg-and-home"),
        pytest.param({"HOME": "/h"}, Path("/h/.cache/uv"), id="home-only"),
        pytest.param({}, None, id="none"),
        pytest.param(
            {"UV_CACHE_DIR": "", "XDG_CACHE_HOME": "/x", "HOME": "/h"},
            Path("/x/uv"),
            id="empty-uv-cache-dir",
        ),
        pytest.param(
            {"XDG_CACHE_HOME": "", "HOME": "/h"}, Path("/h/.cache/uv"), id="empty-xdg-cache-home"
        ),
        pytest.param({"HOME": ""}, None, id="empty-home"),
        pytest.param({"UV_CACHE_DIR": "", "XDG_CACHE_HOME": "", "HOME": ""}, None, id="all-empty"),
    ],
)
def test_the_uv_cache_is_found_in_the_order_of_its_variables(
    environment: Mapping[str, str], expected: Path | None
) -> None:
    assert uv_cache_directory(environment) == expected


@pytest.mark.parametrize(
    ("uv_cache", "printed"),
    [
        pytest.param(Path("/shared/uv-cache"), "[/shared/uv-cache]", id="with-cache"),
        pytest.param(None, "[]", id="without-cache"),
    ],
)
def test_a_command_sees_the_runners_uv_cache_or_none(
    monkeypatch: pytest.MonkeyPatch, uv_cache: Path | None, printed: str
) -> None:
    # The caller's own value must not reach the command.
    monkeypatch.setenv("UV_CACHE_DIR", "/the/callers/cache")
    runner = ProcessExampleRunner(time_limit=ROOMY_LIMIT, uv_cache=uv_cache)
    text = document(block('$ echo "[$UV_CACHE_DIR]"', printed))

    assert _findings(runner, text, EmptyFixture()) == []


def test_a_fixtures_uv_cache_does_not_replace_the_runners() -> None:
    runner = ProcessExampleRunner(time_limit=ROOMY_LIMIT, uv_cache=Path("/shared/uv-cache"))
    text = document(block('$ echo "$UV_CACHE_DIR"', "/shared/uv-cache"))

    assert _findings(runner, text, LiftingFixture("UV_CACHE_DIR", FIXTURE_CACHE)) == []


def test_with_a_uv_cache_home_stays_the_documents_own_folder(tmp_path: Path) -> None:
    callers_home = tmp_path / "callers-home"
    cache = callers_home / ".cache" / "uv"
    cache.mkdir(parents=True)
    runner = ProcessExampleRunner(time_limit=ROOMY_LIMIT, uv_cache=cache)
    text = document(
        block(
            f'$ test "$HOME" = "{callers_home}" && echo shared || echo own',
            "own",
            '$ test -d "$HOME" && echo there',
            "there",
            '$ ls -A "$HOME" | wc -l',
            "0",
        )
    )

    assert _findings(runner, text, EmptyFixture()) == []


class _NoVariableFixture(Fixture):
    """A fixture that gives the command no variable of its own."""

    def prepare(self, folder: Path) -> dict[str, str]:
        """Check the folder is there and give nothing."""
        assert folder.is_dir()
        return {}


@pytest.mark.parametrize(
    ("uv_cache", "printed"),
    [
        pytest.param(Path("/shared/uv-cache"), "[copy]", id="with-cache"),
        pytest.param(None, "[]", id="without-cache"),
    ],
)
def test_a_command_copies_from_the_uv_cache_only_when_the_runner_has_one(
    monkeypatch: pytest.MonkeyPatch, uv_cache: Path | None, printed: str
) -> None:
    # The caller's own value must not reach the command.
    monkeypatch.setenv("UV_LINK_MODE", "clone")
    runner = ProcessExampleRunner(time_limit=ROOMY_LIMIT, uv_cache=uv_cache)
    text = document(block('$ echo "[$UV_LINK_MODE]"', printed))

    assert _findings(runner, text, _NoVariableFixture()) == []


@pytest.mark.parametrize(
    ("uv_cache", "printed"),
    [
        pytest.param(Path("/shared/uv-cache"), "[copy]", id="with-cache"),
        pytest.param(None, "[hardlink]", id="without-cache"),
    ],
)
def test_a_fixtures_link_mode_reaches_the_command_only_without_a_uv_cache(
    uv_cache: Path | None, printed: str
) -> None:
    runner = ProcessExampleRunner(time_limit=ROOMY_LIMIT, uv_cache=uv_cache)
    text = document(block('$ echo "[$UV_LINK_MODE]"', printed))

    assert _findings(runner, text, LiftingFixture("UV_LINK_MODE", "hardlink")) == []
