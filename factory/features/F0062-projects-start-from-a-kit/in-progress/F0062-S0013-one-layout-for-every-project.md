---
stage: smoke-test
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 705
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T06:47:26.854758Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T06:47:26.862966Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T06:47:54.215861Z'
  stage: intake
  run: 6e9fb6e9f50a4ce592a37ad4cda26e18
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-17T06:47:59.401485Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-17T06:52:09.255746Z'
  stage: tests
  run: e0ccf9f4ddcd4fb9b3aa35099a54160c
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-17T06:52:14.789438Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-17T06:55:26.918099Z'
  stage: doing
  run: 33c2c3c901d64cebbc76d7ae434ceb36
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-17T06:55:32.572249Z'
  stage: tests
- number: 9
  speaker: tester
  kind: result
  at: '2026-11-17T06:55:55.324565Z'
  stage: tests
  run: 50ccfa35122e498aa2a0df4dab8b8104
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-17T06:56:00.642017Z'
  stage: doing
- number: 11
  speaker: coder
  kind: result
  at: '2026-11-17T06:58:23.536057Z'
  stage: doing
  run: d11e7cafcfdf40f8aeda5f4548852b40
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-17T06:58:28.866442Z'
  stage: review
- number: 13
  speaker: reviewer
  kind: result
  at: '2026-11-17T06:59:31.091508Z'
  stage: review
  run: b76fc64198114b61876ac8587146944c
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-17T06:59:36.203635Z'
  stage: tests
- number: 15
  speaker: tester
  kind: result
  at: '2026-11-17T07:00:52.613415Z'
  stage: tests
  run: c5ed437ec8a546869d6e1718b47ad55f
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-17T07:00:57.881651Z'
  stage: doing
- number: 17
  speaker: coder
  kind: result
  at: '2026-11-17T07:03:22.626510Z'
  stage: doing
  run: d12c40003e8a4a998d8628fbcf077a53
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-17T07:03:28.170331Z'
  stage: review
- number: 19
  speaker: reviewer
  kind: result
  at: '2026-11-17T07:04:12.225506Z'
  stage: review
  run: 2065d595e37d40268e15b8e70d6c7959
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-17T07:04:18.214424Z'
  stage: docs
- number: 21
  speaker: documenter
  kind: result
  at: '2026-11-17T07:13:19.244521Z'
  stage: docs
  run: 1ba28b8a41a54d4294e4df0495d63e4c
---

# One layout for every project

## Description

A project assembled from the kit and a pack has two layouts today: a fresh start gets the pack's `Makefile` at the root, an existing repository gets it at `factory/Makefile` with `make_file` in the pipeline definition, and the Java pack puts a script and the gitleaks rules at the root in both. After this story there is one layout: everything the factory needs, beside `CLAUDE.md`, lives in the project's `factory/` folder, for a fresh start and for an existing repository alike. Both pipeline definitions of the kit name `make_file: factory/Makefile`; every pack file but the two pages a person reads (`CLAUDE.sections.md`, `TRAPS.md`) goes into `factory/` at its own path; and the kit gains `root.Makefile`, a makefile of four lines that forwards every target to `factory/Makefile`, which a repository without a root `Makefile` of its own copies as `Makefile`, so that `make check` still works at the root, for a developer and for the agents. The human has reworded the drafts in `planning/kit-draft/` and `planning/packs-draft/` (2026-11-17, the human's wish for a clean layout); this story puts them in place unchanged and moves the tests and the documents to the one layout. No module under `src/factory/` changes: `make_file` and its protection are built.

## Interface

- `operator/kit/` and `operator/packs/`: each file again a copy, byte for byte, of the file of the same path under `planning/kit-draft/` and `planning/packs-draft/`, but for what a guard of this repository asks of a file (the licence header line that `operator/packs/java-gradle/scripts/trust-store.sh` already carries stays). What differs from today:
  - `operator/kit/factory/pipeline.thin.yml` and `pipeline.full.yml` hold the line `make_file: factory/Makefile` instead of the commented one.
  - `operator/kit/root.Makefile` is new.
  - `operator/kit/factory/kit.mk`, `operator/kit/factory/README.md` and `operator/kit/CLAUDE.md` have new words about where the makefile lives.
  - `operator/packs/java-gradle/.gitleaks.toml` becomes `operator/packs/java-gradle/gitleaks.toml`; the Java pack's `Makefile` names `factory/scripts/trust-store.sh` and `factory/gitleaks.toml`; the Java pack's `TRAPS.md` and `CLAUDE.sections.md` and the C pack's `Makefile` name the new paths.
- How a project is assembled, which the helper `tests/support/kit_support.py` does and the documents describe: the kit as before; every file of the pack but `CLAUDE.sections.md` and `TRAPS.md` goes to the project's `factory/` at the same path (`Makefile` to `factory/Makefile`, `stage.Containerfile` to `factory/stage.Containerfile`, `scripts/trust-store.sh` to `factory/scripts/trust-store.sh`, `gitleaks.toml` to `factory/gitleaks.toml`); `operator/kit/root.Makefile` goes to the root as `Makefile` only when the repository has no root `Makefile` of its own; the pack's sections replace the skeleton's as before. There is no second way.
- Tests: `tests/operator_scripts/test_one_layout.py`, new. The human gives this leave (feature decision 36): "S0013 may change the helper `tests/support/kit_support.py` and every earlier test of the kit and the packs (`tests/operator_scripts/test_kit_files.py`, `test_kit_makefile.py`, `test_packs.py`, and any other earlier test whose only failure is the new layout) so that it assembles and checks the one layout: a row or a test that was only about the pack's makefile at the root is changed to the root's forwarding makefile, or removed where the new test covers it; each other test keeps its name and what it checks. The tester names every changed file and every removed row in its entry."

## Acceptance criteria

1. Both pipeline definitions of the kit load with `make_file` equal to `factory/Makefile`, and neither holds a commented `make_file` line: rows of one parametrized test.
2. For each pack and each line, a project assembled the one way, with one file under every write path, committed: `ProjectCheck.run` gives no fault at all; and the only files outside `factory/` that the assembly wrote are `CLAUDE.md` and, for a repository without a root makefile, `Makefile`: rows over the three packs and the two lines.
3. The same assembly into a repository that already has a root `Makefile` of its own leaves that file byte for byte as it was, and `ProjectCheck.run` gives no fault.
4. `root.Makefile` as a root `Makefile`, with a `factory/Makefile` that includes `kit.mk` and has the targets `lint` and `check`: `make` without a target runs `check` of `factory/Makefile`; `make lint` prints that target's green line; `make nosuch` ends red; and make does not try to remake `Makefile` through the forwarding rule (no line of the output names a target `Makefile`): real runs in `tmp_path`.
5. The Java pack's `sync`, run with stand-ins and `SSL_CERT_FILE` naming a file, calls `factory/scripts/trust-store.sh`, and its `secrets` calls gitleaks with `--config factory/gitleaks.toml`; no pack file names `scripts/trust-store.sh` or `.gitleaks.toml` at the root.
6. `factory/Makefile` and `factory/kit.mk` of an assembled project are protected paths for every role of both lines (`protected_paths` with the definition's `make_file`).
7. `make check` stays green.
8. docs: `operator/kit/README.md`, `operator/packs/README.md`, `docs/operator-guide/start-a-project.md` and the part of `docs/operator-guide/pipeline.md` on naming the makefile describe the one layout: everything but `CLAUDE.md` in `factory/`, the pack's files that go there, `root.Makefile` and when to copy it, how a target is run by hand, and what a repository with its own root `Makefile` writes into `CLAUDE.md` so that the agents run `make -f factory/Makefile <target>`; no document describes the pack's makefile at the root as a way to assemble a project any more; `docs/decisions.md` records the decision of 2026-11-17 that a project holds `CLAUDE.md` and the `factory/` folder and nothing else of the factory's, with its price (a forwarding root makefile, or `-f`) and its gain (one layout to explain and to upgrade, and the makefile among the protected paths).

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
for pack in python c-host java-gradle; do
  p="$d/$pack"; git init -q "$p"; mkdir -p "$p/src" "$p/tests" "$p/docs"
  cp -r operator/kit/factory "$p/factory"; cp operator/kit/CLAUDE.md "$p/"; cp operator/kit/root.Makefile "$p/Makefile"
  mv "$p/factory/pipeline.thin.yml" "$p/factory/pipeline.yml"; rm "$p/factory/pipeline.full.yml"
  (cd operator/packs/$pack && find . -type f ! -name CLAUDE.sections.md ! -name TRAPS.md) | while read f; do mkdir -p "$p/factory/$(dirname "$f")"; cp "operator/packs/$pack/$f" "$p/factory/$f"; done
  touch "$p/src/a" "$p/tests/a" "$p/docs/a" "$p/README.md"
  git -C "$p" add -A; git -C "$p" -c user.name=t -c user.email=t@example.com commit -q -m one
  echo "$pack $(uv run python -m factory.entry.check_project --agent-home agents "$p" | tail -1) $(git -C "$p" ls-files | grep -v -e '^factory/' -e '^src/' -e '^tests/' -e '^docs/' -e '^README.md$' | tr '\n' ' ')"
done
```
Expect: `python project: ready CLAUDE.md Makefile`, `c-host project: ready CLAUDE.md Makefile`, `java-gradle project: ready CLAUDE.md Makefile`.

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
mkdir -p "$d/factory"; cp operator/kit/factory/kit.mk "$d/factory/"; cp operator/kit/root.Makefile "$d/Makefile"
printf 'include factory/kit.mk\nlint:\n\t$(start)\n\t$(green)\ncheck: lint\n\techo "check: green"\n' > "$d/factory/Makefile"
env -u MAKEFLAGS -u MAKELEVEL -u MFLAGS make -C "$d" --no-print-directory | sed 's/([0-9]*\.[0-9] s)/(N s)/'
```
Expect: `lint: green (N s)`, then `check: green`.

```bash
uv run pytest tests/operator_scripts/
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: accepted
   - Interface: names concrete files: the drafts under `planning/kit-draft/` and `planning/packs-draft/` exist, and `diff -rq` against `operator/kit/` and `operator/packs/` shows exactly the differences the Interface lists (pipeline.thin/full.yml, kit.mk, factory/README.md, CLAUDE.md, new root.Makefile, `.gitleaks.toml` → `gitleaks.toml`, Java Makefile/TRAPS/CLAUDE.sections, C Makefile, trust-store.sh, which differs only by the licence header the Interface keeps). The assembly rule (pack files but the two pages into `factory/` at the same path, root.Makefile only when there is no root Makefile) is stated once, for the helper `tests/support/kit_support.py` and the documents. No module under `src/factory/` changes.
   - Criteria: each testable by one test function: 1 parametrized over the two definitions (value and no commented line); 2 over three packs × two lines, both sides of "outside `factory/`" (only `CLAUDE.md` and `Makefile`); 3 the other side of the root.Makefile rule (an existing root Makefile is kept byte for byte); 4 the forwarding makefile's default goal, a target, an unknown target red and no remaking of `Makefile`, all real runs; 5 the Java pack's new paths, with the refused side (no pack file names the old root paths); 6 protection of `factory/Makefile` and `factory/kit.mk`. Test changes to other stories' tests carry the human's leave (feature decision 36, quoted in the Interface).
   - Smoke test: three blocks, runnable from the checkout (`factory.entry.check_project` exists, root.Makefile draft forwards with `.DEFAULT_GOAL := check` and `Makefile: ;`); each `Expect:` is checkable (three exact lines, two green lines with the time masked, a pytest summary with only `passed`); the pytest command passes no `-q`, and `addopts` already sets `-q`, so the summary line prints.
   - Docs criterion: names what the reader must know (the one layout, the pack files in `factory/`, root.Makefile and when to copy it, running a target by hand, the `CLAUDE.md` line for `make -f factory/Makefile`, the decision with its price and gain); it dictates no sentences, and its files are in the documenter's write paths.
   - Architecture: the changes are data files under `operator/kit/` and `operator/packs/` (coder's write paths), tests under `tests/` (tester's) and documents (documenter's); `make_file` and its protection are already built, so no layer or wrapper is touched.
   - Scope: within F0062 and exactly its decision 36 (one layout, story S0013); nothing from its Out of scope. Route `tests`, since the coder must write `operator/kit/` and `operator/packs/`.
4. factory: started tests as self.
5. tester: Wrote the tests for the one layout and moved the kit and pack helper and the earlier tests to it, under the leave the human gave in feature decision 36.

   Criteria → tests (all in `tests/operator_scripts/test_one_layout.py`):
   - criterion 1: `test_each_kit_pipeline_definition_names_the_factory_makefile` (rows: thin and full). Checks that `make_file == "factory/Makefile"` and that no line matches `^\s*#\s*make_file\s*:`.
   - criterion 2: `test_a_one_way_project_is_ready_with_only_claude_md_and_makefile_outside_factory` (rows: 3 packs × 2 lines). `project_faults` must be all empty. Apart from `WRITTEN_FILES`, the assembly writes only `CLAUDE.md` and `Makefile` outside `factory/`, and `Makefile` is `operator/kit/root.Makefile` byte for byte.
   - criterion 3: `test_an_own_root_makefile_is_kept_byte_for_byte` (rows: 3 packs × 2 lines). Uses an own root `Makefile`; the committed file must equal it byte for byte, and `ProjectCheck.run` must give no fault.
   - criterion 4: `test_the_root_makefile_forwards_every_target_to_the_factory_makefile` (rows: no target, `lint`, `nosuch`). Real make runs in `tmp_path`:
     - with no target, the `lint` green line prints, then `check: green` as the last line;
     - `lint` prints its green line and not `check: green`;
     - `nosuch` ends red;
     - in every row, no output line names `'Makefile'` or `` `Makefile' ``.
   - criterion 5: `test_the_java_pack_calls_its_files_under_factory`.
     - `sync` runs with `SSL_CERT_FILE` set and calls a recording stand-in placed at `factory/scripts/trust-store.sh`.
     - `secrets` calls a stand-in `gitleaks` with `--config factory/gitleaks.toml`.
     - Refused side: no file in the three pack folders names `scripts/trust-store.sh` without `factory/` in front, or `.gitleaks.toml`.
   - criterion 6: `test_the_factory_makefiles_are_protected_for_every_role` (rows: 2 lines × `factory/Makefile` and `factory/kit.mk`). Checks `matches_any(path, protected_paths(definition.make_file))`.
   - criteria 7 and 8: no test (`make check` and docs).

   Files:
   - Created: `tests/operator_scripts/test_one_layout.py`.
   - Changed under decision 36's leave:
     - `tests/support/kit_support.py`:
       - new `ROOT_MAKEFILE` and `PACK_PAGES`;
       - `kit_project_files` now also writes `root.Makefile` as the root `Makefile`;
       - `pack_project_files` has a single assembly: every pack file but `CLAUDE.sections.md` and `TRAPS.md` goes to `factory/<same path>`;
       - the `brownfield=` keyword is replaced by `own_root_makefile=`;
       - `_PACK_PLACED_FILES` and `_MAKE_FILE_LINE` are removed.
     - `tests/operator_scripts/test_kit_files.py`:
       - in `test_each_kit_pipeline_definition_loads_through_the_reader`, removed the two lines that asserted `make_file is None` and the commented line (criterion 1 now covers them);
       - in `test_a_project_from_the_kit_alone_lacks_only_the_makefile_and_written_files`, the expected fault is now `factory/Makefile is missing`;
       - `test_a_kit_project_with_its_makefile_and_written_files_is_ready` puts its makefile at `factory/Makefile`.
     - `tests/operator_scripts/test_packs.py`:
       - removed `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready` (all 6 rows; the criterion 2 and 3 tests cover it);
       - `test_the_java_sync_builds_the_trust_store_once_per_bundle` writes its stand-in to `factory/scripts/trust-store.sh`;
       - every other test keeps its name and what it checks. The stand-in `make check` now runs through the forwarding root makefile.
   - Left as they are: `test_kit_makefile.py`, whose tests are about `kit.mk` with any includer and do not depend on the layout, and `test_claude_files.py`, which uses only `pack_claude_md`.

   Test run: `make test` is red as intended. Every failure seen was `FileNotFoundError` on `operator/kit/root.Makefile`, which does not exist yet; no module failed to import. `make lint` is green.

   Open: I tried to check these tests against the drafts by copying the drafts into `operator/` for a moment; the call was refused. They have not been run against the finished files, so the coder's run is the first one. The working tree's `operator/` was not changed.

   `lint`: lint: green (0.1 s)
6. factory: started doing as self.
7. coder: Put the human's drafts in place, unchanged. `make check` is red on one earlier test that only the new layout breaks, so the story goes back to the tester.

   Built (data files only; no module under `src/factory/` changed):
   - Copied byte for byte from `planning/kit-draft/`: `operator/kit/CLAUDE.md`, `operator/kit/factory/README.md`, `operator/kit/factory/kit.mk`, `operator/kit/factory/pipeline.thin.yml`, `operator/kit/factory/pipeline.full.yml`, and the new `operator/kit/root.Makefile`.
   - Copied byte for byte from `planning/packs-draft/`: `operator/packs/c-host/Makefile`, `operator/packs/java-gradle/Makefile`, `operator/packs/java-gradle/TRAPS.md`, `operator/packs/java-gradle/CLAUDE.sections.md`, and the new `operator/packs/java-gradle/gitleaks.toml`. Removed `operator/packs/java-gradle/.gitleaks.toml`.
   - Left `operator/packs/java-gradle/scripts/trust-store.sh` as it was. It differs from the draft only by the SPDX licence header line, which the Interface keeps.
   - `diff -rq` against the drafts now shows only that header and the two `README.md` files, which exist only under `operator/`.

   Main choice: copy the drafts as files rather than edit the old files line by line, because the Interface asks for byte-for-byte copies. There was nothing to refactor.

   Results:
   - `uv run pytest -q tests/operator_scripts/`: all passed. This was the first run of the new tests against the finished files.
   - `make guides`: green.
   - `make check`: red at `make test`, with one failure:
     `FAILED tests/agent_files/test_claude_files.py::test_template_holds_only_the_rules_file_the_makefile_and_the_pipeline_definition`
     `E         Left contains one more item: 'root.Makefile'`
     `tests/agent_files/test_claude_files.py:173: AssertionError`

   Change asked of the tester: in `tests/agent_files/test_claude_files.py`, `test_template_holds_only_the_rules_file_the_makefile_and_the_pipeline_definition`, add `"root.Makefile"` to the expected kit listing, after `"factory/story-form.md"` (the list is sorted). The test fails only because of the new layout, so feature decision 36's leave covers the change; the tester's entry had left this file out because it uses only `pack_claude_md`, but this test lists the kit's files.

   Noticed, not touched: nothing else.
8. factory: started tests as self.
9. tester: Made the one test change the coder named in entry 7. The new layout broke this test and nothing else, so feature decision 36's leave covers it.

   - Changed: in `tests/agent_files/test_claude_files.py`, `test_template_holds_only_the_rules_file_the_makefile_and_the_pipeline_definition` now has `"root.Makefile"` in its expected listing of `operator/kit/`, after `"factory/story-form.md"` (the list is sorted). The test keeps its name, and it still checks that the kit holds only the listed files.
   - Why: the story adds `operator/kit/root.Makefile`, so the earlier listing failed with `Left contains one more item: 'root.Makefile'`. My entry 5 had wrongly left this file out, saying it uses only `pack_claude_md`; this test also lists the kit's files.
   - No other test was changed or removed.

   Test run (the single-file command from `CLAUDE.md`): `uv run pytest -q tests/agent_files/test_claude_files.py` passed all 22 tests. Every module imported.

   `lint`: lint: green (0.1 s)

   `lint`: lint: green (0.1 s)
10. factory: started doing as self.
11. coder: With the tester's change from entry 9 in place, `make check guides` is green. No code was changed in this run.

    - Built in entry 7: the human's drafts are copied byte for byte into `operator/kit/` (`CLAUDE.md`, `factory/README.md`, `factory/kit.mk`, `factory/pipeline.thin.yml`, `factory/pipeline.full.yml`, and the new `root.Makefile`) and into `operator/packs/` (`c-host/Makefile`, `java-gradle/Makefile`, `java-gradle/TRAPS.md`, `java-gradle/CLAUDE.sections.md`). `java-gradle/.gitleaks.toml` was renamed to `java-gradle/gitleaks.toml`. No module under `src/factory/` changed.
    - Checked again in this run:
      - `diff -rq` against `planning/kit-draft/` and `planning/packs-draft/` shows only `operator/kit/README.md` and `operator/packs/README.md`, which exist only under `operator/`, and `java-gradle/scripts/trust-store.sh`, which differs only by the SPDX licence header line the Interface keeps.
      - `uv run pytest -q tests/agent_files/test_claude_files.py`: all 22 tests passed.
      - `make check`: green, ending `check: green`, with 99.14 % coverage.
      - `make guides`: green.
    - Main choice: copy the draft files whole rather than edit the old files line by line, because the Interface asks for byte-for-byte copies. Rejected: hand edits, which risk drift from the drafts.
    - Refactor: nothing to refactor, because the diff holds only data files copied from the drafts.
    - What the journal changed: entry 9 added `root.Makefile` to the expected kit listing in one test, under the leave in feature decision 36. The meaning of the task did not change, so I left the Description as it is.
    - Noticed, not touched: nothing.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
12. factory: started review as self.
13. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'` against the work item. I read the code myself, including the helpers the tests call (`tests/support/kit_support.py`, `src/factory/agents/domain/write_paths.py:22-58`) and `tests/operator_scripts/test_packs.py`. I also ran `diff -rq` against `planning/kit-draft/` and `planning/packs-draft/`. It shows only the two `README.md` files that exist only under `operator/`, and the SPDX licence line of `java-gradle/scripts/trust-store.sh`, which the Interface keeps. So the data files are the drafts, unchanged.

    Findings:
    1. `tests/operator_scripts/test_one_layout.py:42-46` (`_write_stand_in`) and `:128-151` (inside `test_the_java_pack_calls_its_files_under_factory`) copy existing test helpers:
       - `_write_stand_in` copies `_stand_in` of `tests/operator_scripts/test_packs.py:58-63`: a `#!/bin/sh` script that logs `$(basename "$0") $*` and gets `chmod 0o755`.
       - The Java project setup copies `_stand_in_project` of `test_packs.py:66-85`: a committed `java-gradle` thin project, `gitleaks` on a `bin` PATH, `gradlew` in the project, a `home` folder, and the PATH and HOME variables.
       - The trust-store stand-in body and the bundle copy `test_the_java_sync_builds_the_trust_store_once_per_bundle` (`test_packs.py:190-200`).
       - Fix, under CLAUDE.md's standing leave to move a shared test helper: move `_stand_in` and `_stand_in_project`, with `PATH_TOOLS`, `PROJECT_TOOLS` and a helper that writes the trust-store stand-in, into a support module, for example `tests/support/pack_make_support.py`. Use them from both test files. Every earlier test keeps its name and what it checks, and the tester's entry names `test_packs.py` as changed.

    Everything else checked, with no finding:
    - Group 1, criteria:
      - Criterion 1: thin and full rows check both the value and the absence of a commented line.
      - Criterion 2: 3 packs × 2 lines; all faults empty; only `CLAUDE.md` and `Makefile` outside `factory/`; `Makefile` is `root.Makefile`.
      - Criterion 3: an own root makefile, read back from the committed repository byte for byte; no fault.
      - Criterion 4: real runs for no target, `lint` and `nosuch`, with no line naming `'Makefile'` in any row. The forwarded `check` recipe echoes without `@`, so `^check: green$` matches only the output line, not the echoed command.
      - Criterion 5: the stand-in sits only at `factory/scripts/trust-store.sh`, so a call to the old root path would fail the test. gitleaks is checked for `--config factory/gitleaks.toml`, and the refused side scans every pack file for both old paths.
      - Criterion 6: `protected_paths(definition.make_file)` covers both files for both lines. The root `Makefile` stays protected through `PROTECTED_PATHS`.
      - The assembly rule's other side (an own root makefile is kept) is criterion 3.
      - The journal reports `make check` green after the coder (entry 11).
    - Group 2, architecture: no module under `src/` changed. The diff holds only data files and tests.
    - Group 3, security: no secrets, no silencing markers. The gitleaks rules file is a pure rename (similarity 100 %).
    - Group 4, quality: beyond finding 1, the names fit and `kit_support.py`'s docstrings describe the one assembly.
    - Group 5, hygiene: the journal names the main choice (whole-file copies of the drafts, hand edits rejected). The Description matches what was built. The docs criterion still names what the documenter must write.

    Earlier tests (changed, not added):
    - `tests/support/kit_support.py`: the human's leave in feature decision 36, quoted in the Interface (assembly moved to the one layout; `brownfield=` replaced by `own_root_makefile=`).
    - `tests/operator_scripts/test_kit_files.py`: feature decision 36. Two assertions about the old commented `make_file` were removed because criterion 1 covers them. The other changed tests keep their names and what they check, with the makefile now at `factory/Makefile`.
    - `tests/operator_scripts/test_packs.py`: feature decision 36. `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready` was removed because criteria 2 and 3 cover it. The trust-store stand-in path moved to `factory/scripts/`.
    - `tests/agent_files/test_claude_files.py`: feature decision 36, as asked in entry 7 and made in entry 9 (`root.Makefile` added to the kit listing). Its only failure was the new layout.

    Decision: `tests`. The one finding needs a change only to this story's tests and the helpers moved under the standing leave.
14. factory: started tests as self.
15. tester: Answered the reviewer's one finding (entry 13) by moving the shared test helpers, under the standing leave in `CLAUDE.md` to move a shared test helper. No criterion's test changed what it checks.

    Finding 1 (copied stand-in helpers): answered by the new `tests/support/pack_make_support.py`, which holds:
    - `PATH_TOOLS` and `PROJECT_TOOLS`, moved from `test_packs.py`.
    - `stand_in`, which was `_stand_in` in `test_packs.py`.
    - `stand_in_project`, which was `_stand_in_project`: a committed thin project of the pack, with tool stand-ins logging to `tmp_path / "calls"`, plus the PATH and HOME variables.
    - `stand_in_trust_store`, new. It replaces the project's `factory/scripts/trust-store.sh` with a script that records its arguments and writes the store, and writes a certificate bundle. It returns the record's path and the bundle's.

    Earlier test file changed under the standing leave:
    - `tests/operator_scripts/test_packs.py`: removed `PATH_TOOLS`, `PROJECT_TOOLS`, `_stand_in` and `_stand_in_project`. Its tests now use `stand_in_project`. `test_the_java_sync_builds_the_trust_store_once_per_bundle` uses `stand_in_trust_store` instead of its inline stand-in and bundle. Every test keeps its name and what it checks.

    This story's test changed:
    - `tests/operator_scripts/test_one_layout.py`: removed `_write_stand_in`. `test_the_java_pack_calls_its_files_under_factory` now builds its project with `stand_in_project(tmp_path, "java-gradle", 0)` and `stand_in_trust_store`, then sets `SSL_CERT_FILE`. Its assertions are unchanged.

    Criteria → tests (unchanged since entry 5):
    - criterion 1: `tests/operator_scripts/test_one_layout.py::test_each_kit_pipeline_definition_names_the_factory_makefile`
    - criterion 2: `tests/operator_scripts/test_one_layout.py::test_a_one_way_project_is_ready_with_only_claude_md_and_makefile_outside_factory`
    - criterion 3: `tests/operator_scripts/test_one_layout.py::test_an_own_root_makefile_is_kept_byte_for_byte`
    - criterion 4: `tests/operator_scripts/test_one_layout.py::test_the_root_makefile_forwards_every_target_to_the_factory_makefile`
    - criterion 5: `tests/operator_scripts/test_one_layout.py::test_the_java_pack_calls_its_files_under_factory`
    - criterion 6: `tests/operator_scripts/test_one_layout.py::test_the_factory_makefiles_are_protected_for_every_role`
    - criteria 7 and 8: no test (`make check`, docs).

    Files:
    - Created: `tests/support/pack_make_support.py`.
    - Changed: `tests/operator_scripts/test_packs.py` and `tests/operator_scripts/test_one_layout.py`.

    Test run:
    - `uv run pytest -q tests/operator_scripts/test_one_layout.py tests/operator_scripts/test_packs.py`: all passed, and every module imported.
    - The layout and shared-helper guards also passed: `tests/guards/test_tests_layout.py`, `test_shared_imports.py`, `test_test_folder_readmes.py` and `test_shared_test_helpers.py`.
    - I did not run `make test` or `make check`; the coder runs them next.

    Open, for the documenter: `docs/project-guide/README.md` lists the shared test helpers, and it does not yet name `tests/support/pack_make_support.py`.

    `lint`: lint: green (0.1 s)

    `lint`: lint: green (0.1 s)
16. factory: started doing as self.
17. coder: Round 1. The tester's helper move (entry 15) answers the reviewer's one finding (entry 13), and every test passes against the data files from entry 7. I changed no code in this run, and the working tree is clean.

    - Built (entry 7, unchanged since):
      - The human's drafts are copied byte for byte into `operator/kit/`: `CLAUDE.md`, `factory/README.md`, `factory/kit.mk`, `factory/pipeline.thin.yml`, `factory/pipeline.full.yml`, and the new `root.Makefile`.
      - The same for `operator/packs/`: `c-host/Makefile`, `java-gradle/Makefile`, `java-gradle/TRAPS.md` and `java-gradle/CLAUDE.sections.md`.
      - `java-gradle/.gitleaks.toml` is renamed to `java-gradle/gitleaks.toml`.
      - No module under `src/factory/` changed.
    - Checked in this run:
      - `uv run pytest -q tests/operator_scripts/test_one_layout.py tests/operator_scripts/test_packs.py`: all passed.
      - `make check`: green, ending `check: green` (coverage 99.14 %).
      - `make guides`: green.
    - Main choice: whole-file copies of the drafts, because the Interface asks for byte-for-byte copies. I rejected hand edits of the old files, which risk drifting from the drafts.
    - Refactor: nothing to change. My diff holds only data files copied from the drafts.
    - What the journal changed: entries 13 and 15 changed only the tests: the shared stand-in helpers moved to `tests/support/pack_make_support.py`. The meaning of the task did not change, so I left the Description as it is.
    - Noticed, not touched: the tester's open point for the documenter still stands. `docs/project-guide/README.md` does not yet name `tests/support/pack_make_support.py`.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
18. factory: started review as self.
19. reviewer: Round 1 review of `git diff develop...HEAD -- . ':!factory'`. I read the diff against the work item and the code the tests call: `tests/support/kit_support.py` (`run_kit_make` at :127-142 runs with `merge_stderr=True`), `tests/support/kit_make_support.py` (`green_line`), the new `tests/support/pack_make_support.py`, and `src/factory/agents/domain/write_paths.py:22-58`. I also ran `diff -rq` against `planning/kit-draft/` and `planning/packs-draft/`. It shows only the two `README.md` files that exist only under `operator/`, and `java-gradle/scripts/trust-store.sh`, which differs only by the licence header line the Interface keeps.

    no findings

    Round 0's finding 1 (copied stand-in helpers) is answered. `_stand_in`, `_stand_in_project`, `PATH_TOOLS` and `PROJECT_TOOLS` moved to `tests/support/pack_make_support.py`, and a shared `stand_in_trust_store` was added there. Both `test_packs.py` and `test_one_layout.py` use them, and no copy is left in either file.

    Checked, with no finding:
    - Group 1, acceptance criteria:
      - Criterion 1: thin and full rows check both the value `factory/Makefile` and that no line is a commented `make_file`.
      - Criterion 2: 3 packs × 2 lines. All faults are empty, the only files outside `factory/` are `CLAUDE.md` and `Makefile`, and `Makefile` is `root.Makefile`.
      - Criterion 3: the own root `Makefile` is read back from the committed repository byte for byte, and there is no fault.
      - Criterion 4: real runs for no target, `lint` and `nosuch`. stderr is merged into the output, so a "No rule to make target 'Makefile'" from a remake through `%:` would be caught by `MAKEFILE_TARGET`. The echoed `check` recipe line does not match the anchored `^check: green$`.
      - Criterion 5: the trust-store stand-in exists only at `factory/scripts/trust-store.sh`, so a call to the old root path would fail. gitleaks is checked for `--config factory/gitleaks.toml`. The refused side scans every pack file for both old paths, and `\.gitleaks\.toml` does not match `factory/gitleaks.toml`.
      - Criterion 6: `factory/kit.mk` is protected through `KIT_MAKEFILE` and `factory/Makefile` through `make_file`, for both lines. `protected_paths` is one list for every role, so the row per line covers every role.
      - Journal entry 17 reports `make check` green after the coder.
    - Group 2, architecture: no module under `src/` changed. The diff holds only data files and tests.
    - Group 3, security: no secrets and no silencing markers. The gitleaks rules file is a pure rename (R100).
    - Group 4, quality: names and docstrings of the new support module fit, and there is no dead code.
    - Group 5, work item hygiene: the journal names the main choice (whole-file copies of the drafts; hand edits rejected). The Description matches what was built, and the docs criterion still names what the documenter must write.
    - Documents: the diff changes no document the documenter writes. The kit's `CLAUDE.md` and `factory/README.md` are kit data and are the drafts unchanged.

    Open point for the documenter (from entries 15 and 17; not a finding): `docs/project-guide/README.md` does not yet name `tests/support/pack_make_support.py` among the shared test helpers.

    Earlier tests (changed, not added):
    - `tests/agent_files/test_claude_files.py`: feature decision 36 (the human's leave quoted in the Interface), asked for in entry 7 and made in entry 9. `root.Makefile` was added to the kit listing; the new layout was its only failure.
    - `tests/operator_scripts/test_kit_files.py`: feature decision 36. Two assertions about the old commented `make_file` were removed because criterion 1 covers them. The makefile is now at `factory/Makefile`, and the tests keep their names and what they check.
    - `tests/operator_scripts/test_packs.py`: feature decision 36 removed `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready`, which criteria 2 and 3 cover. The standing leave to move a shared test helper covers the move of `PATH_TOOLS`, `PROJECT_TOOLS`, `_stand_in`, `_stand_in_project` and the trust-store stand-in to `tests/support/pack_make_support.py`. Every remaining test keeps its name and what it checks.
    - `tests/support/kit_support.py`: feature decision 36 (one assembly; `brownfield=` replaced by `own_root_makefile=`).
20. factory: started docs as self.
21. documenter: Round 1 docs. I wrote what the docs criterion asks for: the one layout, everywhere a project's assembly is described. No findings for the coder: the data files are the drafts, and the behaviour I describe matches what I ran.

    Files changed:
    - `operator/kit/README.md`:
      - Rewrote the assembly steps. Step 4 now writes `factory/Makefile`, which both definitions name with `make_file`. The new step 5 copies `root.Makefile` as `Makefile` only when the repository has no root `Makefile` of its own; otherwise the `CLAUDE.md` wording for `make -f factory/Makefile <target>` applies. Steps 6 and 7 cover the write paths and the check; the check's missing-makefile fault is now `factory/Makefile is missing`.
      - Added how to run a target by hand, and a paragraph on the one layout.
      - Removed the old "existing repository" paragraph with the commented `make_file`.
      - The `kit.mk` default goal bullet now names the forwarding makefile.
      - The Files table has a `root.Makefile` row, and the Tests section names `test_one_layout.py`.
    - `operator/packs/README.md`:
      - Replaced the fresh-start and existing-repository paths with one way: every pack file but `CLAUDE.sections.md` and `TRAPS.md` goes into `factory/` at the same path, and `root.Makefile` goes to the root only when the repository has no `Makefile` of its own. Also covers the `## Checks` wording in `CLAUDE.md` and running a target by hand.
      - The Files table now has `factory/Makefile`, `gitleaks.toml` → `factory/gitleaks.toml`, and `factory/scripts/trust-store.sh`.
      - The new-pack paragraph says the makefile names its files under `factory/` and points to `test_one_layout.py`.
    - `docs/operator-guide/start-a-project.md`:
      - Added a layout paragraph and how to run a target by hand.
      - Step 3: the pack's files go to `factory/`, plus `root.Makefile` and when to copy it. Step 5: the `CLAUDE.md` line for `make -f factory/Makefile`.
      - Rewrote the firmware example for the new layout. The `make_file` sed step is gone, and the first check now fails only on write paths; I ran this output myself.
      - "What the project owns afterwards" now names the forwarding `Makefile` and the pack's files under `factory/`.
    - `docs/operator-guide/pipeline.md`:
      - *Name the makefile*: the kit's definitions name `factory/Makefile` for every project, and a new bullet covers running by hand, `root.Makefile` and the `CLAUDE.md` line for a repository with its own root `Makefile`.
      - The `factory-check-project` example now writes the broken Python makefile to `my-project/factory/Makefile`. Its old root `Makefile` would now give `factory/Makefile is missing`.
    - `docs/decisions.md`: new entry "A project holds `CLAUDE.md` and the `factory/` folder, and nothing else of the factory's" (2026-11-17, F0062-S0013), with the decision, its price, its gain and why. It has no "Rejected" line, because the story names no rejected option.
    - `docs/project-guide/operator.md`: changed the packs bullet's assembly wording from "at the root or brownfield" to the one way, and added `test_one_layout.py` and `pack_make_support.py`.
    - `docs/project-guide/README.md`: added `tests/support/pack_make_support.py` to the list of shared test helpers. This was the open point in entries 15, 17 and 19.

    Checks run:
    - Smoke block 2 (the forwarding makefile): printed `lint: green` and then `check: green`. `make -f factory/Makefile lint` alone also printed its green line.
    - `make documents`:
      - The first run found bare `factory/...` paths, which the check reads as repository paths. I rewrote them as `<project>/factory/...`, as the guides already do.
      - The final run ended `documents ok (48.0 s)`.
    - `make check`: green (coverage 99.14 %). I ran it because the operator READMEs are outside `docs/`.
    - `make guides`: green.

    Cross-read and found current:
    - `docs/operator-guide/site.md`: its link to the pack's `trust-store.sh` under `operator/packs/` is still right.
    - `docs/operator-guide/agent-runtime.md`, `docs/project-guide/agents.md` (protected paths, `protected_paths('factory/Makefile')` example), `docs/project-guide/pipeline.md`, `docs/project-guide/machine.md`, `README.md`.
    - The C traps line in `start-a-project.md` ("factory's makefile at `<project>/factory/Makefile`").

    Stale text noticed, not touched:
    - `docs/project-guide/README.md` does not list `tests/support/kit_support.py` among the shared helpers, though the page says it names every module of `tests/support/`. This predates this story.

    `guides`: guides: green (9.5 s)
    `secrets`: secrets: green (2.1 s)
    `documents`: documents ok (48.2 s)
