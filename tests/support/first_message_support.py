"""One run's facts with a work item body and a role, shared by the tests of the first message."""

from factory.agents.domain.prompts import PromptFacts, allowed_decisions

CODER_BODY = "# Demo\n\n## Journal\n\n1. 2026-11-08 human: created.\n"
CODER_INSTRUCTIONS = "Write the code."
CODER_FACTS = PromptFacts(
    work_item="F0001-S0003",
    path="factory/features/F0001-demo/in-progress/F0001-S0003-demo.md",
    stage="doing",
    allowed_decisions=allowed_decisions(["doing"]),
    branch="work-item/F0001-S0003",
    pull_request=7,
    round=0,
    body=CODER_BODY,
    role="coder",
    role_instructions=CODER_INSTRUCTIONS,
)
