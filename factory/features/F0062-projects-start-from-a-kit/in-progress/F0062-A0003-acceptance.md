---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 704
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-17T06:19:55.836698Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-17T06:19:59.656745Z'
  stage: acceptance
- number: 3
  speaker: factory
  kind: started
  at: '2026-11-17T06:20:01.221142Z'
  stage: acceptance
- number: 4
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-17T06:24:33.761413Z'
  stage: acceptance
  run: 9c6aa22531794ae3bf874e62496396da
stories: [F0062-S0001, F0062-S0002, F0062-S0003, F0062-S0004, F0062-S0005, F0062-S0006, F0062-S0007, F0062-S0008, F0062-S0009, F0062-S0010, F0062-S0011, F0062-S0012]
outcome: null
---

# Acceptance of Projects start from a kit and a stack pack

## Recommendation

`accepted`. The second acceptance (F0062-A0002, pull request 702) proposed one more story, and S0012 closed the one gap it found. A `make_file` that is not in its plain form is now a fault of the pipeline definition, and the fault names the plain spelling. So the definition, the take and the check all read one path. `make check` is green as I found it, and the feature's smoke test is green end to end: all twelve assemblies of kit and pack, the protection, and the four non-plain spellings refused with the right fault. Nothing of weight is left, and no story is proposed.

## 1 Scope

None. The first acceptance (F0062-A0001) found every scope item covered by S0001 to S0008. S0009 to S0011 were its proposals, judged inside the feature by the second acceptance. S0012 is the second acceptance's one proposal, built as proposed (decision 34). It changes only the load-time rule `_make_file_faults` (`src/factory/pipeline/domain/pipeline_definition.py:274`), which belongs to the scope item "the makefile a pipeline definition names". Every promise of the Goal holds (check 2). The human's change 3 (the three starters) is the human's and is not judged here.

## 2 Feature smoke test

This is the second acceptance's walk-through, run again on today's `develop`. Its last section now walks every spelling S0012 refuses and the plain spelling after them. It assembles a project as `docs/operator-guide/start-a-project.md` says:

- for every pack, both lines and both makefile places;
- with the kit alone;
- with an uncommitted fix, then the same fix committed.

It checks each project with the installed `factory-check-project`. It asks the factory's own definition reader and `protected_paths` what a role widened to `factory/*` and `src/*` may write. It runs the kit's start facts through a named makefile, and it tries `--run`. Everything ran in `mktemp -d` folders that remove themselves.

`smoke.sh`:

```bash
#!/usr/bin/env bash
set -u
F=/work/checkout; CHECK=$F/.venv/bin/factory-check-project; S=$(dirname "$0")
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
  out=$(cd $F && $CHECK --agent-home agents "$p"); rc=$?
  echo "$pack, $line line, makefile at $place: $(echo "$out" | grep -c ': ok$') points ok, $(echo "$out" | tail -1), exit $rc"
done; done; done
echo "### the factory's makefiles are protected in assembled projects (a role widened to factory/* and src/*)"
(cd $F && uv run --quiet python $S/protect.py $d/python-full-root $d/python-full-factory $d/c-host-thin-factory $d/java-gradle-full-factory)
echo "### the kit alone (no pack): not ready but for the stack's targets"
p=$d/kit-only; mkdir -p $p/factory $p/src $p/tests $p/docs; git init -q -b develop $p; touch $p/src/a $p/tests/a $p/docs/a $p/README.md
cp $F/operator/kit/factory/* $p/factory/; cp $F/operator/kit/CLAUDE.md $p/; mv $p/factory/pipeline.thin.yml $p/factory/pipeline.yml; rm $p/factory/pipeline.full.yml
printf 'include factory/kit.mk\n' > $p/Makefile; commit $p kit
(cd $F && $CHECK --agent-home agents "$p"); echo "exit $?"
echo "### an uncommitted fix does not count, the committed one does"
printf 'include factory/kit.mk\nsync lint test check:\n\techo $@\n' > $p/Makefile
(cd $F && $CHECK --agent-home agents "$p" | tail -1); commit $p fix; (cd $F && $CHECK --agent-home agents "$p" | tail -1)
echo "### the kit's start facts through the brownfield makefile"
p=$d/python-full-factory; git init -q --bare $d/remote.git; git -C $p remote add origin $d/remote.git; git -C $p push -q origin develop
git -C $p checkout -q -b work-item/x; echo 'print(1)' > $p/src/new.py; commit $p change
(cd $p && echo "facts-changes:" && make --no-print-directory -f factory/Makefile facts-changes && echo "facts-files:" && make --no-print-directory -f factory/Makefile facts-files && echo "facts-diff:" && make -s -f factory/Makefile facts-diff > $d/diff.txt; echo "exit $?"; head -2 $d/diff.txt)
echo "### make_file spellings not in their plain form (S0012), then the plain one again"
p=$d/c-host-full-factory
for v in ./factory/Makefile factory//Makefile factory/./Makefile factory/Makefile/ ../Makefile factory/Makefile; do
  sed -i "s|^make_file: .*|make_file: $v|" $p/factory/pipeline.yml; commit $p "spell $v"
  echo "-- make_file: $v"; (cd $F && $CHECK --agent-home agents "$p" | grep -E '^(pipeline definition|makefile)|^project'); echo "exit ${PIPESTATUS[0]}"
done
(cd $F && uv run --quiet python $S/protect.py $p)
echo "### --run here (no stage environment in this container)"
(cd $F && $CHECK --run --agent-home agents "$d/c-host-thin-root" > $d/run.txt 2>&1); echo "exit $?"; tail -3 $d/run.txt
```

`protect.py`, beside it. It reads each project's `factory/pipeline.yml` with the factory's reader and asks `refusal` under `protected_paths(definition.make_file)`:

```python
import sys
from pathlib import Path

from factory.agents.domain.agent_runs import WritePathSettings
from factory.agents.domain.write_paths import protected_paths, refusal
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader

for project in sys.argv[1:]:
    text = (Path(project) / "factory/pipeline.yml").read_text()
    definition = RuamelPipelineDefinitionReader().parse(text)
    settings = WritePathSettings(
        root=Path(project),
        write_paths=["factory/*", "src/*"],
        protected_paths=protected_paths(definition.make_file),
    )
    paths = ("factory/kit.mk", "factory/Makefile", "Makefile", "src/a.py")
    verdict = {p: refusal(p, settings) is None for p in paths}
    print(Path(project).name, "make_file:", definition.make_file, "writable:", verdict)
```

What it printed:

```console
$ bash smoke.sh
python, thin line, makefile at root: 6 points ok, project: ready, exit 0
python, thin line, makefile at factory: 6 points ok, project: ready, exit 0
python, full line, makefile at root: 6 points ok, project: ready, exit 0
python, full line, makefile at factory: 6 points ok, project: ready, exit 0
c-host, thin line, makefile at root: 6 points ok, project: ready, exit 0
c-host, thin line, makefile at factory: 6 points ok, project: ready, exit 0
c-host, full line, makefile at root: 6 points ok, project: ready, exit 0
c-host, full line, makefile at factory: 6 points ok, project: ready, exit 0
java-gradle, thin line, makefile at root: 6 points ok, project: ready, exit 0
java-gradle, thin line, makefile at factory: 6 points ok, project: ready, exit 0
java-gradle, full line, makefile at root: 6 points ok, project: ready, exit 0
java-gradle, full line, makefile at factory: 6 points ok, project: ready, exit 0
### the factory's makefiles are protected in assembled projects (a role widened to factory/* and src/*)
python-full-root make_file: None writable: {'factory/kit.mk': False, 'factory/Makefile': True, 'Makefile': False, 'src/a.py': True}
python-full-factory make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'src/a.py': True}
c-host-thin-factory make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'src/a.py': True}
java-gradle-full-factory make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'src/a.py': True}
### the kit alone (no pack): not ready but for the stack's targets
pipeline definition: ok
makefile: FAIL: no target check; no target lint; no target test; no target sync
stage file: ok
agents: ok
write paths: ok
forms: ok
project: not ready (4 faults)
exit 1
### an uncommitted fix does not count, the committed one does
project: not ready (4 faults)
project: ready
### the kit's start facts through the brownfield makefile
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
facts-diff:
exit 0
 src/new.py | 1 +
 1 file changed, 1 insertion(+)
### make_file spellings not in their plain form (S0012), then the plain one again
-- make_file: ./factory/Makefile
pipeline definition: FAIL: make_file ./factory/Makefile must be written as factory/Makefile
makefile: skipped: no valid pipeline definition
project: not ready (1 fault)
exit 0
-- make_file: factory//Makefile
pipeline definition: FAIL: make_file factory//Makefile must be written as factory/Makefile
makefile: skipped: no valid pipeline definition
project: not ready (1 fault)
exit 0
-- make_file: factory/./Makefile
pipeline definition: FAIL: make_file factory/./Makefile must be written as factory/Makefile
makefile: skipped: no valid pipeline definition
project: not ready (1 fault)
exit 0
-- make_file: factory/Makefile/
pipeline definition: FAIL: make_file factory/Makefile/ must be written as factory/Makefile
makefile: skipped: no valid pipeline definition
project: not ready (1 fault)
exit 0
-- make_file: ../Makefile
pipeline definition: FAIL: make_file ../Makefile must be a path inside the checkout
makefile: skipped: no valid pipeline definition
project: not ready (1 fault)
exit 0
-- make_file: factory/Makefile
pipeline definition: ok
makefile: ok
project: ready
exit 0
c-host-full-factory make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'src/a.py': True}
### --run here (no stage environment in this container)
exit 2
cannot run: FACTORY_REPOSITORY_URL: missing
```

Each `exit 0` in the spelling loop is my script's own slip, not the command's. `PIPESTATUS[0]` there reads the subshell's status, which is the status of `grep`. So I ran the `./factory/Makefile` project again on its own (`dot.sh`, the same assembly of the C pack's full line):

```console
$ bash dot.sh
pipeline definition: FAIL: make_file ./factory/Makefile must be written as factory/Makefile
makefile: skipped: no valid pipeline definition
stage file: ok
agents: skipped: no valid pipeline definition
write paths: skipped: no valid pipeline definition
forms: ok
project: not ready (1 fault)
exit 1
```

**Green.** Every promise of the Goal holds:

- All twelve assemblies are ready.
- The kit alone lacks exactly the stack's four targets.
- The check reads the commit and not the work tree.
- The start facts leave out `factory/` through a named makefile.
- The take refuses `factory/kit.mk` everywhere, and refuses `factory/Makefile` wherever the definition names it.
- `--run` refuses before it builds anything, because this container has no instance environment (decision 12). The human ran the live part on factory-vm2 (decision 23).

The second acceptance's finding is closed. `./factory/Makefile`, `factory//Makefile`, `factory/./Makefile` and `factory/Makefile/` are each refused with `must be written as factory/Makefile` and exit 1. The misleading `./factory/Makefile is missing` is gone, and `../Makefile` keeps its one fault. A definition no longer loads with a spelling that `protected_paths` would miss, so the protection no longer depends on how the human spells the path.

One edge, of no weight. `make_file: .` is accepted, because it is in plain form and inside the checkout. Through the reader it gives `'.'`, and `make -f .` would fail. Only the human writes the definition, a stage's check would fail loudly, and the root `Makefile` stays protected. `make_file: factory/.` gives `must be written as factory`, which is correct, if odd. Not proposed.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

From S0012, the one story since the second acceptance:

- Intake: the story's third smoke test asked for `pytest -q`, but `pyproject.toml` already sets `-q` in `addopts`. At `-qq`, pytest prints no summary line. The human chose to drop the `-q` (option a). This is a trap for every story form that quotes a pytest command. It already appears in the smoke-test lines of later stories, which use no `-q`. Not proposed: the project's own `CLAUDE.md` prescribes `uv run pytest -q <files> 2>&1 | tail -5` for the tester and the coder. That command still works, because `tail -5` shows the failure lines and a red run still prints its summary.
- Coder: none beyond the docs criterion. `make duplicates` stayed at `8 new, 38 known, 5 gone`, the same as at the second acceptance, so S0012 added no similar or dead code.
- Reviewer: no findings and no remarks.
- Documenter: the document check took backticked bare values such as `factory//Makefile` for paths of files that do not exist. So the pages write each value as `make_file: <value>`. This is a known quirk of the check, and the pages read well as written. Not proposed.
- Smoke tester: criterion 3 (`factory-check-project` on a non-plain spelling) had no smoke-test command of its own, only its test. My check 2 ran it for real, and it holds.

Still not proposed, as the second acceptance listed them:

- `LIVE_POINT_NAMES` is used only by tests.
- The `test_template_*` function names and `TEMPLATE_PIPELINE` were kept on purpose.
- The untested real wiring of `extra_environment` and `ca_bundle`.
- `list.pop(0)` in `_Makefiles.read`.
- The draft `trust-store.sh` has no licence header (the human's).

## 5 Documentation

S0012's docs criterion is met:

- `docs/operator-guide/pipeline.md:112`, *Name the makefile*, names the plain-form rule, its reason, the four refused spellings with their fault, and the single fault for `../Makefile`.
- `docs/project-guide/pipeline.md:168` names the rule beside the `MakeFilePath` and `is_inside_checkout` rules, and says the schema does not carry it.

The faults shown on both pages match, word for word, what the smoke test printed. `docs/operator-guide/pipeline.md:109` still lists only the character rule's values. Line 112 follows it at once, so the two paragraphs read as one rule and do not contradict each other.

Read as a newcomer, from `README.md` through the operator guide's index and `start-a-project.md` to *Name the makefile* and *Checking a repository*, the pages agree with each other and with the smoke test. Two remarks:

- The decision log's entry *The makefile a definition names, and the kit's `kit.mk`, are protected paths* (`docs/decisions.md:1775`) does not mention that a protected `make_file` is compared as written and is therefore held to its plain form. The reason is in both guides, and S0012's docs criterion did not ask for it in the log. So this is a remark, not a finding.
- `docs/brochure/README.md:457-459`, dated v1.1, still says "A new project starts from the **template**" and "Only Python is proven". It is still the human's call (6).

## 6 Decisions taken for the human

The lasting ones of `feature.md` 1 to 33 are listed in the first two acceptances' reports. Added since then:

1. Decision 34: the second acceptance's proposal S0012 was built as proposed. This took the second acceptance's choice to refuse a non-plain `make_file` rather than normalise it silently.
2. S0012, intake, answered by the human: the story's third smoke test drops `-q`, because `addopts` already holds it (option a).
3. S0012, coder's choice: the plain-form rule lives inside `_make_file_faults` rather than as a separate entry of `_RULES`, so a value outside the checkout (`./../Makefile`) keeps exactly one fault. The reviewer agreed.
4. Still open from the earlier acceptances, with no answer recorded in `feature.md`:
   - whether the decision log's "Why after the static part" (S0009) keeps the reviewer's wording;
   - whether `docs/brochure/README.md` should stop naming the template and stop calling Python the only proven stack;
   - whether to ratify the change to `tests/guards/test_tests_layout.py` in S0011, which decision 33's leave did not name.

Earlier tests changed since the second acceptance: none. The reviewer of S0012 confirms it. The tester appended one test to `tests/pipeline/domain/test_pipeline_definition_make_file.py` and one to `tests/entry/test_check_project.py`, and only extended the imports of the latter. Every earlier test is unchanged, so no leave was needed and none was used.

## 7 Slow checks

The project offers nothing beyond `make check` except `make mutants` (check 3). `make check` as found ended with `check: green`, `test: green (106.6 s)` and coverage of 99.14 %. The JUnit report holds 11331 test cases, 10 more than at the second acceptance, which are S0012's rows.

The slowest tests in `.reports/junit.xml` are all outside the feature:

- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other`, 20.6 s;
- then the `ROOMY_LIMIT` kills at 10.0 s each: `test_podman_timeout_status` twice, `test_claude_runtime_resume` twice, `test_process_session`, `test_document_examples`, `test_opencode_events` and `test_opencode_resume_session`.

To count the feature's tests, I selected the test cases whose module or name matches `check_project`, `project_check`, `project_run`, `kit`, `pack`, `make_file`, `installed_builder` or `write_paths`. That gives 487 cases, 19.3 s together.

Disk: at the start and now, `/srv/factory/self` has 71.2 GB free and 1.2 GB used, and `/srv/factory/self/state` and `/tmp` have 71.2 GB free and 0.0 GB used. No growth.

## 8 Cost

The twelve stories cost 122 runs, 236.2 min, 1008 turns and $39.53, about $3.29 a story. S0012 added 7 runs, 9.5 min and $1.11, the cheapest story with code in the feature. It went once through each stage with no rework round: intake twice (one question), then tests, doing, review, docs and smoke test.

S0003 still stands out, at $6.53. As the first acceptance reported, its journal gives the cause: two leaves, a `PLR0913` exception and a test rework.

Human interventions: 15 questions answered, all of cause `question`, and 2.0 h waited. The one since the second acceptance is S0012's intake, about the `-q` in its smoke test. It waited about a minute, from the intake at 06:03 to the second intake at 06:05.

The story that needed the human most is still S0001, with two questions, one of which waited 102 minutes overnight. Over the whole feature, most questions asked for a leave to change an earlier test (decisions 15, 16, 20, 21, 25, 29, 30, 32 and 33). The stories that came with their leave already worded (S0012 needed none) asked least.

## Proposed stories

None. S0012 closed the second acceptance's one finding. What remains (the `make_file: .` edge, the decision log's remark, the brochure, the earlier noticed items) is either of no weight or the human's to decide.

## Journal

1. factory: started acceptance as self.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit 12a46ec53f19cc4d698727a871cf050123b3c157.
3. factory: started acceptance as self.
4. acceptance-reviewer: accepted; 0 stories proposed

   1 Scope: none. S0012, the second acceptance's one proposal (decision 34), stays inside the scope item "the makefile a pipeline definition names". Every scope item has its story.
   2 Feature smoke test: green.
     - The guide's assembly is `project: ready`, exit 0, for all three packs, both lines and both makefile places (12 of 12).
     - The kit alone lacks exactly the stack's four targets. An uncommitted fix does not count, and the committed one does.
     - The start facts run through the named makefile.
     - The take refuses `factory/kit.mk`, and the named `factory/Makefile` wherever the definition names it.
     - S0012's four spellings that are not plain (`./factory/Makefile`, `factory//Makefile`, `factory/./Makefile`, `factory/Makefile/`) are refused with `must be written as factory/Makefile` and exit 1, and the misleading "is missing" is gone. `../Makefile` keeps its one fault.
     - `--run` refuses before it builds anything, because this container has no instance environment.
     - Edge of no weight: `make_file: .` is accepted. Not proposed.
   3 Mutation testing: by sweep, not run here.
   4 Noticed:
     - S0012's intake found that `-q` in the story's pytest command doubles the `-q` in `addopts`; the human dropped it.
     - The documenter worked around the document check reading backticked bare values as file paths.
     - `make duplicates` is unchanged (8 new, 38 known, 5 gone).
     - The earlier items that were not proposed are still not proposed.
   5 Documentation: S0012's docs criterion is met in both guides, and the faults match the smoke test's output word for word. Remarks: the decision log's protected-paths entry does not mention the plain form, and the dated brochure still names the template (the human's call).
   6 Decisions for the human:
     - Decision 34.
     - The intake answer (a).
     - The coder kept the rule inside `_make_file_faults`, so a value outside the checkout keeps one fault.
     - Still open from the earlier acceptances: the decision log wording from S0009, the brochure, and ratifying the change to `test_tests_layout.py` (S0011).
     - Earlier tests changed in S0012: none.
   7 Slow checks: nothing offered beyond `make check`, which is green (11331 cases, test 106.6 s, coverage 99.14 %). Slowest test: `test_documents_marker`, 20.6 s. The feature's 487 cases take 19.3 s together. Disk unchanged since the start (71.2 GB free, 1.2 GB used).
   8 Cost: 122 runs, 236.2 min, $39.53, about $3.29 a story. S0012 cost $1.11 and had no rework round. S0003 still stands out at $6.53 (two leaves, a `PLR0913` exception, a test rework). 15 questions answered, 2.0 h waited. S0001 needed the human most (two questions, 102 min overnight). Most questions over the feature asked for a leave to change an earlier test.
