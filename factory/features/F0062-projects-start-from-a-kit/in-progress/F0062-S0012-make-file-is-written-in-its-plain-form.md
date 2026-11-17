---
stage: review
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 703
comments_read: [6940217140]
handed_over: null
claim:
  instance: self
  stage: review
  started_at: '2026-11-17T06:10:56.532448Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T06:03:43.313600Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T06:03:43.320645Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T06:04:10.866048Z'
  stage: intake
  run: 233e96fc8a444ea0a2f4fe1119d9d922
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T06:04:56.089165Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T06:04:58.457306Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T06:05:16.447030Z'
  stage: intake
  run: c94ba50822794f90bbbcdd2c60e70622
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T06:05:21.572673Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T06:08:07.999870Z'
  stage: tests
  run: b5e1a497e6b74b79b2622dba4c517519
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T06:08:13.094165Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T06:10:50.920059Z'
  stage: doing
  run: 6fa5fbe7020e4178a994238647bbd96f
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T06:10:56.532448Z'
  stage: review
---

# A `make_file` is written in its plain form, or the definition refuses it


## Description

The pipeline definition accepts `make_file: ./factory/Makefile`, `factory//Makefile` and `factory/Makefile/`, because each passes the characters rule and `is_inside_checkout`. make reads every one of them as `factory/Makefile`, but two other parts of the factory compare the text as written. First, `protected_paths` adds the text unchanged, so the take does not protect `factory/Makefile`: a role whose write paths cover `factory/*` may change the factory's own targets. Second, `factory-check-project` looks the text up in the commit and prints `makefile: FAIL: ./factory/Makefile is missing` for a file that is there. The feature acceptance of 2026-11-17 saw both in its smoke test. The reviewer of F0062-S0010 had named the hole first. After this story, a `make_file` that is not in its plain form is a fault of the pipeline definition. The fault names the plain spelling, so the definition, the take, the sync and the check all read one path. A `make_file` in its plain form behaves as before. The records contract's schema does not change, because the rule is a load-time rule and not the pattern of `MakeFilePath`.

## Interface

`factory.pipeline.domain.pipeline_definition` (domain): `_make_file_faults` gains one rule. When `make_file` is inside the checkout and `posixpath.normpath(make_file) != make_file`, the fault is:

```text
make_file <value> must be written as <posixpath.normpath(value)>
```

- `./factory/Makefile` gives `make_file ./factory/Makefile must be written as factory/Makefile`.
- `factory//Makefile` gives `make_file factory//Makefile must be written as factory/Makefile`.
- `factory/./Makefile` gives `make_file factory/./Makefile must be written as factory/Makefile`.
- `factory/Makefile/` gives `make_file factory/Makefile/ must be written as factory/Makefile`.
- `Makefile`, `factory/Makefile` and `build/factory.mk` give no fault, as before.
- The existing fault for a path outside the checkout stays as it is. A value outside the checkout gets that fault only, not both.

`MakeFilePath`, `protected_paths`, the take and the conformance check do not change. They receive only plain paths once the definition refuses the others.

Tests: a new test in `tests/pipeline/domain/test_pipeline_definition_make_file.py`, beside the earlier ones, which stay unchanged. A row for the conformance check goes in the tests of `factory.entry.check_project` or `factory.pipeline.application.project_check` that the tester picks.

## Acceptance criteria

1. A definition whose `make_file` is `./factory/Makefile`, `factory//Makefile`, `factory/./Makefile` or `factory/Makefile/` is refused, each with exactly the fault the Interface names. `Makefile`, `factory/Makefile` and `build/factory.mk` are accepted.
2. A definition whose `make_file` is `../Makefile` has the fault `make_file ../Makefile must be a path inside the checkout` and no fault saying `must be written as`.
3. `factory-check-project` on a committed project whose definition names `make_file: ./factory/Makefile` prints a `pipeline definition: FAIL:` line holding `make_file ./factory/Makefile must be written as factory/Makefile`. It never prints `./factory/Makefile is missing`, and its last line starts with `project: not ready`. The same project with `make_file: factory/Makefile` prints `pipeline definition: ok`.
4. `src/factory/contract/pipeline-definition.schema.json` is unchanged by this story.
5. `make check` stays green.
6. docs: `docs/operator-guide/pipeline.md`, *Name the makefile*, names the rule and its fault, with `./factory/Makefile` among the refused values. The project guide's page on the pipeline definition names the rule beside the existing `make_file` rules.

## Smoke test

```bash
sed 's|^# make_file: factory/Makefile|make_file: ./factory/Makefile|' operator/kit/factory/pipeline.full.yml | uv run python -c "import sys; from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader as R; print(R().parse(sys.stdin.read()).make_file)" 2>&1 | tail -1
```
Expect: the last line is the `PipelineDefinitionInvalid` error, holding `make_file ./factory/Makefile must be written as factory/Makefile`. Today, this line prints `./factory/Makefile`.

```bash
sed 's|^# make_file: factory/Makefile|make_file: factory/Makefile|' operator/kit/factory/pipeline.full.yml | uv run python -c "import sys; from factory.pipeline.adapters.pipeline_yaml import RuamelPipelineDefinitionReader as R; print(R().parse(sys.stdin.read()).make_file)" 2>&1 | tail -1
```
Expect: `factory/Makefile`

```bash
uv run pytest tests/pipeline/domain/test_pipeline_definition_make_file.py 2>&1 | tail -1
```
Expect: one line ending with `passed` and a time, with no `failed`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: 1. The third smoke test cannot meet its `Expect:`. `pyproject.toml` already sets `addopts = "-q --strict-markers -p no:cacheprovider"`, so `uv run pytest -q tests/pipeline/domain/test_pipeline_definition_make_file.py` runs at `-qq`, and at that level pytest prints no summary line. I ran it on `develop`'s code: the last line is `...............                                                          [100%]`, not `15 passed in 0.03s`. The same command without `-q` ends with `15 passed in 0.03s`. Options: (a) remove the `-q` from the command and keep the `Expect:` as it is (my choice); (b) keep `-q` and change the `Expect:` to a line of dots ending in `[100%]` with no `F` or `E`, which is weaker.

   The rest of the story looks ready to build:
   - Interface: it names `_make_file_faults` in `factory.pipeline.domain.pipeline_definition` (currently at line 274) and the exact text of the fault. The rule that a value outside the checkout gets only that fault matches how the current function returns early.
   - Criteria: each one is testable. Criterion 1 covers both sides of the rule, and criterion 2 covers the case outside the checkout. The test modules it names exist: `tests/pipeline/domain/test_pipeline_definition_make_file.py`, `tests/entry/test_check_project.py` and `tests/pipeline/application/test_project_check_make_file.py`.
   - Smoke tests 1 and 2: the `sed` pattern matches line 9 of `operator/kit/factory/pipeline.full.yml`, and each `Expect:` can be checked against the output.
   - Docs criterion: it says what the reader must know and dictates no sentences.
   - Architecture: the change is a load-time rule in the domain layer, and the schema does not change.
   - Scope: within F0062 and not in its out-of-scope list.
4. 2026-11-17 human: (a): remove the `-q` from the command and keep the `Expect:` as it is.
5. factory: started intake as self.
6. intake: accepted
   - Human's answer carried in: following journal entry 4, option (a), I removed the `-q` from the third smoke test's command. It now reads `uv run pytest tests/pipeline/domain/test_pipeline_definition_make_file.py 2>&1 | tail -1`. Its `Expect:` is unchanged. Nothing else in the story was edited.
   - Interface: it names `_make_file_faults` in `factory.pipeline.domain.pipeline_definition` and gives the exact fault text, `make_file <value> must be written as <posixpath.normpath(value)>`. It lists the inputs the rule refuses and the ones it accepts. A value outside the checkout keeps its fault alone, which matches how the current function already returns early. `MakeFilePath`, `protected_paths`, the take and the conformance check are named as unchanged.
   - Criteria: each one is testable. Criterion 1 covers both sides of the plain-form rule, with the four refused spellings and the three accepted ones. Criterion 2 covers the outside-the-checkout case and checks that no "must be written as" fault is added. Criterion 3 covers `factory-check-project` on both sides: the FAIL line, no "is missing" line, the `project: not ready` last line, and `ok` for the plain form. Criterion 4 pins the schema as unchanged. `make check` and `docs:` are the last two criteria.
   - Smoke test: smoke tests 1 and 2 run the reader on `operator/kit/factory/pipeline.full.yml` after a `sed` edit. That `sed` pattern matches its line 9, and each `Expect:` is a concrete line to compare with the output. `pyproject.toml` already sets `addopts = "-q ..."`, so with `-q` removed the third smoke test ends with pytest's summary line, which its `Expect:` checks.
   - Docs criterion: it names what the reader must know, in `docs/operator-guide/pipeline.md` under *Name the makefile* and on the project guide's page about the pipeline definition. It dictates no sentences.
   - Architecture: the change is a load-time rule in the pipeline area's domain layer, a pure function with no I/O. No new dependency, and the records contract does not change.
   - Scope: within F0062 (projects start from a kit) and not in its out-of-scope list. It closes a gap that the feature acceptance of 2026-11-17 found in its smoke test.
   - Route: tests. The Interface changes `src/factory`, which the documenter may not write.
7. factory: started tests as self.
8. tester: Wrote the tests for every criterion. `make test` is red for the right reason: the four plain-form rows get `assert None == 'make_file … must be written as factory/Makefile'`, because the definition still accepts them. `make lint` is green. I skipped the type check, as the stage says.

   - criterion 1: `tests/pipeline/domain/test_pipeline_definition_make_file.py::test_a_make_file_not_in_its_plain_form_is_refused_with_its_plain_spelling`. The rows `dot-slash`, `double-slash`, `dot-inside` and `trailing-slash` check the exact fault. The rows `root-makefile`, `factory-makefile` and `mk-file` check that the value is accepted.
   - criterion 2: the same test, row `outside-the-checkout`. It checks that the whole fault equals `make_file ../Makefile must be a path inside the checkout`, so a `must be written as` fault would fail it.
   - criterion 3: `tests/entry/test_check_project.py::test_main_refuses_a_make_file_not_in_its_plain_form`, rows `not-plain` and `plain`. It runs `main` on a committed project that holds `factory/Makefile`.
     - `not-plain` expects a line starting `pipeline definition: FAIL: make_file ./factory/Makefile must be written as factory/Makefile`, no line with `./factory/Makefile is missing`, and a last line starting with `project: not ready`.
     - `plain` expects `pipeline definition: ok`, and also expects the last line to start with `project: ready`.
   - criterion 4: no new test. The existing `tests/entry/test_contract.py::test_the_committed_schemas_are_the_generated_ones` keeps the committed schema equal to the generated one. That `pipeline-definition.schema.json` itself is unchanged is a matter of the diff, for the reviewer to check.
   - criterion 5: `make check`, run by the coder.
   - criterion 6: docs, for the documenter stage.

   Files changed:
   - `tests/pipeline/domain/test_pipeline_definition_make_file.py`: one new test appended. The earlier tests there are unchanged.
   - `tests/entry/test_check_project.py`: one new test appended. Its imports gain `PIPELINE_YAML` and `READY_MAKEFILE`, and the earlier tests are unchanged.

   No created files, and every module the test run needed imported.

   `lint`: lint: green (0.1 s)
9. factory: started doing as self.
10. coder: Built the plain-form rule for `make_file`. All tests pass, and `make check` ends with `check: green`. `make guides` is green too.

    - What I changed: `_make_file_faults` in `src/factory/pipeline/domain/pipeline_definition.py`. It now imports `posixpath`.
      - A value outside the checkout still gets only `make_file <value> must be a path inside the checkout`, and the function returns there.
      - A value inside the checkout whose `posixpath.normpath` differs from the text gets `make_file <value> must be written as <plain>`.
      - A comment gives the reason: the take and the conformance check compare the text as written.
    - Test runs:
      - The tester's two files (`tests/pipeline/domain/test_pipeline_definition_make_file.py`, `tests/entry/test_check_project.py`) failed in 5 rows at first. All of them pass now.
      - Smoke test 1 by hand: its last line is `PipelineDefinitionInvalid: make_file ./factory/Makefile must be written as factory/Makefile`.
    - Main choice: I added the rule to the existing function, so a value outside the checkout keeps exactly one fault. I rejected a separate rule in `_RULES`: an outside value such as `./../Makefile` would then get both faults, which criterion 2 does not allow.
    - `MakeFilePath`, `protected_paths`, the take, the conformance check and the records contract are unchanged. `git status` shows only the one source file, so `pipeline-definition.schema.json` is untouched.
    - Refactor: I read the diff and found nothing to change.
    - The journal did not change the meaning of the task beyond the smoke-test command, which intake already fixed, so I left the Description as it is.
    - Noticed but not touched: the docs criterion (operator guide *Name the makefile* and the project guide's pipeline-definition page) is the documenter's.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
11. factory: started review as self.
