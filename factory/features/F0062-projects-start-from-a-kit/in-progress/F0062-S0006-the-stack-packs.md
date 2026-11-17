---
stage: review
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 695
comments_read: [6937495535]
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
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-17T03:36:58.715956Z'
  stage: doing
- number: 7
  speaker: coder
  kind: question
  at: '2026-11-17T03:39:59.769254Z'
  stage: doing
  run: 5d8ac46f33484314bb5cf6a916521746
  blocked: question
- number: 8
  speaker: human
  kind: comment
  at: '2026-11-17T03:41:49.059254Z'
  stage: doing
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T03:41:51.600290Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T03:46:41.139558Z'
  stage: doing
  run: 15849d18913c473fac8692cff4725d22
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T03:46:46.316482Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-17T03:47:56.172460Z'
  stage: review
  run: bf1b2f9af9ee49d79ebfdf014765bc40
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-17T03:48:02.399659Z'
  stage: tests
- number: 14
  speaker: tester
  kind: result
  at: '2026-11-17T03:48:50.646183Z'
  stage: tests
  run: 5ed569757a1c4cdd9989d7076a71f0e1
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-17T03:48:56.116030Z'
  stage: doing
- number: 16
  speaker: coder
  kind: result
  at: '2026-11-17T03:51:27.952540Z'
  stage: doing
  run: b14aced5462b4e23b2aba011c5571784
---

# The stack packs

## Description

The kit holds what every project shares; what a stack needs on top has so far lived in three hand-made templates: the Python template in this repository, an ESP32 template and a Spring service template. After this story the factory holds one small pack per stack under `operator/packs/`: `python`, `c-host` (C that builds and tests on the host with CMake, firmware logic included) and `java-gradle`. A pack holds the stack's makefile, which includes the kit's `kit.mk` and defines `sync`, `lint`, `test` and `check`; the stage file with the tools those targets need; the stack's sections of `CLAUDE.md`, the review points among them; and a page of the stack's traps. A pack holds no application source. The human has worded the packs in `planning/packs-draft/` and has run the C and the Java pack for real, with `factory-check-project --run` on the VM (2026-11-17, all nine points `ok`); this story puts them in place unchanged, but for the licence header this repository's guard asks of `scripts/trust-store.sh`, and proves with tests that kit and pack together make a ready project for each stack. `operator/template/` stays as it is; the next story removes it.

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
6. factory: started doing as self.
7. coder: Stopped before `review`: `make secrets` is red because of a false positive in a draft that has to be copied byte for byte. Fixing it needs a baseline entry or a pragma, and `CLAUDE.md` lists both under "Not without asking".

   What I did:
   - Copied the three drafts unchanged from `planning/packs-draft/` into `operator/packs/` (`python/`, `c-host/` and `java-gradle/`, including `.gitleaks.toml` and `scripts/trust-store.sh`). `diff -r planning/packs-draft operator/packs` shows no difference. The copies are in the working tree, and no file under `planning/` or `src/` changed.
   - All 28 tests of `uv run pytest -q tests/operator_scripts/test_packs.py` pass.
   - `make lint`, `types`, `layers`, `licenses` and `test` are green (`test: green (109.5 s)`). `make guides` is green too (the folder-readme row did not fail).
   - `make check` is red only on `make secrets`: detect-secrets reports `Secret Type: Secret Keyword`, `Location: operator/packs/python/CLAUDE.sections.md:8`. That line is the Python pack's `## Checks` bullet, ``make secrets` (detect-secrets against `.secrets.baseline`)``. It is not a secret. The same wording in `operator/template/CLAUDE.md:25` passes because more text follows `.secrets.baseline` there. I ran `detect-secrets-hook` against the baseline on every file under `operator/packs/`, and this is the only hit.

   Options:
   1. Add an entry for that finding to `.secrets.baseline`, with `is_secret: false`. Run detect-secrets with `--baseline .secrets.baseline` over the file so the baseline is updated by the tool, not by hand. The pack stays byte for byte, and nothing extra reaches the projects that copy the pack. **I would choose this.**
   2. Add `# pragma: allowlist secret` to that line, as the "a guard asks more of a file" clause allows. But the marker would then be copied into every Python project's `CLAUDE.md`, and the pack's own `## Review` section counts such a marker as a finding.
   3. Add `^operator/packs/.*` to the baseline's `should_exclude_file` pattern. This is broader: secrets in future pack files would no longer be checked.
   4. You reword the draft and the pack, for example the way the template words it.

   Which one? If it is option 1 or 3, also confirm that `.secrets.baseline` is within the coder's write paths for this change.

   Main choice: copy the drafts unchanged, as the Interface asks. I rejected rewording line 8 myself, because that would break the byte-for-byte rule. I did not refactor, because the change is only copied files.
8. 2026-11-17 human: Option 4. I reworded the line in the draft on `develop`: the bullet now says "`make secrets` (detect-secrets with the reviewed findings of its baseline file)". Copy `planning/packs-draft/python/CLAUDE.sections.md` again, byte for byte; no baseline entry, no marker, no exclusion.
9. factory: started doing as self.
10. coder: Took up the human's answer (option 4). `make check` and `make guides` are now green: `make check` ends with `check: green` and `make guides` with `guides: green (9.3 s)`. All 28 tests of `tests/operator_scripts/test_packs.py` pass.

    What I built:
    - `operator/packs/python/`, `operator/packs/c-host/` and `operator/packs/java-gradle/`: copies of `planning/packs-draft/` (the earlier copy from my first run, still in the working tree). `operator/packs/python/CLAUDE.sections.md` is copied again from the reworded draft on `develop`, byte for byte. The `make secrets` finding is gone, with no baseline entry, no marker and no exclusion.
    - The one change beyond a copy, made under the Interface's clause for guards: `operator/packs/java-gradle/scripts/trust-store.sh` got the line `# SPDX-License-Identifier: Apache-2.0` after its `#!/bin/sh` shebang. Without it the guard `tests/guards/test_license_headers.py::test_every_file_in_scope_carries_the_license_header` failed in `make guides`. That guard applies to every `.sh` under `operator/` except `operator/template/`. `diff -r planning/packs-draft operator/packs` now shows only that one added line. No file under `planning/`, `src/` or `tests/` changed.

    Main choice: I copied the drafts unchanged and added only what a guard requires. I rejected two alternatives: excluding `operator/packs/` from the licence guard (that is a test change, and broader than needed), and asking the human to add the header to the draft (the Interface already allows the coder to add it).

    Refactor: nothing to change. The diff is copied files plus one header line.

    What the journal changed: the human reworded the Python pack's `make secrets` bullet in the draft. The Description needs no rewrite, because the copy is still byte for byte from the draft.

    Noticed but not touched:
    - The draft `planning/packs-draft/java-gradle/scripts/trust-store.sh` has no licence header. Adding it there would keep draft and pack equal, but `planning/` is the human's.
    - The folder-readme row for `operator/README.md` did not fail, so leave 27 was not needed.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
11. factory: started review as self.
12. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'` against the criteria and the Interface. I ran `diff -r planning/packs-draft operator/packs`: the only difference is the `# SPDX-License-Identifier: Apache-2.0` line in `java-gradle/scripts/trust-store.sh`, which the Interface's guard clause allows. No file under `planning/` or `src/` changes. I also ran `uv run pytest -q tests/operator_scripts/test_packs.py tests/operator_scripts/test_kit_files.py`, and every test passed.

    Criteria 1 to 7 each have a test that checks what the criterion says:
    - The thin, full and brownfield lines cover all three packs. Both kit pipeline definitions have the commented `# make_file: factory/Makefile` line that the brownfield helper uncomments.
    - Criterion 6 checks both sides, with the stand-ins called each time.
    - Criterion 7 checks both the shebang and `sh -n`, and that the store is built once on the first sync and not again on the second.

    Architecture: no module under `src/` changes. Security: both stage files run `sha256sum -c` after every `curl`. `changeit` is the JDK's default store password, not a secret. There are no markers, no baseline entries and no exclusions. No document the documenter writes is changed. This project's `CLAUDE.md` has no `## Review` section.

    Findings:
    1. `tests/operator_scripts/test_packs.py` `_faults` is a second copy of `_check` in `tests/operator_scripts/test_kit_files.py:59`: the same `committed_repository` + `run_project_check` dict comprehension. Fix: under the standing leave, move one helper (for example `project_faults(tmp_path, files)`) to `tests/support/kit_support.py` or `tests/support/project_check_support.py`, and use it from both modules. `test_packs.py` passes `{**files, **WRITTEN_FILES}`.
    2. `tests/operator_scripts/test_packs.py` `_section_texts` trims trailing blank lines with its own `while own and not own[-1].strip(): own.pop()`. This copies `_without_trailing_blanks` in `tests/support/kit_support.py`. Fix: make that helper public in `kit_support.py` (or move `_section_texts` there as a public helper built on it), and use it in the test.

    Both findings need only a change to this story's own tests and the shared support module. That is why I'm sending it to `tests`.

    description corrected: "this story puts them in place unchanged and proves" -> "this story puts them in place unchanged, but for the licence header this repository's guard asks of `scripts/trust-store.sh`, and proves". The Interface's guard clause and entry 10 settle this.

    Earlier tests:
    - `tests/operator_scripts/test_kit_files.py`: changed under the standing leave to move a shared test helper. `WRITTEN_FILES` moved to `tests/support/kit_support.py`, and every test keeps its name and what it checks.
13. factory: started tests as self.
14. tester: Answered the reviewer's two findings. I changed only this story's tests and the shared support modules, and moved the helpers under the standing leave to move a shared test helper.

    - Finding 1 (`_faults` in `test_packs.py` copied `_check` in `test_kit_files.py`): added `project_faults(tmp_path, files)` to `tests/support/project_check_support.py`. It commits `files` under `tmp_path / "project"` and returns each project check point's faults, with agents from the shipped `AGENT_HOME`. `test_packs.py` drops `_faults` and calls `project_faults(tmp_path, {**files, **WRITTEN_FILES})` in `test_a_project_from_the_kit_and_a_pack_is_ready` and `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready`. `tests/operator_scripts/test_kit_files.py` drops `_check` and calls `project_faults` in its two tests that used it, which keep their names and what they check.
    - Finding 2 (`_section_texts` in `test_packs.py` copied `_without_trailing_blanks`): in `tests/support/kit_support.py`, renamed `_without_trailing_blanks` to the public `without_trailing_blanks` and added the public `section_texts(body)`, which is built on it. `pack_claude_md` now takes its replacements from `section_texts`, so it behaves as before. `test_each_pack_sections_replace_the_kit_sections_of_the_same_heading` uses `section_texts` and no longer has its own copy.

    Earlier test file changed under the standing leave: `tests/operator_scripts/test_kit_files.py`.

    Criterion → test is unchanged. All tests are in `tests/operator_scripts/test_packs.py`:
    - criterion 1: `test_a_project_from_the_kit_and_a_pack_is_ready`
    - criterion 2: `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready`
    - criterion 3: `test_each_pack_makefile_includes_the_kit_first_and_defines_only_the_stack_targets`
    - criterion 4: `test_each_stage_file_keeps_the_layer_rule_and_checks_every_download`
    - criterion 5: `test_each_pack_sections_replace_the_kit_sections_of_the_same_heading`
    - criterion 6: `test_make_check_of_a_pack_is_green_only_when_its_tools_pass`
    - criterion 7: `test_the_java_trust_store_script_is_a_posix_shell_script` and `test_the_java_sync_builds_the_trust_store_once_per_bundle`

    Runs:
    - `uv run pytest -q tests/operator_scripts/test_packs.py tests/operator_scripts/test_kit_files.py`: all 44 passed.
    - `make lint`: lint: green (0.1 s). ruff removed the imports the moves left unused.

    No file was created; every module imports. Not checked: I did not run `make types`. A direct `mypy --strict` call on the four files, run outside the project's configuration, gave `import-untyped` errors for `factory` modules, which says nothing about the code. The coder's `make check` covers types.

    `lint`: lint: green (0.1 s)
15. factory: started doing as self.
16. coder: Round 1: the reviewer's two findings were test-helper copies, and the tester has already fixed both (entry 14). That left no code change for me. I ran the tests and the checks:
    - `uv run pytest -q tests/operator_scripts/test_packs.py tests/operator_scripts/test_kit_files.py`: all passed.
    - `make check guides`: `check: green` (`test: green (109.9 s)`) and `guides: green (9.3 s)`. This also covers `make types`, which the tester's entry left unchecked for the moved helpers in `tests/support/kit_support.py` and `tests/support/project_check_support.py`; types was green (4.9 s).

    What I built is unchanged from entry 10:
    - `operator/packs/python/`, `operator/packs/c-host/` and `operator/packs/java-gradle/` are byte-for-byte copies of `planning/packs-draft/`.
    - The one exception is the `# SPDX-License-Identifier: Apache-2.0` line in `operator/packs/java-gradle/scripts/trust-store.sh`, which the licence guard requires.
    - No file under `src/`, `planning/` or `tests/` was changed by me.

    Main choice: I changed nothing this round. The findings were about test helpers, so they were the tester's to fix under the standing leave, and that is done.

    Refactor: nothing to change. My part of the diff is copied files plus one header line.

    The journal did not change the meaning of the task this round. The reviewer already corrected the Description for the licence header.

    Noticed but not touched: the draft `planning/packs-draft/java-gradle/scripts/trust-store.sh` still has no licence header. `planning/` is the human's.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
