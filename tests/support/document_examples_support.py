"""Fixtures and document builders for the tests of the process runner of a document's examples."""

from pathlib import Path

from factory.shared.application.document_examples import Fixture
from support.document_texts import FENCE

FIXTURE_VARIABLE = "EXAMPLE_FIXTURE"
LIFTED_VALUE = "from-the-fixture"


class EmptyFixture(Fixture):
    """A fixture that leaves the folder it is given empty and gives one variable."""

    def __init__(self, variable: str = FIXTURE_VARIABLE) -> None:
        """Give `variable` the value `set`."""
        self._variable = variable

    def prepare(self, folder: Path) -> dict[str, str]:
        """Check the folder is there and give the one variable."""
        assert folder.is_dir()
        return {self._variable: "set"}


class LiftingFixture(Fixture):
    """A fixture that gives one of the fixed variables a value of its own."""

    def __init__(self, name: str, value: str = LIFTED_VALUE) -> None:
        """Give `name` the value `value`, `from-the-fixture` unless given."""
        self._name = name
        self._value = value

    def prepare(self, folder: Path) -> dict[str, str]:
        """Check the folder is there and give the one variable."""
        assert folder.is_dir()
        return {self._name: self._value}


def block(*lines: str, info: str = "console") -> list[str]:
    """One fenced block of `lines`, with the info string `info`, and a blank line after it."""
    return [f"{FENCE}{info}", *lines, FENCE, ""]


def document(*blocks: list[str]) -> str:
    """A guide with a heading and the given blocks."""
    return "\n".join(["# A guide", "", *(line for one in blocks for line in one)])
