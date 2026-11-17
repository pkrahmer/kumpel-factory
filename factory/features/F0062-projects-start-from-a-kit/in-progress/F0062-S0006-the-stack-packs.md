---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 695
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T03:31:08.754463Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T03:31:08.761944Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T03:31:42.680454Z'
  stage: intake
  run: e7624172905e494187529fc95a6caf25
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-17T03:31:47.953725Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-17T03:36:52.736072Z'
  stage: tests
  run: ade89571e3a145f1b6e3a76479c6c11c
---

# The stack packs

## Description

The kit holds what every project shares; what a stack needs on top has so far lived in three hand-made templates: the Python template in this repository, an ESP32 template and a Spring service template. After this story the factory holds one small pack per stack under `operator/packs/`: `python`, `c-host` (C that builds and tests on the host with CMake, firmware logic included) and `java-gradle`. A pack holds the stack's makefile, which includes the kit's `kit.mk` and defines `sync`, `lint`, `test` and `check`; the stage file with the tools those targets need; the stack's sections of `CLAUDE.md`, the review points among them; and a page of the stack's traps. A pack holds no application source. The human has worded the packs in `planning/packs-draft/` and has run the C and the Java pack for real, with `factory-check-project --run` on the VM (2026-11-17, all nine points `ok`); this story puts them in place unchanged and proves with tests that kit and pack together make a ready project for each stack. `operator/template/` stays as it is; the next story removes it.

## Interface

- `operator/packs/python/` with `Makefile`, `CLAUDE.sections.md` and `TRAPS.md`; `operator/packs/c-host/` with `Makefile`, `stage.Containerfile`, `CLAUDE.sections.md` and `TRAPS.md`; `operator/packs/java-gradle/` with `Makefile`, `stage.Containerfile`, `CLAUDE.sections.md`, `TRAPS.md`, `.gitleaks.toml` and `scripts/trust-store.sh`: each a copy, byte for byte, of the file of the same path under `planning/packs-draft/`. Where a guard of this repository asks more of a file (a licence header, for example), the coder adds only that and names it in its entry. No file under `planning/` changes.
- The Python pack has no stage file: the factory's stage image holds what it needs.
- How a project is assembled from kit and pack, which the tests do in a helper (extending `tests/support/kit_support.py`): the kit as S0005 describes it; then the pack's `Makefile` to the root, or to `factory/Makefile` with `make_file: factory/Makefile` in the pipeline definition for an existing repository; the pack's `stage.Containerfile`, where it has one, to `factory/`; the pack's other files (`.gitleaks.toml`, `scripts/`) to the same path from the root; and the sections of `CLAUDE.sections.md` in place of the kit skeleton's sections of the same heading.
- No module under `src/factory/` changes.
- `feature.md` gives this leave (decision 27): "the coder may end its run with `make guides` red only on the folder-readme row for `operator/README.md` naming `packs/`, which the docs stage fixes".
- Tests: `tests/operator_scripts/test_packs.py`.

## Acceptance criteria

1. For each pack, a project assembled from the kit's thin line and the pack, with one file under every write path, committed: `ProjectCheck.run` gives no fault at all; the same for the kit's full line: rows of one parametrized test over the three packs and the two lines.
2. For each pack, the same project assembled the brownfield way (the pack's makefile at `factory/Makefile`, `make_file: factory/Makefile` in the definition, no root `Makefile`): `ProjectCheck.run` gives no fault at all.
3. Each pack's `Makefile` holds the line `include factory/kit.mk` before its first rule, defines the targets `sync`, `lint`, `test` and `check`, and defines none of the kit's own targets (`facts-diff`, `facts-changes`, `facts-files`): rows of one parametrized test, read with `makefile_targets`.
4. Each stage file passes the layer rule (`stage_layer`), and every `curl` download in it is followed by a checksum check (`sha256sum -c`) in the same instruction: rows over the two stage files.
5. Each `CLAUDE.sections.md` holds the headings `## Tests`, `## Checks`, `## Review` and `## Not without asking (end the stage with `question`)`, every one a heading the kit's `CLAUDE.md` holds too; the assembled `CLAUDE.md` holds each heading once, the pack's text under it, and the kit's `## Language` and `## Architecture` unchanged.
6. In a makefile assembled from kit and pack, with stand-ins on the `PATH` for the stack's tools (a script named `uv`, `cmake`, `ctest`, `clang-format`, `gitleaks` or `gradlew` that records its arguments and ends with 0), `make check` in `tmp_path` ends with `check: green` and prints one green line for each target `check` depends on; with a stand-in that ends with 1, `make check` ends red and prints no `check: green`: rows over the three packs. The Python pack's placeholders `SOURCE` and `LAYERS` are set on make's command line.
7. `scripts/trust-store.sh` of the Java pack is a POSIX shell script that passes `sh -n`, and the Java pack's `sync`, run with stand-ins and `SSL_CERT_FILE` naming a file, calls it once with the bundle and the trust store's path, and not again on a second sync with the same bundle.
8. `make check` stays green.
9. docs: a new `operator/packs/README.md` says what a pack is and what it is not (no application source: that is a starter's), lists the three packs with what each file is for and who owns it after the copy (all the project's own), how kit and pack are assembled for a fresh start and for an existing repository (`make_file`), that each pack's `TRAPS.md` is the page to read before the first story, that the C and the Java pack were run with `factory-check-project --run` on 2026-11-17, and how a new stack gets a pack; `operator/README.md` lists the packs; the project guide (`docs/project-guide/operator.md`) names the packs and their test.

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
for pack in python c-host java-gradle; do
  p="$d/$pack"; git init -q "$p"; mkdir -p "$p/src" "$p/tests" "$p/docs"
  cp -r operator/kit/factory "$p/factory"; cp operator/kit/CLAUDE.md "$p/"
  mv "$p/factory/pipeline.thin.yml" "$p/factory/pipeline.yml"; rm "$p/factory/pipeline.full.yml"
  cp operator/packs/$pack/Makefile "$p/Makefile"
  if [ -f operator/packs/$pack/stage.Containerfile ]; then cp operator/packs/$pack/stage.Containerfile "$p/factory/"; fi
  touch "$p/src/a" "$p/tests/a" "$p/docs/a" "$p/README.md"
  git -C "$p" add -A; git -C "$p" -c user.name=t -c user.email=t@example.com commit -q -m one
  echo "$pack $(uv run python -m factory.entry.check_project --agent-home agents "$p" | tail -1)"
done
```
Expect: `python project: ready`, `c-host project: ready`, `java-gradle project: ready`.

```bash
uv run pytest tests/operator_scripts/test_packs.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: accepted
   - Interface: concrete. It names the files of each pack and their drafts under `planning/packs-draft/`, and every listed draft file exists. It gives the assembly helper's place (`tests/support/kit_support.py`), the test module `tests/operator_scripts/test_packs.py`, and the existing functions the criteria use (`ProjectCheck.run`, `makefile_targets`, `stage_layer(text, base_identity)`). No module under `src/factory/` changes. Leave 27 of `feature.md` covers the red folder-readme row for `packs/`.
   - Criteria: each one can be tested by one test function. The pass side and the fail side are covered for `make check` with stand-ins (6) and for the trust store being called once and then not again (7). The thin, full and brownfield lines are covered (1, 2). The draft files match what the criteria expect: the `include factory/kit.mk` line, `curl` followed by `sha256sum -c` in the same `RUN` in both stage files, and the four headings in each `CLAUDE.sections.md`, which the kit's `CLAUDE.md` also holds. A note for the tester: the Java makefile calls `./gradlew`, not `gradlew` from the `PATH`, so its stand-in must sit in `tmp_path`, the folder make runs in. For the Python pack, every tool goes through `uv` and `$(LAYERS)`, which is set on make's command line.
   - Smoke test: runnable. Each block ends in a line the output can be checked against (`<pack> project: ready` three times; a pytest summary with only `passed`). `pyproject.toml` sets `-q` in `addopts`, and the pytest command passes no `-q` of its own, so the summary line is printed.
   - Docs criterion: it names what the reader must know (what a pack is and what it is not, its files and who owns them, the fresh and the existing-repository assembly, `TRAPS.md`, the run on 2026-11-17, how a new stack gets a pack, the listing in `operator/README.md` and in the project guide). It dictates no sentences.
   - Architecture: only operator files and tests are added. No code under `src/` changes, and the assembly helper extends the shared `tests/support/kit_support.py` as the test rules require.
   - Scope: within F0062: the packs are in its scope, and S0006 is the story for them. Decisions 3, 23 and 24 are respected: no application source in a pack, the drafts copied unchanged, and the emulator not in the Java pack. Starters and the removal of `operator/template/` stay out (S0007 removes the template).
4. factory: started tests as self.
5. tester: Wrote the tests of the stack packs. They are red on purpose: every one fails with `FileNotFoundError` on `operator/packs/<pack>/…`, which does not exist yet.

   Criterion → test (all in `tests/operator_scripts/test_packs.py`):
   - criterion 1: `test_a_project_from_the_kit_and_a_pack_is_ready` (3 packs × thin/full, plus one file under every write path, committed, `ProjectCheck.run` with no fault)
   - criterion 2: `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready` (3 packs × thin/full; the makefile is at `factory/Makefile`, the kit's commented `# make_file: factory/Makefile` line is uncommented, there is no root `Makefile`)
   - criterion 3: `test_each_pack_makefile_includes_the_kit_first_and_defines_only_the_stack_targets` (uses `makefile_targets` per line to find the first rule)
   - criterion 4: `test_each_stage_file_keeps_the_layer_rule_and_checks_every_download` (`stage_layer(text, "base")`; joins continuation lines into instructions, and after each `curl ` in an instruction there must be a `sha256sum -c` before the next one)
   - criterion 5: `test_each_pack_sections_replace_the_kit_sections_of_the_same_heading`
   - criterion 6: `test_make_check_of_a_pack_is_green_only_when_its_tools_pass` (3 packs × stand-ins ending with 0 or with 1)
   - criterion 7: `test_the_java_trust_store_script_is_a_posix_shell_script` (shebang `#!/bin/sh`, then `sh -n`) and `test_the_java_sync_builds_the_trust_store_once_per_bundle`
   - criteria 8 and 9: no test (`make check`, docs).

   Files:
   - Created `tests/operator_scripts/test_packs.py`.
   - Extended `tests/support/kit_support.py` as the Interface says: `PACKS_FOLDER`, `Pack`, `PACKS`, `pack_claude_md` (each pack section replaces the kit section with the same heading; trailing blank lines are kept from the kit) and `pack_project_files(pack, line, brownfield=…)`. The pack's other files except `TRAPS.md` (`.gitleaks.toml`, `scripts/`) go to the same path from the root.
   - Under the standing leave to move a shared test helper, I moved `WRITTEN_FILES` from `tests/operator_scripts/test_kit_files.py` into `tests/support/kit_support.py`. `test_kit_files.py` now imports it; its tests keep their names and checks.

   Choices the coder should know (all within the criteria):
   - For criterion 6, the project is a committed git repository: the Python pack's `secrets` recipe fails outside one. The stand-ins are shell scripts that record their name and arguments in `tmp_path/calls`. `PATH` is `tmp_path/bin:/usr/bin:/bin`, and `HOME` is a folder in `tmp_path`. The Java `gradlew` stand-in sits in the project, since the makefile calls `./gradlew`.
   - The Python licence check runs `sed` on the file that `uv export` writes. A stand-in writes nothing, so the test creates an empty `.reports/licenses-requirements.txt` beforehand. The make command line sets `SOURCE=src/app` and `LAYERS=uv run lint-imports`.
   - Which targets need a green line is read from the pack makefile's `check:` line. The test also checks that the stand-ins were called on both sides.
   - For criterion 7, the project's `scripts/trust-store.sh` is replaced by a recording stand-in that also creates the store file. The test runs `make sync` twice with `SSL_CERT_FILE` naming a bundle, and expects exactly one call with `<bundle> <HOME>/.cache/java-trust-store.p12`.

   Checked against the drafts: copying them into `operator/packs/` was refused, so I loaded a throwaway pytest plugin from a `mktemp` folder that pointed `PACKS_FOLDER` at `planning/packs-draft/`. With that, all 28 tests of `test_packs.py` passed. This means a byte-for-byte copy of the drafts should turn them green. No file under `operator/` or `planning/` was changed.

   The one `make test` run: 28 failures, all in `test_packs.py` and all `FileNotFoundError` on the missing pack files. The JUnit report shows no other failure. `make lint` is green. Every module the tests import exists; the runner could import all of them, only the pack files are missing.

   `lint`: lint: green (0.2 s)
