---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 692
comments_read: [6935336014]
handed_over: null
claim:
  instance: self
  stage: intake
  started_at: '2026-11-17T01:48:01.841639Z'
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
---

# The conformance check runs a repository

## Description

The static conformance check says that a repository's files fit the factory; it cannot say that the project's image builds and that its targets run green in the factory's containers. A cache that follows the working directory, a tool that ignores `HOME`, a certificate the stack does not read: such faults showed only in a first story's stops. After this story `factory-check-project --run <folder>` does the static part first and then, on a ready repository, the live part on a machine that has an instance's environment: it builds the project's image from the stage file, runs the sync in a container as a stage does, and runs `make check` in a second, fresh container as a stage's check does. It prints one more line for each of the three live points and ends with the same last line as before. It works on a temporary folder with a clone of the commit at `HEAD`, never on the instance's dataset, its checkout or its project image, so it can run beside a working instance and for another repository than the instance's. Without `--run` nothing changes.

## Interface

- `src/factory/entry/check_project.py` (`entry`): usage `factory-check-project [--agent-home <dir>] [--run] <folder>`.
  - With `--run` the command reads the instance's settings from the environment, as `factory-run` does; a fault of the settings is one line on standard error, `cannot run: <fault>`, and status 2, before anything is printed or started. The agent home then comes from the settings unless `--agent-home` is given.
  - The static part's lines are printed first. When the static part has a fault, the live part does not run, and the output and the status are those of the command without `--run`.
- A use case in `src/factory/machine/application/project_run.py` (`application`) does the live part through the interfaces `Images`, `ContainerRuns` and `Git`; the wiring of the concrete classes is in `src/factory/entry/`. It returns `ProjectPoint`s (`factory.pipeline.domain.project_check`), named `image`, `sync` and `check`, in this order; `LIVE_POINT_NAMES` in the domain module holds the three names.
  - The work folder: a new temporary directory with `checkout/` (a clone of `<folder>` at its `HEAD` commit) and `home/`, mounted at `/work` as a stage's dataset is. It is removed at the end, after a fault too.
  - `image`: without `factory/stage.Containerfile` the containers run in the instance's stage image and the point has no fault. Otherwise the stage file is built on the stage image under the tag `<stage image>-check`, never under the tag of the instance's own project image, with the time limit a stage's build has; a build that does not pass is the fault `the image does not build: <the last line of the build's output>`.
  - `sync`: one container that does what a stage's sync does after its checkout: started in `/work`, it changes into `/work/checkout` and runs `make sync`, or `make -f <path> sync` when the definition names a makefile, with the environment, the `PATH`, the site's variables (`FACTORY_CONTAINER_ENV`) and the CA bundle of a stage's sync, and the time limit of the definition's `sync` command.
  - `check`: a second container that does what a stage's check does: started in `/work/checkout`, it runs the sync and then `check`, as `ContainerMakeCommands.run` does, with the time limit of the definition's `check` command.
  - The faults of `sync` and of `check`, the first that applies: `could not start: <reason>` for a `ContainerError`; `timed out after <n> min`; `exit status <n>: <the last line of the output>`; and, for a run that ended with status 0, `no line "sync: green (<seconds> s)"` when the sync's output holds no such line, or `the last line is not "check: green": <the last line>` for the check.
  - A point after a live point with a fault is not run and not printed.
  - The scripts and the environment are those the stage uses, reused from their modules and not copied.
- The report: the static lines, the lines of the live points that ran, then the last line of `report_lines` over all printed points. Status 0 when no point has a fault, 1 otherwise.
- Tests: `tests/machine/application/test_project_run.py` (fakes of `ContainerRuns` and `Images` from `tests/support/`, a real repository in `tmp_path`) and `tests/entry/test_check_project_run.py`. `feature.md` gives this leave (decision 4): "S0001 to S0004 may add their new modules to the table of `tests/guards/test_areas.py`, and to any other guard table that lists every module or every entry command."

## Acceptance criteria

1. On a ready repository without a stage file, with fakes whose sync prints `sync: green (1.0 s)` and whose check ends with `check: green`, the live part returns the three points without a fault, no image is built, and both containers ran in the stage image.
2. With a stage file, the image is built on the stage image under `<stage image>-check`, and both containers run in that image; a build that does not pass gives `image` the fault `the image does not build: <last line>`, and `sync` and `check` are not run.
3. The sync container starts in `/work` and runs `make sync` in `/work/checkout`; the check container starts in `/work/checkout` and runs the sync, then `check`; with `make_file: factory/Makefile` in the definition both call make with `-f factory/Makefile`. Each gets the time limit of its command in the definition.
4. The faults of a run, as rows of one parametrized test for `sync` and for `check`: a container that could not start; a run that reached its time limit; exit status 2 with a last line; status 0 without the green line (for the check: with another last line). A fault of `sync` leaves `check` unrun.
5. The work folder holds the commit at `HEAD` and not an uncommitted change of the work tree, and it is gone after a green run, after a fault and after an exception of a container run.
6. The containers get the variables that the settings name in `FACTORY_CONTAINER_ENV` and the CA bundle's mount and names, as a stage's sync does.
7. `main` with `--run` and incomplete settings returns 2, prints `cannot run: ...` on standard error and nothing on standard output; with `--run` on a repository with a static fault it prints exactly what it prints without `--run` and returns 1, and starts no container and no build.
8. `main` with `--run`, complete settings and faked containers on a ready repository prints the six static lines, `image: ok`, `sync: ok`, `check: ok` and `project: ready`, and returns 0; with a red check it prints `check: FAIL: exit status 2: ...`, `project: not ready (1 fault)` and returns 1.
9. `make check` stays green.
10. docs: the operator guide, where it explains `factory-check-project`, says what `--run` adds and needs (an instance's environment, podman and the stage image; no dataset), that it works on a temporary clone of the commit at `HEAD` and builds its image under `<stage image>-check`, so it may run beside a working instance and for another repository, how to run it on the VM as the factory's user with the instance's environment (an example marked for the VM), and what each of the faults means; the project guide (`docs/project-guide/machine.md`) names the use case and the rule that it reuses the stage's scripts.

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
