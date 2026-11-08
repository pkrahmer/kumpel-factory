"""A stage's `context` names project commands, counts toward its lease and loads at 1.0 and 1.1."""

import pytest

from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from support.git_support import PIPELINE_YAML, pipeline_outcome

TESTS_STAGE = "tests: {role: tester, next: [doing], checks: [lint], reports: [test]}"


def _with_context(*, context: str = "facts", minutes: int = 1, contract: str = "1.0") -> str:
    """`PIPELINE_YAML` with the project command `facts` and the tests stage's `context`."""
    text = PIPELINE_YAML.replace('contract: "1.0"', f'contract: "{contract}"')
    text = text.replace(
        "  test: {time_limit: 10}\n",
        f"  test: {{time_limit: 10}}\n  facts: {{time_limit: {minutes}}}\n",
    )
    stage = TESTS_STAGE.removesuffix("}") + f", context: [{context}]}}"
    assert TESTS_STAGE in text
    return text.replace(TESTS_STAGE, stage)


@pytest.mark.parametrize(
    ("context", "fault"),
    [("facts", None), ("nowhere", "nowhere")],
    ids=["project-command", "unknown"],
)
def test_a_context_name_must_be_a_project_command(context: str, fault: str | None) -> None:
    outcome = pipeline_outcome(_with_context(context=context))

    if fault is None:
        assert outcome is None
    else:
        assert outcome is not None
        assert fault in outcome


# The tester's 40 minutes, lint's 5 and test's 10 leave 5 of the lease's 60 for `facts`.
@pytest.mark.parametrize(("minutes", "fits"), [(5, True), (6, False)], ids=["fits", "exceeds"])
def test_the_context_time_limits_count_toward_the_lease(minutes: int, *, fits: bool) -> None:
    outcome = pipeline_outcome(_with_context(minutes=minutes))

    if fits:
        assert outcome is None
    else:
        assert outcome is not None
        assert "lease_duration" in outcome


@pytest.mark.parametrize("contract", ["1.0", "1.1"])
def test_a_definition_at_either_contract_loads_with_a_stage_carrying_context(
    contract: str,
) -> None:
    definition = RuamelPipelineDefinitionReader().parse(_with_context(contract=contract))

    assert definition.contract == contract
    assert definition.stages["tests"].context == ["facts"]
