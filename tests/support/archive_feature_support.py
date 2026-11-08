"""A feature on `develop` for the tests of `archive-feature.sh`: its files and the remote's tree."""

from pathlib import Path

from support.git_support import run_git

FEATURE_FOLDER = "F0001-example"
FEATURE = f"factory/features/{FEATURE_FOLDER}"
ARCHIVED = f"factory/archive/{FEATURE_FOLDER}"
OTHER = "factory/features/F0002-other"
FEATURE_TEXT = "# Example feature\n\n## Stories\n\n- S0001: first\n- S0002: second\n"
FIRST = "# First story\n\n## Journal\n\n1. human: created.\n"
SECOND = "# Second story\n\n## Journal\n\n1. human: created.\n"
THIRD = "# Third story\n\n## Journal\n\n1. human: created.\n"
DONE_FRONT_MATTER = "---\nstage: done\n---\n"
ACCEPTANCE_BODY = "# Acceptance of F0001\n\n## Journal\n\n1. factory: created.\n"
# A booked acceptance: the factory writes its outcome into the front matter.
ACCEPTANCE = "---\nstage: done\noutcome: accepted\n---\n" + ACCEPTANCE_BODY
LOG_FORMAT = "%s%n%an <%ae>%n%cn <%ce>"


def finished_feature(folder: str) -> dict[str, str]:
    """A feature in `folder` whose two stories and whose accepted acceptance are done."""
    return {
        f"{folder}/feature.md": FEATURE_TEXT,
        f"{folder}/done/F0001-S0001-first.md": DONE_FRONT_MATTER + FIRST,
        f"{folder}/done/F0001-S0002-second.md": DONE_FRONT_MATTER + SECOND,
        f"{folder}/done/F0001-A0001-acceptance.md": ACCEPTANCE,
    }


def tree(remote: Path, branch: str) -> list[str]:
    """The files `branch` of `remote` holds."""
    return run_git(remote, "ls-tree", "-r", "--name-only", branch).splitlines()
