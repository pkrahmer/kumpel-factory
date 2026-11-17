# SPDX-License-Identifier: Apache-2.0
"""Where the classes that call make learn which makefile the pipeline definition names."""

from abc import ABC, abstractmethod


class MakeFileSource(ABC):
    """The makefile make runs with, asked again at every call so that a change takes effect."""

    @abstractmethod
    def make_file(self) -> str | None:
        """The makefile the pipeline definition names now, or `None` for make's own default."""


def asked_make_file(source: MakeFileSource | None) -> str | None:
    """The makefile `source` names now; `None` without a source."""
    return None if source is None else source.make_file()
