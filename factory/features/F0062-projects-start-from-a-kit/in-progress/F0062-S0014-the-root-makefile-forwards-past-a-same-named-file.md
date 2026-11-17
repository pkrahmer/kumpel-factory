---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: self
  stage: intake
  started_at: '2026-11-17T07:25:19.507875Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T07:25:19.500779Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T07:25:19.507875Z'
  stage: intake
---

# The root makefile forwards a target that a file at the root is named after


## Description

The kit's `operator/kit/root.Makefile` forwards every target to `factory/Makefile` through a match-anything rule `%:` with no prerequisite. When a file or a folder at the project's root has a target's name, make treats that target as an existing file with nothing to remake: `make test` in a C project that keeps its tests in `test/` prints `make: 'test' is up to date.`, runs no test and exits 0, which is a false green for a developer and for an agent whose `CLAUDE.md` says that `make test` works at the root. The factory's own project commands are not touched, because they run as `make -f factory/Makefile <target>` through `make_file`. After this story, the forwarding rule depends on a phony target, as in the GNU make manual's idiom for overriding another makefile, so that every target is forwarded whether or not a file of its name exists. Nothing else of the one layout changes: `check` stays the default goal, `Makefile` is still never remade through the forwarding rule, and an unknown target still ends red. The kit's files are copies of the human's drafts (feature decision 18), so the human's seat changes `planning/kit-draft/root.Makefile` to the text below before the story starts, and the story copies it.

## Interface

- `operator/kit/root.Makefile`, the whole file afterwards (the two comment lines stay as they are):

```make
# Forwards every target to the factory's makefile, so that `make check` works at the root.
# For a repository without a root Makefile of its own; copied from kumpel-factory's kit as `Makefile`.
.DEFAULT_GOAL := check
Makefile: ;
.PHONY: factory-forward
factory-forward: ;
%: factory-forward
	@$(MAKE) --no-print-directory -f factory/Makefile $@
```

- Rules:
  - every target named on the command line is run by `factory/Makefile`, also when a file or a folder of that name exists at the root;
  - `make` without a target runs `check` of `factory/Makefile`;
  - an unknown target ends with a non-zero exit status;
  - make never tries to remake `Makefile` through the forwarding rule;
  - the name `factory-forward` is the forwarding makefile's own and is not forwarded.
- Tests: `tests/operator_scripts/test_root_makefile.py`, new, with real make runs in `tmp_path`, built on `ROOT_MAKEFILE` of `tests/support/kit_support.py`. No earlier test changes; `tests/operator_scripts/test_one_layout.py::test_the_root_makefile_forwards_every_target_to_the_factory_makefile` keeps passing as it is.

## Acceptance criteria

1. With `root.Makefile` as the root `Makefile` and a `factory/Makefile` that includes `factory/kit.mk` and has the targets `lint`, `test` and `check` (`check` depending on both), `make test` prints `test`'s green line and exits 0, in three rows: nothing named `test` at the root, a folder `test/` at the root, and an empty file `test` at the root.
2. In the same project with a folder `check/` at the root, `make` without a target prints the green lines of `lint` and `test` and ends with `check: green`.
3. In the same project with a folder `test/` at the root and a `test` recipe that ends with `exit 3`, `make test` exits with a non-zero status: a red target is not hidden by the folder.
4. `make nosuch` exits non-zero, and in every row of criteria 1 to 3 no output line names a target `Makefile` (`'Makefile'` or `` `Makefile' ``).
5. `make check` stays green.
6. docs: `operator/kit/README.md` (the `root.Makefile` row of its Files table, or the paragraph on the forwarding makefile) says that the forwarding makefile forwards a target also when a file or a folder at the root has the target's name; `docs/decisions.md` records, beside the one-layout entry, why the forwarding rule depends on a phony target (a `test/` folder made `make test` a false green).

## Smoke test

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
mkdir -p "$d/factory" "$d/test"; cp operator/kit/factory/kit.mk "$d/factory/"; cp operator/kit/root.Makefile "$d/Makefile"
printf 'include factory/kit.mk\n.PHONY: test check\ntest:\n\t$(start)\n\t$(green)\ncheck: test\n\techo "check: green"\n' > "$d/factory/Makefile"
env -u MAKEFLAGS -u MAKELEVEL -u MFLAGS make -C "$d" --no-print-directory test | sed 's/([0-9]*\.[0-9] s)/(N s)/'
```
Expect: `test: green (N s)`, and no line `make: 'test' is up to date.`

```bash
uv run pytest tests/operator_scripts/test_root_makefile.py tests/operator_scripts/test_one_layout.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
