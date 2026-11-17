# The factory's folder

What kumpel-factory (github.com/pkrahmer/kumpel-factory) reads to build this repository. Nothing in it is part of what the repository ships.

- `pipeline.yml` The pipeline definition: the stages, the roles with their write paths, the project commands. The project's own.
- `Makefile` The factory's targets `sync`, `lint`, `test` and `check`, from the stack pack; `pipeline.yml` names it. The project's own. By hand: `make -f factory/Makefile check` from the root.
- `kit.mk` The factory's part of the makefile: the green line and the start facts. The kit's file: an upgrade replaces it.
- `story-form.md`, `feature-form.md` The forms a story and a feature follow. The kit's files.
- `stage.Containerfile` The tools `make check` needs on top of the factory's stage image. The project's own, from its stack pack.
- `scripts/`, `gitleaks.toml` What the pack's makefile needs beside it, where the stack has such files. The project's own.
- `agents/` Only when this project replaces one of the factory's installed agents: one file per replaced role.
- `features/` One folder per feature, with its stories.

`factory-check-project <this repository>` says whether these files are ready for the factory.
