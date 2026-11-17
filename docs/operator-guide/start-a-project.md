# Starting a project

A topic of the [operator guide](README.md). It is for the person who sets up a repository so that the factory can build it. It leads from an empty or an existing repository to the first [story](../project-guide/glossary.md) the factory works on. You know git and a terminal; you do not need to read the factory's code.

Words the factory gave its own meaning, such as [feature](../project-guide/glossary.md), [write paths](../project-guide/glossary.md) and [backlog](../project-guide/glossary.md), are explained in the [glossary](../project-guide/glossary.md).

## What a project needs

Before the factory can build a repository, the repository holds three layers of files:

1. **The kit**, for every project. It is the factory's contract, the same for every stack: the pipeline definitions of the thin and of the full line, the story and feature forms, `kit.mk` (the factory's part of the makefile) and the skeleton of `CLAUDE.md`. It lives in [`operator/kit/`](../../operator/kit/README.md).
2. **A stack pack**, for every project of one stack. It brings the makefile's targets (`sync`, `lint`, `test`, `check`), a stage file with the tools those targets need, the stack's sections of `CLAUDE.md` and a page of the stack's traps. The packs live in [`operator/packs/`](../../operator/packs/README.md).
3. **A starter**, for a fresh start only. It is a repository of its own, built from the kit and a pack, with a first piece of code that already passes `make check`.

What exists today:

- the kit;
- three packs: `python` (uv, a src layout), `c-host` (C built and tested on the host with CMake and CTest) and `java-gradle` (Java with the Gradle wrapper);
- no public starter. Starters for every stack, and a pull request that sets a repository up for you, do not exist yet. Until they do, a project is set up by hand, as *An existing repository* below describes; that walk works for an empty repository too.

## An existing repository

The walk below takes a repository you already have and makes it ready for the factory. Run the commands from the root of your clone of the factory's repository, where `operator/kit/` and `operator/packs/` are; `<project>` is the folder of your repository.

1. **Choose a line.** The thin line has one builder and one reviewer before your approval: cheap, for small changes. The full line has intake, tester, coder, reviewer, documenter and smoke tester, and an acceptance per feature: dearer, and every story's tests are written before its code. Both lines are a pipeline definition in the kit, `pipeline.thin.yml` and `pipeline.full.yml`.
2. **Copy the kit.** Copy every file of `operator/kit/factory/` into `<project>/factory/`. Keep the chosen line's pipeline definition as `factory/pipeline.yml` and delete the other one. Copy `operator/kit/CLAUDE.md` to the root of the project.
3. **Copy the pack.** Copy the pack's `Makefile` to the project's root. When the repository has a root `Makefile` of its own, copy it to `<project>/factory/Makefile` instead, leave your own makefile as it is, and remove the comment sign from the line `# make_file: factory/Makefile` in `factory/pipeline.yml`; the pack's include line, `include factory/kit.mk`, stays as it is, because make runs from the root. Copy the pack's `stage.Containerfile`, where it has one, to `<project>/factory/stage.Containerfile`, and the pack's other files to the same path from the root (for Java: `.gitleaks.toml` and `<project>/scripts/trust-store.sh`). The Python pack's makefile has two placeholders to fill in, `SOURCE` and `LAYERS`.
4. **Set the write paths.** In `factory/pipeline.yml`, each role has `write_paths`: the folders and files the factory may write. Name the folders the factory may change, and nothing else; everything outside them stays yours. Each path without a placeholder must match at least one committed file.
5. **Fill `CLAUDE.md`.** Fill in each `<...>` placeholder of the kit's skeleton with what is true of the project. Replace the skeleton's sections `## Tests`, `## Checks`, `## Review` and `## Not without asking (end the stage with `question`)` with the pack's sections of the same headings from its `CLAUDE.sections.md`.
6. **Commit.** The factory and its checks read commits, never the work tree.
7. **Run `factory-check-project`** on the project's folder, with `--agent-home` naming the installed agents (in the factory's checkout, the folder `agents`). It prints one line per point and then `project: ready`, or a `FAIL` line for each point that is not ready. Read each `FAIL`: it names the missing target, the write path that matches no file, or the missing form. Fix it, commit, and run the check again. Each point and each fault is listed in *Checking a repository before the factory runs it* in [pipeline.md](pipeline.md).
8. **Run it with `--run` on the machine.** On the VM, with the instance's environment loaded, `factory-check-project --run` also builds the project's image and runs `make sync` and `make check` in containers, as a stage does. Only this shows a tool that ignores `HOME` or a certificate the stack does not read. It ends with nine points `ok` and `project: ready`.
9. **Write the first feature and story** by the forms the kit copied: a folder `factory/features/F0001-<slug>/` with `feature.md` after `factory/feature-form.md`, and a story `backlog/F0001-S0001-<slug>.md` in it after `factory/story-form.md`. Check the story with `factory-check-story <path>` (see *Checking a story before it starts* in [pipeline.md](pipeline.md)).
10. **Start the story.** Move the story's file from the feature's `backlog/` to its `in-progress/` and push that commit to the working branch (`develop`). The factory takes the story on its next tick and opens a pull request for it.

### The walk in one example

The example sets up a small firmware repository that has a root `Makefile` of its own, with the kit's thin line and the C pack. Its first check finds the two slips the walk warns about: the factory's makefile is not named yet, and the builder may write to `tests/` and `docs/`, which hold no file. It runs in the factory's checkout:

```console
$ git init -q my-firmware && mkdir -p my-firmware/src
$ printf 'all:\n\tcc -o fw src/main.c\n' > my-firmware/Makefile
$ touch my-firmware/src/main.c my-firmware/README.md
$ mkdir -p my-firmware/factory && cp operator/kit/factory/* my-firmware/factory/
$ mv my-firmware/factory/pipeline.thin.yml my-firmware/factory/pipeline.yml && rm my-firmware/factory/pipeline.full.yml
$ cp operator/kit/CLAUDE.md my-firmware/
$ cp operator/packs/c-host/Makefile operator/packs/c-host/stage.Containerfile my-firmware/factory/
$ git -C my-firmware add -A && git -C my-firmware -c user.name=t -c user.email=t@example.com commit -q -m kit
$ python -m factory.entry.check_project --agent-home agents my-firmware
pipeline definition: ok
makefile: FAIL: no target check; no target lint; no target test; no target sync; no target facts-diff; no target facts-files
stage file: ok
agents: ok
write paths: FAIL: role builder: write path tests/* matches no tracked file; role builder: write path docs/* matches no tracked file
forms: ok
project: not ready (8 faults)
```

The makefile fault comes from the root `Makefile`, which the check reads while the pipeline definition names no other. Name the factory's makefile, let the builder write only `src/`, `tests/` and `README.md`, give `tests/` its first file, commit, and check again:

```console
$ git init -q my-firmware && mkdir -p my-firmware/src my-firmware/tests my-firmware/factory
$ printf 'all:\n\tcc -o fw src/main.c\n' > my-firmware/Makefile
$ touch my-firmware/src/main.c my-firmware/README.md my-firmware/tests/test_main.c
$ cp operator/kit/factory/* my-firmware/factory/ && cp operator/kit/CLAUDE.md my-firmware/
$ mv my-firmware/factory/pipeline.thin.yml my-firmware/factory/pipeline.yml && rm my-firmware/factory/pipeline.full.yml
$ cp operator/packs/c-host/Makefile operator/packs/c-host/stage.Containerfile my-firmware/factory/
$ sed -i 's|^# make_file: factory/Makefile|make_file: factory/Makefile|' my-firmware/factory/pipeline.yml
$ sed -i 's|"tests/\*", "docs/\*", |"tests/*", |' my-firmware/factory/pipeline.yml
$ grep -e '^make_file' -e 'builder: ' my-firmware/factory/pipeline.yml
make_file: factory/Makefile
  builder: {write_paths: ["src/*", "tests/*", "README.md"]}
$ git -C my-firmware add -A && git -C my-firmware -c user.name=t -c user.email=t@example.com commit -q -m kit
$ python -m factory.entry.check_project --agent-home agents my-firmware
pipeline definition: ok
makefile: ok
stage file: ok
agents: ok
write paths: ok
forms: ok
project: ready
```

### The live check on the machine

On the VM, run the check as `factory` with the instance's environment loaded. This is an example for the VM, where `/srv/factory/vm` is the instance's folder; it is the command of the runs below and is not run here:

```sh
sudo -iu factory
set -a; . /srv/factory/vm/factory.env; set +a
/srv/factory/vm/factory/.venv/bin/factory-check-project --run /path/to/my-project
```

Real runs, for what to expect:

- The static check on the Spring demo and on a fork of the HeishaMon firmware, on the VM factory-vm2, on 2026-11-17: both `project: ready`.
- `factory-check-project --run` on the Spring demo, on 2026-11-17: all nine points `ok`, in 1 min 42 s.
- The same on a small C project assembled from the kit and the C pack: 19 s; and on the Spring demo's sources with the kit and the Java pack: 1 min 45 s.
- The first Java story the factory built, on 2026-11-16: 6 runs, $1.79.

## A fresh start from a starter

A repository that begins from a starter has the kit and a pack already, and a first piece of code that passes `make check`. The walk is short:

1. Create the new repository from a copy of the starter's files.
2. Fill in the project's name and the placeholders the starter leaves in `CLAUDE.md` and the makefile, and adjust the write paths to the project's folders.
3. Commit, and run `factory-check-project` and then `factory-check-project --run`, as steps 7 and 8 above.
4. Write the first feature and story, and start the story, as steps 9 and 10 above.

A company keeps its own starter, private, because a starter carries the company's habits, which do not belong in a public one. No public starter exists yet.

## What the project owns afterwards

Once copied, most files are the project's own: `factory/pipeline.yml`, `CLAUDE.md`, `factory/README.md`, and every file of the pack (the makefile, the stage file, the scripts). Change them as the project needs; no upgrade of the kit or the pack replaces them.

Three files stay the kit's: `<project>/factory/kit.mk`, `<project>/factory/story-form.md` and `<project>/factory/feature-form.md`. An upgrade of the kit replaces them, so the project does not edit them.

**The agents.** The project copies no agent: the agents installed with the factory are the default for every role. To replace one, commit a file `<project>/factory/agents/<role>.md`; it replaces the installed agent whole and is never merged with it. See *A project's own agents* in [agent-runtime.md](agent-runtime.md).

**The review points.** What the reviewer checks in every diff of this project, beyond its general checklist, goes into `## Review` in `CLAUDE.md`, one bullet each. A pack brings its stack's points there; add your own.

## The traps of each stack

Each pack has a `TRAPS.md`: what cost time when the first projects of that stack ran in the factory, and what the pack does about each. Read it before the first story. It is not copied into the project.

- **Python** ([TRAPS.md](../../operator/packs/python/TRAPS.md)). No stage file is needed: the stage image holds uv, and `make sync` is `uv sync --frozen`. Every tool must be a pinned development dependency, called through `uv run`. The tests stage runs `lint` and not the type check, because the tests are written before the code. The tests run on every core, so a test must pass on a worker of its own.
- **C** ([TRAPS.md](../../operator/packs/c-host/TRAPS.md)). A stage has no device and no vendor toolchain: only the host build is checked, so the logic must build with the host's compiler, and a cross build or a flash is a target of its own, outside `check`. An existing firmware keeps its own build, with the factory's makefile at `<project>/factory/Makefile`. What `CMakeLists.txt` fetches is fetched by `make sync` and pinned by hash.
- **Java** ([TRAPS.md](../../operator/packs/java-gradle/TRAPS.md)). A stage has no container runtime, so an image build and Testcontainers stay in the CI pipeline; what the tests need runs as a plain process. Every target but `sync` is offline: the build file registers the task `resolveAll`, and a new dependency shows as a red check until the next sync. Java reads neither `HOME` nor `SSL_CERT_FILE`, which the makefile and `make sync` make up for. A private Maven repository and a company CA need the site's settings in *A Java project* in [site.md](site.md).
