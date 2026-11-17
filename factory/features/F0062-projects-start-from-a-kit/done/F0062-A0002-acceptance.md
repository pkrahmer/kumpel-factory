---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 702
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-17T05:55:27.855030Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-17T06:02:16.709254Z'
  stage: acceptance
  run: f9e89ac01ff741ab9f5e96a13bd69030
- number: 3
  speaker: factory
  kind: done
  at: '2026-11-17T06:03:05.813733Z'
  stage: done
stories: [F0062-S0001, F0062-S0002, F0062-S0003, F0062-S0004, F0062-S0005, F0062-S0006, F0062-S0007, F0062-S0008, F0062-S0009, F0062-S0010, F0062-S0011]
outcome: accepted
---

# Acceptance of Projects start from a kit and a stack pack

## Recommendation

`accepted`. Every scope item has its story, and the three follow-ups of the first acceptance (S0009 to S0011) did what they promised. `make check` is green as I found it. The feature's smoke test is green: a project assembled from the kit and any of the three packs, on either line, with the factory's makefile at the root or named as `factory/Makefile`, is `project: ready`, and the take now refuses both `factory/kit.mk` and the named makefile. One finding remains, and it breaks no promise. A `make_file` spelled `./factory/Makefile` loads, but it escapes the protection and gets a misleading `is missing` from the check. One story is proposed for it.

## 1 Scope

None. The first acceptance (F0062-A0001, pull request 698) found every scope item covered: the static check (S0001), `make_file` (S0002), the live check (S0003), the installed builder (S0004), the kit (S0005), the three packs (S0006), the template's removal (S0007, decision 22) and the guide (S0008). Since then, three stories were added by decision 31. They are its proposals, and each stays inside the feature:

- S0009 brought the operator guide and the decision log up to the console script and the live part.
- S0010 made `factory/kit.mk` and the makefile `make_file` names protected paths: `protected_paths(make_file)` in `src/factory/agents/domain/write_paths.py:53`, used by `WritePathService.at` at the stage-start commit.
- S0011 tidied the feature's tests.

None of the three touches an out-of-scope item. The human's change 3 (the three starters) is the human's and is not judged here.

## 2 Feature smoke test

This is the first acceptance's walk-through, run again on today's `develop`. It assembles a project exactly as `docs/operator-guide/start-a-project.md` says, for every pack, both lines and both makefile places, and checks each with the installed `factory-check-project`. Since S0010, it also asks the factory's own rules, through the real definition reader, what a role widened to `factory/*` and `src/*` may write in four of the assembled projects. Further steps:

- the kit alone;
- an uncommitted fix, then the same fix committed;
- the kit's start facts through the brownfield makefile;
- the spelling `./factory/Makefile` that S0010's reviewer worried about;
- `--run`.

Everything ran from `mktemp -d` folders, which were removed afterwards.

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
echo "### a make_file spelled ./factory/Makefile"
p=$d/c-host-full-factory; sed -i 's|^make_file: factory/Makefile|make_file: ./factory/Makefile|' $p/factory/pipeline.yml; commit $p dot
(cd $F && $CHECK --agent-home agents "$p" | tail -1)
(cd $F && uv run --quiet python $S/protect.py $p)
echo "### --run here (no stage environment in this container)"
(cd $F && $CHECK --run --agent-home agents "$d/c-host-thin-root" > $d/run.txt 2>&1); echo "exit $?"; tail -3 $d/run.txt
```

`protect.py`, beside it, which reads each project's `factory/pipeline.yml` with the factory's reader and asks `refusal` under `protected_paths(definition.make_file)`:

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
### a make_file spelled ./factory/Makefile
project: not ready (1 fault)
c-host-full-factory make_file: ./factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': True, 'Makefile': False, 'src/a.py': True}
### --run here (no stage environment in this container)
exit 2
cannot run: FACTORY_REPOSITORY_URL: missing
```

The fault of the `./factory/Makefile` case, from the same project run alone (a second script, `dot.sh`, that assembles the C pack's full line with that spelling):

```console
$ bash dot.sh
pipeline definition: ok
makefile: FAIL: ./factory/Makefile is missing
stage file: ok
agents: ok
write paths: ok
forms: ok
project: not ready (1 fault)
```

**Green.** Every promise of the Goal holds:

- All twelve assemblies are ready.
- The kit alone lacks exactly the stack's four targets.
- The check reads the commit and not the work tree.
- The start facts leave out `factory/` through a named makefile.
- With S0010, `factory/kit.mk` is refused everywhere, and so is `factory/Makefile` wherever the definition names it. Where it does not, as in the first protection line, the root `Makefile` is the factory's and is refused instead.
- `--run` refuses before it builds anything. This container has no instance environment, and decision 12 says the live part needs one. Its exit status is 2. The human ran the live part on factory-vm2 (decision 23).

One finding, from the spelling `./factory/Makefile`. The definition loads it: `_make_file_faults` in `src/factory/pipeline/domain/pipeline_definition.py:274` checks only `is_inside_checkout`. `make -f ./factory/Makefile` would run the same file. But `protected_paths` appends the text as written, so `factory/Makefile` becomes writable. And the check reports `./factory/Makefile is missing` for a file that is committed. Only the human writes the definition, so no agent can open this hole by itself. The fault message still misleads, though, and the protection S0010 promised depends on a spelling. Proposed: F0062-S0012.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

From S0009 to S0011, the stories since the first acceptance:

- S0010 reviewer, documenter and smoke tester: a `make_file` spelled `./factory/Makefile` is not normalised and does not protect `factory/Makefile`. Confirmed in check 2, together with the misleading `is missing` from the check. Proposed: F0062-S0012.
- S0009 documenter: the decision log's reason "Why after the static part" (`docs/decisions.md`, entry *The live part of the conformance check works on a clone with an image of its own*) comes from the reviewer's reading of the code, not from the human. Listed under 6 for the human to reword or accept.
- S0010 and S0011 coders: `make duplicates` records `8 new, 38 known, 5 gone`. I ran it again and got the same counts. One of the new findings is the feature's: `LIVE_POINT_NAMES` (`src/factory/pipeline/domain/project_check.py:21`) is used only by tests. `ProjectRun` spells `"image"` four times (`src/factory/machine/application/project_run.py:127-137`) and keeps its own `_SYNC` and `_CHECK`. The tests pin the order against the constant, so nothing is wrong, but the code does not take the names from the constant. Not proposed: it is small, and the duplicates baseline is the place to decide it. The other seven new findings are outside this feature: the runtimes' similar lines, `hand_over`, `readme_problems` and three cost-record fields.
- S0011 tester: the renames kept every test function's name, as the Interface asked. So `test_template_*` functions still live in the `test_python_pack_*` modules, and `TEMPLATE_PIPELINE` (`tests/support/shipped_agents.py:17`, named in `docs/project-guide/agents.md:404`) still names the kit's `pipeline.full.yml`. Not proposed: they are names only, and they were kept on purpose.
- From the first acceptance, still not proposed: the untested real wiring of `extra_environment` and `ca_bundle` in `src/factory/entry/check_project.py`; `list.pop(0)` in `_Makefiles.read`; and the draft `planning/packs-draft/java-gradle/scripts/trust-store.sh` without a licence header, which is the human's. The one-time import-linter segfault did not recur in my `make check`.

## 5 Documentation

S0009 closed the first acceptance's two document findings:

- The stale "Until the command is installed" sentence is gone.
- Both pages say why their examples run `python -m factory.entry.check_project`.
- The decision log has an entry for the live part, which widens the S0001 entry.

S0010 brought the protected paths into `docs/operator-guide/pipeline.md:107` and `:210`, `docs/project-guide/agents.md:452` and the decision log. Its console example in `agents.md:443` prints `True True 14 13 13`, which matches the code. S0011's links in the project guide name `kit_make_support.py` and `dockerfile_instructions`.

Read as a newcomer, from `README.md` through the operator guide's index and `start-a-project.md` to `pipeline.md`'s *Name the makefile* and *Checking a repository*, the pages agree with each other and with what the smoke test showed. Two remarks, neither of which misleads a user:

- `docs/operator-guide/pipeline.md:109` lists the accepted and refused values of `make_file`, but says nothing of `./factory/Makefile`. It is accepted today and works badly (check 2). F0062-S0012's docs criterion covers it.
- `docs/brochure/README.md`, dated v1.1, still says "A new project starts from the **template**" (line 459) and "Only Python is proven … Another stack is the test still to come" (line 457). The brochure says its figures are a record of their time, so this is the human's call (6).

## 6 Decisions taken for the human

The lasting ones of `feature.md` 1 to 30 are listed in the first acceptance's report and are not repeated here. Added since then:

1. Decision 31: the first acceptance's three proposals were built in its order.
2. Decision 32 (S0010): `protected_paths(make_file)` is `PROTECTED_PATHS`, then `factory/kit.mk`, then the named makefile. A `make_file` already in the list is not added again, and the duplicate test is an exact string match, not `matches_any`; the coder chose this. `PROTECTED_PATHS` keeps its twelve patterns.
3. S0009: the decision log's "Why after the static part" is the reviewer's wording, taken from the code (the live points use the definition's makefile and time limits). Accept it, or reword it.
4. Decision 33 (S0011): test function names were kept through the renames, so `test_template_*` function names and `TEMPLATE_PIPELINE` remain (4).
5. Still open from the first acceptance: whether `docs/brochure/README.md` should stop naming the template and stop calling Python the only proven stack.
6. For the proposed F0062-S0012: refuse a `make_file` that is not in its plain form (my choice), or normalise it silently in `protected_paths` and the check. Refusing keeps one spelling in the definition, the take and the check. Normalising would accept a definition that the human might not have meant.

Earlier tests changed since the first acceptance, each with its leave as the reviewers' entries name it:

- S0009: none (documents only).
- S0010: `tests/agents/application/test_write_paths_guard.py` and `tests/pipeline/application/test_write_paths.py` (decision 32's leave, `protected_paths(None)`).
- S0011, under decision 33's leave ("exactly the changes this story's Interface names to the earlier tests it names"):
  - `test_project_check_run.py`, `test_make_commands_make_file.py`, `test_installed_builder.py`, `test_packs.py` and `dockerfile_support.py`;
  - the three renamed `test_python_pack_*` modules, and `kit_make_support.py` with its importers `test_kit_makefile.py` and `kit_support.py`;
  - `test_operator_guide_files.py`.
  
  `tests/vm/test_stage_image.py` was changed under the standing leave to move a shared helper.

A finding on the letter of a leave: `tests/guards/test_tests_layout.py` (its `FORMER_ROOT_HELPERS`, `FORMER_ROOT_TEST_MODULES` and the placement pattern `test_template_*.py` → `test_python_pack_*.py`) is not named in S0011's Interface. Decision 33's leave covers only the earlier tests the Interface names. The reviewer accepted the change as "carried by the renames". The tester named the change in its entry, and the guard checks the same placement. So this is a change the human should ratify, not a hidden one. No earlier test was changed without some named leave.

## 7 Slow checks

The project offers nothing beyond `make check` but `make mutants` (check 3). `make check` as found: `check: green`, `test: green (110.1 s)`, coverage 99.14 %, 11321 test cases.

The slowest tests in `.reports/junit.xml`:

- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other` (20.0 s);
- then seven tests at 10.0 s each, the `ROOMY_LIMIT` kills (`test_podman_timeout_status` twice, `test_claude_runtime_resume` twice, `test_process_session`, `test_opencode_resume_session`, `test_opencode_events`).

None of them is the feature's. The feature's 434 test cases (check, run, kit, packs, builder, `make_file`, write paths) take 17.9 s together. The slowest of them is a row of the areas guard, at 2.2 s.

Disk: `/srv/factory/self` had 71.5 GB free at the start and 71.4 GB now, and its use stayed at 1.2 GB. `/srv/factory/self/state` and `/tmp` show the same 0.1 GB less, so they share one pool. A tenth of a gigabyte fits my `make check` and smoke-test caches and the rounding. No growth to explain.

## 8 Cost

The eleven stories cost 115 runs, 226.8 min, 970 turns and $38.42, about $3.49 a story. The first eight cost $34.05, as the first acceptance reports. The three follow-ups cost $4.36:

| Story | Runs | Minutes | Cost |
| --- | --- | --- | --- |
| S0009 | 5 | 5.8 | $0.85 |
| S0010 | 7 | 11.9 | $1.79 |
| S0011 | 7 | 9.7 | $1.72 |

S0003 still stands out, at $6.53. Its journal gives the cause, as the first acceptance reported: two leaves, a `PLR0913` exception and a test rework. Among the follow-ups, S0010 is the dearest, a full route with a new test module for the take. S0009 needed one docs-review round (an unexplained reason and two long sentences).

Human interventions: 14 questions answered, all of cause `question`, and 2.0 h waited. The first eight stories had 12 of them and 1.9 h. The two since then are the intakes of S0010 (the unworded leave and the exact list for `"Makefile"`) and S0011 (the unworded leave, the wrong docs criterion, the builder assertion and the function names). Together they waited a few minutes.

The story that needed the human most is still S0001, with two questions, one of which waited 102 minutes overnight. Both follow-ups with tests asked for the same thing, a leave that the first acceptance's proposals left as "proposed wording". F0062-S0012 needs no such leave, because its tests go beside the earlier ones and change none.

## Proposed stories

- `F0062-S0012-make-file-is-written-in-its-plain-form.md`: the pipeline definition refuses a `make_file` that is not in its plain form (`./factory/Makefile`, `factory//Makefile`), and names the plain spelling. This closes the gap in S0010's protection and the misleading `is missing` of the check (checks 2 and 4).

## Journal

1. factory: started acceptance as self.
2. acceptance-reviewer: accepted; 1 story proposed (F0062-S0012)

   1 Scope: none. Every scope item has its story. S0009 to S0011 are the first acceptance's three proposals (decision 31), each inside the feature.
   2 Feature smoke test: green.
     - For the three packs, both lines and both makefile places, the guide's assembly is `project: ready`, exit 0, in all twelve combinations.
     - The kit alone lacks exactly the stack's four targets. An uncommitted fix does not count, and the same fix committed does.
     - The start facts run through the named makefile.
     - The take refuses `factory/kit.mk`, and also the named `factory/Makefile` when the definition names it.
     - `--run` refuses before it builds anything, because this container has no instance environment.
     - One finding: `make_file: ./factory/Makefile` loads, but leaves `factory/Makefile` writable, and the check reports it as "is missing". Proposed in F0062-S0012.
   3 Mutation testing: by sweep, not run here.
   4 Noticed:
     - The `./factory/Makefile` spelling (S0010's reviewer, documenter and smoke tester): proposed in S0012.
     - The decision log's "Why after the static part" is the reviewer's wording: listed under 6.
     - `LIVE_POINT_NAMES` is used only by tests, and `ProjectRun` spells the point names itself: not proposed.
     - `test_template_*` function names and `TEMPLATE_PIPELINE` were kept on purpose by S0011: not proposed.
     - The first acceptance's items that it did not propose are still not proposed.
   5 Documentation: S0009 closed the first acceptance's two document findings. The protected paths and the renamed support module are documented consistently. The pages say nothing of the `./` spelling (S0012's docs criterion). The dated brochure still names the template and calls Python the only proven stack: the human's call.
   6 Decisions for the human:
     - Decisions 31 to 33.
     - S0010's exact-match duplicate rule.
     - The reviewer-worded reason in the decision log.
     - The brochure.
     - For S0012: refuse the spelling (my choice) or normalise it.
     - On the letter of a leave: `tests/guards/test_tests_layout.py` was changed in S0011, but the Interface that decision 33's leave covers does not name it. It is forced by the renames and checks the same placement, so the human should ratify it.
   7 Slow checks: nothing beyond `make check`, which is green (test 110.1 s, coverage 99.14 %). The slowest test is `test_documents_marker` at 20 s. The feature's 434 cases take 17.9 s together. Disk: 0.1 GB less free on the shared pool and use unchanged at 1.2 GB, which fits caches and rounding.
   8 Cost: 115 runs, 226.8 min, $38.42, about $3.49 a story. The follow-ups cost $4.36. S0003 still stands out at $6.53. 14 questions were answered, 2.0 h waited. S0001 needed the human most (two questions, 102 min overnight). S0010 and S0011 each asked for a leave that the proposals had left unworded.
3. factory: done (pull request merged); cost: 1 runs, 6.7 min, 40 turns, 96140 tokens in (2764498 more from cache), 28088 out, $1.60
