---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 711
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-17T08:27:14.161840Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-17T08:32:44.766152Z'
  stage: acceptance
  run: 30453305afff4e86b1179e8703622a15
stories: [F0062-S0001, F0062-S0002, F0062-S0003, F0062-S0004, F0062-S0005, F0062-S0006, F0062-S0007, F0062-S0008, F0062-S0009, F0062-S0010, F0062-S0011, F0062-S0012, F0062-S0013, F0062-S0014, F0062-S0015, F0062-S0016]
outcome: null
---

# Acceptance of Projects start from a kit and a stack pack

## Recommendation

`accepted`. S0016, the one story since the fifth acceptance, did what that acceptance proposed. Each pack's `## Checks` section now carries the kit's line about `factory/Makefile`. A `CLAUDE.md` filled by step 5 of the guide therefore keeps exactly one such line, for all three packs and both wordings.

`make check` is green as I found it. The feature's smoke test is green across all twelve assemblies of kit and pack. Nothing I found has the weight of a story: what remains open is the human's (the starters, the brochure, the drafts' wording), and it is listed under 6.

## 1 Scope

None. The first five acceptances found every scope item covered by S0001 to S0015. S0016 comes from the fifth acceptance's proposal and was built as proposed (decision 38). It belongs to the scope item "the kit, and the stack packs". It changes only the three `operator/packs/<pack>/CLAUDE.sections.md` files, as byte-for-byte copies of the human's drafts, plus two guide steps and one new test. No module under `src/factory/` changed.

The Goal holds:

- a project of each stack is assembled from kit and pack;
- `factory-check-project` says whether it is ready;
- an existing repository keeps its own root `Makefile` unchanged, and its agents are now told in `CLAUDE.md` to run `make -f factory/Makefile` (check 2).

The human's change 3 (the three starters, each run with `--run` on the VM) is the human's and is not judged here.

## 2 Feature smoke test

This is the walk-through of the fifth acceptance, with one addition: each assembly now also fills `CLAUDE.md` as step 5 of `docs/operator-guide/start-a-project.md` says. The script `claude.py` does this independently of the tests' `pack_claude_md`:

- it replaces the kit skeleton's sections with the pack's sections of the same heading;
- it keeps one wording of the `<Either: … Or: …>` placeholder: the forwarding wording where the root `Makefile` is the kit's, the `make -f factory/Makefile` wording where the repository keeps its own;
- it counts the lines of `## Checks` that name `factory/Makefile`.

Then, for the c-host project with its own root `Makefile`, the script does what an agent following that `CLAUDE.md` would do:

- it runs the root's `make check`, which is the repository's own makefile and has no `check`;
- it takes the command the line names and runs it dry (`-n`), because the stack's tools are not in this container.

`protect.py` reads each project's `factory/pipeline.yml` with `RuamelPipelineDefinitionReader` and asks `refusal` under `protected_paths(definition.make_file)` for a role widened to `factory/*`, `src/*` and `*`.

Everything ran in `mktemp -d` folders, removed afterwards. On my first run, my own `claude.py` cut the placeholder at the nested `<target>`. That was my regular expression, not the kit, and the run below is with it fixed (see 4).

`smoke.sh`:

```bash
#!/usr/bin/env bash
set -u
F=/work/checkout; CHECK=$F/.venv/bin/factory-check-project; S=$(dirname "$0")
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
unset MAKEFLAGS MAKELEVEL MFLAGS
commit() { git -C "$1" add -A && git -C "$1" -c user.name=t -c user.email=t@example.com commit -q -m "$2"; }
assemble() { # $1 project, $2 pack, $3 line, $4 own root makefile (own|none) -- steps 2 to 6 of start-a-project.md
  p=$1; mkdir -p "$p/factory" "$p/src" "$p/test" "$p/docs"; git init -q -b develop "$p"
  touch "$p/src/main.x" "$p/test/t.x" "$p/docs/index.md" "$p/README.md"
  [ "$4" = own ] && printf 'all:\n\techo own\n' > "$p/Makefile"
  cp $F/operator/kit/factory/* "$p/factory/"; cp $F/operator/kit/CLAUDE.md "$p/"
  mv "$p/factory/pipeline.$3.yml" "$p/factory/pipeline.yml"; sed -i "s|\"tests/\*\"|\"test/*\"|" "$p/factory/pipeline.yml"; rm -f "$p/factory/pipeline."{thin,full}.yml
  (cd $F/operator/packs/$2 && find . -type f ! -name CLAUDE.sections.md ! -name TRAPS.md) | while read -r f; do
    mkdir -p "$p/factory/$(dirname "$f")"; cp "$F/operator/packs/$2/$f" "$p/factory/$f"; done
  [ -f "$p/Makefile" ] || cp $F/operator/kit/root.Makefile "$p/Makefile"
  w=either; [ "$4" = own ] && w=or
  (cd $F && uv run --quiet python $S/claude.py operator/kit/CLAUDE.md operator/packs/$2/CLAUDE.sections.md $w "$p/CLAUDE.md")
  commit "$p" assemble
}
for pack in python c-host java-gradle; do for line in thin full; do for own in none own; do
  p=$d/$pack-$line-$own; echo "$pack, $line, root makefile $own:"; assemble "$p" $pack $line $own
  out=$(cd $F && $CHECK --agent-home agents "$p"); rc=$?
  outside=$(git -C "$p" ls-files | grep -v -e '^factory/' -e '^src/' -e '^test/' -e '^docs/' -e '^README.md$' | tr '\n' ' ')
  echo "  check: $(echo "$out" | grep -c ': ok$') ok, $(echo "$out" | tail -1), exit $rc; outside factory/: $outside"
done; done; done
echo "### an agent in a repository with its own root Makefile, following CLAUDE.md (c-host, thin)"
p=$d/c-host-thin-own
echo "-- what the root's make check does:"; (cd $p && make check 2>&1; echo "exit $?")
cmd=$(grep -o 'make -f factory/Makefile check' $p/CLAUDE.md | head -1); echo "-- CLAUDE.md says: $cmd (dry run)"
(cd $p && $cmd -n 2>&1 | head -4; echo "exit ${PIPESTATUS[0]}")
echo "-- the same in the forwarding case (c-host, thin, none): make -n check"
(cd $d/c-host-thin-none && make -n check 2>&1 | head -4; echo "exit ${PIPESTATUS[0]}")
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
echo "### root forwarding makefile, with root files and folders named after targets"
p=$d/fwd; mkdir -p $p/factory; cp $F/operator/kit/factory/kit.mk $p/factory/; cp $F/operator/kit/root.Makefile $p/Makefile
printf 'include factory/kit.mk\n.PHONY: check lint test\nlint:\n\t$(start)\n\t$(green)\ntest:\n\t$(start)\n\techo running tests\n\t$(TEST_EXIT)\n\t$(green)\ncheck: lint test\n\techo "check: green"\n' > $p/factory/Makefile
mkdir $p/test $p/check; touch $p/lint
run() { (cd $p && make "$@" 2>&1 | sed 's/([0-9]*\.[0-9] s)/(N s)/'; echo "exit ${PIPESTATUS[0]}"); }
echo "-- make"; run
echo "-- make test with a red recipe"; run test TEST_EXIT='exit 3'
echo "-- make factory-forward"; run factory-forward
echo "### the kit's start facts through the forwarding root makefile"
p=$d/python-thin-none; git init -q --bare $d/remote.git; git -C $p remote add origin $d/remote.git; git -C $p push -q origin develop
git -C $p checkout -q -b work-item/x; echo 'print(1)' > $p/src/new.py; echo x >> $p/factory/pipeline.yml; commit $p change
(cd $p && echo "facts-changes:" && make facts-changes; echo "exit $?")
echo "### --run here (no stage environment in this container)"
(cd $F && $CHECK --run --agent-home agents "$d/c-host-thin-none" > $d/run.txt 2>&1); echo "exit $?"; tail -1 $d/run.txt
```

`claude.py`:

```python
"""Fill CLAUDE.md as step 5 of start-a-project.md says: replace four sections, keep one wording."""
import re, sys
from pathlib import Path
kit, pack, wording, out = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])
def sections(text):
    parts = re.split(r"(?m)^(?=## )", text)
    return parts[0], {p.splitlines()[0]: p for p in parts[1:]}
head, kit_s = sections(kit.read_text())
_, pack_s = sections(pack.read_text())
assert set(pack_s) <= set(kit_s), set(pack_s) - set(kit_s)
text = head + "".join(pack_s.get(h, body) for h, body in kit_s.items())
m = re.search(r"<Either: (.*?) Or: (.*)>$", text, re.M)
assert m and text.count("<Either:") == 1, "the placeholder must be there once"
text = text[: m.start()] + (lambda w: w[0].upper() + w[1:])(m.group(1) if wording == "either" else m.group(2)) + text[m.end():]
out.write_text(text)
checks = sections(text)[1]["## Checks"]
print(f"  CLAUDE.md: sections replaced {sorted(h[3:] for h in pack_s)}; Checks lines naming factory/Makefile: {sum('factory/Makefile' in l for l in checks.splitlines())}; placeholder left: {'<Either' in text}")
print("  " + next(l for l in checks.splitlines() if "factory/Makefile" in l))
```

`protect.py`:

```python
import sys
from pathlib import Path
from factory.agents.domain.agent_runs import WritePathSettings
from factory.agents.domain.write_paths import protected_paths, refusal
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader
for p in sys.argv[1:]:
    d = RuamelPipelineDefinitionReader().parse(Path(p, "factory/pipeline.yml").read_text())
    s = WritePathSettings(root=Path(p), write_paths=["factory/*", "src/*", "*"], protected_paths=protected_paths(d.make_file))
    paths = ["factory/kit.mk", "factory/Makefile", "Makefile", "CLAUDE.md", "factory/pipeline.yml", "factory/gitleaks.toml", "src/a.py"]
    print(Path(p).name, "make_file:", d.make_file, "writable:", {x: refusal(x, s) is None for x in paths})
```

What it printed (`bash smoke.sh`, exit 0). The twelve assemblies each printed three lines. Below are the first block and the last block in full, then all twelve condensed to one line each:

```console
python, thin, root makefile none:
  CLAUDE.md: sections replaced ['Checks', 'Not without asking (end the stage with `question`)', 'Review', 'Tests']; Checks lines naming factory/Makefile: 1; placeholder left: False
  - The factory's targets are in `factory/Makefile`. The root `Makefile` forwards every target to it, so `make check` works at the root.
  check: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
[…]
java-gradle, full, root makefile own:
  CLAUDE.md: sections replaced ['Checks', 'Not without asking (end the stage with `question`)', 'Review', 'Tests']; Checks lines naming factory/Makefile: 1; placeholder left: False
  - The factory's targets are in `factory/Makefile`. The root `Makefile` is this repository's own, and every target the agents' instructions name is run as `make -f factory/Makefile <target>`, `make check` as `make -f factory/Makefile check`.
  check: 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
```

```text
python, thin, root makefile none: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
python, thin, root makefile own: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
python, full, root makefile none: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
python, full, root makefile own: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, thin, root makefile none: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, thin, root makefile own: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, full, root makefile none: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
c-host, full, root makefile own: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, thin, root makefile none: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, thin, root makefile own: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, full, root makefile none: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
java-gradle, full, root makefile own: naming factory/Makefile: 1; placeholder left: False; 6 ok, project: ready, exit 0; outside factory/: CLAUDE.md Makefile
```

```console
### an agent in a repository with its own root Makefile, following CLAUDE.md (c-host, thin)
-- what the root's make check does:
make: *** No rule to make target 'check'.  Stop.
exit 2
-- CLAUDE.md says: make -f factory/Makefile check (dry run)
started=$(date +%s%N)
if [ -n "" ]; then clang-format --dry-run --Werror ; fi
tenths=$(( ($(date +%s%N) - started) / 100000000 )); echo "lint: green ($((tenths / 10)).$((tenths % 10)) s)"
started=$(date +%s%N)
exit 0
-- the same in the forwarding case (c-host, thin, none): make -n check
make --no-print-directory -f factory/Makefile check
started=$(date +%s%N)
if [ -n "" ]; then clang-format --dry-run --Werror ; fi
tenths=$(( ($(date +%s%N) - started) / 100000000 )); echo "lint: green ($((tenths / 10)).$((tenths % 10)) s)"
exit 0
### protection (a role widened to factory/*, src/* and *)
python-full-none make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'CLAUDE.md': False, 'factory/pipeline.yml': False, 'factory/gitleaks.toml': True, 'src/a.py': True}
java-gradle-thin-own make_file: factory/Makefile writable: {'factory/kit.mk': False, 'factory/Makefile': False, 'Makefile': False, 'CLAUDE.md': False, 'factory/pipeline.yml': False, 'factory/gitleaks.toml': True, 'src/a.py': True}
### the kit alone
exit 1
makefile: FAIL: factory/Makefile is missing
write paths: FAIL: role builder: write path tests/* matches no tracked file; role builder: write path docs/* matches no tracked file
project: not ready (3 faults)
### an uncommitted factory/Makefile does not count, the committed one does
project: not ready (3 faults)
project: not ready (2 faults)
### root forwarding makefile, with root files and folders named after targets
-- make
lint: green (N s)
running tests
test: green (N s)
check: green
exit 0
-- make test with a red recipe
running tests
make[1]: *** [factory/Makefile:7: test] Error 3
make: *** [Makefile:8: test] Error 2
exit 2
-- make factory-forward
make: Nothing to be done for 'factory-forward'.
exit 0
### the kit's start facts through the forwarding root makefile
facts-changes:
A	src/new.py
exit 0
### --run here (no stage environment in this container)
exit 2
cannot run: FACTORY_REPOSITORY_URL: missing
```

Green. The fifth acceptance's finding is gone. A `CLAUDE.md` filled by step 5 now keeps exactly one line naming `factory/Makefile` under `## Checks`, for each pack, both lines and both root makefiles, and no placeholder is left. In the repository with its own root `Makefile`:

- the root's `make check` ends with status 2;
- the command that `CLAUDE.md` names reaches the pack's `check` in `factory/Makefile`, as the forwarding root does.

The rest is as at the fifth acceptance:

- All twelve assemblies are `project: ready`, with only `CLAUDE.md` and `Makefile` outside `factory/`.
- `factory/Makefile`, `factory/kit.mk`, `Makefile`, `CLAUDE.md` and `factory/pipeline.yml` are protected.
- The forwarding root `Makefile` runs targets beside a folder or file of their name, passes on a red recipe's status, and does not forward `factory-forward`.
- The start facts leave out `factory/`.
- An uncommitted fix does not count.

`--run` refuses here before building anything, because this container has no instance environment. No `--run` of a project in the one layout is recorded since S0013. That run is part of the human's change 3, on the VM.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

From S0016, the one story since the fifth acceptance:

- S0016, coder (entry 7): the tester's first test pinned each pack file by its sha256. `make secrets` flagged the three hex values as high-entropy strings. The project's `CLAUDE.md` already asks for low-entropy hex in tests for this reason, but a hash of real text cannot be low-entropy. The human answered (a), an expected list of lines, with no marker and no baseline entry (entry 8). The tester changed the test (entry 12). This is a lesson for the tester rather than a story: a pin by content hash is a secrets finding in this project.
- S0016, coder (entry 14) and reviewer (entry 16): noticed nothing else. `make duplicates` stayed at `8 new, 38 known, 5 gone`, the same as at the second to fifth acceptances.
- S0016, documenter (entry 18): it found nothing stale. It cross-read the guide's firmware example (`start-a-project.md:87`), the kit entry of `agents.md`, the `kit_support.py` entry of the index and the one-layout decision, and found them current. It again wrote `<project>/factory/Makefile` in prose because of the document check, as S0015 did.
- Mine:
  - The kit's placeholder `<Either: … Or: …>` holds a nested placeholder, `<target>`, in its second wording. My own script first cut the placeholder at that inner `>`. A person who fills it by hand is unlikely to slip there, and the tests read the line verbatim. Not proposed.
  - The guide's firmware example (`start-a-project.md:80-87`) copies the kit's `CLAUDE.md` but does not fill it, because the example stops at the check. Its closing sentence says that the project's `CLAUDE.md` names `make -f factory/Makefile` under `## Checks`, which holds once step 5 is done. It does not mislead, since step 5 is the step before. Not proposed.
  - `operator/packs/c-host/TRAPS.md:6` still advises naming `make_file: factory/Makefile` for an existing firmware repository, which the kit now does for every project. This is the human's draft text, as at the fifth acceptance, and is listed under 6.

Still not proposed, as the earlier acceptances listed them:

- `LIVE_POINT_NAMES` is used only by tests;
- the `test_template_*` names remain, `tests/agent_files/test_claude_files.py::test_template_rules_file_is_the_python_project_text` among them, which S0016 changed again under its leave;
- the real wiring of `extra_environment` and `ca_bundle` is untested;
- `_Makefiles.read` uses `list.pop(0)`;
- `factory/gitleaks.toml` and the other pack files under `factory/` are not protected paths (check 2 shows it).

## 5 Documentation

S0016's docs criterion is met:

- `docs/operator-guide/start-a-project.md` step 5 says the pack's `## Checks` section carries the kit's line as its second bullet, so the replacement keeps it. It says to keep the one wording that fits, and why the line matters.
- `operator/packs/README.md` step 4 says the same.
- Neither page asks the reader to keep a line that the replacement removes, and check 2 shows the assembly they describe.
- `docs/project-guide/operator.md:25` names the new test `tests/operator_scripts/test_pack_checks_line.py`.

Read as a newcomer from `README.md` through `docs/operator-guide/start-a-project.md`, the kit README and the packs README, the pages agree with each other and with the behaviour. One example: "A target is run by hand from the root: `make check` through the forwarding root `Makefile`, or `make -f factory/Makefile check`" says the same thing in the kit README, the guide and `pipeline.md:108`. Kit README step 3 ("fill in each `<...>` placeholder") is for the kit alone and does not contradict the packs README's step 4, which the kit README's step 4 points to.

Still the human's, as before: `docs/brochure/README.md:457-459` (v1.1) names the template and calls Python the only proven stack.

## 6 Decisions taken for the human

`feature.md` lists decisions 1 to 38, and the first five acceptances gathered them up to 37. Added since:

1. Decision 38, the human's: S0016 built as proposed, with its leave as worded, and the drafts in `planning/packs-draft/` hold the kit's line. The fifth acceptance's option (a) was taken.
2. S0016, the coder's question (entry 7), answered (a) by the human (entry 8): the test pins each pack file's other lines by an expected list instead of a sha256. No `pragma: allowlist secret` and no `.secrets.baseline` entry.
3. S0016, the documenter's choice: no decision-log entry, because the packs being copies of the drafts is already decision 23.
4. Still open for the human, from the fifth acceptance: `operator/packs/c-host/TRAPS.md:6` repeats advice the kit now carries for every project. Reword the draft or leave it.
5. Still open from earlier acceptances, with no answer recorded in `feature.md`:
   - the brochure (see 5);
   - the wording of the decision log's "Why after the static part" (S0009);
   - ratifying the S0011 change to `tests/guards/test_tests_layout.py`, which decision 33's leave did not name;
   - whether `factory/*` becomes a protected path as a whole;
   - the human's change 3 (the three starters, each run with `--run` on the VM);
   - moving this feature's folder to `factory/archive/`, and a release.

Earlier tests changed since the fifth acceptance, as S0016's reviewer entry 16 lists them:

- `tests/agent_files/test_claude_files.py`: `TEMPLATE_RULES_LINES` gained only the kit's line, under the leave in S0016's Interface, which the human wrote with the story and decision 38 gave as worded. `test_template_rules_file_is_the_python_project_text` keeps its name and what it checks.

The other changed test file, `tests/operator_scripts/test_pack_checks_line.py`, is S0016's own. No earlier test was changed without a leave.

## 7 Slow checks

The project offers nothing beyond `make check` except `make mutants` (check 3). `make check` as I found it ended with `check: green`, `test: green (102.0 s)` and coverage of 99.14 %.

The JUnit report holds 11370 test cases, 8 more than at the fifth acceptance. S0016's `test_pack_checks_line.py` added 7 of them (3 + 3 + 1 rows), which take 0.01 s together. As at the fifth acceptance, I did not trace the one case left over.

The slowest tests are all outside the feature:

- `tests/guards/test_documents_marker.py::test_the_documents_marker_selects_every_test_of_the_marked_modules_and_no_other`, 19.8 s;
- then the `ROOMY_LIMIT` kills at 10.0 s each: `test_podman_timeout_status` twice, `test_document_examples`, `test_claude_runtime_provider_limit` and `test_claude_runtime_resume`.

The feature's tests are the cases matching `check_project`, `project_check`, `project_run`, `kit`, `pack`, `make_file`, `installed_builder`, `write_paths`, `one_layout` or `root_makefile`: 526 cases, 17.7 s together.

Disk: the Disk now line shows 70.6 GB free on `/srv/factory/self`, `/srv/factory/self/state` and `/tmp`. At the previous record (the fifth acceptance's) it was 70.8 GB. Used space is unchanged at 1.2 GB and 0.0 GB. The 0.2 GB less free space is on the shared pool, outside this instance's used space. S0016 changed three small text files and one test, which cannot explain it. As at the fourth and fifth acceptances, the likely cause is snapshots or the pool's other datasets during S0016's nine runs; I cannot see that from here.

## 8 Cost

The sixteen stories cost:

- 157 runs, 294.1 min, 1238 turns;
- 4788077 tokens in (50808692 more from cache) and 695441 out;
- $48.01, about $3.00 a story.

Since the fifth acceptance, S0016 alone cost 9 runs, 13.3 min and $1.74. Its coder's `make secrets` stop, the tester's sha256 pin (see 4), added one question and a second tests and doing round (entries 7 to 14). Without that, it would have been a five-run story. It does not stand out. S0003 is still the dearest, at $6.53, for the reasons the first acceptance gave: two leaves, a `PLR0913` exception and a test rework.

Human interventions: 17 questions answered, all of cause `question`, with 2.0 h waited. That is one more question than at the fifth acceptance (S0016's entry 7), and the wait rounds to the same 2.0 h. The story that needed the human most is still S0001: two questions, one of which waited 102 minutes overnight. Across the feature, most questions asked for a leave to change an earlier test, and S0016's one question was a test's form against `make secrets`.

## Proposed stories

None. Nothing I found has the weight of a story. The open items are the human's (the drafts' wording, the brochure, the starters) or were judged below a story's weight at earlier acceptances.

## Journal

1. factory: started acceptance as self.
2. acceptance-reviewer: accepted; 0 stories proposed
   1. Scope: none. S0016 was the fifth acceptance's proposal, built as proposed (decision 38). It copies the three packs' `CLAUDE.sections.md` from the human's drafts and changes two guide steps. No module under `src/factory/` changed, and every scope item is covered.
   2. Feature smoke test: green. All 12 assemblies (3 packs × 2 lines × with/without an own root `Makefile`) are `project: ready`, with only `CLAUDE.md` and `Makefile` outside `factory/`. Each assembly's `CLAUDE.md` was filled independently by the guide's step 5, and each keeps exactly one `## Checks` line naming `factory/Makefile`, with no placeholder left. In the own-root case, the root's `make check` exits 2, while the command `CLAUDE.md` names reaches the pack's `check`. Protection, the forwarding root makefile, the start facts and the HEAD-only reading still hold. `--run` is not possible in this container.
   3. Mutation testing: by sweep, not run here.
   4. Noticed: the tester's sha256 pin tripped `make secrets` (a lesson: a content hash is a secrets finding here). The kit placeholder nests `<target>`, which my own script first cut short. The firmware example's closing sentence holds only after step 5. c-host `TRAPS.md:6` repeats the kit's advice. Earlier acceptances' items stay unproposed.
   5. Documentation: none. `start-a-project.md` step 5 and `operator/packs/README.md` step 4 now match the behaviour, and the pages agree with each other. The brochure is still the human's.
   6. Decisions: decision 38; S0016's answer (a), expected lines instead of hashes, with no marker and no baseline entry; no decision-log entry by the documenter's choice. Still open for the human: c-host `TRAPS.md:6`, the brochure, the "Why after the static part" wording, ratifying the S0011 change to `test_tests_layout.py`, `factory/*` protection, the starters (change 3), and archiving and release. The one earlier test changed, `test_claude_files.py`, was changed under S0016's leave.
   7. Slow checks: nothing beyond `make check`, which was green (102.0 s, 99.14 %, 11370 cases, 8 more, 7 of them S0016's). The slowest test is `test_documents_marker` at 19.8 s. The feature's tests are 526 cases taking 17.7 s. Disk: 0.2 GB less free on the shared pool with used space unchanged, which the feature does not explain.
   8. Cost: $48.01 for 157 runs. S0016 cost $1.74 over 9 runs, which includes one secrets-driven round, and does not stand out; S0003 is still the dearest at $6.53. 17 questions were answered with 2.0 h waited, one more question than before (S0016 entry 7). S0001 is still the story that needed the human most.
