# <project>

<One sentence: what this repository is.> Built by kumpel-factory (github.com/pkrahmer/kumpel-factory); the pipeline's rules reach every agent in its instructions, so this file holds only what is true of this project.

## Language
- Everything in this repository is English: code, comments, docs, work items, commit messages.

## Architecture
- <Layers, dependency direction, what is pure, where wiring happens.>
- <Typing and validation rules.>

## Tests
- <Framework; where tests live; what may be faked and what may not.>
- The sides of one rule are rows of one parametrized test, not separate test functions.

## Docs
- `README.md` is for the newcomer: what it is, how to run it, where to look next. `docs/decisions.md` is the decision log.
- <Which comments and doc comments the code carries.> Comments say why, never what.

## Checks
- `make check` must be green before any stage reports done. It runs <the targets, each with what it checks>. Each target ends with the line `<target>: green (<seconds> s)`; `make check` ends with `check: green`.
- Run `make check` and every other make target in the foreground and read its output.

## Review
- <The stack's review points, one bullet each: what the reviewer checks in every diff of this project beyond its general checklist.>

## Not without asking (end the stage with `question`)
- New dependency, change to the build files or to `factory/`, change to a test another story wrote, a marker that silences a check.
