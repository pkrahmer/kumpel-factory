# The guide

## Description

The kit, the packs and the conformance check exist, but an operator who wants the factory to build a repository finds them only piece by piece: the kit's and the packs' own `README.md`, the page on the pipeline definition, the page on a site. After this story the operator guide has one page, "Starting a project", that leads through both ways from start to the first story: a fresh repository from a starter, and an existing repository by hand with the kit, a pack and the check. The page on a site gains what a Java project needs from it. This is a story of documents only: no code, no test and no kit or pack file changes. It describes what is built, with examples that were really run, and it names what does not exist yet (the onboarding pull request, starters for every stack) as not existing.

## Interface

- No module under `src/factory/` and no file under `operator/` changes; no test is written or changed.
- `docs/operator-guide/start-a-project.md`, new, with the operator guide's index (`docs/operator-guide/README.md`) pointing to it, and `README.md` naming it as the place to begin with a repository of one's own.
- `docs/operator-guide/site.md` gains the part on a Java project.
- The real runs the page may quote, each with its date: the conformance check on the Spring demo and on the HeishaMon fork on factory-vm2 (2026-11-17, static, both `project: ready`); `factory-check-project --run` on the Spring demo (2026-11-17, nine points `ok`, 1 min 42 s), on a small C project from kit and C pack (19 s) and on the Spring demo's sources with kit and Java pack (1 min 45 s); the first Java story in the factory (2026-11-16, 6 runs, $1.79).

## Acceptance criteria

1. The new page opens with what a project needs before the factory can build it, as the three layers: the kit (every project), a stack pack (every project of that stack), a starter (a fresh start only); and says which of them exist today: the kit, the packs `python`, `c-host` and `java-gradle`, and no public starter yet.
2. The page's part for an existing repository is a numbered walk that a reader can follow without another page: choose the thin or the full line and what each means; copy the kit; copy the pack, with the makefile at `factory/Makefile` and `make_file` when the repository has a root `Makefile` of its own; set the write paths to the folders the factory may write; fill `CLAUDE.md` from the kit's skeleton and the pack's sections; commit; run `factory-check-project`, and read each `FAIL`; run it with `--run` on the machine; write the first feature and story by the forms; start the story.
3. The page's part for a fresh start says the same in short for a repository that begins from a starter, and that a company keeps its own private starter because it carries the company's habits.
4. The page says what the project owns afterwards and what stays the kit's (`kit.mk`, the forms), that the installed agents are the default and how a project replaces one, and where a stack's review points go (`## Review` in `CLAUDE.md`).
5. The page names each pack's `TRAPS.md` as the page to read before the first story, and says in one paragraph per stack what to expect of it in a stage (for Java: no container runtime in a stage, so an image build and Testcontainers stay in the CI pipeline; every target but `sync` offline).
6. Every command the page shows is a runnable example that the document check runs, or is marked as an example for the VM that names the real run it was copied from, with its date.
7. `docs/operator-guide/site.md` says what a Java project needs from a site: the private Maven repository's address and login as variables named in `FACTORY_CONTAINER_ENV` and set in the instance's `factory.local.env`, never in the repository; the CA bundle in `FACTORY_CA_BUNDLE`, which Java does not read by itself and the Java pack turns into a trust store at `make sync`; and that both were proven with a stand-in repository on 2026-11-16.
8. `make check` stays green.
9. docs: the page `docs/operator-guide/start-a-project.md`, the index's entry for it, `README.md`'s pointer to it and the Java part of `docs/operator-guide/site.md`, as criteria 1 to 7 describe them; `docs/decisions.md` records that the guide for starting a project is the operator's page, not the agents' project guide, because its reader is a person who sets a repository up.

## Smoke test

```bash
test -f docs/operator-guide/start-a-project.md && grep -c 'start-a-project.md' docs/operator-guide/README.md README.md
```
Expect: two lines, each a file name, a colon and a number of at least 1.

```bash
grep -c -e 'factory-check-project' -e 'make_file' -e 'TRAPS.md' docs/operator-guide/start-a-project.md; grep -c -e 'FACTORY_CONTAINER_ENV' -e 'FACTORY_CA_BUNDLE' docs/operator-guide/site.md
```
Expect: two numbers, each at least 3 for the first and at least 2 for the second.

## Journal
