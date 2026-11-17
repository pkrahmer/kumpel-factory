---
stage: docs
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 707
comments_read: [6941636547]
handed_over: null
claim:
  instance: self
  stage: docs
  started_at: '2026-11-17T07:37:36.265472Z'
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
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T07:29:54.872193Z'
  stage: tests
  run: cba05b7a76c14b0082ad22e782e3efc2
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T07:30:00.044010Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T07:32:33.830935Z'
  stage: doing
  run: a8712e58926a459cb50723f0b1d36130
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T07:32:39.378059Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-17T07:33:22.273750Z'
  stage: review
  run: e0d12146bcc747109e8b428f3f4fff8d
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-17T07:33:27.656634Z'
  stage: tests
- number: 14
  speaker: tester
  kind: result
  at: '2026-11-17T07:34:23.024960Z'
  stage: tests
  run: 5bd4194c546d4916982f986fbcc6ba6c
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-17T07:34:28.452524Z'
  stage: doing
- number: 16
  speaker: coder
  kind: result
  at: '2026-11-17T07:36:58.297367Z'
  stage: doing
  run: a46390a63f4e4f80b0e5dcea40475168
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-17T07:37:04.117715Z'
  stage: review
- number: 18
  speaker: reviewer
  kind: result
  at: '2026-11-17T07:37:31.237096Z'
  stage: review
  run: dd802303fe154c8aa0811d008bb48b56
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-17T07:37:36.265472Z'
  stage: docs
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
8. tester: I wrote the new test module `tests/operator_scripts/test_root_makefile.py` and created no other file. Its tests run real make in `tmp_path`, using `ROOT_MAKEFILE`, `KIT_MAKEFILE` and `run_kit_make` of `tests/support/kit_support.py` and `green_line` of `tests/support/kit_make_support.py`. I changed no earlier test.

   Each project has a `factory/Makefile` that includes `factory/kit.mk`. It declares `lint`, `test`, `check` (on `lint` and `test`) and `factory-forward` (`echo forwarded`) as `.PHONY`, as the smoke test's makefile does, so that only the root makefile's forwarding is tested and the `test/` folder does not also stop `factory/Makefile`.

   - criterion 1: `tests/operator_scripts/test_root_makefile.py::test_a_target_is_forwarded_past_a_file_or_folder_of_its_name`, with three rows: nothing named `test`, a folder `test/`, an empty file `test`.
   - criterion 2: `tests/operator_scripts/test_root_makefile.py::test_the_default_goal_runs_check_past_a_check_folder`
   - criterion 3: `tests/operator_scripts/test_root_makefile.py::test_a_red_target_is_not_hidden_by_a_folder_of_its_name` (the `test` recipe ends with `exit 3`).
   - criterion 4: `tests/operator_scripts/test_root_makefile.py::test_an_unknown_target_ends_red_and_no_run_remakes_the_makefile`. It has one row for each case of criteria 1 to 3 plus `nosuch`, and checks the expected exit status and that no line matches `` [`']Makefile' ``.
   - criterion 5: `tests/operator_scripts/test_root_makefile.py::test_the_forwarding_target_name_is_not_forwarded`
   - criterion 6: the coder's `make check`.
   - criterion 7: docs stage.

   The test runner imported every module. `make test` is red for the right reasons against the current `operator/kit/root.Makefile`:
   - the `test-folder` and `test-file` rows, the `check/` folder case and the red `test/` folder case fail with "make: 'test' is up to date." (or 'check');
   - `make factory-forward` prints `forwarded`.

   The rows that already pass are criterion 1's `nothing-named-test`, and in criterion 4 the `nothing-named-test`, `test-folder`, `test-file`, `default-goal-check-folder` and `unknown-target` rows. They hold already and must keep holding.

   `make lint` is green. I deviated from the procedure once: after `make test` I also ran the new file alone with pytest to read the failure reasons. The helper functions are named `with_*` so that pytest does not collect them as tests.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: I copied `planning/kit-draft/root.Makefile` into `operator/kit/root.Makefile`, and the two are now identical. The forwarding rule `%:` now depends on the phony, empty target `factory-forward` (declared as `.PHONY: factory-forward` and `factory-forward: ;`). Because the prerequisite is phony, make always runs the forwarding recipe, even when a file or folder of the target's name exists at the root. `.DEFAULT_GOAL := check` and `Makefile: ;` are unchanged. That was the only change. No code under `src/` and no test was touched.

    Main choice: I copied the human's draft as it is, following feature decision 18 and the Interface's whole-file text. I rejected two alternatives: `.PHONY` on a list of known target names, because the root makefile cannot know a project's targets; and `MAKECMDGOALS` tricks, which the GNU make manual's idiom makes unnecessary.

    Checks:
    - Before the change, 5 of the tester's tests in `tests/operator_scripts/test_root_makefile.py` failed, for the reasons the tester gave.
    - After the change, that file passes together with `tests/operator_scripts/test_one_layout.py` (34 passed).
    - `make check guides` is green: `check: green`, `guides: green`.

    Refactor: there is nothing to refactor, because the diff is the human's draft word for word. The journal changed the meaning of the Description only by adding criterion 5, which intake already carried in, so I made no Description rewrite.

    Noticed but not touched: nothing.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
11. factory: started review as self.
12. reviewer: Findings:

    1. `tests/operator_scripts/test_root_makefile.py:18-19`: `MAKEFILE_TARGET` (`[`']Makefile'`) and its comment are copied word for word from `tests/operator_scripts/test_one_layout.py:36-37`. Fix: under the standing leave to move a shared test helper, move the constant to `tests/support/kit_support.py`, import it in both modules, and name `test_one_layout.py` in the entry.
    2. `tests/operator_scripts/test_root_makefile.py:35-43` (`forwarding_project`): this repeats the project setup that `tests/operator_scripts/test_one_layout.py:106-109` writes inline (make `project/factory`, copy `KIT_MAKEFILE` as `factory/kit.mk` and `ROOT_MAKEFILE` as `Makefile`, write `factory/Makefile`). Fix: under the same leave, move one helper that takes `tmp_path` and the `factory/Makefile` text into `tests/support/kit_support.py`. Use it in both modules, and keep `test_the_root_makefile_forwards_every_target_to_the_factory_makefile`'s name and what it checks.

    Both findings change only the tests, so the decision is `tests`.

    Checked and found to hold:
    - **Criteria:**
      - 1: three parametrized rows (nothing, a `test/` folder, an empty `test` file). Each asserts exit 0, exactly one `test` green line and no "up to date".
      - 2: a `check/` folder; the `lint` and `test` green lines, and `check: green` as the last line.
      - 3: a `test/` folder and `exit 3`, asserting a non-zero exit.
      - 4: one parametrized test whose rows are every case of 1 to 3 plus `nosuch`. Each row checks the expected exit status and that no line names `Makefile`. `run_kit_make` merges stderr, so make's error lines are seen too.
      - 5: `factory-forward` is declared in `factory/Makefile` with `echo forwarded`. The test asserts exit 0 and no line `forwarded`.
      - 6: the coder's journal entry reports `check: green` and `guides: green`.
      - Every one of the Interface's five rules is tested on its failing side.
    - **The kit file:** `operator/kit/root.Makefile` is identical to `planning/kit-draft/root.Makefile` (`diff` reports no difference). It matches the Interface's whole-file text, and the two comment lines are kept.
    - **Architecture and security:** nothing under `src/` changed, and the diff has no marker, secret or string-built shell.
    - **Quality:** the new module and its helpers have docstrings. The `with_*` names keep pytest from collecting the helpers as tests.
    - **Work item hygiene:** the Description matches what was built. The coder's entry names the main choice (copy the draft as it is) and what was rejected (a `.PHONY` list of known targets, `MAKECMDGOALS` tricks). Docs criterion 7 still says what the reader must know.

    Earlier tests: none changed. The diff only adds `tests/operator_scripts/test_root_makefile.py`. The fixes above will change `tests/operator_scripts/test_one_layout.py` under the standing leave to move a shared test helper.
13. factory: started tests as self.
14. tester: I fixed both of the reviewer's findings by moving shared test helpers under the standing leave in `CLAUDE.md` (*Tests*). The earlier test file I changed is `tests/operator_scripts/test_one_layout.py`. I created no new file.

    - Finding 1 (`MAKEFILE_TARGET` copied): the constant and its comment now live in `tests/support/kit_support.py`. `tests/operator_scripts/test_root_makefile.py` and `tests/operator_scripts/test_one_layout.py` both import it from there, and neither defines it any more.
    - Finding 2 (project setup repeated): I added `forwarding_project(tmp_path, factory_makefile)` to `tests/support/kit_support.py`. It builds `project/` with `factory/kit.mk` copied from `KIT_MAKEFILE`, `Makefile` copied from `ROOT_MAKEFILE` and the given text as `factory/Makefile`.
      - `test_one_layout.py::test_the_root_makefile_forwards_every_target_to_the_factory_makefile` now calls `forwarding_project(tmp_path, FORWARDED_MAKEFILE)` instead of writing the project inline. Its name, rows and assertions are unchanged.
      - Imports that are no longer used were removed from `test_one_layout.py`: `shutil` and `KIT_MAKEFILE`.
      - In `test_root_makefile.py`, the local helper is now `project_with(tmp_path, test_recipe)`, a thin wrapper that passes this story's `factory_makefile(test_recipe)` to the shared helper.

    Criteria mapping, unchanged:
    - criterion 1: `tests/operator_scripts/test_root_makefile.py::test_a_target_is_forwarded_past_a_file_or_folder_of_its_name`
    - criterion 2: `tests/operator_scripts/test_root_makefile.py::test_the_default_goal_runs_check_past_a_check_folder`
    - criterion 3: `tests/operator_scripts/test_root_makefile.py::test_a_red_target_is_not_hidden_by_a_folder_of_its_name`
    - criterion 4: `tests/operator_scripts/test_root_makefile.py::test_an_unknown_target_ends_red_and_no_run_remakes_the_makefile`
    - criterion 5: `tests/operator_scripts/test_root_makefile.py::test_the_forwarding_target_name_is_not_forwarded`
    - criterion 6: the coder's `make check`.
    - criterion 7: the docs stage.

    Checks:
    - `uv run pytest -q tests/operator_scripts/test_root_makefile.py tests/operator_scripts/test_one_layout.py`: all passed (the coder's root makefile is already in place).
    - `make lint` is green (`lint: green (0.1 s)`); I applied ruff's import sort once.
    - `make types` is green.
    - Every module was imported; none failed to import.

    `lint`: lint: green (0.1 s)
15. factory: started doing as self.
16. coder: Round 1. The reviewer's two findings were about the tests only, and the tester fixed both in entry 14 by moving `MAKEFILE_TARGET` and `forwarding_project` to `tests/support/kit_support.py`. So I had no code change to make this round. I changed no file.

    Built (from round 0): `operator/kit/root.Makefile`. It is still the same as `planning/kit-draft/root.Makefile`: `diff` reports no difference. The forwarding rule `%:` depends on the phony, empty target `factory-forward`, so the rule runs even when a file or a folder at the root has the target's name.

    Main choice: copy the human's draft as it is (feature decision 18). Rejected: a `.PHONY` list of known target names, because the root makefile cannot know a project's targets.

    Checks:
    - `uv run pytest -q tests/operator_scripts/test_root_makefile.py tests/operator_scripts/test_one_layout.py`: 34 passed.
    - `make check guides`: `check: green`, `guides: green`.

    Refactor: nothing to change, because the code diff is the draft word for word. The journal changed the Description only by adding criterion 5, which intake already carried in, so I did not rewrite the Description.

    Noticed but did not touch: nothing.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
17. factory: started review as self.
18. reviewer: Round 1. No findings.

    Both findings from round 0 are fixed. `MAKEFILE_TARGET` and `forwarding_project` are now in `tests/support/kit_support.py` and both modules use them. Neither test module defines its own copy any more.

    What I checked and found to hold:
    - **Criteria:**
      - 1: three parametrized rows (nothing named `test`, a `test/` folder, an empty `test` file). Each row asserts exit 0, exactly one `test` green line and no "up to date".
      - 2: with a `check/` folder, `make` with no target gives one green line each for `lint` and `test`, and `check: green` is the last line.
      - 3: with a `test/` folder and a recipe ending in `exit 3`, the exit status is non-zero.
      - 4: one parametrized test with a row for each case of criteria 1 to 3 plus `nosuch`. Each row checks the expected exit status and that no line names `Makefile`, on merged output.
      - 5: `make factory-forward` exits 0 and no line reads `forwarded`, although `factory/Makefile` has that target and declares it phony.
      - 6: the coder's entry 16 reports `check: green` and `guides: green`.
      - 7: left for the docs stage, and its wording still names what the reader must know.
      - Each of the Interface's five rules is tested on its failing side.
    - **Kit file:** `operator/kit/root.Makefile` is identical to `planning/kit-draft/root.Makefile` (`diff` reports no difference). It matches the Interface's whole-file text, and the two comment lines are kept.
    - **Architecture and security:** nothing under `src/` changed. The diff adds no marker, no secret and no shell built from strings.
    - **Quality:**
      - `forwarding_project` writes `factory/Makefile`, the same path as `FACTORY_MAKEFILE` in `test_one_layout.py`, which that module still uses at lines 48 and 153.
      - `shutil` and `KIT_MAKEFILE` were removed from `test_one_layout.py` and are no longer used there.
      - The new helpers have docstrings.
    - **Work item hygiene:**
      - The journal names the main choice (copy the draft as it is) and what was rejected (a `.PHONY` list of known targets, `MAKECMDGOALS` tricks).
      - The Description matches what was built.

    Notes:
    - `tests/operator_scripts/test_root_makefile.py:59` (`matching`): it counts matching lines with the same expression that `tests/operator_scripts/test_one_layout.py:111` and `tests/operator_scripts/test_packs.py:131` write inline. A shared helper in `tests/support/kit_make_support.py` could serve all three. This is a quality point in a test file the diff adds, so it does not send the work item back.

    Earlier tests:
    - `tests/operator_scripts/test_one_layout.py`: changed under the standing leave to move a shared test helper. `MAKEFILE_TARGET` and the project setup moved to `tests/support/kit_support.py`. `test_the_root_makefile_forwards_every_target_to_the_factory_makefile` keeps its name, rows and assertions.
    - `tests/support/kit_support.py`: changed under the same leave. It is the shared place, and it only gained `MAKEFILE_TARGET` and `forwarding_project`.
19. factory: started docs as self.
