"""The agent definitions are read from one place only: the agent home of the settings."""

import ast

from support.source_search import called_name, modules

READER = "FrontmatterAgentDefinitionReader"


def test_the_agent_definition_reader_is_built_once_from_the_settings_agent_home() -> None:
    found = [
        (module, [ast.unparse(argument) for argument in node.args])
        for module, tree in modules().items()
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and called_name(node) == READER
    ]

    assert found == [("factory.entry.wiring", ["agent_home"])]
