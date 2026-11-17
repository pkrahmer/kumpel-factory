---
stage: review
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 691
comments_read: [6934588171, 6934893656]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T01:08:39.851444Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T01:08:39.858634Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T01:09:14.563663Z'
  stage: intake
  run: 69127c53d0de492b8c00c9907e2b72e6
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T01:10:02.416640Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T01:10:05.309025Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T01:10:28.407312Z'
  stage: intake
  run: 0508575d6bee47dd8eb59f2c59c531f2
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T01:10:33.860407Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T01:15:24.604809Z'
  stage: tests
  run: 1444c256ecff4b33989e488f616b04fd
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T01:15:30.218705Z'
  stage: doing
- number: 10
  speaker: coder
  kind: question
  at: '2026-11-17T01:24:26.140047Z'
  stage: doing
  run: 0b85ebc081ab42459f6598aec9207740
  blocked: question
- number: 11
  speaker: human
  kind: comment
  at: '2026-11-17T01:26:14.880925Z'
  stage: doing
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-17T01:26:18.033795Z'
  stage: doing
- number: 13
  speaker: coder
  kind: result
  at: '2026-11-17T01:26:36.706498Z'
  stage: doing
  run: b204540416f549a09b73a4486885bf40
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-17T01:26:42.434313Z'
  stage: tests
- number: 15
  speaker: tester
  kind: result
  at: '2026-11-17T01:27:05.555731Z'
  stage: tests
  run: 6e0b6024159f4eefa4c8c0fedcae5be7
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-17T01:27:10.950071Z'
  stage: doing
- number: 17
  speaker: coder
  kind: result
  at: '2026-11-17T01:29:46.851313Z'
  stage: doing
  run: bf569057e48f42d797f2fbab8cf4e06c
---

# The pipeline definition names its makefile

## Description

The factory runs every project command as `make <command>` in the root of the checkout, so a project must give its root `Makefile` the factory's targets. An existing repository often has a root `Makefile` of its own, or none and no wish for one. After this story a pipeline definition may name the makefile the factory runs, with the key `make_file`, for example `make_file: factory/Makefile`: the sync before every agent run, every check, every report and every start fact then run as `make -f <path> ...`, still from the root of the checkout. A definition without the key behaves exactly as today. The conformance check of S0001 reads the named makefile instead of `Makefile`. The key is the pipeline contract's minor version 1.2; a definition that says 1.0 or 1.1 and holds the key loads as well, as it was with `context` at 1.1. The interfaces `ProjectCommands` and `StageEnvironment` keep their signatures: the two classes that call make ask for the name themselves.

## Interface

- `src/factory/pipeline/domain/pipeline_definition.py` (`domain`): `PipelineDefinition` gains

```python
    make_file: MakeFilePath | None = None
```

  - `MakeFilePath` is a string of one or more of the characters letters, digits, `_`, `.`, `/` and `-`, that does not start with `-` or `/`, and that stays inside the checkout (`is_inside_checkout`: no `..` segment). Any other value is a fault of the definition, named with the key.
- `src/factory/machine/application/make_file.py` (`application`), new:

```python
class MakeFileSource(ABC):
    @abstractmethod
    def make_file(self) -> str | None:
        """The makefile the pipeline definition names now, or `None` for make's own default."""
```

- `src/factory/pipeline/application/` (`application`): an implementation that reads the pipeline definition at `origin/<working branch>` (`PIPELINE_REF`) through git and the pipeline reader at every call, and returns its `make_file`; it returns `None` when the definition is missing or not valid (the tick stops for that on its own, and the preflight's probe then runs plain make).
- `src/factory/machine/adapters/make_commands.py` (`adapters`): `ContainerMakeCommands.__init__` gains `make_file: MakeFileSource | None = None`. With a source that returns a path, a check runs `make -f <path> sync` and then `make -f <path> --no-print-directory <command>`, and a start fact `make -f <path> --no-print-directory <command>`; with no source, or one that returns `None`, the calls are today's. The path is an argument of the script, never part of its text.
- `src/factory/machine/application/stage_environment.py` (`application`): the container stage environment gains the same optional source; with a path its sync runs `make -f <path> sync` in the checkout, otherwise `make sync`. The path is an argument of the sync script, never part of its text.
- `src/factory/entry/wiring.py` (`entry`): both get the source.
- `src/factory/pipeline/domain/project_check.py` and `src/factory/pipeline/application/project_check.py`: the point `makefile` reads the file `make_file` names when the definition has one, and `Makefile` otherwise; its faults name that file (`factory/Makefile is missing`, `factory/Makefile: included file ... is missing`). Included paths are still taken from the root of the repository, as make takes them.
- `operator/template/factory/pipeline.yml` and `factory/pipeline.yml` stay as they are.
- Tests: `tests/pipeline/domain/test_pipeline_definition_make_file.py`, `tests/machine/adapters/test_make_commands_make_file.py`, `tests/machine/application/test_stage_environment_make_file.py`, `tests/pipeline/application/test_make_file_source.py`, `tests/pipeline/application/test_project_check_make_file.py`, `tests/guards/test_make_file_wiring.py`. `feature.md` gives this leave (decision 4): "S0001 to S0004 may add their new modules to the table of `tests/guards/test_areas.py`, and to any other guard table that lists every module or every entry command." And this one (decision 5): "S0002 may change earlier tests that pin the exact argument list of the sync script or of the check script, where their only failure is the added argument for the makefile."

## Acceptance criteria

1. A definition with `make_file: factory/Makefile` loads and holds that value; one without the key holds `None`; the key loads with `contract: "1.0"`, `"1.1"` and `"1.2"` alike.
2. The definition is refused, with a fault that names `make_file`, for each of: an empty string, `-f`, `/etc/Makefile`, `../Makefile`, `a/../b`, `my file`, `a;b`, and a number; and accepted for `Makefile`, `factory/Makefile` and `build/factory.mk`: rows of one parametrized test.
3. `ContainerMakeCommands` with a source that returns `factory/Makefile` runs, for a check, a container command that calls make with `-f factory/Makefile` for the sync and for the command, and for a start fact for the command alone; the script's text does not hold the path. With no source and with a source that returns `None` the container command is the one of today: rows of one parametrized test, read from the fake container runs.
4. The source is asked at every call: a source that returns `None` first and `factory/Makefile` afterwards changes the second run.
5. The container stage environment with a source that returns `factory/Makefile` runs its sync with `make -f factory/Makefile sync`, and with no source or `None` with `make sync`; the script's text does not hold the path.
6. A real run, without a container, of the scripts' make calls on a checkout in `tmp_path` whose only makefile is `factory/Makefile` with the targets `sync` and `check`: the check's result is green and its last line is the one `factory/Makefile`'s `check` prints; without the source the same checkout's check is red.
7. The source built on git returns the `make_file` of the definition at `origin/<working branch>`, the new value after that branch moved, and `None` for a missing file, an invalid definition and a definition without the key: rows of one parametrized test where they share a setup.
8. `ProjectCheck.run` on a repository whose definition names `factory/Makefile`: no fault when that file holds every target and there is no root `Makefile`; the fault `factory/Makefile is missing` when it is not there, also when a root `Makefile` with every target exists.
9. `ProjectCheck.run` on a repository whose definition names `factory/Makefile`, which includes `common.mk`: no fault when `common.mk` is at the root of the repository and holds the targets `factory/Makefile` lacks; the fault `factory/Makefile: included file common.mk is missing` when `common.mk` is only beside it at `factory/common.mk`: rows of one parametrized test.
10. The project commands and the stage environment that `factory.entry.wiring` builds both read `make_file` from the pipeline definition at `origin/<working branch>`: on a wired instance whose definition names `factory/Makefile`, a check and a sync, read from the fake container runs, call make with `-f factory/Makefile` (a guard in the style of `tests/guards/test_agent_home_wiring.py` is an acceptable test).
11. `make check` stays green.
12. docs: the operator guide's page on the pipeline definition (`docs/operator-guide/pipeline.md`) explains `make_file`: what it is for (an existing repository keeps its own root `Makefile`), that every project command and the sync then run as `make -f <path>` from the root of the checkout, that paths inside that makefile are therefore still relative to the root, which values are refused, and that it is contract 1.2 while 1.0 and 1.1 still load; the project guide (`docs/project-guide/pipeline.md` and `docs/project-guide/machine.md`) names the source interface and the rule that the path is always an argument; `docs/decisions.md` records the decision of 2026-11-16 that the pipeline definition names the makefile and that make stays the one command runner for every stack.

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
git init -q "$d/p"; mkdir -p "$d/p/factory" "$d/p/src" "$d/p/tests" "$d/p/docs"
sed '1a make_file: factory/Makefile' operator/template/factory/pipeline.yml > "$d/p/factory/pipeline.yml"
cp factory/story-form.md factory/feature-form.md "$d/p/factory/"
cp operator/template/Makefile "$d/p/factory/Makefile"
touch "$d/p/src/a.py" "$d/p/tests/t.py" "$d/p/docs/d.md" "$d/p/README.md"
git -C "$d/p" add -A; git -C "$d/p" -c user.name=t -c user.email=t@example.com commit -q -m one
uv run python -m factory.entry.check_project --agent-home agents "$d/p"; echo "status $?"
git -C "$d/p" mv factory/Makefile Makefile; git -C "$d/p" -c user.name=t -c user.email=t@example.com commit -q -m two
uv run python -m factory.entry.check_project --agent-home agents "$d/p"; echo "status $?"
```
Expect: first six lines ending in `: ok`, then `project: ready` and `status 0`; then, in the second report, `makefile: FAIL: factory/Makefile is missing`, `project: not ready (1 fault)` and `status 1`.

```bash
uv run python -c "
from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader as R
from factory.shared.domain.errors import PipelineDefinitionInvalid
text = open('operator/template/factory/pipeline.yml').read()
print(R().parse(text).make_file, R().parse('make_file: build/factory.mk\n' + text).make_file)
try:
    R().parse('make_file: ../Makefile\n' + text)
except PipelineDefinitionInvalid as error:
    print('refused', 'make_file' in error.fault)
"
```
Expect: two lines: `None build/factory.mk` and `refused True`.

```bash
uv run pytest tests/pipeline/domain/test_pipeline_definition_make_file.py tests/machine/adapters/test_make_commands_make_file.py tests/machine/application/test_stage_environment_make_file.py tests/pipeline/application/test_make_file_source.py tests/pipeline/application/test_project_check_make_file.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: Intake: the format check passed, and I read feature.md along with the modules the Interface names. Most of the story is buildable. MakeFilePath has both sides tested in criterion 2. Criteria 3 to 5 pin the container argv and keep the path out of the script's text. Criterion 7 covers the git-based source. The smoke test is runnable: pyproject's addopts already sets `-q`, so the third block prints its summary line. The docs criterion says what the reader must know without dictating sentences. Placement fits the architecture (an ABC in `machine.application`, the git-based implementation in `pipeline.application`, wiring in `entry`). The story is within the feature's scope (decisions 5, 8, 9). Three clauses of the Interface have no criterion. Lessons: "every clause of an Interface rule has its own criterion"; "every behaviour that the Description, the Interface or a decision of the feature states has its own criterion".

   1. Project check, included files. The Interface says the point's faults name the named file for an include as well (`factory/Makefile: included file ... is missing`), and that "included paths are still taken from the root of the repository, as make takes them". Criterion 8 tests only `factory/Makefile is missing` and the passing case. Options: (a) add a criterion before the two closing ones: "`ProjectCheck.run` on a repository whose definition names `factory/Makefile`, which includes `common.mk`: no fault when `common.mk` is at the root and holds the targets `factory/Makefile` lacks; the fault `factory/Makefile: included file common.mk is missing` when `common.mk` is only beside it at `factory/common.mk`", written as rows of one parametrized test; (b) drop both sentences from the Interface. I would choose (a).

   2. Wiring. The Interface says "`src/factory/entry/wiring.py`: both get the source", but no criterion checks that the wired `ContainerMakeCommands` and the container stage environment hold a source built on git. Neither the smoke test nor criteria 3 to 7 would catch wiring that leaves it out. Options: (a) add a criterion: "the project commands and the stage environment that `factory.entry.wiring` builds both read `make_file` from the pipeline definition at `origin/<working branch>`", tested on a wired instance whose definition names `factory/Makefile`, through the fake container runs; (b) accept that the wiring line is not tested and leave it to review. I would choose (a), with a guard in the style of `tests/guards/test_agent_home_wiring.py` as an acceptable test.

   3. Plain make when there is no source. "When the definition is missing or not valid … the preflight's probe then runs plain make" is covered only through criteria 3 and 7 (a source returning `None` gives today's call). I take that to be enough and need no new criterion. Please confirm.
4. 2026-11-17 human: 1: (a). 2: (a), and the guard in the style of `tests/guards/test_agent_home_wiring.py` is an acceptable test. 3: confirmed, no new criterion.
5. factory: started intake as self.
6. intake: accepted. I added the human's answers from journal entry 4 to the story. Criterion 9 is new and covers the included-file fault and that included paths are taken from the root, as rows of one parametrized test. That is answer 1 (a). Criterion 10 is new and checks that the project commands and the stage environment built by `factory.entry.wiring` both read `make_file` from the definition at `origin/<working branch>`. A guard in the style of `tests/guards/test_agent_home_wiring.py` is an acceptable test for it. That is answer 2 (a). Both go before the two closing criteria, which are now 11 and 12. The Interface's Tests line also names `tests/guards/test_make_file_wiring.py` for criterion 10. Answer 3 confirmed that no further criterion is needed.
   - Interface: it names concrete modules and signatures: `MakeFilePath` on `PipelineDefinition`, the `MakeFileSource` ABC, the git-based source, the optional source on `ContainerMakeCommands` and on the container stage environment, the wiring, and the project check. It also lists the tests and the human's leave for test changes (feature decisions 4 and 5).
   - Criteria: each one can be tested by a single test function, and each rule has its failing side. Criterion 2 covers the refused and accepted `make_file` values. Criteria 3 to 5 cover a source, no source and `None`, and keep the path out of the script text. Criterion 6 is a real run, red and green. Criterion 7 covers the moved branch, a missing file, an invalid definition and a definition without the key. Criteria 8 and 9 cover the missing-file fault and the included-file fault. Criterion 10 covers the wiring.
   - Smoke test: the three blocks can be run, and each `Expect:` line can be checked against the output. The pytest block passes no `-q` because pyproject's addopts already sets it.
   - Docs criterion: it names what the reader must know in the operator guide, the project guide and the decision log, and it dictates no sentences.
   - Architecture: the ABC is in `machine.application`, the git-based implementation in `pipeline.application`, the adapters take the source optionally, and only `entry` wires. The `ProjectCommands` and `StageEnvironment` interfaces keep their signatures.
   - Scope: within F0062 (feature decisions 4, 5, 8 and 9). The template and `factory/pipeline.yml` are not changed.
7. factory: started tests as self.
8. tester: Tests written for criteria 1 to 10. They are red on purpose because the modules under test do not exist yet. `make lint` is green.

   Criterion → test:
   - criterion 1: tests/pipeline/domain/test_pipeline_definition_make_file.py::test_the_definition_holds_its_make_file (contract 1.0, 1.1 and 1.2, and a definition without the key)
   - criterion 2: tests/pipeline/domain/test_pipeline_definition_make_file.py::test_a_make_file_outside_its_characters_or_the_checkout_is_refused (8 refused rows, each fault naming `make_file`, and 3 accepted rows)
   - criterion 3: tests/machine/adapters/test_make_commands_make_file.py::test_the_container_command_names_the_makefile_as_an_argument_only_when_the_source_gives_one (check and start fact × named, no source and `None`; today's exact argv for the last two)
   - criterion 4: tests/machine/adapters/test_make_commands_make_file.py::test_the_source_is_asked_at_every_call
   - criterion 5: tests/machine/application/test_stage_environment_make_file.py::test_the_sync_runs_the_makefile_the_source_names_as_an_argument (the root `Makefile` and `factory/Makefile` each leave their own marker, so the test shows which one the sync ran)
   - criterion 6: tests/machine/adapters/test_make_commands_make_file.py::test_a_check_runs_the_named_makefile_s_sync_and_command (real make through FakeContainerRuns; the base's only makefile is `factory/Makefile`; green with its last line when there is a source, red without one)
   - criterion 7: tests/pipeline/application/test_make_file_source.py::test_the_source_returns_the_make_file_of_the_definition_at_the_working_ref (rows: named, invalid definition, invalid `make_file`, no key), plus ::test_the_source_returns_none_for_a_missing_definition and ::test_the_source_reads_the_new_value_after_the_branch_moved. The last two need a setup of their own.
   - criterion 8: tests/pipeline/application/test_project_check_make_file.py::test_the_makefile_point_reads_the_named_makefile
   - criterion 9: tests/pipeline/application/test_project_check_make_file.py::test_the_named_makefile_s_includes_are_taken_from_the_root. In the row where `common.mk` sits beside the named makefile, the missing include also leaves `lint` and `sync` missing. So the test asserts that the include fault is among the faults, not that it is the only one.
   - criterion 10: tests/guards/test_make_file_wiring.py::test_the_wiring_builds_the_git_source_and_both_users_get_a_source. This is an AST guard in the style of test_agent_home_wiring.py, which the human accepted. It checks three things: `factory.entry.wiring` builds the git-based source class; `ContainerMakeCommands` is built only there, with a `make_file=` that is not None; every `ContainerEnvironment(...)` in src passes a `make_file=` that is not None.

   Files created: the six test files above and tests/support/make_file_support.py (`git_make_file_source_class()`, shared by test_make_file_source.py and the guard).

   Assumptions for the coder, where the Interface leaves a name open:
   - The git-based source class has no name in the Interface. The tests find it as the one concrete subclass of `MakeFileSource` in a module under `factory.pipeline.application`, and build it as `cls(git, pipeline_reader)`, positionally, in that order.
   - `ContainerEnvironment.__init__` takes its source as the keyword `make_file`, the same name `ContainerMakeCommands` uses ("the same optional source").
   - The stage environment is built by `stage_environment_of(boundaries)`, not in wiring. That call must therefore pass `make_file=` (for example from Boundaries) for the guard to pass. How the source reaches it is left to the coder.
   - New modules go in the table of tests/guards/test_areas.py under feature decision 4. I did not touch it, because `make_file.py` does not exist yet. If the coder needs that table changed, it is a test change for the tester.

   `make test` result: the 7 new modules (the domain test included) could not be imported, because `factory.machine.application.make_file` and `MakeFileSource` are missing. The domain test's red is the missing `make_file` key on `PipelineDefinition`. The two tests in tests/guards/test_documents_marker.py also errored, because the suite's collection failed on those imports. They should pass again once the imports resolve.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: Question: should the records contract's version rise to 4.6 for the new optional `make_file`? Raising it means changing three tests that earlier stories wrote, and the feature's leave does not cover that.

    The story is otherwise built. `make check` and `make guides` are green with the version left at 4.5. Every test the tester named passes.

    **The contradiction.** `make_file` is a field of `PipelineDefinition`, which `CONTRACT` names. So `uv run python -m factory.entry.contract` regenerated `src/factory/contract/pipeline-definition.schema.json`, and the new property is in it. The version rule in `docs/decisions.md` (records contract, "the minor for an added optional field or value") calls for 4.5 → 4.6. That is what `context` did with 4.4 → 4.5 (fd273e69d). I raised `RECORDS_CONTRACT` to 4.6 and regenerated. 17 tests then failed, because they pin "4.5":
    - `tests/pipeline/domain/test_contract.py:54` (`assert parsed["x-records-contract"] == "4.5"`)
    - `tests/shared/domain/test_contract_version_4.py:12,23`
    - `tests/shared/domain/test_contract_version_4_2.py:12,23`

    For example: `E AssertionError: assert '4.6' == '4.5'` at `tests/shared/domain/test_contract_version_4_2.py:12` in `_version`. Feature decision 5 allows changing only tests that pin the argv of the sync or check script. The standing leave in CLAUDE.md is only for moving shared helpers. So I set the version back to 4.5, and the working tree is green that way.

    Options:
    - (a) The records contract becomes 4.6. The tester changes "4.5" to "4.6" in those three files: `test_contract.py:54`, and lines 12 and 23 of both `test_contract_version_4*.py`. Then I set `RECORDS_CONTRACT = "4.6"` and regenerate the schemas.
    - (b) The version stays at 4.5 even though the schema changed. The reviewer will likely count that as a finding against the version rule.

    I would choose (a).

    **Built** (in the working tree, nothing committed):
    - `src/factory/pipeline/domain/pipeline_definition.py`:
      - `MakeFilePath` is a pattern of letters, digits and `_./-`. It may not start with `-` or `/`.
      - A new rule `_make_file_faults` refuses a `..` segment, using `is_inside_checkout`. Pattern faults name `make_file` through pydantic's location.
      - `make_file: MakeFilePath | None = None`.
      - The docstring says contract 1.2, and that 1.0 and 1.1 still load.
    - `src/factory/machine/application/make_file.py`: the `MakeFileSource` ABC, plus `asked_make_file(source)` so both callers ask the source the same way.
    - `src/factory/pipeline/application/make_file_source.py`: `GitMakeFileSource(git, pipeline_reader)`. It reads `PIPELINE_REF` at every call and returns `None` for a missing file, an invalid definition or a `GitError`.
    - `src/factory/machine/adapters/make_commands.py`: `ContainerMakeCommands(make_file=...)`. With a path it uses its own scripts, `"$1" -f "$3" sync && "$1" -f "$3" --no-print-directory "$2"` and the start fact's `"$1" -f "$3" --no-print-directory "$2"`. The path is the extra argument `$3`. Without a path the argv is unchanged.
    - `src/factory/machine/application/stage_environment.py`:
      - `_SYNC_SCRIPT` is now `_SYNC_PREPARATION + "make sync\n"`. `_NAMED_SYNC` ends with `make -f "$7" sync`, the path being a seventh argument.
      - `ContainerEnvironment(make_file=...)`.
      - `stage_environment_of` passes `boundaries.make_file`.
    - `src/factory/pipeline/application/boundaries.py`: new field `make_file: MakeFileSource | None = None`.
    - `src/factory/entry/wiring.py`: builds one `GitMakeFileSource(git, pipeline_reader)` and passes it to `ContainerMakeCommands` and to `Boundaries`.
    - `src/factory/pipeline/application/project_check.py`: the makefile point reads `definition.make_file or MAKEFILE` and names that path in its faults. Includes are still taken from the root.
    - `src/factory/contract/pipeline-definition.schema.json`: regenerated.
    - `pyproject.toml`: a per-file `PLR0913` ignore for `stage_environment.py`, as `make_commands.py` already has. The test pins `ContainerEnvironment(boundaries, snapshots, containers, make_file=...)`, and `tests/support/container_extra_support.py` passes `extra_environment` and `ca_bundle`, so all six arguments stay.

    **Main choice.** The stage environment gets its source from a `Boundaries` field that wiring fills, rather than having `stage_environment_of` build `GitMakeFileSource` itself. That keeps wiring as the only place sources are built. With a path, the scripts are separate texts rather than one script with `${3:+-f "$3"}`, so every argv pinned today stays exactly as it was.

    **Refactor.** I pulled the repeated "ask the source if there is one" into `asked_make_file`. Nothing else needed changing.

    **Not touched.** The new modules are not added to the table in `tests/guards/test_areas.py`; that guard passes as it is. The docs are the documenter's.

    The factory left out changes outside the write paths: pyproject.toml.
11. 2026-11-17 human: (a). The records contract becomes 4.6. Leave given: the tester may change 4.5 to 4.6 in `tests/pipeline/domain/test_contract.py`, `tests/shared/domain/test_contract_version_4.py` and `tests/shared/domain/test_contract_version_4_2.py`, and in any other earlier test whose only failure is that version. The `PLR0913` exception for `src/factory/machine/application/stage_environment.py` is on `develop` now, in `pyproject.toml`.
12. factory: started doing as self.
13. coder: Test change for the tester, as the human allowed in entry 11. In `tests/pipeline/domain/test_contract.py:54`, `tests/shared/domain/test_contract_version_4.py:12,23` and `tests/shared/domain/test_contract_version_4_2.py:12,23`, change the pinned records contract version from "4.5" to "4.6". A grep of `tests/` finds no other earlier test that pins "4.5" as the contract version. The other two hits are an opencode version and a time, and they stay as they are.

    I changed no code this round. The build from entry 10 is unchanged on the branch. Once the tests come back with 4.6, I will set `RECORDS_CONTRACT = "4.6"` and regenerate the schemas with `uv run python -m factory.entry.contract`. Then I will run `make check` and `make guides`. Entry 11 says the `PLR0913` exception for `stage_environment.py` is on `develop`. I will check that it is in this branch's `pyproject.toml` at that run.
14. factory: started tests as self.
15. tester: Made the test change the human approved in entry 11, which the coder named in entry 13. The pinned records contract version goes from "4.5" to "4.6" in five places:
    - `tests/pipeline/domain/test_contract.py:54`
    - `tests/shared/domain/test_contract_version_4.py:12,23`
    - `tests/shared/domain/test_contract_version_4_2.py:12,23`

    Nothing else changed in these tests. A grep of `tests/` finds no other earlier test that pins the contract at 4.5. The other two hits are a `TargetTime` of 4.5 seconds and the opencode version "4.5.6", and they stay as they are.

    Run: `uv run pytest -q` on the three files. They are red on purpose: `RECORDS_CONTRACT` is still "4.5" on the branch. The last lines show `test_the_records_contract_is_at_version_4_2_with_the_machine_measures[...]` failing for every contract entry. The coder raises `RECORDS_CONTRACT` to "4.6" and regenerates the schemas with `uv run python -m factory.entry.contract`, and these tests then pass. `make lint` is green: `lint: green (0.2 s)`.

    `lint`: lint: green (0.2 s)
16. factory: started doing as self.
17. coder: I finished the build after the tester's version change (entry 15). Following the human's answer (a) in entry 11, I raised `RECORDS_CONTRACT` in `src/factory/shared/domain/contract.py` from "4.5" to "4.6". I then regenerated the schemas with `uv run python -m factory.entry.contract`. All five schemas under `src/factory/contract/` were rewritten with the new `x-records-contract`. `pipeline-definition.schema.json` also carries the optional `make_file` property.

    Run:
    - The three test files that pin the version (`tests/pipeline/domain/test_contract.py`, `tests/shared/domain/test_contract_version_4.py`, `tests/shared/domain/test_contract_version_4_2.py`) now pass.
    - `make check guides`: `check: green` and `guides: green`. Coverage is 99.18 %.
    - The `PLR0913` exception for `stage_environment.py` is in this branch's `pyproject.toml`.

    What was built (from entry 10, unchanged in this round):
    - `src/factory/pipeline/domain/pipeline_definition.py`: `MakeFilePath`, a rule that refuses a `..` segment through `is_inside_checkout`, and the field `make_file`.
    - `src/factory/machine/application/make_file.py`: the `MakeFileSource` ABC and `asked_make_file`.
    - `src/factory/pipeline/application/make_file_source.py`: `GitMakeFileSource`, which reads `PIPELINE_REF` at every call and returns `None` for a missing or invalid definition.
    - `src/factory/machine/adapters/make_commands.py`: with a path, separate scripts that take the path as the argument `$3`; without one, the old argv.
    - `src/factory/machine/application/stage_environment.py`: `make -f "$7" sync`, with the path as the seventh argument.
    - `src/factory/pipeline/application/boundaries.py`: a new field `make_file`.
    - `src/factory/entry/wiring.py`: builds one source and hands it to both users.
    - `src/factory/pipeline/application/project_check.py`: reads the named makefile; includes are still taken from the root.

    Main choice: the stage environment gets its source through a `Boundaries` field that the wiring fills, so the wiring stays the only place that builds a source. I rejected having `stage_environment_of` build `GitMakeFileSource` itself. A path gets its own script text instead of `${3:+-f "$3"}`, so every argv pinned today stays exactly the same.

    Refactor: entry 10 already went through the diff (it pulled out `asked_make_file`). The version change needed no further refactor.

    Not touched: the new modules are not in the table of `tests/guards/test_areas.py`, and that guard passes as it is. The docs are the documenter's. The journal changed no meaning of the Description: the version rise follows the contract's rule.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
