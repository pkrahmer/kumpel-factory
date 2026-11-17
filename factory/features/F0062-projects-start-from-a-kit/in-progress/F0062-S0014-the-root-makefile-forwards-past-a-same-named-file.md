---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 707
comments_read: [6941636547]
handed_over: null
claim:
  instance: self
  stage: tests
  started_at: '2026-11-17T07:27:06.803288Z'
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
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T07:25:51.598570Z'
  stage: intake
  run: 0bc5fe6427e7426798199c0da7cef2d8
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T07:26:37.207177Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T07:26:39.694476Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T07:27:01.632336Z'
  stage: intake
  run: 3f921c8b067b4fe8b65e51f881cfee8c
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T07:27:06.803288Z'
  stage: tests
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
5. In the same project, with a target `factory-forward` in `factory/Makefile` whose recipe prints `forwarded`, `make factory-forward` exits 0 and prints no line `forwarded`.
6. `make check` stays green.
7. docs: `operator/kit/README.md` (the `root.Makefile` row of its Files table, or the paragraph on the forwarding makefile) says that the forwarding makefile forwards a target also when a file or a folder at the root has the target's name; `docs/decisions.md` records, beside the one-layout entry, why the forwarding rule depends on a phony target (a `test/` folder made `make test` a false green).

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
3. intake: 1. The Interface states the rule "the name `factory-forward` is the forwarding makefile's own and is not forwarded", but no criterion tests it, on either side, so a coder could forward that name too and every test would still pass. Options: (a) add a criterion before the two closing ones, for example: "5. In the same project, with a target `factory-forward` in `factory/Makefile` whose recipe prints `forwarded`, `make factory-forward` exits 0 and prints no line `forwarded`"; (b) take the rule out of the Interface, since it only records what the given makefile text does anyway and is not a promise to the project. I would choose (a), because the rule says that a project must not use that name, and a test makes that visible.

   Everything else checks out and needs no change. The Interface's text matches `planning/kit-draft/root.Makefile` exactly. Criteria 1 to 4 cover the other four rules on both sides: forwarding with nothing, a folder or a file of the target's name at the root; the default goal; a red target and an unknown target; no `Makefile` remake. Both smoke tests run as written: `kit.mk` has `.ONESHELL`, `$(start)` and `$(green)`; pytest gets `-q` from `addopts`, and the command passes none. Docs criterion 6 names what the reader must know without dictating sentences. The architecture fits: a kit file plus a new test in `tests/operator_scripts/` on `ROOT_MAKEFILE` of `tests/support/kit_support.py`, and no earlier test changes. Scope: within F0062 (kit, decision 18) and not in its Out of scope. If the human answers (a), the route is `tests`.
4. 2026-11-17 human: (a), with your wording of criterion 5.
5. factory: started intake as self.
6. intake: accepted
   - Human's answer carried in: following journal entry 4 ("(a), with your wording of criterion 5"), I added criterion 5 word for word as intake proposed it in entry 3. It goes before the two closing criteria, which are now 6 (`make check`) and 7 (`docs:`). The Description's meaning is unchanged.
   - Interface: names the whole new text of `operator/kit/root.Makefile`, which matches `planning/kit-draft/root.Makefile`. It states five rules, and it names the new test file `tests/operator_scripts/test_root_makefile.py`, built on `ROOT_MAKEFILE` of `tests/support/kit_support.py`.
   - Criteria: each can be tested by one test function. Every rule is tested on both sides:
     - forwarding when nothing, a folder or a file of the target's name is at the root (1);
     - the default goal past a `check/` folder (2);
     - a red target is not hidden by a folder (3);
     - an unknown target ends red, and nothing tries to remake `Makefile` (4);
     - `factory-forward` is not forwarded (5): an explicit empty phony rule, so it exits 0 and prints nothing from `factory/Makefile`.
   - Smoke test: both blocks can be run as written. `kit.mk` provides `.ONESHELL`, `$(start)` and `$(green)`. The pytest command passes no `-q`, because `addopts` already sets it. Each `Expect:` line names output that can be checked.
   - Docs criterion: names what the reader of `operator/kit/README.md` and `docs/decisions.md` must know, and dictates no sentences.
   - Architecture: one kit file copied from the human's draft (feature decision 18) and one new test module in `tests/operator_scripts/`. No earlier test changes, and the factory's own `make -f factory/Makefile` calls are not touched.
   - Scope: within F0062 (the kit, its one layout) and not in its Out of scope.
   - Route: `tests`, because the Interface changes `operator/kit/root.Makefile` and adds a test, which the documenter may not write.
7. factory: started tests as self.
