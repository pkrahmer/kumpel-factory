# Projects start from a kit and a stack pack

## Goal

Today a new project copies `operator/template/`, a Python example, and every other stack copied and rewrote it by hand: the ESP32 template, the HeishaMon fork and the Spring service template each carry their own copy of the pipeline definition, the forms, the agents and the Makefile's contract part. When this feature is done, the factory holds one kit that every project shares and one small pack per stack, a project of any stack is assembled from the two, and one command says whether a repository is ready for the factory. An existing repository can be made ready without a change to its own Makefile. Done when every story below is merged and `make check` is green.

## Scope

- The conformance check, static and live.
- The makefile a pipeline definition names.
- An installed builder, so that the thin line needs no agent file in the project.
- The kit, and the stack packs `python`, `c-host` and `java-gradle`.
- The guide for a fresh start and for a brownfield repository.

## Out of scope

- The onboarding pull request and the upgrade pull request: the next feature.
- Starters. They are repositories of their own; cutting the three existing templates down to starters is the human's change below.
- An agent that analyses a repository and writes its pack.
- A container runtime inside a stage.

## Stories

The build order; start one at a time, the next when the one before is archived in `done/`.

- S0001: The conformance check reads a repository. A command `factory-check-project <folder>` prints one line per point (`ok` or `FAIL` with the reason) and ends with `project: ready` or `project: not ready (<n> faults)`: the pipeline definition is valid for this contract, every project command has a target in the makefile, the stage file passes the layer rule, every role's agent exists, every write path matches a tracked path, the forms are there. It starts no container.
- S0002: The pipeline definition names its makefile. `make_file: <path>` in `pipeline.yml` (contract 1.2) makes every project command, the sync included, run as `make -f <path>` from the root of the checkout; without the key nothing changes. S0001's check follows the key.
- S0003: The conformance check runs a repository. With `--run`, on a machine with the stage environment, the command builds the project image, runs `make sync`, and runs `make check` from another working directory than the sync's; each target must end with its green line inside its time limit. It uses the same container runs as a stage.
- S0004: The installed builder. The factory's own agents gain `builder` for the thin line (one builder, one reviewer), and the installed reviewer reads a project's review points from the section `## Review` of its `CLAUDE.md`. A project's own agent file still wins over the installed one.
- S0005: The kit. `operator/kit/` replaces `operator/template/`: the pipeline definition of the thin and of the full line, the forms, the makefile's contract part as a file a project includes (the green line, the start facts), and the skeleton of `CLAUDE.md`. A test assembles a project from the kit alone and S0001's check calls it ready but for the stack's targets.
- S0006: The stack packs. `operator/packs/python`, `operator/packs/c-host` and `operator/packs/java-gradle`: each a stage file, a makefile that includes the kit's contract part, the stack's sections of `CLAUDE.md` and a page of traps. A test assembles kit and pack for each stack and S0001's check calls the result ready.
- S0007: The guide. The project guide gains "Starting a project": from a starter, and for an existing repository by hand with the kit, a pack and the check, step by step; the operator guide gains what a Java project needs from a site (the private repository's variables, the CA bundle).

## The human's changes

1. After S0001 is merged: `pyproject.toml` gains the console script `factory-check-project = "factory.entry.check_project:main"`.
2. Before S0005: in `factory/pipeline.yml` the coder's write paths gain `operator/kit/*` and `operator/packs/*`, and the documenter's the `README.md` of each new folder that the folder guard asks for.
3. After S0006: the three templates become starters built from kit and pack (`spring-service-template`, `esp32-template`, and a Python starter from the todo demo), each checked with `factory-check-project --run` on the VM. These are repositories of their own and wait for the human.

## Decisions taken for the human

1. Placement, agents, the first step and the makefile key: the human's four answers of 2026-11-16, recorded in `planning/templates-plan.md`.
2. The check is a console command of its own, not a preflight item: the preflight guards a machine, the check a repository. The preflight may call it later.
3. The packs hold no application source. The Spring worker, the ESP32 logic and the todo service stay in their starters.
4. Leave for the areas table (S0001 to S0004): "S0001 to S0004 may add their new modules to the table of `tests/guards/test_areas.py`, and to any other guard table that lists every module or every entry command." Taken when the stories were written, 2026-11-17: a new module cannot pass that guard otherwise.
5. Leave for S0002: "S0002 may change earlier tests that pin the exact argument list of the sync script or of the check script, where their only failure is the added argument for the makefile." Taken with the story, 2026-11-17.
6. The conformance check reads the commit at `HEAD`, never the work tree, because the factory reads commits too; an uncommitted file does not count (S0001, 2026-11-17).
7. A project without `factory/stage.Containerfile` passes the point `stage file`: it runs on the factory's stage image, as this repository does (S0001, 2026-11-17).
8. The contract's minor version 1.2 is not enforced: a definition at 1.0 or 1.1 that holds `make_file` loads, as it was with `context` at 1.1. The version's text in `docs/` is S0002's docs criterion, which the documenter can reach, so the draft's change "before S0002" is not needed (S0002, 2026-11-17).
9. `ProjectCommands` and `StageEnvironment` keep their signatures; the two classes that call make ask a source for the makefile's name at every call. Reason: no fake and no other implementation has to change (S0002, 2026-11-17).
10. S0003 to S0007 are written out one by one while the earlier stories are built, so that each can name what the one before really built (2026-11-17, the night's plan).
11. Leave for S0004: "S0004 may change earlier tests under `tests/agent_files/`, and any other earlier test, that pin the list or the number of the shipped agents or the text or a checksum of `reviewer.md`, where their only failure is the eighth agent `builder` or the reviewer's new part." Taken with the story, 2026-11-17.
12. The live part of the check (`--run`) works on a temporary clone and builds its image under `<stage image>-check`, never on the instance's dataset or project image, so it can run beside a working instance and for another repository. It needs an instance's settings, not a dataset (S0003, 2026-11-17).
13. With `--run`, the live part runs only on a repository whose static part has no fault, and a live point after a failed one is not run and not printed (S0003, 2026-11-17).
14. The installed builder's text is the Spring template's builder without its stack's words; the story gives the exact text, since an agent's text is the human's to word (S0004, 2026-11-17).
15. S0001, answers on pull request 690 (2026-11-17): the intake's six added test rows are accepted; a tab after `include` counts as the separator, as make reads it. Leave: "the tester may change the expected list of `tests/guards/test_agent_home_wiring.py` to the one construction in `factory.entry.wiring` with the argument `agent_home`", because the check command builds the agents' reader from a folder and not from the instance's settings; the reader is still built in one place.
