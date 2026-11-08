"""The document check accepts the words of a promotion in a checked document."""

import pytest

from factory.shared.domain.documents import OPERATOR_INSTALL, DocumentFinding, check_documents
from support.document_texts import clean_texts, operator_install


@pytest.mark.parametrize(
    ("line", "findings"),
    [
        pytest.param("The switch promote merges the pull request.", [], id="promote"),
        pytest.param("The switch `promote` merges the pull request.", [], id="promote-quoted"),
        pytest.param("The feature is promoted to main.", [], id="promoted"),
        pytest.param(
            "A ticket is read.",
            [DocumentFinding(document=OPERATOR_INSTALL, message="uses the v1 word 'ticket'")],
            id="ticket-still-forbidden",
        ),
    ],
)
def test_the_words_of_a_promotion_are_no_v1_words(
    line: str, findings: list[DocumentFinding]
) -> None:
    texts = clean_texts()
    texts[OPERATOR_INSTALL] = operator_install(suffix=line)

    assert check_documents(texts) == findings
