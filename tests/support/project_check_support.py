"""A committed repository that is ready for the factory, and the agent home its roles need."""

from pathlib import Path

from support.git_support import (
    PIPELINE_YAML,
    STORY_FORM,
    commit_all,
    install_agents,
    run_git,
    write_files,
)

ROLES = (
    "intake",
    "tester",
    "coder",
    "reviewer",
    "documenter",
    "smoke-tester",
    "acceptance-reviewer",
)
READY_MAKEFILE = "check:\n\t@:\nlint:\n\t@:\ntest:\n\t@:\nsync:\n\t@:\n"
READY_FILES: dict[str, str] = {
    "factory/pipeline.yml": PIPELINE_YAML,
    "factory/story-form.md": STORY_FORM,
    "factory/feature-form.md": "# Feature title\n",
    "Makefile": READY_MAKEFILE,
    "src/a.py": "",
    "tests/t.py": "",
    "docs/d.md": "# D\n",
    "README.md": "# R\n",
}


def ready_files(changes: dict[str, str | None] | None = None) -> dict[str, str]:
    """The files of a ready repository, each of `changes` written over it, `None` left out."""
    files: dict[str, str | None] = {**READY_FILES, **(changes or {})}
    return {path: text for path, text in files.items() if text is not None}


def committed_repository(directory: Path, files: dict[str, str]) -> Path:
    """A new git repository in `directory` whose one commit holds `files`."""
    directory.mkdir(parents=True)
    run_git(directory, "init", "-q")
    write_files(directory, files)
    commit_all(directory, "one")
    return directory


def installed_home(agent_home: Path, roles: tuple[str, ...] = ROLES) -> Path:
    """`agent_home` with a valid installed agent for each of `roles`."""
    agent_home.mkdir(parents=True, exist_ok=True)
    install_agents(agent_home, roles)
    return agent_home
