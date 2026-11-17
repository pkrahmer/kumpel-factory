# The stack packs

A stack pack holds what one stack needs on top of the [kit](../kit/README.md): the makefile's four targets (`sync`, `lint`, `test`, `check`), the stage file with the tools those targets call, the stack's sections of `CLAUDE.md` and a page of the stack's traps. A pack holds no application source: a project's first code is a starter's, and a starter is a repository of its own, built from the kit and a pack. The decision log has the reasons, in [decisions.md](../../docs/decisions.md) (*A project starts from a kit, a stack pack and a starter*).

There are three packs:

- `python/`: a Python project with a src layout, built with uv. It has no stage file, because the factory's stage image already holds uv, and uv fetches the Python the project pins.
- `c-host/`: C that builds and tests on the host with CMake and CTest, firmware logic included, as long as its tests need no device. A cross build, a flash or a monitor is the project's own target, outside `check`.
- `java-gradle/`: a Java project built with the Gradle wrapper.

The C and the Java pack were run for real by the human on 2026-11-17: a project assembled from each passed `factory-check-project --run` on the VM, with all nine points `ok`.

Before the first story, read the pack's `TRAPS.md`. It lists what cost time when the first projects of that stack ran in the factory, and what the pack does about each.

## Assembling a project from the kit and a pack

For a fresh start:

1. Assemble the kit as its [README](../kit/README.md) says, steps 1 to 3: `factory/` with the chosen line's `pipeline.yml`, and `CLAUDE.md` at the root.
2. Copy the pack's `Makefile` to the project's root. It already begins with `include factory/kit.mk`, so it takes the place of the kit README's step 4.
3. Copy the pack's `stage.Containerfile`, where it has one, to `factory/stage.Containerfile`. The factory builds it on top of its stage image; see *The project's stage file* in [machine.md](../../docs/operator-guide/machine.md).
4. Copy the pack's other files to the same path from the project's root: for the Java pack, `.gitleaks.toml` and `scripts/trust-store.sh`.
5. In `CLAUDE.md`, replace each of the kit skeleton's sections `## Tests`, `## Checks`, `## Review` and `## Not without asking (end the stage with `question`)` with the pack's section of the same heading from `CLAUDE.sections.md`. Keep the kit's `## Language` and `## Architecture`, and fill in their placeholders.
6. Fill in the pack makefile's placeholders. The Python pack has two that must be set: `SOURCE` (the package's folder, `src/<package>`) and `LAYERS` (the command that checks the layers, such as `uv run lint-imports`). The C and the Java pack give every variable a default that a project may override.
7. Fill the write paths and commit, then run the conformance check, as in the kit README's steps 5 and 6. It ends with `project: ready`.

For an existing repository that keeps a root `Makefile` of its own, copy the pack's `Makefile` to `factory/Makefile` instead of the root, and remove the comment sign from the line `# make_file: factory/Makefile` in `factory/pipeline.yml`. The include line stays `include factory/kit.mk`, because make runs from the root of the checkout. Every other step is the same.

## A pack for a new stack

A new stack gets a pack of its own as a new folder here, written by a story like any other change. Its makefile includes `factory/kit.mk` before its first rule, defines `sync`, `lint`, `test` and `check`, and defines none of the kit's own targets (`facts-diff`, `facts-changes`, `facts-files`). A stage file, where the stack needs tools beyond the stage image, keeps the stage file's rule, and every download in it is checked against its SHA-256. Its `CLAUDE.sections.md` holds the four sections above, each under a heading the kit's `CLAUDE.md` holds too. Its `TRAPS.md` says what cost time in the stack's first projects. Add the pack to `Pack` and `PACKS` in [kit_support.py](../../tests/support/kit_support.py), so that the tests in [test_packs.py](../../tests/operator_scripts/test_packs.py) prove that kit and pack make a ready project, and run a project assembled from it with `factory-check-project --run`, as the C and the Java pack were.

## Reference

### Files

Every file of a pack becomes the project's own once copied: the project edits it as it likes, and no upgrade of the pack replaces it. Only the kit's `kit.mk` and forms stay the kit's.

| File | Packs | Path in the project | What it is for |
|---|---|---|---|
| `Makefile` | all | `Makefile`, or `factory/Makefile` with `make_file: factory/Makefile` | the targets `sync`, `lint`, `test` and `check`, and the stack's other targets (`check` depends on them) |
| `stage.Containerfile` | `c-host`, `java-gradle` | `factory/stage.Containerfile` | the tools the targets need beyond the stage image, each download pinned by version and SHA-256 |
| `CLAUDE.sections.md` | all | the sections of `CLAUDE.md` with the same headings | the stack's rules for the tests, the checks, the review and what an agent must not do without asking |
| `TRAPS.md` | all | not copied; read before the first story | what cost time in the stack's first projects, and what the pack does about each |
| `.gitleaks.toml` | `java-gradle` | `.gitleaks.toml` | gitleaks' own rules, without the folders a build writes |
| `scripts/trust-store.sh` | `java-gradle` | `scripts/trust-store.sh` | builds a copy of the JDK's trust store with the certificates of the CA bundle `SSL_CERT_FILE` names; `make sync` runs it again only when the bundle changes |

### The targets `check` depends on

| Pack | `check` runs | Tools |
|---|---|---|
| `python` | `lint types layers sast secrets licenses test` | uv, and the development dependencies the makefile's opening comment lists |
| `c-host` | `lint secrets test` | a C compiler, CMake, CTest, clang-format, gitleaks |
| `java-gradle` | `lint secrets test package` | a JDK, the project's `./gradlew`, gitleaks |

The Python pack also has `duplicates`, a report outside `check`, and `mutants`, for a sweep by hand and never a stage.
