---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 690
comments_read: [6933812910, 6934072851]
handed_over: null
claim:
  instance: self
  stage: doing
  started_at: '2026-11-17T00:44:36.259417Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-16T22:49:41.566527Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-16T22:49:41.573495Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-16T22:50:21.062434Z'
  stage: intake
  run: 90d27bf0547c4f7da1847693825a8b1b
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T00:32:00.839227Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T00:32:03.988821Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T00:32:30.976450Z'
  stage: intake
  run: 48772020b7f24fcf8a7d8710fe7a63a8
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T00:32:36.179283Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T00:36:54.547685Z'
  stage: tests
  run: 445ed7c542a84cdabee463cd059c3c7a
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T00:36:59.687217Z'
  stage: doing
- number: 10
  speaker: coder
  kind: question
  at: '2026-11-17T00:43:46.266651Z'
  stage: doing
  run: 3636fea364e14879aa0823c607bdb426
  blocked: question
- number: 11
  speaker: human
  kind: comment
  at: '2026-11-17T00:44:33.779412Z'
  stage: doing
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-17T00:44:36.259417Z'
  stage: doing
---

# The conformance check reads a repository

## Description

Whether a repository is ready for the factory is found out today by starting a story and reading the stop. This story builds the static part of the conformance check: a command `factory-check-project <folder>` that reads the commit at `HEAD` of the git repository in `<folder>`, prints one line per point and ends with `project: ready` or `project: not ready`. It judges six points: the pipeline definition, the makefile's targets, the stage file, the agents of the roles, the write paths and the forms. It starts no container and no project command, and it reads the committed files only, never the work tree, since the factory reads commits too. The live part (building the image, running `make sync` and `make check`) is a later story of this feature, and so is the makefile that a pipeline definition names: this story reads `Makefile` at the root. The console script's line in `pyproject.toml` is the human's change after this story; until then the command runs as `python -m factory.entry.check_project`.

## Interface

- `src/factory/pipeline/domain/project_check.py` (`domain`):

```python
POINT_NAMES: tuple[str, ...] = ("pipeline definition", "makefile", "stage file", "agents", "write paths", "forms")
MAKEFILE = "Makefile"
SYNC_COMMAND = "sync"

class ProjectPoint(BaseModel):          # frozen, unknown keys forbidden
    name: str
    faults: list[str] = []
    skipped: bool = False

class MakefileInclude(BaseModel):       # frozen, unknown keys forbidden
    path: str
    optional: bool

def makefile_targets(text: str) -> frozenset[str]: ...
def makefile_includes(text: str) -> list[MakefileInclude]: ...
def target_faults(commands: Sequence[str], targets: Collection[str]) -> list[str]: ...
def write_path_faults(definition: PipelineDefinition, tracked: Sequence[str]) -> list[str]: ...
def report_lines(points: Sequence[ProjectPoint]) -> list[str]: ...
def is_ready(points: Sequence[ProjectPoint]) -> bool: ...
```

  - `makefile_targets`: the names before the colon of every rule line. A rule line starts at column 0 with one or more names separated by spaces or tabs, then optional spaces, then `:` or `::`; a name holds only letters, digits, `_`, `.` and `-`. A line where the colon is followed by `=` (`X := 1`, `X ::= 1`) is an assignment and gives no target; an indented line, a comment line, a line whose names hold `%` or `$` give none.
  - `makefile_includes`: one entry for each path of every line that starts at column 0 with `include`, `-include` or `sinclude` followed by a space or a tab; `optional` is true for `-include` and `sinclude`. A path that holds `$` is left out.
  - `target_faults`: `no target <name>` for every name of `commands` that is not in `targets`, in the order of `commands`.
  - `write_path_faults`: `role <role>: write path <pattern> matches no tracked file` for every write path of every role that matches no path of `tracked`, matched as the factory matches write paths (`factory.agents.domain.write_paths.matches_any`). A write path that holds `{` (a placeholder such as `{work_item}`) is not judged.
  - `report_lines`: one line per point in the given order, `<name>: ok` without faults, `<name>: FAIL: <fault>; <fault>` with faults (joined by `; `), `<name>: skipped: no valid pipeline definition` when `skipped`; then the last line: `project: ready` when no point has a fault, otherwise `project: not ready (<n> faults)` with the number of all faults, `(1 fault)` for one. A skipped point has no fault of its own.
  - `is_ready`: true when no point has a fault.
- `src/factory/pipeline/application/project_check.py` (`application`):

```python
class ProjectCheck:
    def __init__(self, git: Git, pipeline_reader: PipelineDefinitionReader, agents: AgentDefinitionReader, ref: str = "HEAD") -> None: ...
    def run(self) -> list[ProjectPoint]: ...
```

  - `run` returns the six points in the order of `POINT_NAMES`, every file read through `git` at `ref`.
  - `pipeline definition`: fault `factory/pipeline.yml is missing` when the file is not there; otherwise the fault text of `PipelineDefinitionInvalid` when `pipeline_reader.parse` refuses it.
  - Without a valid pipeline definition the points `makefile`, `agents` and `write paths` are `skipped`; `stage file` and `forms` are judged all the same.
  - `makefile`: fault `Makefile is missing` when it is not there. Otherwise the targets are those of `Makefile` and of every file it includes, followed through included files until no new file appears, each file read once, every path taken from the root of the repository; a missing file of a non-optional include is the fault `<including file>: included file <path> is missing`, a missing optional one is nothing. The commands are the names of the definition's `project_commands` in their order, and `sync` after them when they do not hold it; their faults are `target_faults`.
  - `stage file`: no fault when `factory/stage.Containerfile` is not there (the project then runs on the factory's stage image); otherwise the reason of `StageLayerRefused` when `factory.machine.domain.stage_layer.stage_layer` refuses its text.
  - `agents`: for every role of the definition, in its order, `agents.read(<role>)`; an `AgentDefinitionMissing` is the fault `role <role>: no agent file`, any other `AgentDefinitionError` the fault `role <role>: <its fault>`.
  - `write paths`: `write_path_faults` with all files tracked at `ref`.
  - `forms`: fault `<path> is missing` for each of `factory/story-form.md` and `factory/feature-form.md` that is not there.
- `src/factory/entry/check_project.py` (`entry`): `main(argv: Sequence[str] | None = None) -> int`, with `if __name__ == "__main__": sys.exit(main())`. Usage: `factory-check-project [--agent-home <dir>] <folder>`.
  - The installed agents are read from `--agent-home`, or from the environment's `FACTORY_CLAUDE_HOME` when the option is not given; the project's own agents come first, as in a stage (`ProjectAgentDefinitions` with the ref `HEAD`).
  - It prints the lines of `report_lines` and returns 0 when the project is ready and 1 when it is not.
  - It returns 2 and prints one line on standard error: the usage when the folder is not given, more than one is given, or no agent home is known; `cannot read <folder>: <reason>` when the folder is no git repository or has no commit at `HEAD`.
- Tests: `tests/pipeline/domain/test_project_check.py`, `tests/pipeline/application/test_project_check_run.py` (real repositories in `tmp_path`, the agents through a real agent home written there) and `tests/entry/test_check_project.py`. The table of `tests/guards/test_areas.py` gains the two new modules; `feature.md` gives the leave for it (decision 4): "S0001 to S0004 may add their new modules to the table of `tests/guards/test_areas.py`, and to any other guard table that lists every module or every entry command."

## Acceptance criteria

1. `makefile_targets` returns the names of rule lines and nothing else: `check: lint` gives `check`; `a b: c` gives `a` and `b`; `a<tab>b: c` gives `a` and `b`; `check : lint` gives `check`; `x::` gives `x`; `X := 1`, `X ::= 1`, an indented `y: z`, `# c: d`, `%.o: %.c`, `$(T): u` and `src/a.o: x` give nothing: rows of one parametrized test.
2. `makefile_includes` returns `include a.mk b.mk` as two entries that are not optional, `-include c.mk` and `sinclude d.mk` as optional ones, `include<tab>e.mk` as one entry that is not optional, and nothing for `include $(X).mk`, an indented `include e.mk` and `included: f`: rows of one parametrized test.
3. `target_faults(["check", "lint"], {"check"})` is `["no target lint"]`, and `[]` when both are there.
4. `write_path_faults` names a role's write path that matches no tracked file, names none for one that matches, and none for `{work_item}` and `{feature}/backlog/*`: rows of one parametrized test.
5. `report_lines` prints `ok`, `FAIL` with two faults joined by `; `, and `skipped` lines as the Interface says, and ends with `project: ready`, `project: not ready (1 fault)` or `project: not ready (3 faults)`; `is_ready` is true only in the first case: rows of one parametrized test.
6. `ProjectCheck.run` on a committed repository that holds a valid pipeline definition, a `Makefile` with every command's target, both forms, a file under every write path and an installed agent for every role, and no `factory/stage.Containerfile`, returns six points without a fault, in the order of `POINT_NAMES`.
7. Each fault alone turns its point and no other: a missing `factory/pipeline.yml`; a definition the reader refuses (its fault text is the fault); a missing `Makefile`; a `Makefile` without the target `lint`; a `Makefile` without a `sync` target when `project_commands` does not name `sync`; a stage file with two `FROM`; a role without any agent file; a project agent file under `factory/agents/` without front matter; a write path that matches nothing; a missing `factory/feature-form.md`; and a valid stage file (an `ARG` for the base and a `FROM ${...}` alone) as a row that turns no point: rows of one parametrized test.
8. Without a valid pipeline definition, `makefile`, `agents` and `write paths` are skipped, and `stage file` and `forms` are still judged.
9. A target that only an included file holds counts: `Makefile` with `include factory/kit.mk`, the target in `factory/kit.mk`, and the same through a second level of include. A missing included file is the fault `Makefile: included file factory/kit.mk is missing`; with `-include` it is no fault. `factory/kit.mk` including a missing `factory/deep.mk` is the fault `factory/kit.mk: included file factory/deep.mk is missing`. `Makefile` including `a.mk` and `a.mk` including `Makefile` again ends, and the target in `a.mk` counts without a fault: rows of one parametrized test.
10. A role whose agent exists only as the project's file `factory/agents/<role>.md` at `HEAD` has no fault; a file that exists only in the work tree and is not committed does not count.
11. `main` prints the report and returns 0 for a ready repository and 1 for one with a fault; returns 2 with the usage on standard error without a folder, with two folders, and without `--agent-home` when `FACTORY_CLAUDE_HOME` is not set; returns 2 with `cannot read <folder>: ...` for a folder that is no git repository and for a repository without a commit; reads the agent home from `FACTORY_CLAUDE_HOME` when the option is not given; and returns 0 when `FACTORY_CLAUDE_HOME` names an empty folder and `--agent-home` a real agent home, since the option wins: rows of one parametrized test.
12. `make check` stays green.
13. docs: the operator guide (`docs/operator-guide/`, where it explains setting up a project) says that `factory-check-project <folder>` answers whether a repository is ready, what its six points judge, that it reads the commit at `HEAD` and starts nothing, what its three exit statuses mean, and where it takes the installed agents from; the project guide (`docs/project-guide/pipeline.md`) names the two modules and the rule that the check reads commits, not the work tree; `docs/decisions.md` records that the check is a command of its own and not a preflight item, because the preflight guards a machine and the check a repository.

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
git init -q "$d/p"; mkdir -p "$d/p/factory" "$d/p/src" "$d/p/tests" "$d/p/docs"
cp operator/template/factory/pipeline.yml factory/story-form.md factory/feature-form.md "$d/p/factory/"
cp operator/template/Makefile "$d/p/Makefile"
touch "$d/p/src/a.py" "$d/p/tests/t.py" "$d/p/docs/d.md" "$d/p/README.md"
git -C "$d/p" add -A; git -C "$d/p" -c user.name=t -c user.email=t@example.com commit -q -m one
uv run python -m factory.entry.check_project --agent-home agents "$d/p"; echo "status $?"
```
Expect: seven lines and the status: `pipeline definition: ok`, `makefile: ok`, `stage file: ok`, `agents: ok`, `write paths: ok`, `forms: ok`, `project: ready`, `status 0`.

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
git init -q "$d/p"; mkdir -p "$d/p/factory" "$d/p/src" "$d/p/tests" "$d/p/docs"
cp operator/template/factory/pipeline.yml factory/story-form.md "$d/p/factory/"
grep -v '^lint:' operator/template/Makefile > "$d/p/Makefile"
touch "$d/p/src/a.py" "$d/p/tests/t.py" "$d/p/docs/d.md" "$d/p/README.md"
git -C "$d/p" add -A; git -C "$d/p" -c user.name=t -c user.email=t@example.com commit -q -m one
uv run python -m factory.entry.check_project --agent-home agents "$d/p"; echo "status $?"
```
Expect: `makefile: FAIL: no target lint`, `forms: FAIL: factory/feature-form.md is missing`, the other four points `ok`, the last line `project: not ready (2 faults)`, then `status 1`.

```bash
uv run pytest tests/pipeline/domain/test_project_check.py tests/pipeline/application/test_project_check_run.py tests/entry/test_check_project.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-16 human: created.
2. factory: started intake as self.
3. intake: Intake found the story mostly buildable. I checked it against the code: `PipelineDefinitionReader`, `AgentDefinitionReader`, `ProjectAgentDefinitions`, `AgentDefinitionMissing` and `AgentDefinitionError`, `matches_any`, `stage_layer` and `StageLayerRefused`, `PipelineDefinitionInvalid`, `FACTORY_CLAUDE_HOME`, and the template's `pipeline.yml` and `Makefile` used by the smoke test. All of them exist as the Interface assumes. The placement in `domain`, `application` and `entry` fits the architecture. The story is within F0062's scope and follows decisions 2, 4, 6 and 7. The smoke test can run: `addopts` already sets `-q`, so the summary line prints. The docs criterion names what the reader must know and dictates no sentences. Six Interface clauses still have no criterion. I would like your word on adding these criteria:

   1. Each included file is read only once, so an include cycle ends. No criterion tests this. I would add a row to criterion 9: `Makefile` includes `a.mk`, `a.mk` includes `Makefile` again, and the target in `a.mk` counts with no fault and no endless loop. Add it, or drop the clause?

   2. Decision 7 and the Interface say a missing `factory/stage.Containerfile` gives no fault. A valid stage file (`ARG` base and `FROM ${...}` alone) should also be `ok`. No criterion pins either case. Criterion 6 does not say whether its repository has a stage file, and criterion 7 has only the refused side. I would make criterion 6's repository have no stage file and add a valid-stage-file row to criterion 8 or a new criterion.

   3. `makefile_targets` has clauses whose cases are missing from criterion 1. Names separated by a tab (`a\tb: c`). Spaces before the colon (`check : lint` gives `check`). A name with a character outside the allowed set (`src/a.o: x` gives nothing). I would add these three rows to criterion 1's table.

   4. `makefile_includes` needs the space after the keyword (`include` at column 0 followed by a space). Criterion 2's `included: f` row does not separate that rule from the `include` + space rule. I would add `include\te.mk` (tab after the keyword) as a row that gives nothing. Or should a tab count as the separator? If so, the Interface line changes.

   5. The fault `<including file>: included file <path> is missing` names the including file. Criterion 9 tests it only with `Makefile` as the includer. I would add a row where `factory/kit.mk` includes a missing `factory/deep.mk`, giving `factory/kit.mk: included file factory/deep.mk is missing`. That also tests that paths are taken from the repository root.

   6. Criterion 11 tests the agent home taken from `FACTORY_CLAUDE_HOME`, but not that `--agent-home` wins when both are given. I would add a row: the variable points to an empty folder, the option to a real agent home, and `main` returns 0.

   What I'd choose: add all six as rows of the existing parametrized criteria, with the tab case in question 4 counting as no include. Then I would accept the story on the `tests` route.
4. 2026-11-17 human: Add all six, as rows of the existing parametrized criteria. On 4: a tab after the keyword counts as the separator, as make itself reads it, so change the Interface line to "followed by a space or a tab" and make `include<tab>e.mk` a row that gives one entry; keep `included: f` as the row that gives nothing. On 2: criterion 6's repository has no stage file, and a valid stage file is a new row that is ok.
5. factory: started intake as self.
6. intake: accepted
   Carried in the human's answer from journal entry 4. Interface: `makefile_includes` now accepts a space or a tab after the keyword. Criterion 1 gains three rows: `a<tab>b: c` gives `a` and `b`, `check : lint` gives `check`, and `src/a.o: x` gives nothing. Criterion 2 gains `include<tab>e.mk` as one entry that is not optional, and `included: f` stays a row that gives nothing. Criterion 6's repository has no `factory/stage.Containerfile`. Criterion 7 gains a valid stage file as a row that turns no point. Criterion 9 gains the nested missing include (`factory/kit.mk: included file factory/deep.mk is missing`) and the include cycle that ends, and its cases are now rows of one parametrized test. Criterion 11 gains the row where `--agent-home` beats `FACTORY_CLAUDE_HOME`. The Description is unchanged, because the meaning of the task did not change.
   - Interface: concrete modules and signatures in `factory.pipeline.domain`, `factory.pipeline.application` and `factory.entry`, and every collaborator the Interface names exists (checked in round 0).
   - Criteria: every Interface clause now has a criterion, with both sides of each rule: the separators and the refused names of `makefile_targets`; the tab, the optional forms and the `$` path of `makefile_includes`; the missing and present stage file; the missing include at both levels and the cycle; skipped versus judged points; the option versus the environment variable. Each criterion is testable by one test function.
   - Smoke test: runnable from the repository with the template files and `agents/` as the agent home. Each `Expect:` names exact lines and the exit status. The pytest command passes no `-q`, because `addopts` sets it.
   - Docs criterion: names what the operator guide, the project guide and the decision log must tell the reader, and dictates no sentences.
   - Architecture: pure parsing and judging in `domain`; the use case in `application` over the existing `Git`, `PipelineDefinitionReader` and `AgentDefinitionReader` interfaces; the wiring only in `entry`. No new tool and no new dependency.
   - Scope: within F0062 (decisions 2, 4, 6 and 7). The live check and the makefile a pipeline definition names are left to later stories, as the Description says. The guard table change has the feature's leave (decision 4).
   Route: tests, because the Interface adds code under `src/`.
7. factory: started tests as self.
8. tester: Wrote the tests for every criterion against the Interface. `make lint` is green. `make test` is red for the intended reason: the three new test modules cannot import `factory.pipeline.domain.project_check`, `factory.pipeline.application.project_check` and `factory.entry.check_project`, which do not exist yet. Two tests in `tests/guards/test_documents_marker.py` also error in the same run. They collect the whole suite, so the import errors break them; they should pass again once the modules exist.

   Criterion → test:
   - criterion 1: tests/pipeline/domain/test_project_check.py::test_makefile_targets_are_the_names_of_rule_lines
   - criterion 2: tests/pipeline/domain/test_project_check.py::test_makefile_includes_are_the_paths_of_include_lines
   - criterion 3: tests/pipeline/domain/test_project_check.py::test_target_faults_name_each_command_without_a_target
   - criterion 4: tests/pipeline/domain/test_project_check.py::test_write_path_faults_name_write_paths_that_match_no_tracked_file. The definition is `PIPELINE_YAML`, so the `{work_item}` and `{feature}/backlog/*` paths are in every row and never judged.
   - criterion 5: tests/pipeline/domain/test_project_check.py::test_report_lines_name_each_point_and_end_with_the_verdict
   - criterion 6: tests/pipeline/application/test_project_check_run.py::test_a_ready_repository_has_six_points_without_a_fault
   - criterion 7: tests/pipeline/application/test_project_check_run.py::test_each_fault_turns_its_point_and_no_other. The expected fault of the refused definition comes from `pipeline_outcome`, and the two-`FROM` reason from `stage_layer`. For the project agent without front matter, the test checks exactly one fault that starts with `role coder: ` and is not `no agent file`; the reader's own words after that prefix are not pinned.
   - criterion 8: tests/pipeline/application/test_project_check_run.py::test_without_a_valid_definition_three_points_are_skipped_and_two_judged, with a missing and a refused definition as rows.
   - criterion 9: tests/pipeline/application/test_project_check_run.py::test_targets_count_through_included_files
   - criterion 10: tests/pipeline/application/test_project_check_run.py::test_a_project_agent_counts_only_when_committed
   - criterion 11: tests/entry/test_check_project.py::test_main_prints_the_report_or_one_error_and_returns_its_status. The usage row checks that the single stderr line contains `factory-check-project [--agent-home <dir>] <folder>`; any prefix such as `usage: ` is the coder's choice.
   - criterion 12: `make check`, run by the coder.
   - criterion 13: docs, for the docs stage.

   Fixtures used by the tests: `PIPELINE_YAML`, which has no `sync` command. The ready repository's `Makefile` therefore holds `check`, `lint`, `test` and `sync`, plus `src/a.py`, `tests/t.py`, `docs/d.md`, `README.md` and both forms. The agent home holds an installed agent for each of the seven roles.

   Files created:
   - tests/pipeline/domain/test_project_check.py
   - tests/pipeline/application/test_project_check_run.py
   - tests/entry/test_check_project.py
   - tests/support/project_check_support.py: the ready repository and the agent home, shared by the application and entry tests.

   File changed: tests/guards/test_areas.py now lists `domain.project_check` and `application.project_check` under `pipeline`, with the leave of the feature's decision 4.

   Modules the test run could not import: factory.pipeline.domain.project_check, factory.pipeline.application.project_check, factory.entry.check_project.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: Stopped before `review`. The code is built and the story's three test files pass (56 tests). `make check` is red on one test that this story did not write: `tests/guards/test_agent_home_wiring.py::test_the_agent_definition_reader_is_built_once_from_the_settings_agent_home`. Changing that test needs your leave.

    Failure from the `make check` run:
    ```
    E   AssertionError: assert [('factory.en...agent_home'])] == [('factory.en...agent_home'])]
    FAILED tests/guards/test_agent_home_wiring.py::test_the_agent_definition_reader_is_built_once_from_the_settings_agent_home
    ```
    The guard requires exactly one call `FrontmatterAgentDefinitionReader(settings.agent_home)`, in `factory.entry.wiring`. The Interface requires the command to read the installed agents from `--agent-home`, or from `FACTORY_CLAUDE_HOME` when the option is not given, without building the instance settings. A reader built from that folder cannot also match the argument text `settings.agent_home`. The guard therefore contradicts the Interface (R9). Feature decision 4 gives leave only for tables that list every module or every entry command. This guard is neither.

    Options:
    - A (my choice): the reader is still built in exactly one place. The tester changes the guard's expected list to `[("factory.entry.wiring", ["agent_home"])]`. The code already has this shape: the new `build_agent_definitions(git, agent_home, ref=PIPELINE_REF)` in `src/factory/entry/wiring.py` is now the only construction. `build_boundaries` calls it with `settings.agent_home`, and the new command calls it with its folder.
    - B: the guard allows a second call site in `factory.entry.check_project`, and the command builds its own reader. I would revert the wiring builder.
    - C: the command takes its agent home only from the instance settings. This drops `--agent-home` and contradicts criterion 11 and the smoke test.

    With your answer for A or B, I end with `tests` and name the guard change.

    What I built:
    - `src/factory/pipeline/domain/project_check.py`: `POINT_NAMES`, `MAKEFILE`, `SYNC_COMMAND`, `ProjectPoint`, `MakefileInclude`, and the rule and report functions as the Interface states them. A rule line is one regex, and a lookahead refuses `:=` and `::=`. Include lines drop a trailing `#` comment.
    - `src/factory/pipeline/application/project_check.py`: `ProjectCheck`. It reads every file through `Git.show_file` at the ref. A small private `_Makefiles` follows includes breadth-first, and a set of seen paths ends cycles.
    - `src/factory/entry/check_project.py`: `main`. It parses the arguments by hand instead of with argparse, because argparse prints the usage and the error on two stderr lines and the Interface allows one line. "cannot read" covers a `GitError` or `OSError` from `resolve("HEAD")` and a missing commit.
    - `src/factory/hosting/adapters/git_cli.py` and the `Git` interface docstring: `list_files(ref, "")` now lists the whole tree. Before, the empty directory gave `[]` because of its `/` prefix. No existing caller passes `""`. I chose this over a new `Git` operation, which would add to the interface.

    Rejected: building `ProjectAgentDefinitions` directly in the entry module, which breaks the same guard and adds a second construction site.

    Checks:
    - lint, types, layers, sast, secrets, licenses and `make guides` are green.
    - The test stage is red only on the guard above.
    - The smoke test was not run: the shell refused the command, so the smoke-test stage still has to run it.

    No refactor pass yet; it waits for the answer. The journal did not change the Description.
11. 2026-11-17 human: A. Leave given: the tester may change the expected list of `tests/guards/test_agent_home_wiring.py` to the one construction in `factory.entry.wiring` with the argument `agent_home`; the guard keeps its name and still checks that the reader is built in exactly one place.
12. factory: started doing as self.
