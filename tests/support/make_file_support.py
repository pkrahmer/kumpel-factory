"""The makefile source built on git, found by the interface it implements, and a stand-in source."""

import importlib
import inspect
import pkgutil

import factory.pipeline.application
from factory.machine.application.make_file import MakeFileSource


def git_make_file_source_class() -> type[MakeFileSource]:
    """The one concrete implementation of `MakeFileSource` in `factory.pipeline.application`."""
    package = factory.pipeline.application
    found: set[type[MakeFileSource]] = set()
    for module_info in pkgutil.walk_packages(package.__path__, f"{package.__name__}."):
        module = importlib.import_module(module_info.name)
        for _, member in inspect.getmembers(module, inspect.isclass):
            if issubclass(member, MakeFileSource) and not inspect.isabstract(member):
                found.add(member)
    [source_class] = found
    return source_class


class AnsweringSource(MakeFileSource):
    """A source that gives its answers in turn and repeats the last one."""

    def __init__(self, *answers: str | None) -> None:
        """Give `answers` in turn, the last one from then on."""
        self._answers = list(answers)

    def make_file(self) -> str | None:
        """The next answer."""
        if len(self._answers) > 1:
            return self._answers.pop(0)
        return self._answers[0]
