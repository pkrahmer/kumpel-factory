# Projects start from a kit and a stack pack

Draft of 2026-11-16, not pre-checked. The plan behind it is `planning/templates-plan.md`.

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

1. After S0006: the three templates become starters built from kit and pack (`spring-service-template`, `esp32-template`, and a Python starter from the todo demo), each checked with `factory-check-project --run` on the VM.
2. Before S0002: the contract's minor version in `docs/` where a story's write paths do not reach.

## Decisions taken for the human

1. Placement, agents, the first step and the makefile key: the human's four answers of 2026-11-16, recorded in `planning/templates-plan.md`.
2. The check is a console command of its own, not a preflight item: the preflight guards a machine, the check a repository. The preflight may call it later.
3. The packs hold no application source. The Spring worker, the ESP32 logic and the todo service stay in their starters.
