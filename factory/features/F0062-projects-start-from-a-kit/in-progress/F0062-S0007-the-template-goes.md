# The template goes

## Description

With the kit and the stack packs in place, `operator/template/` is a second, older copy of the same things: its pipeline definition is the kit's full line, its `Makefile` is the Python pack's with the kit's part still inside, and its `CLAUDE.md` is the kit's skeleton with the Python pack's sections. Two copies drift. After this story the template is gone: its three files are removed, and every test and every shipped text that read them reads the kit or the Python pack instead. Nothing a project gets changes, since the kit and the packs already hold it, and no module under `src/factory/` reads the template. The documents that still name the template are the documenter's part of this story; `demo/todo-service/README.md` is the human's.

## Interface

- Removed: `operator/template/CLAUDE.md`, `operator/template/Makefile`, `operator/template/factory/pipeline.yml`, and with them the folder.
- Where a shipped file under `agents/`, `operator/` or `src/` names `operator/template`, the coder names the kit or the pack that now holds the thing; a sentence that is only about the template goes.
- What replaces each file for a reader: the pipeline definition is `operator/kit/factory/pipeline.full.yml`; the makefile is `operator/packs/python/Makefile` together with `operator/kit/factory/kit.mk` (the shell settings, `$(start)`, `$(green)` and the start facts are in `kit.mk`, the targets in the pack's makefile); `CLAUDE.md` is `operator/kit/CLAUDE.md`, with the Python sections in `operator/packs/python/CLAUDE.sections.md`.
- Tests: `tests/guards/test_template_removed.py`, new. `feature.md` gives this leave (decision 25): "S0007 may change every earlier test and test helper that reads a file under `operator/template/`, or that pins that folder's name, so that it reads the kit or the Python pack instead: each test keeps its name and checks the same thing at the new place. Where the thing a test checks is now split between `kit.mk` and the pack's makefile, the test reads both, or an assembled makefile from `tests/support/kit_support.py`. A test whose only subject was that the template exists or lists its files is changed to check the same of the kit and the Python pack. The tester names every changed file in its entry."

## Acceptance criteria

1. `operator/template` does not exist, and no tracked file under `src/`, `agents/`, `operator/` or `tests/` holds the text `operator/template`, except the new guard itself and the guard of the removed root folders, which may name it as a folder that must not exist.
2. Every earlier test that read the template passes at its new place, and none of them was deleted: the names of the test functions in the changed files are the names they had, compared in the tester's entry.
3. The checks of the Python makefile that earlier tests made on the template (its header, its `sync`, its `secrets` recipe beside the demo's, its `mutants`, its pins) hold for `operator/packs/python/Makefile` with `kit.mk`.
4. The checks of the template's pipeline definition (valid with the shipped roles, its tool paths, the working branch in its texts) hold for both pipeline definitions of the kit, the thin line included where the check does not depend on the seven roles.
5. `make check` stays green.
6. docs: `README.md`, the operator guide, the project guide and `docs/decisions.md` name the kit and the packs wherever they named the template as the start of a project, and no document tells a reader to copy `operator/template/`; `operator/README.md` has no entry for the template; `docs/decisions.md` records that the template was removed on this date because the kit and the Python pack hold everything it held. An older entry of the decision log that tells history keeps its words.

## Smoke test

```bash
test ! -e operator/template && echo gone
git grep -l 'operator/template' -- src agents operator tests | grep -v -e 'tests/guards/test_template_removed.py' -e 'tests/guards/test_root_operator_folders_removed.py' | wc -l
```
Expect: `gone`, then `0`.

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
p="$d/p"; git init -q "$p"; mkdir -p "$p/src" "$p/tests" "$p/docs"
cp -r operator/kit/factory "$p/factory"; cp operator/kit/CLAUDE.md "$p/"
mv "$p/factory/pipeline.full.yml" "$p/factory/pipeline.yml"; rm "$p/factory/pipeline.thin.yml"
cp operator/packs/python/Makefile "$p/Makefile"
touch "$p/src/a" "$p/tests/a" "$p/docs/a" "$p/README.md"
git -C "$p" add -A; git -C "$p" -c user.name=t -c user.email=t@example.com commit -q -m one
uv run python -m factory.entry.check_project --agent-home agents "$p" | tail -1
```
Expect: `project: ready`.

```bash
uv run pytest tests/guards/test_template_removed.py tests/agent_files/
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal
