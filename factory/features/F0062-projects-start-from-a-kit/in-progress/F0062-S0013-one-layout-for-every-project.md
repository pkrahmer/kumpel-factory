---
stage: tests
blocked: null
round: 0
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
