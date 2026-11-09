# Agent texts are not frozen by checksums

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

Three tests pin the shipped agent texts as they stood before an earlier story: `test_every_agent_file_keeps_its_own_sections_word_for_word_in_order` compares a crc32 of every agent file's opening and sections with `PARTS_BEFORE`, `test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word` compares the shared rules paragraph by paragraph with `RULES_BEFORE`, and `test_the_rest_of_the_reviewer_body_is_unchanged` rebuilds an earlier reviewer body by a growing chain of `.replace` calls and compares its crc32. Each was the right check for the one story that moved or added text; on `develop` they freeze every word of every agent file and of the rules, so each later story that changes an agent text stops for the human's leave to update a checksum: in F0060, four of the six questions the human answered were such leaves (S0002 entry 7, S0003 entries 3, 10 and 15). After this story no test pins an agent file or the system prompt by a checksum or by its whole earlier text; the checks of structure stay (each agent file's headings in order, R1 to R15 once each and in order, `SYSTEM_PROMPT` equal to the file, no rules in an agent file), and so do the tests that pin a single rule or sentence that a story's criterion asked for. No code and no agent text changes.

## Interface

- `tests/agent_files/test_shared_rules_system_prompt.py`: `test_every_agent_file_keeps_its_own_sections_word_for_word_in_order` becomes `test_every_agent_file_has_its_sections_in_order` and checks only the headings (`## Role` where present, `## Stage`, `## Lessons`); `test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word` is removed. Every other test of the module stays as it is.
- `tests/agent_files/test_claude_agent_texts_review_groups.py`: `test_the_rest_of_the_reviewer_body_is_unchanged` and `_EARLIER_BODY_CRC32` are removed; the other tests of the module stay.
- `tests/support/shared_rules_support.py`: `PARTS_BEFORE`, `own_parts`, `RULES_BEFORE` and `OLD_PLACE_SENTENCE` are removed when no test uses them any longer.
- New guard `tests/guards/test_agent_texts_not_frozen.py`, with one helper:

```python
def frozen_modules(root: Path) -> list[Path]: ...
```

  - `frozen_modules` lists, sorted, every `*.py` file under `root` whose text names `crc32`; the guard's own module is never listed.
- The leave (to be given by the human when refining this story; proposed words): "the tests that pin a shipped agent file or `agents/system-prompt.md` by a checksum or by its whole text from before a story (`test_every_agent_file_keeps_its_own_sections_word_for_word_in_order`, `test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word`, `test_the_rest_of_the_reviewer_body_is_unchanged`) lose that check as the Interface says, and the support data only they used is removed."

## Acceptance criteria

1. `frozen_modules` on a folder holding a module that names `crc32` lists it, on a folder whose modules do not name it lists nothing, and on `tests/` of the repository lists nothing: rows of one parametrized test.
2. `test_every_agent_file_has_its_sections_in_order` passes on each shipped agent file, and the same check fails on a body whose `## Lessons` stands before `## Stage`: rows of one parametrized test.
3. `tests/support/shared_rules_support.py` defines none of `PARTS_BEFORE`, `own_parts`, `RULES_BEFORE`, `OLD_PLACE_SENTENCE`.
4. `make check` stays green.
5. docs: the project guide's file on the agents area (`docs/project-guide/agents.md`, where it lists what `test_shared_rules_system_prompt.py` checks) says what the test checks now, and that no test pins an agent text by a checksum, so a story that changes an agent text updates only the tests that read the sentences it changes.

## Smoke test

```bash
grep -rl crc32 tests/ --include='*.py' | grep -v test_agent_texts_not_frozen
```
Expect: no output.

```bash
uv run pytest tests/guards/test_agent_texts_not_frozen.py tests/agent_files/test_shared_rules_system_prompt.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal
