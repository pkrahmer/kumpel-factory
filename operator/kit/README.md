# The kit

The kit is the small set of files that every project the factory builds needs, whatever its stack. They belong to the factory's contract: a pipeline definition, the two forms, the factory's part of the makefile and the skeleton of `CLAUDE.md`. None of them names a language, a build tool or a test framework. A stack adds its own part on top of the kit: the makefile's targets, and the files under the write paths.

The kit is one of three layers. A stack pack adds what one stack needs, and a starter is a repository of its own, built from the kit and a pack. The kit and the packs live in this repository; the starters do not. The decision log has the reasons, in [decisions.md](../../docs/decisions.md) (*A project starts from a kit, a stack pack and a starter*). The packs are in [`operator/packs/`](../packs/README.md).

## Assembling a project by hand

Choose a line first. The thin line has one builder and one reviewer before the human's approval. The full line has intake, tester, coder, reviewer, documenter and smoke tester, and an acceptance per feature. In both, the factory's installed agents do the work, and a file `factory/agents/<role>.md` in the project replaces one of them.

1. Copy every file of `operator/kit/factory/` into the project's `factory/` folder.
2. Keep the chosen line's pipeline definition under the name `factory/pipeline.yml`, and delete the other line's. For the thin line, run this from the project's root:

   ```sh
   mv factory/pipeline.thin.yml factory/pipeline.yml && rm factory/pipeline.full.yml
   ```

   For the full line:

   ```sh
   mv factory/pipeline.full.yml factory/pipeline.yml && rm factory/pipeline.thin.yml
   ```

3. Copy `operator/kit/CLAUDE.md` to the project's root, and fill in each `<...>` placeholder with what is true of the project.
4. Write the factory's makefile, `factory/Makefile`, which both pipeline definitions name with `make_file: factory/Makefile`. Its first line is `include factory/kit.mk`. After it, the makefile defines the four targets the pipeline definition needs: `sync`, `lint`, `test` and `check`. Each of them opens its recipe with `$(start)` and ends it with `$(green)`, and `check` ends with `echo "check: green"`. A stack pack brings this makefile; [packs/README.md](../packs/README.md) says how kit and pack are assembled.
5. If the repository has no root `Makefile` of its own, copy `operator/kit/root.Makefile` to the project's root as `Makefile`. It forwards every target to `factory/Makefile`, so `make check` works at the root, for a developer and for the agents. It forwards a target also when a file or a folder at the root has the target's name, such as `make test` beside a `test/` folder: its forwarding rule depends on a phony target, `factory-forward`, which is the forwarding makefile's own name and is not forwarded. A repository that keeps a root `Makefile` of its own leaves it as it is, and picks the second wording of the `make` line under `## Checks` in `CLAUDE.md`: every target is run as `make -f factory/Makefile <target>`.
6. Fill the write paths. Each role's write path without a placeholder (such as `src/*` or `README.md`) must match at least one committed file. Change the paths in `factory/pipeline.yml` to fit the project.
7. Commit, then run the conformance check on the project's folder:

   ```sh
   factory-check-project --agent-home <the factory's agents folder> <project>
   ```

   It reads the commit at `HEAD`, never the work tree. It ends with `project: ready` when the project is ready for the factory. Otherwise it prints one `FAIL` line for each point that is not ready. Before step 4, `makefile` fails with `factory/Makefile is missing`. Before step 6, `write paths` fails for each path that matches no file. The command is described in the operator guide, in [pipeline.md](../../docs/operator-guide/pipeline.md).

There is one layout for a fresh start and for an existing repository alike: the factory's files live in `factory/`, and the only other file the factory needs is `CLAUDE.md` at the root, with the forwarding `Makefile` where the repository has none of its own. The include line in `factory/Makefile` is `include factory/kit.mk`, because make runs from the root of the checkout, and every path in both files is taken from the root.

A target is run by hand from the root: `make check` (or plain `make`) through the forwarding root `Makefile`, or `make -f factory/Makefile check` in any repository.

A minimal `factory/Makefile` that passes the check:

```make
include factory/kit.mk

sync lint test:
	$(start)
	$(green)

check: lint test
	echo "check: green"
```

## What `kit.mk` gives the makefile

- Every recipe runs in one bash shell, which stops at the first failing line. make echoes no recipe line.
- `check` is the default goal, so `make -f factory/Makefile` without a target runs `check`. The forwarding root `Makefile` has `check` as its default goal too, so plain `make` at the root runs it.
- `$(start)` and `$(green)` time a recipe. `$(green)` prints `<target>: green (<seconds> s)`, which is the line the factory's records read.
- The three start facts: `facts-diff` (the branch's diff), `facts-changes` (the changed and new files) and `facts-files` (the tracked files). The factory runs them before an agent and puts their output into the agent's first message. They leave out `factory/`.

## Reference

### Files

| Path in the kit | Path in the project | Owner afterwards |
|---|---|---|
| `factory/kit.mk` | `factory/kit.mk` | the kit's: an upgrade of the kit replaces it, so the project does not edit it |
| `factory/story-form.md` | `factory/story-form.md` | the kit's: an upgrade replaces it |
| `factory/feature-form.md` | `factory/feature-form.md` | the kit's: an upgrade replaces it |
| `factory/pipeline.thin.yml` | `factory/pipeline.yml`, for the thin line | the project's own |
| `factory/pipeline.full.yml` | `factory/pipeline.yml`, for the full line | the project's own |
| `factory/README.md` | `factory/README.md` | the project's own |
| `CLAUDE.md` | `CLAUDE.md` | the project's own |
| `root.Makefile` | `Makefile`, only when the repository has no root `Makefile` of its own | the project's own: it forwards every target to `factory/Makefile`, also when a file or a folder at the root has the target's name, with `check` as its default goal; `factory-forward` is its own and is not forwarded |

### The variables of `kit.mk`

A project sets them in its makefile before the include line, or in the environment of make.

| Name | What it does | Default | Example |
|---|---|---|---|
| `WORKING_BRANCH` | the working branch: the start facts take their base from `origin/<WORKING_BRANCH>` | `develop` | `WORKING_BRANCH = main` |
| `FACTS_LEFT_OUT` | git pathspecs of files no agent needs to see, left out of all three start facts | empty | `FACTS_LEFT_OUT = ':!build.lock'` |

### Tests

`tests/operator_scripts/test_kit_files.py` checks the kit's files and a project assembled from them. `tests/operator_scripts/test_kit_makefile.py` runs make on `kit.mk`. `tests/operator_scripts/test_one_layout.py` checks the one layout: the definitions' `make_file`, a project assembled from the kit and each pack with and without a root `Makefile` of its own, the forwarding root `Makefile`, and the protection of `factory/Makefile` and `factory/kit.mk`. `tests/operator_scripts/test_root_makefile.py` runs make on the forwarding root `Makefile` with a file or a folder of a target's name at the root, a red target, an unknown target and the name `factory-forward`. The assembling helper is `tests/support/kit_support.py`.
