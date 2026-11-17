"""The pipeline definition's `make_file`: the makefile the factory runs, inside the checkout."""

import pytest

from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from support.git_support import PIPELINE_YAML, pipeline_outcome


def _with_make_file(value: str | None, *, contract: str = "1.0") -> str:
    """`PIPELINE_YAML` at `contract`, with the line `make_file: <value>` unless `value` is None."""
    text = PIPELINE_YAML.replace('contract: "1.0"', f'contract: "{contract}"')
    return text if value is None else f"make_file: {value}\n{text}"


@pytest.mark.parametrize(
    ("value", "contract", "expected"),
    [
        ("factory/Makefile", "1.0", "factory/Makefile"),
        ("factory/Makefile", "1.1", "factory/Makefile"),
        ("factory/Makefile", "1.2", "factory/Makefile"),
        (None, "1.2", None),
    ],
    ids=["contract-1.0", "contract-1.1", "contract-1.2", "without-the-key"],
)
def test_the_definition_holds_its_make_file(
    value: str | None, contract: str, expected: str | None
) -> None:
    definition = RuamelPipelineDefinitionReader().parse(_with_make_file(value, contract=contract))

    assert definition.make_file == expected


@pytest.mark.parametrize(
    ("value", "accepted"),
    [
        ('""', False),
        ('"-f"', False),
        ("/etc/Makefile", False),
        ("../Makefile", False),
        ("a/../b", False),
        ('"my file"', False),
        ('"a;b"', False),
        ("42", False),
        ("Makefile", True),
        ("factory/Makefile", True),
        ("build/factory.mk", True),
    ],
    ids=[
        "empty",
        "option",
        "absolute",
        "parent",
        "parent-inside",
        "space",
        "semicolon",
        "number",
        "root-makefile",
        "factory-makefile",
        "mk-file",
    ],
)
def test_a_make_file_outside_its_characters_or_the_checkout_is_refused(
    value: str, *, accepted: bool
) -> None:
    outcome = pipeline_outcome(_with_make_file(value))

    if accepted:
        assert outcome is None
    else:
        assert outcome is not None
        assert "make_file" in outcome


@pytest.mark.parametrize(
    ("value", "fault"),
    [
        ("./factory/Makefile", "make_file ./factory/Makefile must be written as factory/Makefile"),
        ("factory//Makefile", "make_file factory//Makefile must be written as factory/Makefile"),
        ("factory/./Makefile", "make_file factory/./Makefile must be written as factory/Makefile"),
        ("factory/Makefile/", "make_file factory/Makefile/ must be written as factory/Makefile"),
        ("../Makefile", "make_file ../Makefile must be a path inside the checkout"),
        ("Makefile", None),
        ("factory/Makefile", None),
        ("build/factory.mk", None),
    ],
    ids=[
        "dot-slash",
        "double-slash",
        "dot-inside",
        "trailing-slash",
        "outside-the-checkout",
        "root-makefile",
        "factory-makefile",
        "mk-file",
    ],
)
def test_a_make_file_not_in_its_plain_form_is_refused_with_its_plain_spelling(
    value: str, fault: str | None
) -> None:
    assert pipeline_outcome(_with_make_file(value)) == fault
