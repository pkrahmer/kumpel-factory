# Document examples share the check's uv cache

## Goal

The document check (`make documents`) runs each document's examples in a fresh copy of the repository with an empty home, so the first `uv run` of every document builds a new virtual environment and downloads every package. Its time depends on the package index: on 2026-11-08 a cold start took 7 s at one moment and 99 s a few minutes earlier, against the examples' limit of 60 s, and F0060-S0001's docs stage stalled twice on examples it had not changed (`docs/runs/2026-11-05-f0052/log.md`). After this feature the examples' commands use the uv cache of the process that runs the check, which the check's own `uv run` has already filled, so a fresh copy's first `uv run` links from it in about a second (measured on the VM: 1 s). The examples keep their own empty home and their own copy. Done when the story is merged and `make check` and `make documents` are green on `develop`.

## Scope

- The examples' commands get `UV_CACHE_DIR` set to the cache the check itself uses (S0001).

## Out of scope

- The examples' time limit stays 60 s.
- A cache shared between instances, or kept between runs of the check beyond what uv already keeps.

## Stories

- S0001: Document examples use the check's uv cache.

## The human's changes

None: the story changes `src/` and `tests/` and the project guide; `Makefile`, `pyproject.toml`, `factory/` and `security/` stay as they are.

## Decisions taken for the human

1. Sharing the cache does not change what an example prints: uv's cache is content-addressed and safe for concurrent use, and the example still builds its own virtual environment in its own copy (the human, 2026-11-08, when choosing a fix story over a longer limit).
2. A separate feature, because its goal is not F0060's; kept in the backlog for later, since the package index was fast again when F0060-S0001 retried (the human, 2026-11-08).
