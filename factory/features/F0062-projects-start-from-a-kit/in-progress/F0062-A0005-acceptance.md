---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 709
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-17T07:57:10.524670Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-17T08:04:25.159456Z'
  stage: acceptance
  run: 7b908c06be554e76be29904bbac663dc
stories: [F0062-S0001, F0062-S0002, F0062-S0003, F0062-S0004, F0062-S0005, F0062-S0006, F0062-S0007, F0062-S0008, F0062-S0009, F0062-S0010, F0062-S0011, F0062-S0012, F0062-S0013, F0062-S0014, F0062-S0015]
outcome: null
---

# Acceptance of Projects start from a kit and a stack pack

## Recommendation

`accepted with stories`. The two stories since the fourth acceptance did what that acceptance proposed:

- S0014: the forwarding `root.Makefile` now runs `make test` beside a `test/` folder, `make` beside a `check/` folder and `make lint` beside a file `lint`. A red target stays red.
- S0015: the two stale pages and the project guide's index follow the one layout.

All twelve assemblies of kit and pack are `project: ready`, and `make check` is green as I found it. One finding is worth a story, and it is not a broken promise of `feature.md`. Both guides tell the reader to replace the kit's whole `## Checks` section of `CLAUDE.md` with the pack's, and no pack's section holds the kit's line about `factory/Makefile`. So the one line that tells an agent in a repository with its own root `Makefile` to run `make -f factory/Makefile check` is lost, although the same step asks the reader to keep it.

## 1 Scope

None. The first four acceptances found every scope item covered by S0001 to S0013. S0014 and S0015 come from the fourth acceptance's proposals, which the human built as proposed (decision 37):

- S0014 belongs to the scope item "the kit, and the stack packs". It changes only `operator/kit/root.Makefile`, as a copy of the human's draft, and adds a test.
- S0015 belongs to "the guide for a fresh start and for a brownfield repository". It changes only documents.

No module under `src/factory/` changed in either story. The Goal holds as before: a project of each stack is assembled from kit and pack, the check says whether it is ready, and an existing repository keeps its own root `Makefile` unchanged (check 2). The human's change 3 (the three starters) is the human's and is not judged here.

## 2 Feature smoke test

This is the walk-through of the fourth acceptance, with three changes:

- Each project keeps its tests in `test/`, as a C project often does, so the root has a folder named after a target.
- Each assembly sets the write paths to that folder, as step 4 of `docs/operator-guide/start-a-project.md` says ("Name the folders the factory may change").
- The forwarding makefile is tried beside folders `test/` and `check/`, a file `lint`, a red recipe and the name `factory-forward`.

The script assembles each project as the guide says: the kit into `factory/`, every pack file but the two pages into `factory/`, and `root.Makefile` as `Makefile` only where the repository has no root makefile of its own. It does this for every pack, both lines, with and without a root `Makefile` of the project's own, and checks each project with the installed `factory-check-project`. `protect.py` beside it is the earlier acceptances' script: it reads each project's `factory/pipeline.yml` with `RuamelPipelineDefinitionReader` and asks `refusal` under `protected_paths(definition.make_file)`, for a role widened to `factory/*`, `src/*` and `*`. Everything ran in `mktemp -d` folders, which were removed afterwards.

`smoke.sh`:

```bash
#!/usr/bin/env bash
set -u
F=/work/checkout; CHECK=$F/.venv/bin/factory-check-project; S=$(dirname "$0")
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
unset MAKEFLAGS MAKELEVEL MFLAGS
commit() { git -C "$1" add -A && git -C "$1" -c user.name=t -c user.email=t@example.com commit -q -m "$2"; }
assemble() { # $1 project, $2 pack, $3 line, $4 own root makefile (own|none) -- as start-a-project.md says
  p=$1; mkdir -p "$p/factory" "$p/src" "$p/test" "$p/docs"; git init -q -b develop "$p"
  touch "$p/src/main.x" "$p/test/t.x" "$p/docs/index.md" "$p/README.md"
  [ "$4" = own ] && printf 'all:\n\techo own\n' > "$p/Makefile"
  cp $F/operator/kit/factory/* "$p/factory/"; cp $F/operator/kit/CLAUDE.md "$p/"
  mv "$p/factory/pipeline.$3.yml" "$p/factory/pipeline.yml"; sed -i "s|\"tests/\*\"|\"test/*\"|" "$p/factory/pipeline.yml"; rm -f "$p/factory/pipeline."{thin,full}.yml
  (cd $F/operator/packs/$2 && find . -type f ! -name CLAUDE.sections.md ! -name TRAPS.md) | while read -r f; do
    mkdir -p "$p/factory/$(dirname "$f")"; cp "$F/operator/packs/$2/$f" "$p/factory/$f"; done
  [ -f "$p/Makefile" ] || cp $F/operator/kit/root.Makefile "$p/Makefile"
  commit "$p" assemble
}
for pack in python c-host java-gradle; do for line in thin full; do for own in none own; do
  p=$d/$pack-$line-$own; assemble "$p" $pack $line $own
  out=$(cd $F && $CHECK --agent-home agents "$p"); rc=$?
  outside=$(git -C "$p" ls-files | grep -v -e '^factory/' -e '^src/' -e '^test/' -e '^docs/' -e '^README.md$' | tr '\n' ' ')
  echo "$pack, $line, root makefile $own: $(echo "$out" | grep -c ': ok$') ok, $(echo "$out" | tail -1), exit $rc; outside factory/: $outside"
done; done; done
echo "### one check output in full (c-host, full, no own root makefile)"
(cd $F && $CHECK --agent-home agents "$d/c-host-full-none"); echo "exit $?"
echo "### protection (a role widened to factory/*, src/* and *)"
(cd $F && uv run --quiet python $S/protect.py $d/python-full-none $d/java-gradle-thin-own)
echo "### the kit alone"
p=$d/kit-only; mkdir -p $p/factory $p/src; git init -q -b develop $p; touch $p/src/a $p/README.md
cp $F/operator/kit/factory/* $p/factory/; cp $F/operator/kit/CLAUDE.md $p/; cp $F/operator/kit/root.Makefile $p/Makefile
mv $p/factory/pipeline.thin.yml $p/factory/pipeline.yml; rm $p/factory/pipeline.full.yml; commit $p kit
out=$(cd $F && $CHECK --agent-home agents "$p"); echo "exit $?"; echo "$out" | grep -v ": ok$"
echo "### an uncommitted factory/Makefile does not count, the committed one does"
printf 'include factory/kit.mk\nsync lint test check:\n\techo $@\n' > $p/factory/Makefile
(cd $F && $CHECK --agent-home agents "$p" | tail -1); commit $p fix; (cd $F && $CHECK --agent-home agents "$p" | tail -1)
echo "### root forwarding makefile, by hand, with root files and folders named after targets"
p=$d/fwd; mkdir -p $p/factory; cp $F/operator/kit/factory/kit.mk $p/factory/; cp $F/operator/kit/root.Makefile $p/Makefile
printf 'include factory/kit.mk\n.PHONY: check lint test\nlint:\n\t$(start)\n\t$(green)\ntest:\n\t$(start)\n\techo running tests\n\t$(TEST_EXIT)\n\t$(green)\ncheck: lint test\n\techo "check: green"\n' > $p/factory/Makefile
run() { (cd $p && make "$@" 2>&1 | sed 's/([0-9]*\.[0-9] s)/(N s)/'; echo "exit ${PIPESTATUS[0]}"); }
echo "-- nothing named after a target: make"; run
mkdir $p/test $p/check; touch $p/lint
echo "-- folders test/ and check/, a file lint at the root: make"; run
echo "-- make test"; run test
echo "-- make lint"; run lint
echo "-- make test with a red test recipe"; run test TEST_EXIT='exit 3'
echo "-- make nosuch"; run nosuch
echo "-- make factory-forward"; run factory-forward
echo "### the kit's start facts through the forwarding root makefile"
p=$d/python-thin-none; git init -q --bare $d/remote.git; git -C $p remote add origin $d/remote.git; git -C $p push -q origin develop
git -C $p checkout -q -b work-item/x; echo 'print(1)' > $p/src/new.py; echo x >> $p/factory/pipeline.yml; commit $p change
(cd $p && echo "facts-changes:" && make facts-changes && echo "facts-files:" && make facts-files; echo "exit $?")
echo "### --run here (no stage environment in this container)"
(cd $F && $CHECK --run --agent-home agents "$d/c-host-thin-none" > $d/run.txt 2>&1); echo "exit $?"; tail -3 $d/run.txt
```

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
### one check output in full (c-host, full, no own root makefile)
pipeline definition: ok
makefile: ok
stage file: ok
agents: ok
write paths: ok
forms: ok
project: ready
exit 0
### protection (a role widened to factory/*, src/* and *)
python-full-none make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'factory/gitleaks.toml': True, 'src/a.py': True}
java-gradle-thin-own make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'factory/gitleaks.toml': True, 'src/a.py': True}
### the kit alone
exit 1
makefile: FAIL: factory/Makefile is missing
write paths: FAIL: role builder: write path tests/* matches no tracked file; role builder: write path docs/* matches no tracked file
project: not ready (3 faults)
### an uncommitted factory/Makefile does not count, the committed one does
project: not ready (3 faults)
project: not ready (2 faults)
### root forwarding makefile, by hand, with root files and folders named after targets
-- nothing named after a target: make
lint: green (N s)
running tests
test: green (N s)
check: green
exit 0
-- folders test/ and check/, a file lint at the root: make
lint: green (N s)
running tests
test: green (N s)
check: green
exit 0
-- make test
running tests
test: green (N s)
exit 0
-- make lint
lint: green (N s)
exit 0
-- make test with a red test recipe
running tests
make[1]: *** [factory/Makefile:7: test] Error 3
make: *** [Makefile:8: test] Error 2
exit 2
-- make nosuch
make[1]: *** No rule to make target 'nosuch'.  Stop.
make: *** [Makefile:8: nosuch] Error 2
exit 2
-- make factory-forward
make: Nothing to be done for 'factory-forward'.
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
test/t.x
exit 0
### --run here (no stage environment in this container)
exit 2
cannot run: FACTORY_REPOSITORY_URL: missing
```

Green. The fourth acceptance's finding is gone:

- Beside a `test/` folder, `make test` runs the tests and does not print `'test' is up to date.`.
- Beside `check/`, `make` runs `check`.
- Beside a file `lint`, `make lint` runs.
- A red recipe ends with status 2, and `make nosuch` ends with status 2.
- `make factory-forward` runs nothing of `factory/Makefile`.

The rest is as at the fourth acceptance:

- All twelve assemblies are ready, with only `CLAUDE.md` and `Makefile` outside `factory/`.
- `factory/Makefile`, `factory/kit.mk` and `Makefile` are protected.
- The start facts leave out `factory/`.
- An uncommitted fix does not count.

On my first run the write paths still named `tests/*` while the project kept its tests in `test/`. Each project then failed only the point `write paths`, with `role tester: write path tests/* matches no tracked file`. That is the check doing what step 4 of the guide warns about, not a fault. `--run` refuses here before building anything, because this container has no instance environment. No `--run` of a project in the one layout is recorded since S0013. It is part of the human's change 3, on the VM.

The smoke test does not show the finding of 5, because the check does not read `CLAUDE.md`'s sections. I showed it with the tests' own assembly: `pack_claude_md(pack)` of `tests/support/kit_support.py`, which follows the guide's step 5, gives for each of `python`, `c-host` and `java-gradle` a `CLAUDE.md` that contains neither `factory/Makefile` nor `make -f` (`'factory/Makefile' in text` is `False` for all three).

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

From S0014 and S0015, the two stories since the fourth acceptance:

- S0014, reviewer (entry 12): two test helpers were copied from `test_one_layout.py`. They were moved to `tests/support/kit_support.py` under the standing leave (entry 14), and round 1 had no findings.
- S0014, reviewer (entry 18, a note): `tests/operator_scripts/test_root_makefile.py:59` (`matching`) counts matching lines with the same expression that `test_one_layout.py:111` and `test_packs.py:131` write inline. One helper in `tests/support/kit_make_support.py` could serve all three. Not proposed: three one-line expressions in tests, below the weight of a story.
- S0014, documenter (entry 20): the decision log's new entry names one rejected option (a `.PHONY` list of known targets) and leaves out the coder's second one (`MAKECMDGOALS` tricks), because the coder named it only in passing. Listed under 6.
- S0014 and S0015, coders: noticed nothing. `make duplicates` stayed at `8 new, 38 known, 5 gone`, the same as at the second, third and fourth acceptances.
- S0015, documenter (entry 5): in prose, the page writes `<project>/factory/Makefile`, because `make documents` reads a bare backticked `factory/Makefile` as a path in this repository and reports it missing. `pipeline.md` already uses that form. A convention, not a finding.
- S0015, reviewer (entry 11): a few sentences run a little over 25 words but hold one idea each, within style.md's "about 25 words". Not proposed.
- Mine: `operator/packs/c-host/TRAPS.md:6` still advises naming `make_file: factory/Makefile` for an existing firmware repository. Since S0013 the kit's definitions name it for every project, so the advice is now redundant, though not false. It is the human's draft text (decision 23). Listed under 6, not proposed.

Still not proposed, as the earlier acceptances listed them: `LIVE_POINT_NAMES` used only by tests; the `test_template_*` names (`tests/agent_files/test_claude_files.py::test_template_rules_file_is_the_python_project_text` among them); the untested real wiring of `extra_environment` and `ca_bundle`; `list.pop(0)` in `_Makefiles.read`; `factory/gitleaks.toml` and the other pack files under `factory/` are not protected paths.

## 5 Documentation

S0014's and S0015's docs criteria are met:

- `operator/kit/README.md` step 5 and the `root.Makefile` row say that a target is forwarded past a file or folder of its name, as check 2 shows.
- `docs/decisions.md` has the entry "The forwarding root `Makefile` forwards a target past a file of its name" beside the one-layout entry.
- `docs/project-guide/operator.md:25` describes one way of assembly.
- `docs/operator-guide/install.md`, *The project's make targets*, names `make_file` and `<project>/factory/Makefile`.
- The project guide's index names every module of `tests/support/` (S0015's smoke test prints only `done` today).

Read as a newcomer from `README.md` to *Starting a project*, the pages agree with each other and with the behaviour, with one exception:

- **Finding:** `docs/operator-guide/start-a-project.md:33` (step 5) and `operator/packs/README.md:22` (step 4) both say two things in one step. First, keep the kit's line under `## Checks` about `factory/Makefile`, with the wording that fits. Second, replace the skeleton's `## Checks` section with the pack's section of the same heading. No pack's `CLAUDE.sections.md` has that line under `## Checks`, so the replacement removes it. The tests' own assembly, `pack_claude_md`, does exactly that (check 2): for all three packs, the assembled `CLAUDE.md` never names `factory/Makefile`. In a repository that keeps its own root `Makefile`, an agent following its `CLAUDE.md` then runs `make check` on the repository's makefile, not the factory's. That is a failed or wrong check at the coder's own step. The factory's gates run `make -f factory/Makefile` through `make_file` and are not affected, so no false green reaches a merge. A careful reader can put the line back by hand. Since the guides ask for something the replacement undoes, I count this as a documentation repair worth a story, not a broken promise. Proposed as S0016: each pack's `## Checks` carries the kit's line, so that the replacement keeps it. The drafts are the human's (decision 23).
- Still the human's, as before: `docs/brochure/README.md:457-459` (v1.1) names the template and calls Python the only proven stack.

## 6 Decisions taken for the human

`feature.md` lists decisions 1 to 37, and the first four acceptances gathered them up to 36. Added since:

1. Decision 37, the human's: S0014 and S0015 built as proposed.
2. S0014, the intake's question (entry 3), answered (a) by the human (entry 4): criterion 5 was added, which tests that `factory-forward` is not forwarded. A project can therefore not use a target named `factory-forward` through the root makefile.
3. S0014, the documenter's choice: the decision log's entry names only the `.PHONY` list as rejected, not `MAKECMDGOALS` tricks (see 4).
4. S0015, the documenter's convention: `<project>/factory/Makefile` in prose, because the document check reads a bare backticked path as one of this repository's.
5. New, for the human, with S0016:
   - (a) The packs' drafts each gain the kit's line under `## Checks`, as S0016 proposes. I would choose this, because then the replacement the guides describe is correct as written.
   - (b) Alternatively, only the two guides change, to say that the line is put back after the replacement. That keeps a manual merge in every assembly.
6. New, for the human: `operator/packs/c-host/TRAPS.md:6` repeats advice the kit now carries for every project (see 4). Reword the draft or leave it.
7. Still open from the earlier acceptances, with no answer recorded in `feature.md`:
   - the brochure (see 5);
   - the wording of the decision log's "Why after the static part" (S0009);
   - ratifying the S0011 change to `tests/guards/test_tests_layout.py`, which decision 33's leave did not name;
   - whether `factory/*` becomes a protected path as a whole.

Earlier tests changed since the fourth acceptance, each with its leave, as S0014's reviewer entry 18 lists them:

- `tests/operator_scripts/test_one_layout.py`: the standing leave to move a shared test helper. `MAKEFILE_TARGET` and the project setup moved to `tests/support/kit_support.py`. `test_the_root_makefile_forwards_every_target_to_the_factory_makefile` keeps its name, rows and assertions.
- `tests/support/kit_support.py`: the same leave. It only gained `MAKEFILE_TARGET` and `forwarding_project`.

S0015 changed no test. No earlier test was changed without a leave.

## 7 Slow checks

The project offers nothing beyond `make check` except `make mutants` (check 3). `make check` as I found it ended with `check: green`, `test: green (111.0 s)` and coverage of 99.14 %. The JUnit report holds 11362 test cases, 13 more than at the fourth acceptance. S0014's `test_root_makefile.py` added 12 of them; I did not trace the one case left over.

The slowest tests are all outside the feature:

- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other`, 19.8 s;
- then the `ROOMY_LIMIT` kills at 10.0 s each (`test_podman_timeout_status` twice, `test_claude_runtime_resume`, `test_document_examples`, `test_claude_runtime_provider_limit`).

The feature's tests are the cases matching `check_project`, `project_check`, `project_run`, `kit`, `pack`, `make_file`, `installed_builder`, `write_paths`, `one_layout` or `root_makefile`: 518 cases, 17.8 s together. S0014's 12 cases, each a real make run, take 0.07 s together.

Disk: the Disk now line shows 70.8 GB free on `/srv/factory/self`, `/srv/factory/self/state` and `/tmp`, against 71.0 GB at the previous record (the fourth acceptance's). Used space is unchanged at 1.2 GB and 0.0 GB. The 0.2 GB less free space is on the shared pool, outside this instance's used space, so it is not this feature's growth. As at the fourth acceptance, its likely cause is snapshots or the pool's other datasets during the fifteen runs of S0014 and S0015; I cannot see that from here.

## 8 Cost

The fifteen stories cost:

- 148 runs, 280.8 min, 1183 turns;
- 4592766 tokens in (49192388 more from cache) and 673517 out;
- $46.27, about $3.08 a story.

Since the fourth acceptance:

- S0014: 10 runs, 13.8 min, $1.85. Its intake asked the human one question, about an untested Interface rule. The reviewer's two copied helpers then took a second tests, doing and review round (entries 12 to 18).
- S0015: 5 runs, 6.6 min, $1.04. The documenter took a second round for four findings on sentence length (entries 7 to 11).

Neither stands out. S0003 is still the dearest, at $6.53, for the reasons the first acceptance gave: two leaves, a `PLR0913` exception and a test rework.

Human interventions: 16 questions answered, all of cause `question`, with 2.0 h waited. That is one more question than at the fourth acceptance (S0014's intake, entry 3), and the wait rounds to the same 2.0 h. The story that needed the human most is still S0001: two questions, one of which waited 102 minutes overnight. Across the feature, most questions asked for a leave to change an earlier test. S0016 therefore names its leave in its Interface, worded for the human to give.

## Proposed stories

- `F0062-S0016-the-packs-checks-keep-the-makefile-line.md`: each pack's `## Checks` section of `CLAUDE.sections.md` gains the kit's line about `factory/Makefile`, after the human's seat changes the drafts. Then replacing the kit's section, as both guides say, keeps the line that tells an agent in a repository with its own root `Makefile` to run `make -f factory/Makefile` (check 5).

## Journal

1. factory: started acceptance as self.
2. acceptance-reviewer: accepted with stories; 1 story proposed (F0062-S0016)
   1. Scope: none. S0014 (forwarding root makefile) and S0015 (guides catch up) were the fourth acceptance's proposals, built as proposed (decision 37). Every scope item is covered, and no module under `src/factory/` changed.
   2. Feature smoke test: green. All 12 assemblies (3 packs × 2 lines × with/without an own root `Makefile`, tests kept in `test/`) are `project: ready`, with only `CLAUDE.md` and `Makefile` outside `factory/`. The forwarding makefile runs `test`, `check` and `lint` beside a `test/` folder, a `check/` folder and a file `lint`. A red recipe and `nosuch` exit 2, and `factory-forward` is not forwarded. Protection, start facts and the HEAD-only reading hold. `--run` is not possible in this container.
   3. Mutation testing: by sweep, not run here.
   4. Noticed: helpers copied in S0014 were moved under the standing leave; a `matching` expression is written inline in three test modules (not proposed); `<project>/factory/Makefile` is the prose convention because of the document check; c-host `TRAPS.md:6` repeats advice the kit now carries (the human's text).
   5. Documentation: one finding. `start-a-project.md` step 5 and `operator/packs/README.md` step 4 say to keep the kit's `## Checks` line about `factory/Makefile` and also to replace the whole section with the pack's, which lacks it. `pack_claude_md` shows the assembled `CLAUDE.md` never names `factory/Makefile` for any pack. Proposed as S0016.
   6. Decisions: decision 37; S0014's intake answer (criterion 5); two documenter choices; the S0016 options (a) packs' drafts carry the line, which I prefer, or (b) guides only; c-host `TRAPS.md` wording. Still open from earlier acceptances: the brochure, the "Why after the static part" wording, ratifying the S0011 change to `test_tests_layout.py`, and `factory/*` protection. Earlier tests changed only under the standing leave (`test_one_layout.py`, `kit_support.py`).
   7. Slow checks: nothing beyond `make check`, which was green (111.0 s, 99.14 %, 11362 cases, 13 more than before). The slowest test is `test_documents_marker` at 19.8 s. The feature's tests are 518 cases taking 17.8 s. Disk: 0.2 GB less free on the shared pool with used space unchanged, so this feature's changes do not explain it.
   8. Cost: $46.27 for 148 runs; S0014 cost $1.85 and S0015 $1.04, neither stands out. 16 questions with 2.0 h waited, one more question than before (S0014's intake). S0001 is still the story that needed the human most.
