---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 691
comments_read: [6934588171]
handed_over: null
claim:
  instance: self
  stage: tests
  started_at: '2026-11-17T01:10:33.860407Z'
  lease_duration: 60
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
