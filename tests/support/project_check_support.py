"""A committed repository that is ready for the factory, and the agent home its roles need."""

from pathlib import Path

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from factory.agents.application.project_agents import ProjectAgentDefinitions
from factory.hosting.adapters.git_cli import GitCli
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.pipeline.application.project_check import ProjectCheck
from factory.pipeline.domain.project_check import ProjectPoint
from support.git_support import (
    PIPELINE_YAML,
    STORY_FORM,
    commit_all,
    install_agents,
    run_git,
    write_files,
)
from support.shipped_agents import AGENT_HOME

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


def run_project_check(repository: Path, agent_home: Path) -> list[ProjectPoint]:
    """The project check's points for the committed `repository`, agents from `agent_home`."""
    git = GitCli(repository)
    agents = ProjectAgentDefinitions(git, FrontmatterAgentDefinitionReader(agent_home), ref="HEAD")
    return ProjectCheck(git, RuamelPipelineDefinitionReader(), agents).run()


def project_faults(tmp_path: Path, files: dict[str, str]) -> dict[str, list[str]]:
    """Each project check point's faults for a repository committed under `tmp_path` with `files`,
    the shipped agents installed."""
    repository = committed_repository(tmp_path / "project", files)
    return {point.name: point.faults for point in run_project_check(repository, AGENT_HOME)}
