---
stage: review
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 700
comments_read: [6939383328]
handed_over: null
claim:
  instance: self
  stage: review
  started_at: '2026-11-17T05:28:31.782149Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T05:20:19.208683Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T05:20:19.216194Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T05:20:50.182426Z'
  stage: intake
  run: c7464a2d0e96478a8cc67a292470fb54
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T05:21:37.434920Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T05:21:40.038923Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T05:22:08.936326Z'
  stage: intake
  run: b489a3cfd4e64d2396ff814d4e3d4e16
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T05:22:14.352379Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T05:25:37.216044Z'
  stage: tests
  run: ecb5447af0a14177b5f2b359e905b144
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T05:25:42.091087Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T05:28:26.235524Z'
  stage: doing
  run: 6c023cf2f750440d86dca3a43647967c
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T05:28:31.782149Z'
  stage: review
---

# The makefile a pipeline definition names, and the kit's `kit.mk`, are protected paths

## Description

Every stage's take leaves out the protected paths: `Makefile`, `CLAUDE.md`, `factory/pipeline.yml`, the forms and the rest of `PROTECTED_PATHS`. They belong to the human, whatever a role's write paths say. Since the feature, a project's factory targets may live in another file: the makefile that `make_file` names (`factory/Makefile` for a repository that keeps its own root `Makefile`), and the kit's `factory/kit.mk`, which every pack's makefile includes and which the kit's README says a project never edits. Neither is protected, so a role whose write paths cover `factory/*` or `*` could change the factory's own targets and its green line. After this story the write path settings of a stage also protect the makefile that the definition at the stage-start commit names, when it names one, and `factory/kit.mk` always. `PROTECTED_PATHS` and a definition without `make_file` behave as before, but for `factory/kit.mk`. This story does not change the conformance check: it judges write paths against tracked files, not against protected paths.

## Interface

`factory.agents.domain.write_paths` (domain):

```python
KIT_MAKEFILE: str = "factory/kit.mk"

def protected_paths(make_file: str | None) -> list[str]:
    """The protected paths of a stage: `PROTECTED_PATHS`, `KIT_MAKEFILE`, and `make_file` when given."""
```

- `protected_paths(None)` is `[*PROTECTED_PATHS, KIT_MAKEFILE]`.
- `protected_paths("factory/Makefile")` is `[*PROTECTED_PATHS, KIT_MAKEFILE, "factory/Makefile"]`.
- `protected_paths("Makefile")` is `[*PROTECTED_PATHS, KIT_MAKEFILE]`: a `make_file` already in the list is not added again; likewise `protected_paths("factory/kit.mk")` is `[*PROTECTED_PATHS, KIT_MAKEFILE]`.
- `PROTECTED_PATHS` keeps its twelve patterns unchanged.

`factory.agents.application.write_paths.WritePathService.at` (application): `protected_paths` of the returned `WritePathSettings` is `protected_paths(definition.make_file)`, read from the definition at the stage-start commit, never from the work tree.

Tests: `tests/agents/domain/test_write_paths.py` (new rows for `protected_paths`, and `refusal` for `factory/kit.mk` and a named makefile), `tests/pipeline/application/test_write_paths.py` (the definition at the commit with and without `make_file`).

Earlier test changed, with the human's leave (journal entry 4): "the tester may change the expected `protected_paths` in `tests/pipeline/application/test_write_paths.py::test_at_returns_the_role_write_paths_with_the_work_item_expanded`, and in any other earlier test whose only failure is the added `factory/kit.mk`, to `protected_paths(None)`".

## Acceptance criteria

1. `protected_paths` returns, for `None`, `"factory/Makefile"`, `"Makefile"` and `"factory/kit.mk"`, exactly the four lists the Interface names, in that order, each without a duplicate.
2. `refusal("factory/kit.mk", settings)` with write paths `["factory/*"]` and `protected_paths(None)` is `factory/kit.mk is owned by the human; a change there is a question.`; `refusal("factory/other.mk", settings)` with the same settings is `None`.
3. `WritePathService.at` for a definition with `make_file: factory/Makefile` at the stage-start commit returns settings whose `protected_paths` hold `factory/Makefile`. The same definition with the key in the work tree only, not committed, gives settings without it. A definition without the key gives `protected_paths(None)`.
4. A take after a stage whose role's write paths are `["factory/*", "src/*"]`, and whose agent changed `factory/Makefile` (named by `make_file`), `factory/kit.mk` and `src/a.py`, takes `src/a.py` only.
5. `make check` stays green.
6. docs: `docs/operator-guide/pipeline.md` (the protected paths) and the project guide's page on agents and write paths name the named makefile and `factory/kit.mk` as protected; `docs/decisions.md` records why: the factory's targets and green line are the human's wherever the makefile lies.

## Smoke test

```bash
uv run python -c "from factory.agents.domain.write_paths import protected_paths; p = protected_paths('factory/Makefile'); print('factory/kit.mk' in p, 'factory/Makefile' in p, len(p))"
```
Expect: `True True 14`

```bash
uv run python -c "from factory.agents.domain.write_paths import protected_paths; print(len(protected_paths(None)), len(protected_paths('Makefile')))"
```
Expect: `13 13`

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: Intake: the story is buildable apart from two points. Code read: `src/factory/agents/domain/write_paths.py`, `src/factory/agents/application/write_paths.py` (the only place in `src/factory` that uses `PROTECTED_PATHS`), `tests/pipeline/application/test_write_paths.py:42-49` and the feature's decisions 1–31. The Interface, the architecture (a pure function in the domain, the definition read at the commit in the application) and the scope (follow-up S0010 of decision 31) look right. The format check passed.

   1. The leave to change an earlier test is only proposed. The Interface says the human gives it "when refining this story (proposed wording)", and the story still holds the comment `<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->`. No journal entry and no decision in `feature.md` grants it. Without it, `test_at_returns_the_role_write_paths_with_the_work_item_expanded` (it asserts `settings.protected_paths == list(PROTECTED_PATHS)`, line 49) fails once `factory/kit.mk` is added, and the tester may not change it (CLAUDE.md, *Not without asking*). Options: (a) grant the leave as worded: "the tester may change the expected `protected_paths` in `tests/pipeline/application/test_write_paths.py::test_at_returns_the_role_write_paths_with_the_work_item_expanded`, and in any other earlier test whose only failure is the added `factory/kit.mk`, to `protected_paths(None)`"; (b) narrow it to that one test. I recommend (a). I will carry it into the story and remove the "refine before starting" comment.

   2. `protected_paths("Makefile")`: the Interface says only that it "holds `Makefile` once". Criterion 1 says it returns "the list the Interface names", and the smoke test expects a length of 13. So the exact list, and its order, is not stated. Options: (a) state that `protected_paths("Makefile")` is `[*PROTECTED_PATHS, KIT_MAKEFILE]`: a `make_file` already in the list is not added again, and the same holds for `"factory/kit.mk"`. Criterion 1 then checks that exact list, and a row for `"factory/kit.mk"` is added. (b) Keep "holds once" and test only the count of `Makefile` and the length. I recommend (a), so that two coders cannot both pass with different orders.
4. 2026-11-17 human: 1: (a), the leave is granted as worded. 2: (a).
5. factory: started intake as self.
6. intake: accepted

   I carried the human's answers from journal entry 4 into the story:
   - (1a) The Interface's "Earlier test changed" paragraph now says the leave is granted (journal entry 4), with the wording unchanged. The "refine before starting" comment is removed.
   - (2a) The Interface now says `protected_paths("Makefile")` and `protected_paths("factory/kit.mk")` are `[*PROTECTED_PATHS, KIT_MAKEFILE]`, because a `make_file` already in the list is not added again. Criterion 1 now checks the exact lists for `None`, `"factory/Makefile"`, `"Makefile"` and `"factory/kit.mk"`.

   - Interface: names concrete modules and signatures. `KIT_MAKEFILE` and the pure `protected_paths(make_file)` go in `factory.agents.domain.write_paths`. `WritePathService.at` in `factory.agents.application.write_paths` reads `make_file` from the definition at the stage-start commit. Every list the function can return is now given exactly. `PROTECTED_PATHS` (twelve patterns, `src/factory/agents/domain/write_paths.py:22`) stays as it is.
   - Criteria: each can be tested by one test function. Criterion 1 covers all four lists the Interface names, the duplicate rule included. Criterion 2 covers both sides of the refusal: `factory/kit.mk` is refused and `factory/other.mk` is not. Criterion 3 covers the definition at the commit, the key in the work tree only (the failing side of "never from the work tree"), and a definition without the key. Criterion 4 covers the take from start to end. The earlier test that breaks has the human's leave.
   - Smoke test: both commands can run once the code exists. Both `Expect:` lines can be checked against the output: `True True 14` follows from 12 + kit.mk + factory/Makefile, and `13 13` follows from the duplicate rule.
   - Docs criterion: names what the reader must know (the named makefile and `factory/kit.mk` are protected, and why) and which pages hold it. It does not dictate any sentences.
   - Architecture: the rule is in the domain layer and the reading at the commit is in the application layer, as CLAUDE.md lays out. The code already has a way to read the definition at a commit (`make_file_source`). No new tool, dependency or interface.
   - Scope: this is follow-up S0010 of feature F0062's decision 31, inside the feature. It changes no `factory/` file and leaves the conformance check alone.

   The route is `tests`, because the Interface changes `src/factory`.
7. factory: started tests as self.
8. tester: Tests written for every criterion. They are red because `protected_paths` and `KIT_MAKEFILE` do not exist yet.

   - criterion 1: tests/agents/domain/test_write_paths.py::test_the_protected_paths_of_a_stage_add_the_kit_and_the_named_makefile_once. It has four rows: `None`, `"factory/Makefile"`, `"Makefile"` and `"factory/kit.mk"`, each giving the exact list from the Interface, with no duplicate. It also checks that `KIT_MAKEFILE == "factory/kit.mk"`.
   - criterion 2: tests/agents/domain/test_write_paths.py::test_the_kit_and_the_named_makefile_are_refused_under_a_matching_write_path. The write paths are `["factory/*"]`. Rows:
     - `factory/kit.mk` with `protected_paths(None)` is refused.
     - `factory/other.mk` with `protected_paths(None)` gives `None`.
     - `factory/Makefile` with `protected_paths("factory/Makefile")` is refused. This is the refusal for a named makefile that the Interface's test line asks for.
   - criterion 3: tests/pipeline/application/test_write_paths.py::test_at_protects_the_makefile_the_definition_at_the_commit_names. Rows:
     - committed: `make_file` is pushed in the definition.
     - work-tree-only: the committed definition has no key, and the work tree copy has `make_file: factory/Makefile`.
     - without-the-key.
   - criterion 4: tests/pipeline/application/test_take_protected_makefiles.py::test_the_take_leaves_the_named_makefile_and_the_kit_makefile. The intake role's write paths are `["factory/*", "src/*"]`, and the stage-start commit's definition names `make_file: factory/Makefile`. The agent adds `factory/Makefile`, `factory/kit.mk` and `src/a.py`. Only `src/a.py` reaches the checkout, and `report.left == ["factory/Makefile", "factory/kit.mk"]`. Run alone, it fails today because `factory/Makefile` is taken.
   - criteria 5 and 6: these are not test criteria (`make check` and docs).

   Files:
   - Created: tests/pipeline/application/test_take_protected_makefiles.py.
   - Changed (this story's tests): tests/agents/domain/test_write_paths.py, which gains a `protected_paths`/`KIT_MAKEFILE` import and two tests.

   Earlier tests changed under the human's leave (journal entry 4). Their only change is that the expected protected paths are now `protected_paths(None)` instead of `list(PROTECTED_PATHS)`:
   - tests/pipeline/application/test_write_paths.py: `_expected` and `test_at_returns_the_role_write_paths_with_the_work_item_expanded`. I also added the new test above to this file, as the Interface names it.
   - tests/agents/application/test_write_paths_guard.py: `test_a_tester_s_stage_gives_the_root_the_write_paths_and_the_protected_paths`. Its only failure would be the added `factory/kit.mk`.

   Three modules the test run cannot import, because `protected_paths` is missing from `factory.agents.domain.write_paths`:
   - tests/agents/domain/test_write_paths.py
   - tests/pipeline/application/test_write_paths.py
   - tests/agents/application/test_write_paths_guard.py

   The `make test` tail also shows two errors in tests/guards/test_documents_marker.py, which compares collected test lists. I expect them to clear once those imports work, but I have not checked this, so the coder should confirm it.

   `make lint` is green.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: I built `KIT_MAKEFILE` and `protected_paths(make_file)`, and connected them to the take. `make check guides` is green.

    - `src/factory/agents/domain/write_paths.py`:
      - `KIT_MAKEFILE = "factory/kit.mk"`.
      - `protected_paths(make_file)` returns `[*PROTECTED_PATHS, KIT_MAKEFILE]`. It appends `make_file` only when one is given and the list doesn't already hold it, so `"Makefile"` and `"factory/kit.mk"` are not added twice.
      - `PROTECTED_PATHS` is unchanged.
    - `src/factory/agents/application/write_paths.py`: `WritePathService.at` now sets `protected_paths=protected_paths(definition.make_file)`. The definition comes from the existing `_definition_at(stage_start.commit)`, which reads it through `git.show_file` at the stage-start commit, never from the work tree. So I needed no new read.

    **Main choice:** the duplicate check is an exact string match against the list (`make_file not in paths`). I rejected testing `make_file` against the patterns with `matches_any`. That would also skip a `make_file` already covered by a wildcard such as `.claude/*`. The Interface asks only that "a `make_file` already in the list is not added again", and an exact match keeps the returned list predictable.

    **Tests:**
    - The four test files the tester named pass when run alone.
    - The two errors in `tests/guards/test_documents_marker.py` that the tester expected to clear have cleared: `make test` is green inside `make check`.

    **Refactor:** I read the diff, which is two small edits. Nothing needed changing beyond shortening the new docstring to fit the line limit.

    **Description:** the journal changed nothing that needed a rewrite. Intake had already carried the human's answers from journal entry 4 into the Description.

    **Noticed, not touched:** none.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
11. factory: started review as self.
