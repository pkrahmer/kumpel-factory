"""Today's install guide names the settings the code reads."""

import pytest

from factory.shared.domain.documents import (
    OPERATOR_INSTALL,
    SETTINGS_SECTION,
    guide_tables,
    settings_findings,
)
from factory.shared.domain.settings import SETTINGS
from support.operator_support import ROOT

pytestmark = pytest.mark.documents


def test_todays_install_guide_gives_no_settings_finding() -> None:
    text = (ROOT / OPERATOR_INSTALL).read_text(encoding="utf-8")

    findings = settings_findings(guide_tables(text, SETTINGS_SECTION), SETTINGS)

    assert findings == []
