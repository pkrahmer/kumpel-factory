"""The preflight names the working branch a remote lacks."""

from dataclasses import replace
from pathlib import Path

from factory.hosting.adapters.git_cli import GitCli
from factory.hosting.domain.git import GitOptions
from factory.machine.application.preflight import agent_run_probe_item
from factory.pipeline.application.boundaries import Boundaries
from support.container_support import container_instance_settings
from support.git_support import TEST_IDENTITY, clone, commit_all, run_git, write_files
from support.probe_support import ENVIRONMENT

OTHER_BRANCH = "main"


def test_a_remote_with_main_but_no_develop_gets_a_finding_naming_origin_develop(
    boundaries: Boundaries, tmp_path: Path, agent_home: Path
) -> None:
    run_git(tmp_path, "init", "-q", f"--initial-branch={OTHER_BRANCH}", "seed")
    seed = tmp_path / "seed"
    write_files(seed, {"README.md": "# Seed\n"})
    commit_all(seed, "seed")
    run_git(tmp_path, "init", "-q", "--bare", f"--initial-branch={OTHER_BRANCH}", "only-main.git")
    remote = tmp_path / "only-main.git"
    run_git(seed, "push", "-q", str(remote), OTHER_BRANCH)
    directory = clone(remote, tmp_path / "only-main-checkout")
    git = GitCli(directory, GitOptions(identity=TEST_IDENTITY))
    settings = container_instance_settings(tmp_path, agent_home)

    item = agent_run_probe_item(
        replace(boundaries, git=git, checkout=directory), settings, ENVIRONMENT
    )

    assert not item.passed
    assert item.detail == "no origin/develop to prepare the stage environment from"
