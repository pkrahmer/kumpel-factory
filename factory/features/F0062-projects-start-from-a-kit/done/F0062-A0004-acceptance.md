---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 706
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-17T07:17:21.776976Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-17T07:23:53.360520Z'
  stage: acceptance
  run: 7d71eb114a8b4f4d99729c678b85dd04
- number: 3
  speaker: factory
  kind: done
  at: '2026-11-17T07:24:42.181300Z'
  stage: done
stories: [F0062-S0001, F0062-S0002, F0062-S0003, F0062-S0004, F0062-S0005, F0062-S0006, F0062-S0007, F0062-S0008, F0062-S0009, F0062-S0010, F0062-S0011, F0062-S0012, F0062-S0013]
outcome: accepted
---

# Acceptance of Projects start from a kit and a stack pack

## Recommendation

`accepted with stories`. S0013, the one story since the third acceptance, delivers the one layout the human asked for (decision 36). For each of the three packs and both lines, with and without a root `Makefile` of the project's own, the guide's assembly gives `project: ready`, with only `CLAUDE.md` and `Makefile` outside `factory/`. `factory/Makefile`, `factory/kit.mk` and `Makefile` are protected, and `make check` is green as I found it. Two findings are worth a story, and neither is a broken promise of `feature.md`. First, the kit's forwarding `root.Makefile` silently skips a target when a file or folder at the root has its name: with a `test/` folder, `make test` prints `'test' is up to date.` and exits 0. The factory's own gates are not affected, because they run `make -f factory/Makefile`. Second, two pages outside S0013's docs criterion still describe the layouts before it, and the project guide's index misses eight shared test helpers.

## 1 Scope

None. The first three acceptances found every scope item covered by S0001 to S0012. S0013 comes from the human's decision 36, taken after the third acceptance. It changes only data files under `operator/kit/` and `operator/packs/`, the tests and the documents; no module under `src/factory/` changes. It belongs to the scope items "the makefile a pipeline definition names", "the kit, and the stack packs" and "the guide for a fresh start and for a brownfield repository". A brownfield repository still needs no change to its own `Makefile` (criterion 3 of S0013, and check 2 below), so the Goal's promise holds in the new layout. The human's change 3 (the three starters) is the human's and is not judged here.

## 2 Feature smoke test

The walk-through of the earlier acceptances, moved to the one layout. It assembles a project exactly as `docs/operator-guide/start-a-project.md` says: the kit into `factory/`, every pack file but the two pages into `factory/` at the same path, and `root.Makefile` as `Makefile` only where the repository has no root makefile of its own. It does this for every pack, both lines, and with and without the project's own root `Makefile`, then checks each project with the installed `factory-check-project`. Then it does the following:

- asks the factory's definition reader and `protected_paths` what a role widened to `factory/*`, `src/*` and `*` may write;
- checks the kit alone, then an uncommitted and a committed fix;
- runs the forwarding makefile by hand, with a folder named after a target and without;
- runs the start facts through the forwarding makefile;
- tries `--run`.

Everything ran in `mktemp -d` folders that remove themselves.

`smoke.sh`:

```bash
#!/usr/bin/env bash
set -u
F=/work/checkout; CHECK=$F/.venv/bin/factory-check-project; S=$(dirname "$0")
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
unset MAKEFLAGS MAKELEVEL MFLAGS
commit() { git -C "$1" add -A && git -C "$1" -c user.name=t -c user.email=t@example.com commit -q -m "$2"; }
assemble() { # $1 project, $2 pack, $3 line, $4 own root makefile (own|none) -- as start-a-project.md says
  p=$1; mkdir -p "$p/factory" "$p/src" "$p/tests" "$p/docs"; git init -q -b develop "$p"
  touch "$p/src/main.x" "$p/tests/t.x" "$p/docs/index.md" "$p/README.md"
  [ "$4" = own ] && printf 'all:\n\techo own\n' > "$p/Makefile"
  cp $F/operator/kit/factory/* "$p/factory/"; cp $F/operator/kit/CLAUDE.md "$p/"
  mv "$p/factory/pipeline.$3.yml" "$p/factory/pipeline.yml"; rm -f "$p/factory/pipeline."{thin,full}.yml
  (cd $F/operator/packs/$2 && find . -type f ! -name CLAUDE.sections.md ! -name TRAPS.md) | while read -r f; do
    mkdir -p "$p/factory/$(dirname "$f")"; cp "$F/operator/packs/$2/$f" "$p/factory/$f"; done
  [ -f "$p/Makefile" ] || cp $F/operator/kit/root.Makefile "$p/Makefile"
  commit "$p" assemble
}
for pack in python c-host java-gradle; do for line in thin full; do for own in none own; do
  p=$d/$pack-$line-$own; assemble "$p" $pack $line $own
  out=$(cd $F && $CHECK --agent-home agents "$p"); rc=$?
  outside=$(git -C "$p" ls-files | grep -v -e '^factory/' -e '^src/' -e '^tests/' -e '^docs/' -e '^README.md$' | tr '\n' ' ')
  echo "$pack, $line, root makefile $own: $(echo "$out" | grep -c ': ok$') ok, $(echo "$out" | tail -1), exit $rc; outside factory/: $outside"
done; done; done
echo "### protection (a role widened to factory/*, src/* and *)"
(cd $F && uv run --quiet python $S/protect.py $d/python-full-none $d/java-gradle-thin-own)
echo "### the kit alone: not ready but for the stack's targets"
p=$d/kit-only; mkdir -p $p/factory $p/src $p/tests $p/docs; git init -q -b develop $p; touch $p/src/a $p/tests/a $p/docs/a $p/README.md
cp $F/operator/kit/factory/* $p/factory/; cp $F/operator/kit/CLAUDE.md $p/; cp $F/operator/kit/root.Makefile $p/Makefile
mv $p/factory/pipeline.thin.yml $p/factory/pipeline.yml; rm $p/factory/pipeline.full.yml; commit $p kit
(cd $F && $CHECK --agent-home agents "$p"); echo "exit $?"
echo "### an uncommitted factory/Makefile does not count, the committed one does"
printf 'include factory/kit.mk\nsync lint test check:\n\techo $@\n' > $p/factory/Makefile
(cd $F && $CHECK --agent-home agents "$p" | tail -1); commit $p fix; (cd $F && $CHECK --agent-home agents "$p" | tail -1)
echo "### root forwarding makefile, by hand (c-host makefile with stand-in targets)"
p=$d/fwd; mkdir -p $p/factory; cp $F/operator/kit/factory/kit.mk $p/factory/; cp $F/operator/kit/root.Makefile $p/Makefile
printf 'include factory/kit.mk\n.PHONY: check lint test\nlint:\n\t$(start)\n\t$(green)\ntest:\n\t$(start)\n\techo running tests\n\t$(green)\ncheck: lint test\n\techo "check: green"\n' > $p/factory/Makefile
for t in "" lint test "lint test" nosuch; do echo "-- make $t"; (cd $p && make $t 2>&1 | sed 's/([0-9]*\.[0-9] s)/(N s)/'; echo "exit ${PIPESTATUS[0]}"); done
echo "-- a directory test/ at the root (common in C projects), then make test and make check"
mkdir $p/test; (cd $p && make test 2>&1 | sed 's/([0-9]*\.[0-9] s)/(N s)/'; echo "exit ${PIPESTATUS[0]}"; make check 2>&1 | sed 's/([0-9]*\.[0-9] s)/(N s)/'; echo "exit ${PIPESTATUS[0]}")
echo "-- same through make -f factory/Makefile test"
(cd $p && make -f factory/Makefile test 2>&1 | sed 's/([0-9]*\.[0-9] s)/(N s)/'; echo "exit ${PIPESTATUS[0]}")
echo "### the kit's start facts through the forwarding root makefile"
p=$d/python-thin-none; git init -q --bare $d/remote.git; git -C $p remote add origin $d/remote.git; git -C $p push -q origin develop
git -C $p checkout -q -b work-item/x; echo 'print(1)' > $p/src/new.py; echo x >> $p/factory/pipeline.yml; commit $p change
(cd $p && echo "facts-changes:" && make facts-changes && echo "facts-files:" && make facts-files; echo "exit $?")
echo "### --run here (no stage environment in this container)"
(cd $F && $CHECK --run --agent-home agents "$d/c-host-thin-none" > $d/run.txt 2>&1); echo "exit $?"; tail -3 $d/run.txt
```

`protect.py`, beside it, is the third acceptance's script. It widens the role to `factory/*`, `src/*` and `*`, and asks about `factory/gitleaks.toml` too. It reads each project's `factory/pipeline.yml` with `RuamelPipelineDefinitionReader` and asks `refusal` under `protected_paths(definition.make_file)` for `factory/kit.mk`, `factory/Makefile`, `Makefile`, `factory/gitleaks.toml` and `src/a.py`.

What it printed:

```console
$ bash smoke.sh
python, thin, root makefile none: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
python, thin, root makefile own: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
python, full, root makefile none: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
python, full, root makefile own: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, thin, root makefile none: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, thin, root makefile own: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, full, root makefile none: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, full, root makefile own: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, thin, root makefile none: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, thin, root makefile own: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, full, root makefile none: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, full, root makefile own: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
### protection (a role widened to factory/*, src/* and *)
python-full-none make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'factory/gitleaks.toml': True, 'src/a.py': True}
java-gradle-thin-own make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'factory/gitleaks.toml': True, 'src/a.py': True}
### the kit alone: not ready but for the stack's targets
pipeline definition: ok
makefile: FAIL: factory/Makefile is missing
stage file: ok
agents: ok
write paths: ok
forms: ok
project: not ready (1 fault)
exit 1
### an uncommitted factory/Makefile does not count, the committed one does
project: not ready (1 fault)
project: ready
### root forwarding makefile, by hand (c-host makefile with stand-in targets)
-- make
lint: green (N s)
running tests
test: green (N s)
check: green
exit 0
-- make lint
lint: green (N s)
exit 0
-- make test
running tests
test: green (N s)
exit 0
-- make lint test
lint: green (N s)
running tests
test: green (N s)
exit 0
-- make nosuch
make[1]: *** No rule to make target 'nosuch'.  Stop.
make: *** [Makefile:6: nosuch] Error 2
exit 2
-- a directory test/ at the root (common in C projects), then make test and make check
make: 'test' is up to date.
exit 0
lint: green (N s)
running tests
test: green (N s)
check: green
exit 0
-- same through make -f factory/Makefile test
running tests
test: green (N s)
exit 0
### the kit's start facts through the forwarding root makefile
facts-changes:
A	src/new.py
facts-files:
CLAUDE.md
Makefile
README.md
docs/index.md
src/main.x
src/new.py
tests/t.x
exit 0
### --run here (no stage environment in this container)
exit 2
cannot run: FACTORY_REPOSITORY_URL: missing
```

Green, but for one finding.

- All twelve assemblies are ready. In each, only `CLAUDE.md` and `Makefile` lie outside `factory/`, and the project's own root `Makefile` is kept.
- The kit alone now lacks exactly one thing, `factory/Makefile`, where it lacked four targets before S0013. An uncommitted fix does not count.
- `factory/Makefile`, `factory/kit.mk` and `Makefile` are protected. `factory/gitleaks.toml` is not, and no kit role writes `factory/` (remark under 4).
- The start facts leave out `factory/` through the forwarding makefile, as through the named one.
- `--run` refuses here before building anything, because the container has no instance environment. The human ran it on factory-vm2 for the C and the Java pack (decision 23), but before S0013's layout. After S0013, no `--run` of a one-layout project is recorded.

**The finding:** with a folder `test/` at the root, `make test` through `root.Makefile` prints `make: 'test' is up to date.` and exits 0, without running a test. `make -f factory/Makefile test` runs them. The cause is the rule `%:` with no prerequisite: make takes the existing folder for the target and finds nothing to remake. I checked the GNU make manual's idiom in a temporary folder: a phony prerequisite on the forwarding rule (`%: force`, `force: ;`, `.PHONY: force`). It forwards `test` with `test/` present and also with a file `lint` present. It keeps `check` as the default goal and ends `nosuch` with status 2. Proposed as S0014.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

From S0013, the one story since the third acceptance:

- Tester (entry 5): it could not run its tests against the drafts, because copying them into `operator/` was refused, so the coder's run was the first one. Its entry 5 left out `tests/agent_files/test_claude_files.py`, which lists the kit's files. The coder found it red (entry 7), and the tester fixed it under leave 36 (entry 9). The process worked. Not proposed.
- Reviewer (entry 13): three test helpers were copied from `test_packs.py`. They were moved to `tests/support/pack_make_support.py` under the standing leave (entry 15), and round 1 had no findings.
- Coder: noticed nothing. `make duplicates` stayed at `8 new, 38 known, 5 gone`, the same as at the second and third acceptances.
- Documenter (entry 21): `docs/project-guide/README.md` does not list `tests/support/kit_support.py`, though the page says it names every module of `tests/support/`. I checked every module. Eight are missing, four of them this feature's: `kit_support.py` (S0005), `make_file_support.py` (S0002), `project_check_support.py` (S0001) and `project_run_support.py` (S0003). The other four are older: `archive_feature_support.py`, `bill_cache_support.py`, `first_message_support.py` and `shared_rules_support.py`. Proposed as part of S0015.
- Mine: `protected_paths` protects the named makefile and `kit.mk`, but not the other pack files under `factory/` (`factory/gitleaks.toml`, `factory/scripts/trust-store.sh`, `factory/stage.Containerfile`). The kit's roles have no write path under `factory/`, and the kit's `CLAUDE.md` names `factory/` under *Not without asking*. A role could reach them only if the project widened its write paths itself. Not proposed. It is the human's to say whether the take should refuse `factory/*` outright.

Still not proposed, as the earlier acceptances listed them:

- `LIVE_POINT_NAMES` is used only by tests.
- The `test_template_*` names.
- The untested real wiring of `extra_environment` and `ca_bundle`.
- `list.pop(0)` in `_Makefiles.read`.

## 5 Documentation

S0013's docs criterion is met on the pages it named:

- `operator/kit/README.md` and `operator/packs/README.md`;
- `docs/operator-guide/start-a-project.md`, whose firmware example matches what my smoke test printed for a project with its own root `Makefile`;
- `docs/operator-guide/pipeline.md:108`, *Name the makefile*;
- the decision log's entry at `docs/decisions.md:1784`, with its price and its gain.

Read as a newcomer from `README.md` through the operator guide to *Starting a project*, the pages agree with each other and with the behaviour, with these exceptions:

- `docs/project-guide/operator.md:25` still says the packs' README tells how kit and pack are assembled "at the root or, for an existing repository, with `make_file: factory/Makefile`". The same bullet then describes the one layout, so it contradicts itself. Proposed as S0015.
- `docs/operator-guide/install.md:230`, *The project's make targets*, says the project defines its targets "in the Makefile at the root of its checkout". A project assembled from the kit defines them in `factory/Makefile`, which `make_file` names. Proposed as S0015.
- `docs/project-guide/README.md` promises to name every module of `tests/support/` and misses eight (see 4). Proposed as S0015.
- `operator/kit/README.md`, `start-a-project.md` step 3 and `pipeline.md:108` say that `root.Makefile` "forwards every target". That is not true for a target that a root file or folder is named after (check 2). S0014 makes the sentence true rather than changing it.
- Still the human's, as before: `docs/brochure/README.md:457-459` (v1.1) names the template and calls Python the only proven stack.

## 6 Decisions taken for the human

`feature.md` lists decisions 1 to 35, and the first three acceptances gathered them. Added since:

1. Decision 36, the human's: one layout. S0013 built it as worded and copied the drafts byte for byte, apart from the licence line of `trust-store.sh`.
2. S0013, the documenter's choice: the decision log's new entry has no "Rejected" line, because the story names no rejected option. The option it replaced (two layouts) is named in its Decision line.
3. S0013, the kit's `CLAUDE.md` skeleton offers two wordings under `## Checks` (forwarding root, or `make -f factory/Makefile`) for the project to choose from. It is the human's draft. I note that an agent in a project that keeps its own root `Makefile` depends on that one line to run the right makefile.
4. Still open from the earlier acceptances, with no answer recorded in `feature.md`:
   - the brochure (see 5);
   - the wording of the decision log's "Why after the static part" (S0009);
   - ratifying the S0011 change to `tests/guards/test_tests_layout.py`, which decision 33's leave did not name.
5. New, for the human: whether `factory/*` should become a protected path as a whole, rather than only the named makefile and `kit.mk` (see 4).

Earlier tests changed by S0013, each with its leave, as the reviewer's entry 19 lists them:

- `tests/support/kit_support.py`: leave 36. It has one assembly, and `brownfield=` became `own_root_makefile=`.
- `tests/operator_scripts/test_kit_files.py`: leave 36. Two assertions on the old commented `make_file` were removed, because S0013's criterion 1 covers them. The expected fault is now `factory/Makefile is missing`.
- `tests/operator_scripts/test_packs.py`, under two leaves:
  - leave 36: `test_a_brownfield_project_with_the_pack_makefile_under_factory_is_ready` (6 rows) was removed, because criteria 2 and 3 cover it;
  - the standing leave to move a shared test helper: `PATH_TOOLS`, `PROJECT_TOOLS`, `_stand_in` and `_stand_in_project` moved to `tests/support/pack_make_support.py`.
- `tests/agent_files/test_claude_files.py::test_template_holds_only_the_rules_file_the_makefile_and_the_pipeline_definition`: leave 36. Its only failure was the new layout, and `root.Makefile` was added to the kit's listing.

No earlier test was changed without a leave.

## 7 Slow checks

The project offers nothing beyond `make check` except `make mutants` (check 3). `make check` as I found it ended with `check: green`, `test: green (111.3 s)` and coverage of 99.14 %. The JUnit report holds 11349 test cases, 18 more than at the third acceptance. S0013 added 23 cases in `test_one_layout.py` and removed the 6 rows of one test in `test_packs.py`, which makes 17; I did not trace the one case left over.

The slowest tests are all outside the feature:

- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other`, 19.8 s;
- then the `ROOMY_LIMIT` kills at 10.0 s each (`test_claude_runtime_resume`, `test_podman_timeout_status` twice, `test_document_examples`, `test_claude_runtime_provider_limit`).

The feature's tests are the cases matching `check_project`, `project_check`, `project_run`, `kit`, `pack`, `make_file`, `installed_builder`, `write_paths` or `one_layout`: 505 cases, 18.4 s together. S0013's `test_one_layout.py` has 23 cases and takes 0.6 s.

Disk: the Disk now line shows 71.0 GB free on `/srv/factory/self`, `/srv/factory/self/state` and `/tmp`, against 71.2 GB at the previous record (the third acceptance's). Used space is unchanged at 1.2 GB and 0.0 GB. The 0.2 GB less free space is on the shared pool, outside this instance's used space, so it is not this feature's growth. Its likely cause is snapshots or the other datasets of the pool during S0013's eleven runs; I cannot see that from here.

## 8 Cost

The thirteen stories cost:

- 133 runs, 260.4 min, 1099 turns;
- 4265602 tokens in (46915329 more from cache) and 633575 out;
- $43.38, about $3.34 a story.

S0013 added 11 runs, 24.1 min and $3.85, a little above the average. Its journal gives two reasons. First, the tester left one earlier test out of its entry 5, so the coder's `make check` went red and the story went back to the tester (entries 7 to 9). Second, the reviewer found copied test helpers, which took a second tests, doing and review round (entries 13 to 19). It asked the human nothing: its leave came worded with the story (decision 36). S0003 still stands out, at $6.53, for the reasons the first acceptance gave: two leaves, a `PLR0913` exception and a test rework.

Human interventions: 15 questions answered, all of cause `question`, with 2.0 h waited. Both numbers are unchanged since the third acceptance. The story that needed the human most is still S0001: two questions, one of which waited 102 minutes overnight. Across the feature, most questions asked for a leave to change an earlier test. The stories that came with their leave already worded (S0012 and S0013) asked nothing.

## Proposed stories

- `F0062-S0014-the-root-makefile-forwards-past-a-same-named-file.md`: the forwarding `root.Makefile` gets a phony prerequisite, so that `make test` with a `test/` folder at the root runs the tests instead of a silent false green (check 2). The human's seat changes the draft `planning/kit-draft/root.Makefile` first.
- `F0062-S0015-the-guides-catch-up-with-the-one-layout.md`: two stale sentences on the layouts before S0013 (`docs/project-guide/operator.md`, `docs/operator-guide/install.md`), and the eight shared test helpers missing from the project guide's index (checks 4 and 5).

## Journal

1. factory: started acceptance as self.
2. acceptance-reviewer: accepted with stories; 2 stories proposed (F0062-S0014, F0062-S0015)

   1 Scope: none. S0013 (decision 36, one layout) touches only kit and pack data, tests and documents, inside the scope items for the named makefile, the kit and packs, and the guide. A brownfield repository still keeps its own `Makefile`.
   2 Feature smoke test: green, with one finding. All twelve assemblies (3 packs × 2 lines × with and without the project's own root `Makefile`) print `project: ready`, with only `CLAUDE.md` and `Makefile` outside `factory/`. `factory/Makefile`, `factory/kit.mk` and `Makefile` are protected. The kit alone lacks only `factory/Makefile`. Finding: with a `test/` folder at the root, `make test` through `root.Makefile` prints `'test' is up to date.` and exits 0 without running a test. The `%:` rule has no phony prerequisite, and the GNU make `force` idiom fixes it (tried in a temporary folder). The factory's own gates are unaffected because they run `make -f factory/Makefile` (S0014). `--run` cannot run in this container, and no `--run` of a one-layout project is recorded.
   3 Mutation testing: by sweep, not run here.
   4 Noticed: the documenter's missing `kit_support.py` turns out to be eight `tests/support/` modules missing from the project guide's index, four of them this feature's (S0015). The tester and reviewer items were resolved in the story. Pack files under `factory/` other than the makefile and `kit.mk` are not protected; left to the human.
   5 Documentation: two places still describe the old layouts, `docs/project-guide/operator.md:25` and `docs/operator-guide/install.md:230`, and the index's promise to name every support module is broken (S0015). The sentence that `root.Makefile` "forwards every target" is made true by S0014. The brochure is still the human's.
   6 Decisions: decision 36 was built as worded. The decision log entry has no Rejected line. The `CLAUDE.md` `## Checks` line chooses between the two wordings. Three items are still open from the earlier acceptances, and one is new: whether all of `factory/*` should be protected. Each earlier test S0013 changed has its leave (36, or the standing leave for the helper move).
   7 Slow checks: none beyond `make check` (green, 111.3 s, 99.14 %). The slowest test is test_documents_marker at 19.8 s. The feature's 505 cases take 18.4 s. Disk: 0.2 GB less free on the shared pool with used space unchanged, so not this feature's growth.
   8 Cost: 133 runs, 260.4 min, $43.38. S0013 cost $3.85, above average because of one test rework (an earlier test the tester missed) and one review round (copied helpers). Questions: 15, 2.0 h waited, unchanged since the third acceptance. S0001 still needed the human most.
3. factory: done (pull request merged); cost: 1 runs, 6.4 min, 26 turns, 90791 tokens in (1510645 more from cache), 27733 out, $1.31
