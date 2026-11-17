---
stage: review
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 692
comments_read: [6935336014, 6935606286]
handed_over: null
claim:
  instance: self
  stage: review
  started_at: '2026-11-17T02:14:20.459909Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T01:46:15.265672Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T01:46:15.272200Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T01:47:14.031915Z'
  stage: intake
  run: c27d9ff020b64c879440d7e9c0b1cc2b
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T01:47:58.988042Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T01:48:01.841639Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T01:48:45.236246Z'
  stage: intake
  run: 45a10d58120d41cab0c75356d02b40fa
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T01:48:50.421574Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T01:54:56.185553Z'
  stage: tests
  run: 8cbc8405911544faabf66604ef3ef28c
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T01:55:03.118753Z'
  stage: doing
- number: 10
  speaker: coder
  kind: question
  at: '2026-11-17T02:01:26.668189Z'
  stage: doing
  run: d4e44ad636da4d26a1ecc1eff54ecd43
  blocked: question
- number: 11
  speaker: human
  kind: comment
  at: '2026-11-17T02:02:13.840299Z'
  stage: doing
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-17T02:02:16.386380Z'
  stage: doing
- number: 13
  speaker: coder
  kind: result
  at: '2026-11-17T02:02:29.152548Z'
  stage: doing
  run: 67be707cf3e5421b9071e5433a0eedde
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-17T02:02:34.345448Z'
  stage: tests
- number: 15
  speaker: tester
  kind: result
  at: '2026-11-17T02:02:56.126470Z'
  stage: tests
  run: c8629d69268645ec87fae5672a510041
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-17T02:03:01.599382Z'
  stage: doing
- number: 17
  speaker: coder
  kind: result
  at: '2026-11-17T02:05:40.951443Z'
  stage: doing
  run: 778f455a2b3e4a8ba2737d4722e72602
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-17T02:05:46.357391Z'
  stage: review
- number: 19
  speaker: reviewer
  kind: result
  at: '2026-11-17T02:07:34.606484Z'
  stage: review
  run: 020318c37c534e20bc3f4b6256985d3c
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-17T02:07:40.120916Z'
  stage: doing
- number: 21
  speaker: coder
  kind: result
  at: '2026-11-17T02:10:20.129104Z'
  stage: doing
  run: 2cbf36f35e7a49eea01ecb7ac873a1f6
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-17T02:10:25.493578Z'
  stage: tests
- number: 23
  speaker: tester
  kind: result
  at: '2026-11-17T02:11:20.253407Z'
  stage: tests
  run: ea9d45b94ba04b53a1de05771c79c607
- number: 24
  speaker: factory
  kind: started
  at: '2026-11-17T02:11:25.776137Z'
  stage: doing
- number: 25
  speaker: coder
  kind: result
  at: '2026-11-17T02:14:14.851380Z'
  stage: doing
  run: 102f002edcb843858b7335556d7e7f6e
- number: 26
  speaker: factory
  kind: started
  at: '2026-11-17T02:14:20.459909Z'
  stage: review
---

# The conformance check runs a repository

## Description

The static conformance check says that a repository's files fit the factory; it cannot say that the project's image builds and that its targets run green in the factory's containers. A cache that follows the working directory, a tool that ignores `HOME`, a certificate the stack does not read: such faults showed only in a first story's stops. After this story `factory-check-project --run <folder>` does the static part first and then, on a ready repository, the live part on a machine that has an instance's environment: it builds the project's image from the stage file, runs the sync in a container as a stage does, and runs `make check` in a second, fresh container as a stage's check does. It prints one more line for each of the three live points and ends with the same last line as before. It works on a temporary folder with a clone of the commit at `HEAD`, never on the instance's dataset, its checkout or its project image, so it can run beside a working instance and for another repository than the instance's. Without `--run` nothing changes.

## Interface

- `src/factory/entry/check_project.py` (`entry`): usage `factory-check-project [--agent-home <dir>] [--run] <folder>`.
  - With `--run` the command reads the instance's settings from the environment, as `factory-run` does; a fault of the settings is one line on standard error, `cannot run: <fault>`, and status 2, before anything is printed or started. The agent home then comes from the settings unless `--agent-home` is given; it serves only the static part's point `agents` (the installed agents): the live part does not use it and mounts no agent files.
  - The static part's lines are printed first. When the static part has a fault, the live part does not run, and the output and the status are those of the command without `--run`.
- A use case in `src/factory/machine/application/project_run.py` (`application`) does the live part through the interfaces `Images`, `ContainerRuns` and `Git`; the wiring of the concrete classes is in `src/factory/entry/`. It returns `ProjectPoint`s (`factory.pipeline.domain.project_check`), named `image`, `sync` and `check`, in this order; `LIVE_POINT_NAMES` in the domain module holds the three names.
  - The work folder: a new temporary directory with `checkout/` (a clone of `<folder>` at its `HEAD` commit) and `home/`, mounted at `/work` as a stage's dataset is. It is removed at the end, after a fault too.
  - `image`: without `factory/stage.Containerfile` the containers run in the instance's stage image and the point has no fault. Otherwise the stage file is built on the stage image under the tag `<stage image>-check`, never under the tag of the instance's own project image, with the time limit a stage's build has; a build that does not pass is the fault `the image does not build: <the last line of the build's output>`.
  - `sync`: one container that does what a stage's sync does after its checkout: started in `/work`, it changes into `/work/checkout` and runs `make sync`, or `make -f <path> sync` when the definition names a makefile, with the environment, the `PATH`, the site's variables (`FACTORY_CONTAINER_ENV`) and the CA bundle of a stage's sync, and the time limit of the definition's `sync` command. The make part of the stage's sync script (`make sync`, and `make -f <path> sync`) becomes public constants in `src/factory/machine/application/stage_environment.py`, which the stage's sync script (after its preparation) and the use case both use; the live sync runs only that part.
  - `check`: a second container that does what a stage's check does: started in `/work/checkout`, it runs the sync and then `check`, as `ContainerMakeCommands.run` does, with the time limit of the definition's `check` command. The two check scripts and `CHECK_ENVIRONMENT` move from `src/factory/machine/adapters/make_commands.py` to a public place in `factory.machine.application` (`project_commands.py`), and `make_commands.py` imports them from there.
  - The faults of `sync` and of `check`, the first that applies: `could not start: <reason>` for a `ContainerError`; `timed out after <n> min`; `exit status <n>: <the last line of the output>`; and, for a run that ended with status 0, `no line "sync: green (<seconds> s)"` when the sync's output holds no such line, or `the last line is not "check: green": <the last line>` for the check.
  - A point after a live point with a fault is not run and not printed.
  - The scripts and the environment are those the stage uses, reused from their modules and not copied.
- The report: the static lines, the lines of the live points that ran, then the last line of `report_lines` over all printed points. Status 0 when no point has a fault, 1 otherwise.
- Tests: `tests/machine/application/test_project_run.py` (fakes of `ContainerRuns` and `Images` from `tests/support/`, a real repository in `tmp_path`) and `tests/entry/test_check_project_run.py`. `feature.md` gives this leave (decision 4): "S0001 to S0004 may add their new modules to the table of `tests/guards/test_areas.py`, and to any other guard table that lists every module or every entry command."

## Acceptance criteria

1. On a ready repository without a stage file, with fakes whose sync prints `sync: green (1.0 s)` and whose check ends with `check: green`, the live part returns the three points without a fault, no image is built, and both containers ran in the stage image.
2. With a stage file, the image is built on the stage image under `<stage image>-check`, and both containers run in that image; the build gets `IMAGE_BUILD_TIME_LIMIT` (`src/factory/machine/application/images.py`); a build that does not pass gives `image` the fault `the image does not build: <last line>`, and `sync` and `check` are not run.
3. The sync container starts in `/work` and runs `make sync` in `/work/checkout`; the check container starts in `/work/checkout` and runs the sync, then `check`; with `make_file: factory/Makefile` in the definition both call make with `-f factory/Makefile`. Each gets the time limit of its command in the definition.
4. The faults of a run, as rows of one parametrized test for `sync` and for `check`: a container that could not start; a run that reached its time limit; exit status 2 with a last line; status 0 without the green line (for the check: with another last line). A fault of `sync` leaves `check` unrun.
5. The work folder holds the commit at `HEAD` and not an uncommitted change of the work tree, and it is gone after a green run, after a fault and after an exception of a container run.
6. The containers get the variables that the settings name in `FACTORY_CONTAINER_ENV` and the CA bundle's mount and names, as a stage's sync does.
7. `main` with `--run` and incomplete settings returns 2, prints `cannot run: ...` on standard error and nothing on standard output; with `--run` on a repository with a static fault it prints exactly what it prints without `--run` and returns 1, and starts no container and no build.
8. `main` with `--run`, complete settings and faked containers on a ready repository prints the six static lines, `image: ok`, `sync: ok`, `check: ok` and `project: ready`, and returns 0; with a red check it prints `check: FAIL: exit status 2: ...`, `project: not ready (1 fault)` and returns 1; with a build that does not pass it prints the six static lines, `image: FAIL: the image does not build: ...` and `project: not ready (1 fault)`, with no `sync` or `check` line, and returns 1.
9. With `--run`, as rows of one parametrized test: without `--agent-home` the static point `agents` reads the agent home of the settings; with `--agent-home <dir>` it reads the given folder. In both rows no container gets a mount of the agent home.
10. `make check` stays green.
11. docs: the operator guide, where it explains `factory-check-project`, says what `--run` adds and needs (an instance's environment, podman and the stage image; no dataset), that it works on a temporary clone of the commit at `HEAD` and builds its image under `<stage image>-check`, so it may run beside a working instance and for another repository, how to run it on the VM as the factory's user with the instance's environment (an example marked for the VM), and what each of the faults means; the project guide (`docs/project-guide/machine.md`) names the use case and the rule that it reuses the stage's scripts.

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
git init -q "$d/p"; mkdir -p "$d/p/factory" "$d/p/src" "$d/p/tests" "$d/p/docs"
cp operator/template/factory/pipeline.yml factory/story-form.md factory/feature-form.md "$d/p/factory/"
cp operator/template/Makefile "$d/p/Makefile"
touch "$d/p/src/a.py" "$d/p/tests/t.py" "$d/p/docs/d.md" "$d/p/README.md"
git -C "$d/p" add -A; git -C "$d/p" -c user.name=t -c user.email=t@example.com commit -q -m one
env -u FACTORY_WORKSPACE -u FACTORY_CHECKOUT uv run python -m factory.entry.check_project --agent-home agents --run "$d/p" > "$d/out" 2> "$d/err"; echo "status $?"
wc -c < "$d/out"; cut -c1-11 "$d/err"
```
Expect: `status 2`, then `0`, then `cannot run:`.

```bash
uv run pytest tests/machine/application/test_project_run.py tests/entry/test_check_project_run.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: Questions from intake. The format check passed. The smoke tests can be run and their `Expect:` lines can be checked: pytest's `addopts` already sets `-q`, and the settings fault comes before the static part. The story fits the feature's scope (decisions 12 and 13). These points have to be settled before tests are written:

   1. **Which sync script does the live `sync` reuse?** The Interface says the sync container does "what a stage's sync does after its checkout" and runs only `make sync` in `/work/checkout`. It also says "the scripts … reused from their modules and not copied". But the stage's script, `_SYNC_SCRIPT`/`_NAMED_SYNC` in `src/factory/machine/application/stage_environment.py`, starts with `_SYNC_PREPARATION`. That part fetches from `/upstream`, checks out a branch and a commit, and copies the agent files into `home/.claude`. There is no stage script that only runs make. The Interface also takes an agent home from the settings or from `--agent-home`, and nothing in the live part says what that home is for. Options:
      - (a) Run the whole stage script. The clone's `.git` is mounted at `/upstream`, the agent home at `/etc/factory/agents`, and the script gets a branch and the commit at `HEAD`. `checkout/` is then filled by the script, not cloned first.
      - (b) Split the make part of the script into public constants in `stage_environment.py`, which the stage's script and the use case both use. The live sync runs only that part, and the agent home is not used by the live part.
      I would choose (b), because it is what the Interface's wording describes. Please also say what the agent home is for under `--run`.
   2. **The check script cannot be imported by the use case.** It is private in `src/factory/machine/adapters/make_commands.py` (`_CHECK_SCRIPT`, `_NAMED_CHECK_SCRIPT`). `project_run.py` sits in `application`, and import-linter forbids it to import from `adapters`. Options:
      - (a) Move the two scripts, and the `CHECK_ENVIRONMENT` they need, to a public place in `factory.machine.application` (for example `project_commands.py`); `make_commands.py` then imports them from there.
      - (b) The use case asks an adapter for the check run through a new interface.
      I would choose (a). Please confirm that the story may move them.
   3. **No criterion for where the agent home comes from.** The Interface says that with `--run` the agent home comes from the settings unless `--agent-home` is given, but no criterion tests either side. If the agent home stays in the live part (question 1), I propose a criterion with two rows: without `--agent-home` the settings' agent home is used, and with it the given folder is used. If it does not stay, the Interface line should go.
   4. **The image build's time limit is untested.** The Interface says the build has "the time limit a stage's build has" (`IMAGE_BUILD_TIME_LIMIT` in `src/factory/machine/application/images.py`), but no criterion checks it. I propose adding to criterion 2: "the build gets `IMAGE_BUILD_TIME_LIMIT`".
   5. **"Not printed" is only tested where the check fails.** The rule is that a point after a failed live point is not printed. Criterion 8 only covers a failing check, which is the last point, so nothing is left out. I propose a row in criterion 8: when the build fails, `main` prints the six static lines, `image: FAIL: the image does not build: …` and `project: not ready (1 fault)`, with no `sync` or `check` line, and returns 1.
4. 2026-11-17 human: 1: (b). Under `--run` the agent home serves only the static part's point `agents` (the installed agents); the live part does not use it and mounts no agent files. 2: (a), the story may move the two check scripts and `CHECK_ENVIRONMENT` to a public place in `factory.machine.application`. 3: add the criterion with the two rows, for the static part's agents. 4: add it. 5: add the row.
5. factory: started intake as self.
6. intake: accepted
   I added the human's answers from journal entry 4 to the story. Interface: the agent home under `--run` is used only by the static point `agents`, and the live part mounts no agent files (answers 1 and 3). The make part of the stage's sync script becomes public constants in `stage_environment.py`, and both the stage's script and the use case use them (answer 1, option b). The two check scripts and `CHECK_ENVIRONMENT` move from `make_commands.py` to `factory.machine.application.project_commands`, and `make_commands.py` imports them from there (answer 2, option a). Criteria: criterion 2 now says the build gets `IMAGE_BUILD_TIME_LIMIT` (answer 4). Criterion 8 has a new row for a failed build (answer 5). New criterion 9 has two rows for where the agent home comes from, and says no container mounts it (answer 3). It sits before the two closing criteria, which are now 10 and 11.
   - Interface: it names concrete modules (`entry/check_project.py`, `machine/application/project_run.py`, `pipeline/domain/project_check.py`), the usage line, the point names and order, the work folder layout, the image tag, each fault's exact text, and where the reused scripts live. Keep two names so earlier tests pass unchanged: `_SYNC_SCRIPT` in `stage_environment.py` (`tests/pipeline/application/test_container_sync_origin.py` reads it) and `CHECK_ENVIRONMENT` importable from `make_commands.py` (`tests/machine/application/test_container_environment_extra.py` imports it). Both survive the split and the move as the answers describe them.
   - Criteria: each can be tested by one test function. Every rule has its failing side: settings fault (7), static fault (7), build failure (2, 8), every fault of sync and check (4), a later point not run or printed (2, 4, 8), work folder removed after an exception (5), agent home from the settings or the option (9).
   - Smoke test: both blocks run. The first checks status 2, empty output and the `cannot run:` prefix, and the settings fault comes before the static part. The second passes no `-q` because `addopts` already sets it, and its summary line can be checked.
   - Docs criterion: it names what the reader must know (what `--run` adds and needs, the temporary clone, the `-check` tag, a VM example, the meaning of each fault, and the use case and its reuse rule in `machine.md`). It dictates no sentences.
   - Architecture: the use case sits in `machine.application` and works only through the `Images`, `ContainerRuns` and `Git` interfaces. Its domain point type is in `pipeline.domain`, and the wiring is in `entry`. Moving the check scripts to `application` keeps the import-linter layers intact, since `application` cannot import from `adapters`.
   - Scope: this is the feature's S0003 (the live check), within decisions 12 and 13. Decision 4 gives leave to add the new modules to the guard tables. Nothing here is in Out of scope.
7. factory: started tests as self.
8. tester: Wrote the tests for criteria 1–9. They are red on purpose: `make test` reports ImportError while collecting `tests/machine/application/test_project_run.py` and `tests/entry/test_check_project_run.py`, because `factory.machine.application.project_run` (`ProjectRun`) and `LIVE_POINT_NAMES` in `factory.pipeline.domain.project_check` do not exist yet. Because of that collection error, the two tests of `tests/guards/test_documents_marker.py` error too; they recover once the modules exist. The guards `test_areas`, `test_shared_bodies`, `test_shared_imports` and `test_test_names` pass on the new files. `make lint` is green.

   Mapping:
   - criterion 1: tests/machine/application/test_project_run.py::test_live_points_of_a_ready_repository_without_a_stage_file
   - criterion 2: tests/machine/application/test_project_run.py::test_a_stage_file_is_built_under_the_check_tag (rows built / red)
   - criterion 3: tests/machine/application/test_project_run.py::test_the_sync_and_the_check_run_as_a_stage_runs_them (rows default / named makefile)
   - criterion 4: tests/machine/application/test_project_run.py::test_faults_of_the_sync_and_the_check (8 rows: not started, timed out, exit 2, no green line, for sync and for check; a sync fault leaves check unrun)
   - criterion 5: tests/machine/application/test_project_run.py::test_the_work_folder_holds_the_commit_and_is_removed (rows green / fault / exception)
   - criterion 6: tests/machine/application/test_project_run.py::test_the_containers_get_the_site_variables_and_the_bundle
   - criterion 7: tests/entry/test_check_project_run.py::test_incomplete_settings_end_before_anything_runs and ::test_a_static_fault_prints_what_the_command_prints_without_run
   - criterion 8: tests/entry/test_check_project_run.py::test_the_report_holds_the_live_points_that_ran (rows green / red-check / red-build)
   - criterion 9: tests/entry/test_check_project_run.py::test_the_agents_point_reads_the_agent_home_of_the_run (rows from-settings / from-option)

   Files created: `tests/machine/application/test_project_run.py`, `tests/entry/test_check_project_run.py`, `tests/support/project_run_support.py`. The support module holds `ScriptedContainerRuns`, a `ContainerRuns` fake that plays scripted results or errors and records each call with the files of `<workspace>/checkout` at that moment, plus `result()`, `definition()` (a `sync` limit of 7 min and a `check` limit of 9 min, optional `make_file`) and the green outputs. `FakeImages` is the existing one from `factory.machine.adapters.fake_images`. I changed no earlier test file.

   The Interface leaves these names and shapes open, so the tests fix them and the coder must follow them:
   - `ProjectRun(images, *, containers: Callable[[Path], ContainerRuns], git: Callable[[Path], Git], stage_image: str, extra_environment: Mapping[str, str] = {}, ca_bundle: Path | None = None)` and `.run(folder: Path, definition: PipelineDefinition) -> list[ProjectPoint]`.
     - `containers` is called with the temporary work folder that is mounted at `/work` (once, before the runs).
     - `git` builds a `Git` on a folder; the tests pass `GitCli`.
     - The use case reads the stage file from the clone.
     - The containers' `PATH` is `images.path(<image used>)`, and `HOME` is `/work/home`.
   - `factory.entry.check_project.build_project_run(settings: InstanceSettings) -> ProjectRun` is the seam that `main` calls under `--run`. The entry tests replace it with monkeypatch, so the real one computes `extra_environment` and the CA bundle itself.
   - Fault texts:
     - `could not start: ` is checked as a prefix, followed by text that contains the `ContainerError`'s reason.
     - `no line "sync: green (<seconds> s)"` is checked literally, `<seconds>` included.
   - Criterion 3 checks the command words loosely: the sync's words contain `/work/checkout`, `make` and `sync`; the check's argv contains `make` and `check`, as `ContainerMakeCommands` builds it; with a makefile both contain `-f` and `factory/Makefile`.
   - The entry tests' complete settings are `BASE` and `CONTAINER` (`tests/support/settings_support.py`) plus `FACTORY_WORKSPACE`, `FACTORY_CHECKOUT`, `FACTORY_STATE` and `FACTORY_IMAGE_ID_FILE` in `tmp_path`. The settings are read as `read_environment_settings` reads them. The incomplete case leaves out `FACTORY_REPOSITORY_URL`.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: Questions from doing. The code is written and the tester's two files pass: `uv run pytest -q tests/machine/application/test_project_run.py tests/entry/test_check_project_run.py` gives 24 passed. `make check` is red only on four earlier tests that contradict the Interface. I may not change them, and they are not mine to change (R9). lint, types, layers, sast, secrets and licenses are green.

    Failures, from `make check` (`--tb=short`):
    - `tests/entry/test_check_project.py::test_main_prints_the_report_or_one_error_and_returns_its_status[no-folder]`, `[two-folders]` and `[no-agent-home]`, at `tests/entry/test_check_project.py:162`:
      `E   AssertionError: assert 'factory-check-project [--agent-home <dir>] <folder>' in 'usage: factory-check-project [--agent-home <dir>] [--run] <folder>'`
    - `tests/guards/test_make_search.py::test_only_the_make_class_names_make`, at `tests/guards/test_make_search.py:33`:
      `E   AssertionError: assert {'factory.mac....project_run'} == {'factory.mac...ake_commands'}` / `Extra items in the left set: 'factory.machine.application.project_run'`

    1. **Usage line.** The Interface's usage is `factory-check-project [--agent-home <dir>] [--run] <folder>`. The earlier test requires the one usage line to contain `factory-check-project [--agent-home <dir>] <folder>`. Options:
       - (a) The tester changes `USAGE` in `tests/entry/test_check_project.py` to the new usage.
       - (b) I print a line that holds both forms, such as `usage: factory-check-project [--agent-home <dir>] <folder>; factory-check-project [--agent-home <dir>] --run <folder>`, and no test changes.

       I would choose (a). (b) only gets around the test.
    2. **The make guard.** The guard allows only `factory.machine.adapters.make_commands` to have the string literal `"make"`. The live check must run the moved check script as `ContainerMakeCommands.run` does: `/bin/sh -c CHECK_SCRIPT factory-check make check [makefile]`. So `project_run.py` passes `"make"` as the script's argument. Options:
       - (a) The tester adds `factory.machine.application.project_run` to the guard's expected set. Feature decision 4 may already allow this, if this set counts as "a guard table that lists every module".
       - (b) A public constant `MAKE = "make"` in `factory.machine.application.project_commands`, imported by both `make_commands.py` and `project_run.py`. The guard's set would then need `project_commands` in place of `make_commands`, so it is still a test change.

       I would choose (a).

    If you approve both (a)s, my next run ends with `tests` and names the two changes. Nothing else changes.

    What is built, all in the working tree:
    - `src/factory/machine/application/project_run.py`: `ProjectRun`, plus `check_image_tag` and `checkout_has_stage_file`.
      - It makes the work folder (`checkout/` and `home/`) with `tempfile.mkdtemp` and removes it in a `finally`.
      - The clone is `GitCli.clone`, then `reset_to` the source's `HEAD` commit.
      - It reads the stage file from the clone with `show_file`, then builds on the stage image under `<stage image>-check` with `IMAGE_BUILD_TIME_LIMIT`.
      - Sync: the script is `set -eu; cd "$1"; shift` plus the stage's make part, run in `/work`.
      - Check: `CHECK_SCRIPT` or `NAMED_CHECK_SCRIPT`, run in `/work/checkout`.
      - Faults are given in the Interface's order. The "last line" here is the last non-blank line with make's own messages kept, because `checks.last_line` skips `make:` lines, which are what explain a red run.
    - `src/factory/machine/application/project_commands.py`: now holds the public `CHECK_ENVIRONMENT`, `CHECK_SCRIPT`, `NAMED_CHECK_SCRIPT` and `CHECK_SCRIPT_NAME`. `src/factory/machine/adapters/make_commands.py` imports them and re-exports `CHECK_ENVIRONMENT` through `__all__` for the earlier test.
      - `CHECK_ENVIRONMENT` is now defined in `project_commands.py`, and `SYNC_ENVIRONMENT = dict(CHECK_ENVIRONMENT)` in `stage_environment.py`. Importing `stage_environment` from `project_commands` would create an import cycle through `boundaries`.
    - `src/factory/machine/application/stage_environment.py`: public `SYNC_MAKE` (`make sync`) and `NAMED_SYNC_MAKE` (`make -f "$1" sync`). The stage's named script now runs `shift 6` before the make part. `_SYNC_SCRIPT` keeps its name.
    - `src/factory/pipeline/domain/pipeline_definition.py`: `command_time_limit(definition, command)`. `pipeline/application/stage.py` now uses it in place of its own copy.
    - `src/factory/pipeline/domain/project_check.py`: `LIVE_POINT_NAMES`. `pipeline/application/project_check.py`: `_ANY_BASE` is now the public `ANY_BASE`, so the use case reuses it instead of copying it.
    - `src/factory/entry/check_project.py`: `--run`, and `build_project_run(settings)`, which wires `PodmanImages` and `PodmanRuns`.
      - `PodmanRuns` gets the `-check` image exactly when the clone holds a stage file. I rejected changing the `containers` callable's signature, because the tests pin it.
      - Settings faults, a missing stage image included, print `cannot run: …` and return 2 before anything else runs.
      - The agent home comes from `--agent-home`, then from the settings, then from the environment variable.
    - `pyproject.toml`: a per-file `PLR0913` ignore for `project_run.py`, following the existing lines for pinned constructors. The tests pin the six-argument constructor.

    Not touched: docs (that is the documenter's job). The refactor step is not done yet; it comes after `make check` is green.

    The factory left out changes outside the write paths: pyproject.toml.
11. 2026-11-17 human: Both (a). Leaves given: the tester may change `USAGE` in `tests/entry/test_check_project.py` to the usage with `[--run]`, and may add `factory.machine.application.project_run` to the expected set of `tests/guards/test_make_search.py`. The `PLR0913` exception for `src/factory/machine/application/project_run.py` is on `develop` now, in `pyproject.toml`.
12. factory: started doing as self.
13. coder: The human's answer in entry 11 asks for two test changes, so I am handing over to the tester. I changed no code in this run, and the code from my previous run is on the branch as committed. Changes for the tester:
    1. In `tests/entry/test_check_project.py`, set `USAGE` to `factory-check-project [--agent-home <dir>] [--run] <folder>`. This fixes the three failing rows `[no-folder]`, `[two-folders]` and `[no-agent-home]` of `test_main_prints_the_report_or_one_error_and_returns_its_status`.
    2. In `tests/guards/test_make_search.py`, add `factory.machine.application.project_run` to the expected set of `test_only_the_make_class_names_make`.

    Nothing else is open on my side. When the tests come back, I will run them and `make check`. Then I will do the refactor step (reading my own diff) and end with `review`. The human has put the `PLR0913` exception for `project_run.py` in `pyproject.toml` on `develop` (entry 11).
14. factory: started tests as self.
15. tester: I made the two test changes the human approved in entry 11, which the coder named in entry 13. Nothing else changed.
    1. `tests/entry/test_check_project.py`: `USAGE` is now `factory-check-project [--agent-home <dir>] [--run] <folder>`, the usage the Interface gives. This fixes the rows `[no-folder]`, `[two-folders]` and `[no-agent-home]` of `test_main_prints_the_report_or_one_error_and_returns_its_status`.
    2. `tests/guards/test_make_search.py`: `test_only_the_make_class_names_make` now also expects `factory.machine.application.project_run`. The live check passes `"make"` to the moved check script, as `ContainerMakeCommands.run` does.

    Both are earlier tests that another story wrote; the human gave leave for both changes in entry 11.

    I ran the changed files once, as `CLAUDE.md` says for an approved change: `uv run pytest -q tests/entry/test_check_project.py tests/guards/test_make_search.py` passed with no failures. `make lint`: lint: green (0.1 s). I did not run the whole `make test`.

    `lint`: lint: green (0.1 s)
16. factory: started doing as self.
17. coder: The tester made the two test changes from entry 11 (entry 15). I changed no code in this run. Both `make check` and `make guides` are green now.

    I first ran `uv run pytest -q tests/entry/test_check_project.py tests/guards/test_make_search.py tests/machine/application/test_project_run.py tests/entry/test_check_project_run.py`, and all of them passed. Then `make check guides` ended with `check: green` (total coverage 99.12 %) and `guides: green`.

    Built in the earlier run (entry 10), as committed on the branch:
    - `src/factory/machine/application/project_run.py`: the use case `ProjectRun`.
      - It makes a temporary work folder with `checkout/` and `home/`, and removes it in a `finally`. The checkout is a `GitCli` clone, reset to the source's `HEAD` commit.
      - It reads the stage file from the clone and builds it on the stage image under `<stage image>-check`, with `IMAGE_BUILD_TIME_LIMIT`.
      - The sync container runs in `/work`. It changes into `/work/checkout` and runs the stage's make part.
      - The check container runs in `/work/checkout`, with the moved check scripts.
      - Faults are reported in the Interface's order. The run stops after the first point with a fault.
      - It also has `check_image_tag` and `checkout_has_stage_file`, which the entry's wiring uses.
    - `src/factory/machine/application/project_commands.py`: the public `CHECK_ENVIRONMENT`, `CHECK_SCRIPT`, `NAMED_CHECK_SCRIPT` and `CHECK_SCRIPT_NAME`. `src/factory/machine/adapters/make_commands.py` imports them, and re-exports `CHECK_ENVIRONMENT` through `__all__` so the earlier test can still import it from there.
    - `src/factory/machine/application/stage_environment.py`: the public `SYNC_MAKE` and `NAMED_SYNC_MAKE`. The stage's named script now runs `shift 6` before the make part. `_SYNC_SCRIPT` keeps its name. `SYNC_ENVIRONMENT` is now a copy of `CHECK_ENVIRONMENT`, which avoids an import cycle through `boundaries`.
    - `src/factory/pipeline/domain/pipeline_definition.py`: `command_time_limit`, which `pipeline/application/stage.py` now uses in place of its own copy.
    - `src/factory/pipeline/domain/project_check.py`: `LIVE_POINT_NAMES`.
    - `src/factory/pipeline/application/project_check.py`: `ANY_BASE` is now public, so the use case reuses it.
    - `src/factory/entry/check_project.py`: the `--run` option and `build_project_run(settings)`, which wires `PodmanImages` and `PodmanRuns`.
      - A settings fault prints `cannot run: …` and returns 2, before anything runs.
      - The agent home comes from `--agent-home`, then from the settings, then from the environment variable.

    Main choice and the alternative I rejected:
    - The live sync runs only the shared make part, after its own `cd`, and does not run the stage's whole script with its preparation. The human chose this in entry 4.
    - `PodmanRuns` gets the `-check` image exactly when the clone holds a stage file. I rejected changing the `containers` callable's signature, because the tests pin it.

    Refactor step: I read my own diff (`git diff develop` outside `factory/` and `tests/`, and the new files) and found nothing to change.
    - `_last_line` in `project_run.py` is not a copy of `checks.last_line`. That one skips `make:` lines, and those lines are what explain a red run here; a comment in the code says so.

    Description: entry 11 only allowed test changes and the `PLR0913` ignore on `develop`, so the task's meaning is unchanged and the Description stays as it is.

    Noticed but not touched: the docs (`docs/operator-guide/`, `docs/project-guide/machine.md`) are left to the documenter for criterion 11.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
18. factory: started review as self.
19. reviewer: Findings:

    1. `src/factory/machine/application/project_run.py` `_run_in` (`path = self._images.path(image)`): `Images.path` raises `ContainerError` when the image cannot be inspected, for example when the stage image is missing on a repository without a stage file. The call sits outside `_point`, so the error escapes `main` as a traceback, not as the `sync` fault `could not start: <reason>` that the Interface gives for a `ContainerError`. The stage's wiring catches this same error (`src/factory/entry/wiring.py:388` `_image_path`, which falls back to `SYSTEM_PATH`). Fix: read the path inside the sync point's guarded run, so the error becomes `could not start: ...`, or fall back as `_image_path` does. The tester then adds a row to criterion 4's test where `path` raises.
    2. `src/factory/entry/check_project.py:93` (`containers` in `build_project_run`) together with `project_run.py` `_image`: the image the containers run in is decided twice. The use case decides from `show_file(HEAD, STAGE_FILE)` and builds `check_image_tag`. The entry decides again from the files on disk (`checkout_has_stage_file`). Both entry tests monkeypatch `build_project_run`, so no test reaches the code that picks the image. Criterion 2 says "both containers run in that image", but its test sees the image only through `PATH`. The real `extra_environment` and `ca_bundle` wiring for criterion 6 is not reached either. Fix: the use case passes the image it chose to the `containers` callable (for example `Callable[[Path, str], ContainerRuns]`), and `checkout_has_stage_file` is dropped. The tester then changes the pinned signature in `tests/support/project_run_support.py` and checks the image of each run in criteria 1 and 2.
    3. `src/factory/machine/application/project_run.py:226` `_last_line` is a second copy of `printed_lines` in `factory.shared.domain.printed_lines`, which `preflight._last_line` and `printed_output.failure_detail` already use to get the last non-blank line. Fix: build `_last_line` on `printed_lines(output)`. It keeps the `make:` lines, which is the only reason it differs from `checks.last_line`.

    Checked and fine:
    - Criteria 1 to 9 each have a test that checks what the criterion says.
    - `make check` was green after the coder (entry 17).
    - Layers hold: `project_run` is in `machine.application` and imports no adapter, and `ANY_BASE` is reused from `pipeline.application`.
    - The scripts are argument-passing constants and are reused, not copied. `_NAMED_SYNC` with `shift 6` keeps the seventh argument.
    - No markers that silence a check, no secrets. A `ContainerError` from `PodmanRuns.run` names only the executable.
    - The journal explains the main choice and what was rejected. The Description and the docs criterion still match.

    Earlier tests:
    - `tests/entry/test_check_project.py`: the human's leave, journal entry 11 (`USAGE` only).
    - `tests/guards/test_make_search.py`: the human's leave, journal entry 11 (adds `factory.machine.application.project_run` to the expected set only).
20. factory: started doing as self.
21. coder: Round 1: I worked through the reviewer's three findings from entry 19. I fixed findings 1 and 3 in the code. Finding 2 changes a signature that the tests pin, so it goes to the tester first. `make check` is green after this run (`check: green`). The tester's two files pass: `uv run pytest -q tests/machine/application/test_project_run.py tests/entry/test_check_project_run.py` gives 24 passed.

    Done in `src/factory/machine/application/project_run.py`:
    - Finding 1: `Images.path(image)` is now read in a guarded step before the sync. A `ContainerError` from it becomes the `sync` fault `could not start: <reason>`, and `check` does not run. It does not escape as a traceback. The fault text is built by one helper, `_not_started`, which `_point` also uses. I rejected falling back to `SYSTEM_PATH` as `wiring._image_path` does: the Interface names `could not start` for a `ContainerError`, and a missing image means the containers cannot start anyway.
    - Finding 3: `_last_line` now takes the last line of `printed_lines(output)` (`factory.shared.domain.printed_lines`) and keeps make's own lines.

    For the tester, these are the test changes the findings call for:
    1. Finding 2: in `tests/support/project_run_support.py`, change `ScriptedContainerRuns.at` to the pinned signature `containers: Callable[[Path, str], ContainerRuns]`, called with the work folder and the image the use case chose. Record the image of each run, and have criterion 1's test (`test_live_points_of_a_ready_repository_without_a_stage_file`) and criterion 2's test (`test_a_stage_file_is_built_under_the_check_tag`) check that each container ran in the stage image or in `<stage image>-check`.
    2. Finding 1: add a row to criterion 4's test `test_faults_of_the_sync_and_the_check`, where `Images.path` raises `ContainerError`. Expect `sync` with `could not start: <reason>` and no `check`. `FakeImages` (`src/factory/machine/adapters/fake_images.py`) cannot raise, so this needs a raising stand-in in `tests/support/`.

    When the tests come back, I will change the `containers` callable in `ProjectRun` to receive the chosen image. I will also update `build_project_run` in `src/factory/entry/check_project.py` to use that image, and drop `checkout_has_stage_file`.

    Noticed, not touched: as finding 2 also says, the entry tests monkeypatch `build_project_run`. So the real wiring of `extra_environment` and `ca_bundle` is still reached by no test.
22. factory: started tests as self.
23. tester: Round 1: I made the test changes for reviewer findings 1 and 2 (entry 19), as the coder listed them in entry 21. These test files are my own story's, so no other leave was needed. Finding 3 needs no test.

    - Finding 2 (the image is picked twice): `tests/support/project_run_support.py`, `ScriptedContainerRuns.at` now has the pinned signature `at(workspace: Path, image: str) -> ContainerRuns`. This means `ProjectRun`'s `containers` is now `Callable[[Path, str], ContainerRuns]`, called with the work folder and the image the use case chose. Each `SeenRun` now records that `image`. The tests that check it:
      - criterion 1, `tests/machine/application/test_project_run.py::test_live_points_of_a_ready_repository_without_a_stage_file`: both runs ran in the stage image.
      - criterion 2, `tests/machine/application/test_project_run.py::test_a_stage_file_is_built_under_the_check_tag` (row `built`): both runs ran in `<stage image>-check`.
      The entry tests pass `runs.at` unchanged, so they now follow the new signature too.
    - Finding 1 (`Images.path` raises): there is a new stand-in, `UninspectableImages(FakeImages)` in `tests/support/project_run_support.py`. Its `path` raises `ContainerError("podman", "no such image: <image>")`. Criterion 4's test `tests/machine/application/test_project_run.py::test_faults_of_the_sync_and_the_check` has a new column, `images` (a factory of the `Images` to use; `FakeImages` in the earlier rows), and a new row, `sync-image-not-inspected`. In that row `sync` has the fault `could not start: ...`, the fault contains `no such image`, `check` is not run and no container is run.

    Files changed: `tests/support/project_run_support.py` and `tests/machine/application/test_project_run.py`. I changed no earlier test of another story and no other file.

    Run: `uv run pytest -q tests/machine/application/test_project_run.py tests/entry/test_check_project_run.py` is red, and it fails for the right reason. Every failing test fails at `src/factory/machine/application/project_run.py:109` with `TypeError: ScriptedContainerRuns.at() missing 1 required positional argument: 'image'`, because the use case still calls `containers(workspace)`. The coder's change from entry 21 fixes this: pass the chosen image, update `build_project_run`, drop `checkout_has_stage_file`. No module failed to import.

    `lint`: lint: green (0.2 s)

    `lint`: lint: green (0.1 s)
24. factory: started doing as self.
25. coder: Round 1: I finished reviewer finding 2 (entry 19) on top of the tester's changes in entry 23. Findings 1 and 3 were already fixed in entry 21. First run: `uv run pytest -q tests/machine/application/test_project_run.py tests/entry/test_check_project_run.py` failed in the expected way. The use case still called `containers(workspace)` without the image. After the change those two files give 25 passed, and `make check guides` ends with `check: green` and `guides: green`.

    Built:
    - `src/factory/machine/application/project_run.py`:
      - `ProjectRun`'s `containers` is now `Callable[[Path, str], ContainerRuns]`. It is called with the work folder and the image the use case chose: the stage image, or `<stage image>-check` when the clone holds a stage file.
      - `checkout_has_stage_file` is removed.
      - The image is now decided in one place, `_image`, which reads it from `show_file(HEAD, STAGE_FILE)`.
    - `src/factory/entry/check_project.py`: in `build_project_run`, `containers(workspace, image)` passes the image it is given to `PodmanRuns` and no longer looks at the files on disk. The imports of `check_image_tag` and `checkout_has_stage_file` are gone.

    Main choice: the use case passes the chosen image to the callable, as the reviewer and the tester's pinned signature ask. I rejected keeping a second decision in the entry from the files of the checkout, because the two could disagree and no test reached that code.

    Refactor: I read the diff and found nothing more to change. `check_image_tag` stays a public function of the use case module, and only that module uses it now.

    Noticed, not touched: the entry tests still monkeypatch `build_project_run`. So the real wiring of `extra_environment` and `ca_bundle` in `src/factory/entry/check_project.py` is reached by no test. The use case's handling of both is tested, under criterion 6.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
26. factory: started review as self.
