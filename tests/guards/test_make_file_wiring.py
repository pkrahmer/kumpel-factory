"""The project commands and the stage environment both get the makefile source the wiring builds."""

import ast

from support.make_file_support import git_make_file_source_class
from support.source_search import modules

WIRING = "factory.entry.wiring"


def _called_name(call: ast.Call) -> str:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return ""


def _make_file_arguments(name: str) -> list[tuple[str, str | None]]:
    """Each module's call of `name`, with what it passes as `make_file` (`None` when nothing)."""
    found: list[tuple[str, str | None]] = []
    for module, tree in modules().items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _called_name(node) == name:
                passed = [ast.unparse(k.value) for k in node.keywords if k.arg == "make_file"]
                found.append((module, passed[0] if passed else None))
    return found


def test_the_wiring_builds_the_git_source_and_both_users_get_a_source() -> None:
    source_name = git_make_file_source_class().__name__
    built = [
        module
        for module, tree in modules().items()
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _called_name(node) == source_name
    ]
    commands = _make_file_arguments("ContainerMakeCommands")
    environments = _make_file_arguments("ContainerEnvironment")

    assert WIRING in built
    assert [module for module, _ in commands] == [WIRING]
    assert all(value not in {None, "None"} for _, value in commands)
    assert environments
    assert all(value not in {None, "None"} for _, value in environments)
