# A `make_file` is written in its plain form, or the definition refuses it

<!-- proposed by feature acceptance of 2026-11-17; refine before starting -->

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
uv run pytest -q tests/pipeline/domain/test_pipeline_definition_make_file.py 2>&1 | tail -1
```
Expect: one line ending with `passed` and a time, with no `failed`.

## Journal
