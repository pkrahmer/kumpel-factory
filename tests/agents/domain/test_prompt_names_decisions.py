"""The message of a run names each decision the run may end with."""

import pytest

from factory.agents.domain.prompts import PromptFacts, compose_prompt


@pytest.mark.parametrize(
    "decisions",
    [["question"], ["doing", "question"], ["review", "tests", "question"]],
)
def test_the_message_names_each_allowed_decision(decisions: list[str]) -> None:
    facts = PromptFacts(
        work_item="F0001-S0003",
        path="factory/features/F0001-demo/in-progress/F0001-S0003-demo.md",
        stage="doing",
        allowed_decisions=decisions,
        branch="work-item/F0001-S0003",
        pull_request=7,
        round=0,
    )

    message = compose_prompt(facts)

    assert all(decision in message for decision in decisions)
