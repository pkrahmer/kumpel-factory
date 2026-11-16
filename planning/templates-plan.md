# Templates: kit, stack packs and starters

The plan for how a project gets what the factory needs, for a fresh start and for an existing (brownfield) repository. Decided with the human on 2026-11-16, after four projects of four stacks had been built: the Python template, the ESP32 template, the HeishaMon fork (the one brownfield case) and the Spring service template.

## The three layers

What was called a template holds three kinds of files with three owners.

| Layer | What it holds | Changes when | Needed by |
|---|---|---|---|
| Kit | the pipeline definition, the forms, the Makefile's contract part (the green line, the start facts), the headings of `CLAUDE.md` | the factory's contract changes | every project |
| Stack pack | `stage.Containerfile`, the bodies of `sync`, `lint` and `test`, the stack's rules for `CLAUDE.md`, the write paths, the stack's traps | the stack changes | every project of that stack |
| Starter | application source, sample tests, Dockerfile, CI file | an organisation's habits change | a fresh start only |

A brownfield project needs the kit and a pack, never a starter. A starter at work carries company specifics and cannot live in the public factory.

## The decisions (the human, 2026-11-16)

1. **Placement.** The kit and the stack packs live in the factory's repository and are tested with it. Starters are repositories of their own (`kumpel-starter-<stack>`); a company keeps its own private starter.
2. **Agents.** The factory's installed agents are the default, and a project may replace single agent files. The code does this already (`ProjectAgentDefinitions`: the project's file first, the installed one otherwise). What changes is the habit: a kit copies no agent file, and a stack's review points live in the project's `CLAUDE.md`.
3. **The first step** is one feature: the conformance check, the kit and the packs, with the three existing templates cut down to starters. The onboarding pull request is a second feature.
4. **The makefile.** The pipeline definition may name the makefile the factory runs, for example `factory/Makefile`, so that an existing root Makefile stays untouched. A definition that names none keeps today's behaviour.

5. **Make stays the one command runner** (my decision, for the human to confirm). `CLAUDE.md` rule R11 foresaw a Gradle or npm implementation of the project commands. The Spring proof showed that a Makefile which wraps `./gradlew` is enough, and it keeps one contract for every stack. No second implementation is planned.

## The conformance check

One command answers "is this repository ready for the factory?", one line per point, and is the single definition of ready. Fresh starts and brownfield repositories pass the same check, and a factory release runs it against every known starter, which is how drift is found.

- Static part, anywhere: the pipeline definition is valid for this factory's contract; every project command has a target in the makefile; the stage file passes the layer rule; every role's agent exists (the project's or the installed one); every write path matches a tracked path; the forms are there.
- Live part, on a machine with the stage environment: the project image builds; `make sync` is green; `make check` is green from another working directory than the sync's, which finds the fault of a cache that follows the working directory; every target ends with its green line inside its time limit.

## What a project owns afterwards

`factory/pipeline.yml`, `factory/stage.Containerfile`, its makefile and `CLAUDE.md`, plus an agent file only where it truly differs. The forms and the makefile's contract part are the kit's files, marked as the factory's, so that an upgrade can replace them.

## Features

1. **F0062, projects start from a kit and a stack pack** (draft in `planning/drafts/F0062-projects-start-from-a-kit/`): the conformance check, the makefile named in the pipeline definition, the installed builder for the thin line, the kit, the packs `python`, `c-host` and `java-gradle`, and the guide.
2. **Later: the onboarding pull request and the upgrade pull request.** An instance on a repository without `factory/pipeline.yml` opens a pull request with the kit and the fitting pack; the same mechanism replaces the kit's files when the contract changes. Weighed on 2026-10-26 in `v1.2-candidates.md` and recommended there.
3. **Not planned:** an agent that analyses a brownfield repository and fills in the pack itself. It waits until the plain route has onboarded one real work project.

## What the Spring proof added (2026-11-16)

- The factory needed no change for Java 21, Spring Boot 4.1 and Gradle: one demo story ran in 6 runs for $1.79.
- A private Maven repository works through `FACTORY_CONTAINER_ENV` and `FACTORY_CA_BUNDLE`. Java reads neither `SSL_CERT_FILE` nor `HOME`: the pack builds a trust store from the bundle and names the home folder to Gradle. Both belong to the `java-gradle` pack and its page of traps.
- A stage has no container runtime, so an image build and Testcontainers stay in the CI pipeline; the Pub/Sub emulator runs as a plain process.
