---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 700
comments_read: [6939383328]
handed_over: null
claim:
  instance: self
  stage: intake
  started_at: '2026-11-17T05:21:40.038923Z'
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
---

# The makefile a pipeline definition names, and the kit's `kit.mk`, are protected paths

<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->

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
- `protected_paths("Makefile")` holds `Makefile` once.
- `PROTECTED_PATHS` keeps its twelve patterns unchanged.

`factory.agents.application.write_paths.WritePathService.at` (application): `protected_paths` of the returned `WritePathSettings` is `protected_paths(definition.make_file)`, read from the definition at the stage-start commit, never from the work tree.

Tests: `tests/agents/domain/test_write_paths.py` (new rows for `protected_paths`, and `refusal` for `factory/kit.mk` and a named makefile), `tests/pipeline/application/test_write_paths.py` (the definition at the commit with and without `make_file`).

Earlier test changed, with a leave the human gives when refining this story (proposed wording): "the tester may change the expected `protected_paths` in `tests/pipeline/application/test_write_paths.py::test_at_returns_the_role_write_paths_with_the_work_item_expanded`, and in any other earlier test whose only failure is the added `factory/kit.mk`, to `protected_paths(None)`".

## Acceptance criteria

1. `protected_paths` returns, for `None`, `"factory/Makefile"` and `"Makefile"`, the three lists the Interface names, each without a duplicate.
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
