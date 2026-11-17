---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 698
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-17T05:00:35.525566Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-17T05:07:57.964541Z'
  stage: acceptance
  run: d6a9e67795f44421820f0ac5e60dffea
- number: 3
  speaker: factory
  kind: done
  at: '2026-11-17T05:09:48.954338Z'
  stage: done
stories: [F0062-S0001, F0062-S0002, F0062-S0003, F0062-S0004, F0062-S0005, F0062-S0006, F0062-S0007, F0062-S0008]
outcome: accepted
---

# Acceptance of Projects start from a kit and a stack pack

## Recommendation

`accepted with stories`. Every scope item has a story, `make check` is green as found, and the feature's smoke test is green: a project assembled from the kit and each of the three packs is `project: ready` on both lines, with the factory's makefile at the root or at `factory/Makefile` next to a root `Makefile` of the project's own. The findings are small and none breaks a promise: a stale sentence and a missing decision in the documents, a named makefile and `kit.mk` that no protected path covers, and the reviewers' notes on the feature's tests.

## 1 Scope

None. Each of the five scope items has its story: the static check (S0001), `make_file` (S0002), the live check `--run` (S0003), the installed `builder` and the reviewer's `## Review` (S0004), the kit (S0005), the packs `python`, `c-host` and `java-gradle` (S0006), the guide (S0008). S0007 (removing `operator/template/`) is outside the original list but inside the Goal, and decision 22 added it. The Goal's "without a change to its own Makefile" holds: `make_file: factory/Makefile` runs every project command and start fact as `make -f factory/Makefile` (`src/factory/pipeline/domain/pipeline_definition.py:105`, `src/factory/pipeline/application/project_check.py:118`). No story touches an out-of-scope item: the guide calls starters and the onboarding pull request not existing yet. The human's change 3 (the three starters, built from the kit and a pack and checked with `--run`) is the human's and not judged here.

## 2 Feature smoke test

Run from `/work/checkout` with the installed console script. For each pack, each line and each makefile placement, the script did what `docs/operator-guide/start-a-project.md` says: copy the kit, keep one line as `factory/pipeline.yml`, copy the pack's makefile (to the root, or to `factory/Makefile` next to a project-owned root `Makefile`, with `make_file` uncommented), copy the stage file and other pack files, commit, then check. It then checked the kit alone, an uncommitted fix, and the kit's start facts through the brownfield makefile. The script ran in a `mktemp -d` folder, which it removed.

The script, `smoke.sh`, as run:

```bash
#!/usr/bin/env bash
set -u
F=/work/checkout; CHECK=$F/.venv/bin/factory-check-project
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
commit() { git -C "$1" add -A && git -C "$1" -c user.name=t -c user.email=t@example.com commit -q -m "$2"; }
assemble() { # $1 project, $2 pack, $3 line, $4 makefile place (root|factory)
  p=$1; mkdir -p "$p/factory" "$p/src" "$p/tests" "$p/docs"; git init -q -b develop "$p"
  touch "$p/src/main.x" "$p/tests/t.x" "$p/docs/index.md" "$p/README.md"
  cp $F/operator/kit/factory/* "$p/factory/"; cp $F/operator/kit/CLAUDE.md "$p/"
  mv "$p/factory/pipeline.$3.yml" "$p/factory/pipeline.yml"; rm -f "$p/factory/pipeline."{thin,full}.yml
  if [ "$4" = root ]; then cp $F/operator/packs/$2/Makefile "$p/"; else
    printf 'all:\n\techo own\n' > "$p/Makefile"; cp $F/operator/packs/$2/Makefile "$p/factory/Makefile"
    sed -i 's|^# make_file: factory/Makefile|make_file: factory/Makefile|' "$p/factory/pipeline.yml"; fi
  [ -f $F/operator/packs/$2/stage.Containerfile ] && cp $F/operator/packs/$2/stage.Containerfile "$p/factory/"
  [ -d $F/operator/packs/$2/scripts ] && cp -r $F/operator/packs/$2/scripts "$p/"
  [ -f $F/operator/packs/$2/.gitleaks.toml ] && cp $F/operator/packs/$2/.gitleaks.toml "$p/"
  commit "$p" assemble
}
for pack in python c-host java-gradle; do for line in thin full; do for place in root factory; do
  p=$d/$pack-$line-$place; assemble "$p" $pack $line $place
  echo "### $pack, $line line, makefile at $place"
  (cd $F && $CHECK --agent-home agents "$p"); echo "exit $?"
done; done; done
echo "### the kit alone (no pack): not ready but for the stack's targets"
p=$d/kit-only; mkdir -p $p/factory $p/src $p/tests $p/docs; git init -q -b develop $p; touch $p/src/a $p/tests/a $p/docs/a $p/README.md
cp $F/operator/kit/factory/* $p/factory/; cp $F/operator/kit/CLAUDE.md $p/; mv $p/factory/pipeline.thin.yml $p/factory/pipeline.yml; rm $p/factory/pipeline.full.yml
printf 'include factory/kit.mk\n' > $p/Makefile; commit $p kit
(cd $F && $CHECK --agent-home agents "$p"); echo "exit $?"
echo "### an uncommitted fix does not count"
printf 'include factory/kit.mk\nsync lint test check:\n\techo $@\n' > $p/Makefile
(cd $F && $CHECK --agent-home agents "$p" | tail -1); commit $p fix; (cd $F && $CHECK --agent-home agents "$p" | tail -1)
echo "### the kit's start facts through the brownfield makefile"
p=$d/python-full-factory; git init -q --bare $d/remote.git; git -C $p remote add origin $d/remote.git; git -C $p push -q origin develop
git -C $p checkout -q -b work-item/x; echo 'print(1)' > $p/src/new.py; commit $p change
(cd $p && make --no-print-directory -f factory/Makefile facts-changes; make --no-print-directory -f factory/Makefile facts-files | head -3; make -s -f factory/Makefile facts-diff | head -2)
echo "### --run on this machine (no stage environment here)"
(cd $F && $CHECK --run --agent-home agents "$d/c-host-thin-root" 2>&1 | tail -3); echo "exit $?"
```

Its output:

```console
$ bash smoke.sh
### python, thin line, makefile at root
pipeline definition: ok
makefile: ok
stage file: ok
agents: ok
write paths: ok
forms: ok
project: ready
exit 0
### python, thin line, makefile at factory
... the same seven lines, exit 0
### python, full line, makefile at root          -> project: ready, exit 0
### python, full line, makefile at factory       -> project: ready, exit 0
### c-host, thin line, makefile at root          -> project: ready, exit 0
### c-host, thin line, makefile at factory       -> project: ready, exit 0
### c-host, full line, makefile at root          -> project: ready, exit 0
### c-host, full line, makefile at factory       -> project: ready, exit 0
### java-gradle, thin line, makefile at root     -> project: ready, exit 0
### java-gradle, thin line, makefile at factory  -> project: ready, exit 0
### java-gradle, full line, makefile at root     -> project: ready, exit 0
### java-gradle, full line, makefile at factory  -> project: ready, exit 0
### the kit alone (no pack): not ready but for the stack's targets
pipeline definition: ok
makefile: FAIL: no target check; no target lint; no target test; no target sync
stage file: ok
agents: ok
write paths: ok
forms: ok
project: not ready (4 faults)
exit 1
### an uncommitted fix does not count
project: not ready (4 faults)
project: ready
### the kit's start facts through the brownfield makefile
A	src/new.py
CLAUDE.md
Makefile
README.md
 src/new.py | 1 +
 1 file changed, 1 insertion(+)
make: *** [factory/kit.mk:30: facts-diff] Broken pipe
### --run on this machine (no stage environment here)
cannot run: FACTORY_REPOSITORY_URL: missing
exit 0
```

(The last `exit 0` is the status of `tail`, not of the check.)

Each of the twelve "ready" blocks printed the same seven lines as the first; they are shortened above to one line each. The `Broken pipe` comes from the script's `| head -2` on `facts-diff`, not from `kit.mk`. `facts-changes` and `facts-files` leave out `factory/`, as `kit.mk` says. The live part (`--run`) cannot run in this container, which has no instance environment and no podman. It refused before it built anything, as decision 12 says it should. A second `--run` attempt, to read its exit status, was refused by the shell's permissions. The live part was run on factory-vm2 by the human (decision 23: all nine points `ok` for the C and the Java pack). Green.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- S0002 documenter: `PROTECTED_PATHS` (`src/factory/agents/domain/write_paths.py:22`) protects `Makefile` but not the makefile that `make_file` names. It also does not protect `factory/kit.mk`, which the kit's README says a project never edits. A role whose write paths cover `factory/*` could change the factory's own targets. The kit's write paths do not cover it today, so this is a hole, not a fault. Proposed: F0062-S0010.
- S0003 documenter: `docs/operator-guide/pipeline.md:219` still says "Until the command is installed as a console script, run it … as `uv run python -m factory.entry.check_project`". `pyproject.toml:19` has declared `factory-check-project` since the human's change 1. Still stale. Proposed: F0062-S0009.
- S0003 documenter: the decision log's entry *The conformance check is a command of its own* (`docs/decisions.md:1720`) says the check "starts no container and runs no project command". No later entry records the live part (feature decisions 12, 13 and 17: a temporary clone, the image `<stage image>-check`, live points only after a clean static part). Proposed: F0062-S0009.
- S0003 coder and reviewer: the entry tests monkeypatch `build_project_run`, so no test reaches the real wiring of `extra_environment` and `ca_bundle` in `src/factory/entry/check_project.py`. The use case's handling of both is tested. Not proposed: the human's VM runs exercised it, and a test of the wiring needs a stage environment.
- S0001 reviewer: no row of `tests/pipeline/application/test_project_check_run.py` has a definition that already names `sync` in `project_commands`. The code handles it (`project_check.py:124`). Proposed in F0062-S0011.
- S0001 coder: `_Makefiles.read` uses `list.pop(0)` as a queue. Harmless for a handful of includes. Not proposed.
- S0002 reviewer: `_assert_named` in `tests/machine/adapters/test_make_commands_make_file.py:74-82` checks only that `-f` appears somewhere, not that it is passed to the sync and to the command. Proposed in F0062-S0011.
- S0004 reviewer: `tests/agent_files/test_installed_builder.py:65` has two assertions on the same heading. Proposed in F0062-S0011.
- S0005 reviewer: in `tests/pipeline/application/test_project_check_make_file.py:28`, the annotation exists mainly to satisfy the areas guard. Harmless. Not proposed.
- S0006 reviewer: `_instructions` in `tests/operator_scripts/test_packs.py:94` is a second copy of the private `_instructions` of `tests/support/dockerfile_support.py:61`. `_stand_in` partly overlaps `recording_stand_in`. Proposed in F0062-S0011 (`_instructions`).
- S0006 coder: `planning/packs-draft/java-gradle/scripts/trust-store.sh` has no licence header, unlike the pack's copy. `planning/` is the human's, so it is listed under 6 and not proposed.
- S0007 documenter and coder: `docs/brochure/README.md:459` still says "A new project starts from the **template**". The brochure is dated (v1.1, November 2026), so it is listed under 6.
- S0007 (by keeping the names under leave 25): `tests/agent_files/test_template_makefile.py`, `test_template_makefile_header.py` and `test_template_sync.py` now test the kit and the Python pack under the old names. S0008: the guard `test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics` now checks eleven topics. Proposed in F0062-S0011.
- S0007 smoke tester: `make layers` crashed once with exit 139 (a segmentation fault of import-linter) in the factory's check, then passed on the rerun. It did not happen in my `make check`. Not proposed; the human should watch for it.

## 5 Documentation

Read from `README.md` through `docs/operator-guide/README.md`, `start-a-project.md`, `pipeline.md` (*Checking a repository before the factory runs it*), `agent-runtime.md`, `operator/kit/README.md` and `operator/packs/README.md`. The path from the newcomer's `README.md` to the new page is direct, and the template is named nowhere a reader would follow, except `docs/brochure/README.md:459`, which is dated. Two findings, neither one misleading a user into a wrong result:

- `docs/operator-guide/pipeline.md:219` is stale: the console script exists (see 4). The text is also uneven. Step 7 of `start-a-project.md` and the prose of `pipeline.md` say `factory-check-project`, but every runnable example on both pages runs `python -m factory.entry.check_project` (`start-a-project.md:49,74`, `pipeline.md:234`), and no sentence says why. The likely reason is that the document check runs the examples in the factory's checkout.
- `docs/decisions.md` has no entry for the live check's lasting choices (decisions 12, 13 and 17 of `feature.md`), while the S0001 entry says the check starts no container.

`pipeline.md`'s list of protected paths matches the code. If F0062-S0010 is accepted, that list changes with it.

## 6 Decisions taken for the human

From `feature.md` (*Decisions taken for the human*, 1 to 30), the ones with lasting effect to accept or revisit:

1. The check is a console command of its own, not a preflight item (2). It reads the commit at `HEAD`, never the work tree (6).
2. A project without `factory/stage.Containerfile` passes the point `stage file` (7).
3. `make_file` is contract 1.2, but 1.2 is not enforced: 1.0 and 1.1 definitions holding it load (8). The records contract rose to 4.6 (16).
4. `ProjectCommands` and `StageEnvironment` keep their signatures. The make-calling classes ask a `MakeFileSource` at every call (9).
5. `--run` works on a temporary clone with the image `<stage image>-check`, needs an instance's settings, and runs live points only after a clean static part (12, 13). The live sync runs only the make part of the sync script (17).
6. The installed builder's text is the Spring template's builder without its stack's words, opening with the boundary sentence (14, 21).
7. The kit and the packs are the human's wording from `planning/kit-draft/` and `planning/packs-draft/`, copied unchanged. The only exception is the licence header of `scripts/trust-store.sh` (18, 23). The draft still lacks that header (see 4).
8. The Java pack's stage file holds the JDK and gitleaks only (no Pub/Sub emulator). The C pack uses gitleaks and the stage image's clang-format (24).
9. The packs hold no application source (3).
10. The guide is an operator-guide page, not a project-guide page (26).
11. Left open for the human: whether `docs/brochure/README.md` (dated v1.1) should stop naming the template, and whether the three template-named test modules should be renamed (proposed in F0062-S0011).

Earlier tests changed, each with its leave as the reviewers' entries name it:

- S0001: `tests/guards/test_agent_home_wiring.py` (decision 15's leave); `tests/guards/test_areas.py` (decision 4).
- S0002: `tests/pipeline/domain/test_contract.py`, `tests/shared/domain/test_contract_version_4.py`, `tests/shared/domain/test_contract_version_4_2.py` (decision 16's leave, 4.5 → 4.6); `tests/guards/test_agent_home_wiring.py` (the standing leave to move a shared helper, `called_name`).
- S0003: `tests/entry/test_check_project.py` (`USAGE`) and `tests/guards/test_make_search.py` (decision 20's two leaves).
- S0004: `tests/agent_files/test_claude_agent_texts.py`, `test_claude_agent_texts_review_groups.py`, `test_claude_files.py`, `test_shared_rules_system_prompt.py`, `test_shared_start_agent_files.py`, and `tests/support/shipped_agents.py` (leave 11 and its extension in decision 21; the standing leave for `REVIEW_POINTS_SUBSECTION`).
- S0005: `tests/pipeline/application/test_project_check_make_file.py` and `test_project_check_run.py` (the standing leave, `run_project_check`).
- S0006: `tests/operator_scripts/test_kit_files.py` (the standing leave, `WRITTEN_FILES` and `project_faults`).
- S0007: every test that read `operator/template/`, among them `tests/README.md`, `tests/agent_files/test_claude_files.py`, `test_template_makefile.py`, `test_template_makefile_header.py`, `test_template_sync.py`, `test_demo_makefile_secrets.py`, `test_claude_agent_texts_mutants.py`, and `tests/guards/test_license_headers.py`, `test_pins.py`, `test_root_operator_folders_removed.py`, `test_working_branch_in_agent_texts.py` (decision 25).
- S0008: `tests/support/check_documents_support.py` and `tests/shared/domain/test_documents_guide_files.py` (decision 30).

No earlier test was changed without a named leave.

## 7 Slow checks

The project offers nothing beyond `make check` but `make mutants` (check 3); `make duplicates` and `make documents` are records and docs-stage checks, not slow checks. `make check` as found: `check: green`, `test: green (110.7 s)`, coverage 99.14 %. The slowest tests in `.reports/junit.xml`: `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other` (20.0 s), then five tests at 10.0 s each, the ten-second `ROOMY_LIMIT` kills (`test_podman_timeout_status` twice, `test_document_examples`, `test_claude_runtime_resume`, `test_claude_runtime_provider_limit`). None of them is the feature's.

Disk: `/srv/factory/self` went from 72.3 GB free at this stage's start to 71.7 GB now, with its own use unchanged at 1.2 GB. `/srv/factory/self/state` and `/tmp` lost the same 0.6 GB of free space, so they share one pool. The feature's committed changes are text and do not explain it. My `make check` writes coverage and pytest caches into the dataset, but the dataset's used figure did not move, so the 0.6 GB lies elsewhere in the shared pool, perhaps container storage. Small, but unexplained.

## 8 Cost

The eight stories cost 96 runs, 199.4 min, 841 turns and $34.05, about $4.26 a story. By story: S0001 14 runs / $5.29, S0002 13 / $5.14, S0003 14 / $6.53, S0004 10 / $3.26, S0005 12 / $3.48, S0006 10 / $3.37, S0007 12 / $4.09, S0008 11 / $2.91.

S0003 stands out at $6.53, with the tester and the coder at about $2.1 each. Its journal shows why: the live check touched the sync script, the stage environment's check scripts and the make search guard. The coder had to ask for two leaves (decision 20) and a `PLR0913` exception, and the first round's tests needed rework for the "not printed" side. S0001 and S0002 each needed a review round. S0007 needed a rework round for a one-time import-linter segfault that was not the story's.

Human interventions: 12 questions answered, all of cause `question`. Five came from intake, five from the coder, one from the documenter and one from the reviewer. The stories waited 1.9 h for the answers. S0001 waited 102 min for its intake question, which was asked at night (journal entries 3 to 4). Every other story waited under 3 minutes. S0001 needed the human most: two questions (intake's six test rows and the tab after `include`, then the coder's leave for the agent home wiring guard).

## Proposed stories

- `F0062-S0009-the-check-s-documents-catch-up.md`: removes the stale console-script sentence, explains why the examples run the module, and records the live check's decisions in the decision log (check 5).
- `F0062-S0010-the-named-makefile-is-protected.md`: protects the makefile that `make_file` names and the kit's `factory/kit.mk` from every role's writes, as `Makefile` already is (check 4).
- `F0062-S0011-the-kit-s-tests-are-tidied.md`: the reviewers' notes on the feature's tests: the missing `sync` row, `_assert_named`, the duplicate assertion, the second `_instructions`, and test names that still say template or ten topics (check 4).


## Journal

1. factory: started acceptance as self.
2. acceptance-reviewer: accepted with stories; 3 stories proposed (F0062-S0009, F0062-S0010, F0062-S0011)

   1 Scope: none. Each scope item has its story. S0007 was added by decision 22 and fits the Goal. A brownfield repository works without changing its own root Makefile, through `make_file`.
   2 Feature smoke test: green. For each of the three packs, both lines (thin and full) and both makefile places (root, or `factory/Makefile` with `make_file`), the guide's assembly gives `project: ready`, exit 0: twelve combinations in all. The kit alone gives `not ready (4 faults)`, which are exactly the stack's four targets. An uncommitted fix does not count; the same fix committed passes. The kit's start facts run through the named makefile. `--run` cannot run in this container, which has no instance environment: it refused before building anything. The human ran it on factory-vm2.
   3 Mutation testing: by sweep, not run here.
   4 Noticed:
   - `PROTECTED_PATHS` leaves out the makefile `make_file` names and `factory/kit.mk` (S0010).
   - `pipeline.md:219`'s console-script sentence is stale (S0009).
   - No decision-log entry exists for `--run` (S0009).
   - The reviewers' test notes (S0011): the missing `sync` row, the weak `_assert_named`, a duplicate assertion, a second copy of `_instructions`, and test names that still say template or ten topics.
   - Not proposed: the untested real wiring of `ca_bundle`, the one-time import-linter segfault, `list.pop(0)`, and a draft without a licence header.
   5 Documentation: coherent from `README.md` to the new `start-a-project.md`. The examples run `python -m factory.entry.check_project` while the prose says `factory-check-project`, and no sentence explains the difference. The decision log still says the check starts no container. `docs/brochure/README.md:459` (dated v1.1) still names the template, which is the human's call.
   6 Decisions for the human: ten lasting ones from `feature.md` are listed in the report. Every earlier test changed names its leave; none was changed without one.
   7 Slow checks: nothing beyond `make check`, which is green (test 110.7 s, coverage 99.14 %). The slowest test is `test_documents_marker` at 20 s. Disk: 0.6 GB less free on the shared pool, with the dataset's used unchanged at 1.2 GB. The feature does not explain it.
   8 Cost: 96 runs, $34.05, about $4.26 a story. S0003 stands out at $6.53 (two leaves and a `PLR0913` exception, plus test rework). 12 questions were answered, 1.9 h waited. S0001 needed the human most: 2 questions, one of which waited 102 minutes overnight.
3. factory: done (pull request merged); cost: 1 runs, 7.3 min, 42 turns, 91275 tokens in (2425230 more from cache), 30026 out, $1.54
