"""The shipped agent files, the shared settings, the kit and the Python pack, as files."""

import json

import pytest

from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
from factory.work.adapters.work_item_markdown import RuamelYamlHandler
from support.kit_support import pack_claude_md
from support.shipped_agents import (
    AGENT_HOME,
    ROOT,
    SHIPPED_AGENTS,
    SHIPPED_NAMES,
    ShippedAgent,
    front_matter_and_body,
    full_line_names,
)

KIT = ROOT / "operator" / "kit"
PYTHON_PACK = ROOT / "operator" / "packs" / "python"

SETTINGS = {
    "permissions": {
        "allow": [
            "Read",
            "Edit",
            "Write",
            "Glob",
            "Grep",
            "Skill",
            "Bash(uv run *)",
            "Bash(uv sync*)",
            "Bash(make *)",
            "Bash(factory-check-story *)",
            "Bash(git status*)",
            "Bash(git diff*)",
            "Bash(git log*)",
            "Bash(git show*)",
            "Bash(git rev-parse*)",
        ],
        "deny": [
            "Bash(git push*)",
            "Bash(git checkout*)",
            "Bash(git switch*)",
            "Bash(git merge*)",
            "Bash(git pull*)",
            "Bash(git rebase*)",
            "Bash(git reset*)",
            "Bash(git branch -D*)",
            "Bash(git add*)",
            "Bash(git commit*)",
            "Bash(gh *)",
            "Bash(rm -rf *)",
        ],
    },
    "env": {"CLAUDE_CODE_FORK_SUBAGENT": "0"},
}

TEMPLATE_RULES_LINES = [
    "# <project>",
    "",
    "<One sentence: what this repository is.> Built by kumpel-factory "
    "(github.com/pkrahmer/kumpel-factory); the pipeline's rules reach every agent in its "
    "instructions, so this file holds only what is true of this project.",
    "",
    "## Language",
    "- Everything in this repository is English: code, comments, docs, work items, commit "
    "messages.",
    "",
    "## Architecture",
    "- <Layers, dependency direction, what is pure, where wiring happens.>",
    "- <Typing and validation rules.>",
    "",
    "## Tests",
    "- pytest. Tests live under `tests/` and mirror the package. Plain test functions, shared "
    "fixtures in `tests/conftest.py`, parametrize for tables of cases. Never mock the code "
    "under test.",
    "- No network, no sleeps, no files outside `tmp_path`.",
    "- Tests pass `mypy --strict` once the code exists: never use the value of a call to a "
    "function typed `-> None`; call it as a statement.",
    '- Fake commit ids and other hexadecimal test values are low-entropy (`"a" * 40`), so that '
    "`make secrets` stays green without a baseline entry.",
    "",
    "## Docs",
    "- `README.md` is for the newcomer: what it is, how to run it, where to look next. "
    "`docs/decisions.md` is the decision log.",
    "- <Which comments and doc comments the code carries.> Comments say why, never what.",
    "",
    "## Checks",
    "- `make check` must be green before any stage reports done. It runs `make lint` (ruff "
    "check and format check), `make types` (`mypy --strict`), `make layers` (<the layers "
    "command>), `make sast` (semgrep with the rules in `security/semgrep`, and bandit), `make "
    "secrets` (detect-secrets with the reviewed findings of its baseline file), `make licenses`"
    " (pip-licenses against an allow list) and `make test` (pytest on every core, with "
    "coverage). Each target ends with the line `<target>: green (<seconds> s)`; `make check` "
    "ends with `check: green`.",
    "- Run Python through `uv run`. All dependencies, runtime and development, are declared and"
    " pinned in `pyproject.toml`; the lockfile is `uv.lock`.",
    "- Run `make check` and every other make target in the foreground and read its output.",
    "",
    "## Review",
    "- Everything is typed; `Any` only at a boundary that validates immediately.",
    "- No `dict[str, Any]` crosses a function boundary: inputs and outputs are models shaped by"
    " what the code needs.",
    "- A marker that silences a check (`noqa`, `type: ignore`, `nosec`, `nosemgrep`, a baseline"
    " entry) is a finding unless this file allows it.",
    "",
    "## Not without asking (end the stage with `question`)",
    "- New dependency, new top-level package, change to `pyproject.toml`, the makefile or "
    "`factory/`, change to a test another story wrote, a new entry in `.secrets.baseline`, a "
    "`nosemgrep` or `nosec` marker, a licence outside the allow list.",
]


def _reader() -> FrontmatterAgentDefinitionReader:
    return FrontmatterAgentDefinitionReader(AGENT_HOME)


def test_agents_directory_holds_exactly_the_seven_agent_files() -> None:
    entries = sorted(path.name for path in (AGENT_HOME / "agents").iterdir())

    assert entries == sorted(f"{name}.md" for name in SHIPPED_NAMES)


def test_every_shipped_agent_is_read_and_listed_sorted() -> None:
    reader = _reader()

    assert reader.names() == sorted(SHIPPED_NAMES)
    for name in SHIPPED_NAMES:
        assert reader.read(name).name == name


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_front_matter_holds_the_four_applied_keys_with_their_values(agent: ShippedAgent) -> None:
    front_matter, _ = front_matter_and_body(agent.name)
    values = RuamelYamlHandler().load(front_matter)
    definition = _reader().read(agent.name)

    assert sorted(values) == ["budget_usd", "effort", "model", "tools"]
    assert definition.model == agent.model
    assert definition.effort == agent.effort
    assert definition.budget_usd == agent.budget_usd
    assert definition.tools == agent.tools


@pytest.mark.parametrize("agent", SHIPPED_AGENTS, ids=SHIPPED_NAMES)
def test_body_starts_with_the_boundary_and_the_entry_sentence(agent: ShippedAgent) -> None:
    _, body = front_matter_and_body(agent.name)

    assert body.startswith(f"{agent.boundary}\n\n{agent.entry}")


def test_settings_are_the_shared_permissions_and_environment() -> None:
    settings = json.loads((AGENT_HOME / "settings.json").read_text(encoding="utf-8"))

    assert settings == SETTINGS


def test_template_pipeline_definition_is_valid_with_the_shipped_roles() -> None:
    text = (KIT / "factory" / "pipeline.full.yml").read_text(encoding="utf-8")

    definition = RuamelPipelineDefinitionReader().parse(text)

    assert sorted(definition.roles) == sorted(full_line_names())


def test_template_holds_only_the_rules_file_the_makefile_and_the_pipeline_definition() -> None:
    kit = sorted(path.relative_to(KIT).as_posix() for path in KIT.rglob("*"))
    pack = sorted(path.relative_to(PYTHON_PACK).as_posix() for path in PYTHON_PACK.rglob("*"))

    assert kit == [
        "CLAUDE.md",
        "README.md",
        "factory",
        "factory/README.md",
        "factory/feature-form.md",
        "factory/kit.mk",
        "factory/pipeline.full.yml",
        "factory/pipeline.thin.yml",
        "factory/story-form.md",
    ]
    assert pack == ["CLAUDE.sections.md", "Makefile", "TRAPS.md"]
    assert (KIT / "CLAUDE.md").is_file()
    assert (PYTHON_PACK / "Makefile").is_file()
    assert (KIT / "factory").is_dir()
    assert (KIT / "factory" / "pipeline.full.yml").is_file()


def test_template_rules_file_is_the_python_project_text() -> None:
    text = pack_claude_md("python")

    assert text == "\n".join(TEMPLATE_RULES_LINES) + "\n"
