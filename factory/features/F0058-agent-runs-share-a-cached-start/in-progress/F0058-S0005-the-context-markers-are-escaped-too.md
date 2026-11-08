---
stage: approval
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 664
comments_read: [6722586434]
handed_over: approval
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T14:09:47.644057Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T14:09:47.652185Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T14:10:11.228703Z'
  stage: intake
  run: 0026dc1e87944dcbb905fe9a60d86f85
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T14:10:16.083740Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-08T14:10:52.109212Z'
  stage: tests
  run: 1b55a7e8917b43899d2250ba7d83bec7
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T14:10:57.265068Z'
  stage: doing
- number: 7
  speaker: coder
  kind: question
  at: '2026-11-08T14:13:30.500366Z'
  stage: doing
  run: b69aab1718194d759776f186d5fababc
  blocked: question
- number: 8
  speaker: human
  kind: comment
  at: '2026-11-08T14:17:19.530739Z'
  stage: doing
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T14:17:21.917900Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-08T14:17:37.809169Z'
  stage: doing
  run: c617e1bf6f8f48199b4d9591ec29fa11
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-08T14:17:43.006578Z'
  stage: tests
- number: 12
  speaker: tester
  kind: result
  at: '2026-11-08T14:18:03.390205Z'
  stage: tests
  run: 43b6f83563b4486bbeb7baca7cbc446f
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-08T14:18:08.602814Z'
  stage: doing
- number: 14
  speaker: coder
  kind: result
  at: '2026-11-08T14:23:18.906112Z'
  stage: doing
  run: 3d844aca03104fbe93d1349dc3072987
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-08T14:23:23.944600Z'
  stage: review
- number: 16
  speaker: reviewer
  kind: result
  at: '2026-11-08T14:24:19.487014Z'
  stage: review
  run: 2ab3c60d76694b1ab42300f8a169da50
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-08T14:24:26.758444Z'
  stage: doing
- number: 18
  speaker: coder
  kind: result
  at: '2026-11-08T14:24:41.723326Z'
  stage: doing
  run: ffcf1f4181344202b329e92f9380926b
- number: 19
  speaker: factory
  kind: started
  at: '2026-11-08T14:24:46.719321Z'
  stage: tests
- number: 20
  speaker: tester
  kind: result
  at: '2026-11-08T14:25:31.015301Z'
  stage: tests
  run: 658d089091cc4d7891255a0fac2ad067
- number: 21
  speaker: factory
  kind: started
  at: '2026-11-08T14:25:36.133642Z'
  stage: doing
- number: 22
  speaker: coder
  kind: result
  at: '2026-11-08T14:29:47.154435Z'
  stage: doing
  run: e28dc69e6f7645df88b3440b00abf27f
- number: 23
  speaker: factory
  kind: started
  at: '2026-11-08T14:29:52.418762Z'
  stage: review
- number: 24
  speaker: reviewer
  kind: result
  at: '2026-11-08T14:30:31.321487Z'
  stage: review
  run: 8e4ed249d6e742a390921cb4f3075272
- number: 25
  speaker: factory
  kind: started
  at: '2026-11-08T14:30:36.485427Z'
  stage: docs
- number: 26
  speaker: documenter
  kind: result
  at: '2026-11-08T14:35:16.202272Z'
  stage: docs
  run: 9199b7e239fc423094b20a8d66a5485a
- number: 27
  speaker: factory
  kind: started
  at: '2026-11-08T14:35:21.271780Z'
  stage: smoke-test
- number: 28
  speaker: smoke-tester
  kind: result
  at: '2026-11-08T14:35:37.377601Z'
  stage: smoke-test
  run: 491c36930e8346f7a80d6c69507b6927
---

# The context markers are escaped too

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

The first message escapes four marker texts inside the work item's body and inside a start fact's output (`<work-item`, `</work-item>`, `<role-instructions`, `</role-instructions>`), so that only the blocks the factory writes count. The `<context>` blocks came after that rule, and their own markers are not escaped. A start fact's output that holds `</context>` closes its block early: a reviewer's diff of `src/factory/agents/domain/prompts.py` holds `CONTEXT_CLOSE = "</context>"`, so the message then shows three `</context>` lines for two blocks. A work item's body that holds `<context name="...">`, as this feature's stories do, shows the agent what looks like a start fact inside the work item. After this story, `<context` and `</context>` are escaped like the other four, in the body and in every start fact's text, its failure line included. The role's instructions stay unescaped, and a text without any marker reaches the message byte for byte, as today. No other part of the message changes.

## Interface

- `factory.agents.domain.prompts` (domain): the marker texts that `compose_prompt` escapes are six: `<work-item`, `</work-item>`, `<role-instructions`, `</role-instructions>`, `<context` and `</context>`. The `<` of each becomes `&lt;`, as for the four today.
- The escape applies to the work item's body and to each start fact's text: its output, the line that names a cut, and its `failed: <reason>` line.
- The role's instructions are not escaped.
- `compose_prompt(facts: PromptFacts) -> str` keeps its signature; `PromptFacts` and `StartFact` keep their fields.
- Tests: `tests/agents/domain/test_prompts_context_markers.py`. No earlier test changes; if one pins the list of four markers, the human names it here with its leave before the story starts.

The human's leave for earlier tests: this story may add `<context` and `</context>` to the lists `MARKERS` in `tests/agents/domain/test_prompts.py` and `tests/pipeline/application/test_stage_context.py`, and change the tests that read those lists only as far as the two new markers need, and nothing else.

## Acceptance criteria

1. A start fact whose output holds `<context name="x">`, or `</context>`, gives a message with exactly one `<context name="` opening and one `</context>` closing per start fact; the marker text reaches the message with its `<` as `&lt;` (rows of one test).
2. A work item body that holds `<context name="x">`, or `</context>`, gives a message in which no `<context` opening and no `</context>` stands between `<work-item>` and `</work-item>`; the marker text reaches the message with its `<` as `&lt;` (rows of one test).
3. A start fact whose failure reason holds `</context>` gives a block whose line reads `failed: ` followed by the reason with `&lt;/context>`, and the message holds one `</context>` for that fact.
4. A body and a start fact output without any of the six marker texts reach the message byte for byte (rows of one test).
5. The role's instructions reach the message unescaped, also when they hold `</context>`.
6. A start fact whose output is longer than `CONTEXT_LIMIT` and holds `</context>` in the part kept before the cut gives a block with that marker as `&lt;/context>`, the line that names the cut, and one `</context>` for that fact.
7. `make check` stays green.
8. docs: the project guide's description of the first message (`docs/project-guide/agents.md` and *Start facts* in `docs/project-guide/pipeline.md`) names all six escaped marker texts and why the context markers are among them.

## Smoke test

```bash
uv run python -c "from factory.agents.domain.prompts import PromptFacts, StartFact, compose_prompt; f = PromptFacts(work_item='F0001-S0001', path='p.md', stage='review', allowed_decisions=['docs', 'question'], branch='b', pull_request=1, round=0, body='# T\n', role='reviewer', role_instructions='Go.', start_facts=[StartFact(command='diff', output='x = \"</context>\"\n')]); print(compose_prompt(f).count('</context>'))"
```
Expect: `1`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: concrete. It names `factory.agents.domain.prompts` (domain) and the six marker texts, and says what gets escaped: the body, and each start fact's output, cut line and `failed:` line. The role's instructions stay as they are. `compose_prompt`, `PromptFacts` and `StartFact` keep their signatures and fields. The change goes in `_MARKER_TEXTS` (`src/factory/agents/domain/prompts.py:42`), which `_escape_markers` already applies to the body and to the whole context text (`_context_block`, line 133), cut and failure lines included. Note on reading the story: the first four markers appear as `&lt;...` in my prompt only because the prompt escapes them. The file itself holds `<work-item` and the others.
   - Criteria: each one is testable by a single test function, and they cover both sides. 1 and 2 cover output and body (escaped, with exactly one opening and one closing per block). 3 covers the failure line. 4 covers text without markers, which must reach the message byte for byte. 5 covers the role's instructions, which stay unescaped. `<context` and `</context>` do not overlap as replacements, because `</context>` does not start with `<context`.
   - Smoke test: runnable with `uv run python -c` and the fields `PromptFacts` already has. `Expect: 1` can be checked against the printed count: the output's `</context>` becomes `&lt;/context>`, so only the block's own closing marker is left.
   - Docs criterion (7): it names what the reader must know (all six markers, and why the context markers are among them) and the two files it goes in. It dictates no sentences.
   - Architecture: a pure domain change in the agents area's domain layer. No I/O, no new dependency, no new module apart from the test file.
   - Scope: within F0058 (the shared, cached start and its context blocks), and nothing in its Out of scope. The earlier tests the story touches have the human's leave in the Interface: `MARKERS` in `tests/agents/domain/test_prompts.py:27` and `tests/pipeline/application/test_stage_context.py:36`, plus the tests that read those lists, only as far as the two new markers need.
   - Route: `tests`. The change is in `src/`.
4. factory: started tests as vm.
5. tester: Wrote the tests for the context markers in one new file, tests/agents/domain/test_prompts_context_markers.py.
   - criterion 1: tests/agents/domain/test_prompts_context_markers.py::test_a_context_marker_in_a_start_fact_output_is_escaped. It has one row for `<context name="x">` and one for `</context>`. Two start facts go in, and the test expects exactly two `<context name="` openings, two `</context>` closings, and the marker with `&lt;`.
   - criterion 2: ::test_a_context_marker_in_the_body_is_escaped_and_opens_no_block. Same two rows. The test expects no `<context` and no `</context>` before the work item's closing marker, and the marker escaped inside the body.
   - criterion 3: ::test_a_context_marker_in_a_failure_reason_is_escaped. The test expects the line `failed: it printed &lt;/context> and stopped` and exactly one `</context>` in the message.
   - criterion 4: ::test_a_text_without_a_marker_reaches_the_message_byte_for_byte. It has two rows: plain text, and near-misses (`<context-free>`, `</contexts`, `<div>`, an umlaut). Each row is used as both the body and a start fact's output.
   - criterion 5: ::test_the_role_instructions_reach_the_message_unescaped. The instructions hold `<context name="x">` and `</context>`.
   - criterion 6 is checked by `make check`, which the coder runs. Criterion 7 is for the docs stage.

   Run of the new file (`uv run pytest -q` on that file, as CLAUDE.md says): the five criterion 1–3 tests fail on assertions, because `_MARKER_TEXTS` in src/factory/agents/domain/prompts.py does not yet hold the context markers. The criterion 4 and 5 tests pass already, since they pin today's behaviour, which must stay. Every module imported; there were no collection errors. `make lint` is green.

   I did not use the human's leave to add the two markers to `MARKERS` in tests/agents/domain/test_prompts.py or tests/pipeline/application/test_stage_context.py. The leave allows that change but does not ask for it, and the new file covers every criterion. No earlier test file was changed.

   `lint`: lint: green (0.2 s)
6. factory: started doing as vm.
7. coder: Question: one test contradicts the Interface. Which way should it be fixed?

   What I built: I added `"<context"` and `CONTEXT_CLOSE` to `_MARKER_TEXTS` in `src/factory/agents/domain/prompts.py:42`. `_escape_markers` already applies that tuple to the body and to each start fact's text (output, cut line and `failed:` line), so nothing else needed to change. This change is in the working tree.

   Result of `make check`: everything ran up to `make test`, and that failed on one test. The criterion 1, 2, 3 and 5 tests pass, and so does the `plain` row of criterion 4. The failure:
   `FAILED tests/agents/domain/test_prompts_context_markers.py::test_a_text_without_a_marker_reaches_the_message_byte_for_byte[near] - assert '<work-item>\n# Demo\n\nA <context-free> <div> and </contex...`

   The contradiction: the Interface names the marker text `<context`, a bare prefix like `<work-item` and `<role-instructions`, which are escaped wherever they appear. The `near` row's text `# Demo\n\nA <context-free> <div> and </contexts ümlaut.\n` holds `<context` (inside `<context-free>`). It is not a text "without any of the six marker texts" (criterion 4), so the Interface requires it to become `&lt;context-free>`. The test expects it unchanged. Its other near-misses (`</contexts`, `<div>`, the umlaut) are fine, because none of them holds `</context>` or `<context`.

   Options:
   A. (my choice) Keep the Interface as written. The human gives leave for the tester to replace `<context-free>` in the `near` row with a text that holds no marker, such as `<contex>` or `context-free`. Then I end with `tests`, and the tester makes exactly that change. This matches the existing four markers, which are also escaped as prefixes (`<work-item-x` is escaped today).
   B. Change the Interface so that `<context` counts only when `>` or whitespace follows it, and implement that matcher. I would reject this: it makes one marker behave differently from the other four, and an over-escaped `&lt;context-free>` costs the agent nothing.

   Noticed, not touched: I did not refactor anything; the change is the two added tuple entries.
8. 2026-11-08 human: Answer from the human: A. Keep the Interface: `<context` is escaped as a prefix, like the other markers. Leave for the tester to replace `<context-free>` in the `near` row of `tests/agents/domain/test_prompts_context_markers.py` with a text that holds no marker (such as `context-free`), and nothing else.
9. factory: started doing as vm.
10. coder: The human's answer (entry 8, option A) calls for one test change. In the `near` row of `test_a_text_without_a_marker_reaches_the_message_byte_for_byte` in `tests/agents/domain/test_prompts_context_markers.py`, replace `<context-free>` with a text that holds no marker, such as `context-free`, and change nothing else. The tester makes this change.

    The code is already on the branch from the last run (commit bae1a49ee). `_MARKER_TEXTS` in `src/factory/agents/domain/prompts.py:42` now also holds `"<context"` and `CONTEXT_CLOSE`. I changed no code this run, and the Description stays as it is: the answer keeps the Interface as written, with `<context` escaped as a prefix like the other markers. After the tester's change the work item comes back to doing. Then I run `make check` and do the refactor step.
11. factory: started tests as vm.
12. tester: Made the one test change the human approved in entry 8 (option A). In the `near` row of `test_a_text_without_a_marker_reaches_the_message_byte_for_byte` in `tests/agents/domain/test_prompts_context_markers.py`, I replaced `<context-free>` with `context-free`, so the row's text no longer holds the marker `<context`. The other near-misses are unchanged: `<div>`, `</contexts` and the umlaut. Nothing else changed in the file or in any other test file.

    - criterion 1: tests/agents/domain/test_prompts_context_markers.py::test_a_context_marker_in_a_start_fact_output_is_escaped
    - criterion 2: ::test_a_context_marker_in_the_body_is_escaped_and_opens_no_block
    - criterion 3: ::test_a_context_marker_in_a_failure_reason_is_escaped
    - criterion 4: ::test_a_text_without_a_marker_reaches_the_message_byte_for_byte (the only test changed in this run)
    - criterion 5: ::test_the_role_instructions_reach_the_message_unescaped

    I ran the file once, as CLAUDE.md says (`uv run pytest -q` on it), with the coder's code from commit bae1a49ee on the branch: all 8 tests pass. Every module imported. `make lint` is green.

    `lint`: lint: green (0.2 s)

    `lint`: lint: green (0.2 s)
13. factory: started doing as vm.
14. coder: The tester changed the `near` row (entry 12), and `make check` is now green. It ends with `test: green (115.9 s)` and `check: green`, with total coverage at 99.21 %.

    What I built: `_MARKER_TEXTS` in `src/factory/agents/domain/prompts.py:42` now also holds `"<context"` and `CONTEXT_CLOSE`. That change was made in an earlier run and is already on the branch (bae1a49ee). `_escape_markers` already applies the tuple to the work item's body and to each start fact's text (its output, the cut line and the `failed:` line), so no other code changed. The role's instructions are still not escaped. I changed no code in this run.

    Main choice: `<context` is escaped as a bare prefix, like `<work-item` and `<role-instructions`, as the human confirmed in entry 8 (option A). Rejected: a matcher that escapes `<context` only when `>` or whitespace follows it. It would make one marker behave differently from the other four.

    Refactor: I read the diff again (two tuple entries). Nothing needs changing.

    Description: the journal did not change what the task means. The human's answer kept the Interface as written, so the Description stays as it is.

    Noticed, not touched: nothing.

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
15. factory: started review as vm.
16. reviewer: Findings:

    1. criterion 6 added: it needs its test. The Interface says the escape applies to "the line that names a cut", and no criterion or test covers the cut path. The code handles it: `_context_block` (`src/factory/agents/domain/prompts.py:137`) escapes the whole text that `_cut` returns. Every test in `tests/agents/domain/test_prompts_context_markers.py` uses an output shorter than `CONTEXT_LIMIT`. Fix: the tester adds a test for the new criterion 6, an output longer than `CONTEXT_LIMIT` that holds `</context>` before the cut. The test expects `&lt;/context>`, the cut line, and one `</context>` for that fact. The old criteria 6 (`make check`) and 7 (docs) are now 7 and 8.
    2. `tests/agents/domain/test_prompts_context_markers.py:16-31`: `VALID` and `_facts` copy `VALID` and `_facts` from `tests/agents/domain/test_prompts.py:29-52`. A shared base already exists in `tests/support/first_message_support.py` (`CODER_FACTS`). Fix: the tester builds the facts from `CODER_FACTS` (for example `CODER_FACTS.model_copy(update=...)`), or moves `VALID`/`_facts` into `tests/support/first_message_support.py` under the standing leave and has both test files use them from there.

    Checked and fine:
    - Code: `_MARKER_TEXTS` (`src/factory/agents/domain/prompts.py:42-49`) now holds six markers, and `_escape_markers` applies them to the body and to the whole context text (output, cut line, `failed:` line). The role's instructions go through `_block` unescaped.
    - Overlaps: `<context` cannot match inside `</context>`, and an `&lt;` that is already escaped is never matched again.
    - Criteria 1–5 each have a test that checks what they name, with parametrized rows where the criterion asks for them.
    - The coder's `make check` was green (entry 14).
    - Architecture: domain-only change, no I/O, no markers that silence a check.
    - The Description and the docs criterion match what was built. Entry 7 and the human's answer in entry 8 record the main choice (`<context` escaped as a prefix) and the rejected matcher.

    Earlier tests: none changed. The diff only adds `tests/agents/domain/test_prompts_context_markers.py`, and the leave to edit `MARKERS` in the two earlier test files was not used.
17. factory: started doing as vm.
18. coder: Both review findings (entry 16) need changes to tests only, so I changed no code and am handing the work item to the tester.

    - New criterion 6 needs only its test. The code already covers it: `_context_block` in `src/factory/agents/domain/prompts.py` escapes the whole text that `_cut` returns, cut line included. The tester should add a test to `tests/agents/domain/test_prompts_context_markers.py` for it. The start fact's output is longer than `CONTEXT_LIMIT` and holds `</context>` before the cut. The test expects `&lt;/context>`, the line that names the cut, and one `</context>` for that fact.
    - The copied helper falls under the standing leave in CLAUDE.md for moving a shared test helper. `VALID` and `_facts` in `tests/agents/domain/test_prompts_context_markers.py:16-31` copy `VALID` and `_facts` from `tests/agents/domain/test_prompts.py:29-52`. The tester should either build the facts from `CODER_FACTS` in `tests/support/first_message_support.py`, or move `VALID`/`_facts` into that module and have both test files import them from there. If they move them, every earlier test keeps its name and checks the same thing, and the entry names `tests/agents/domain/test_prompts.py` as changed.

    What is built: `_MARKER_TEXTS` in `src/factory/agents/domain/prompts.py:42` holds `"<context"` and `CONTEXT_CLOSE`. This was done in an earlier run and is on the branch (bae1a49ee). The coder's last `make check` was green (entry 14).

    Description: the reviewer already added criterion 6, and the journal changed nothing else about the task, so the Description stays as it is.

    Noticed, not touched: nothing.
19. factory: started tests as vm.
20. tester: Made the two test changes the coder named in entry 18, both from the review findings in entry 16. All the changes are in `tests/agents/domain/test_prompts_context_markers.py`. I changed no other test file.

    - New criterion 6: added `test_a_context_marker_before_the_cut_is_escaped`. Its start fact's output is longer than `CONTEXT_LIMIT` (by 5 characters) and holds `</context>` in the part kept before the cut. The test expects `&lt;/context>` in the message, a line starting with `[5 more characters cut here`, and exactly one `</context>`.
    - Copied helper (finding 2): I took the first option the finding offered. I removed the file's own `VALID` dict, and `_facts` now builds the facts from `CODER_FACTS` in `tests/support/first_message_support.py` with `model_copy(update=...)`. It changes only the body, the start facts and the role's instructions. Moving the helper was not needed, so `tests/agents/domain/test_prompts.py` and the support module are unchanged. The unused `BODY` and `INSTRUCTIONS` constants and the `typing.Any` import are gone. Every existing test keeps its name and checks the same thing.

    Criterion map:
    - criterion 1: tests/agents/domain/test_prompts_context_markers.py::test_a_context_marker_in_a_start_fact_output_is_escaped
    - criterion 2: ::test_a_context_marker_in_the_body_is_escaped_and_opens_no_block
    - criterion 3: ::test_a_context_marker_in_a_failure_reason_is_escaped
    - criterion 4: ::test_a_text_without_a_marker_reaches_the_message_byte_for_byte
    - criterion 5: ::test_the_role_instructions_reach_the_message_unescaped
    - criterion 6: ::test_a_context_marker_before_the_cut_is_escaped (new)
    - criterion 7 is the coder's `make check`; criterion 8 is for the docs stage.

    Run of the file (`uv run pytest -q` on it, as CLAUDE.md says): all 9 tests pass against the coder's code on the branch. The code already covers the cut path, so the new test is green from the start. Every module imported. `make lint` is green.

    Files created: none (the file was already there; I edited it).

    `lint`: lint: green (0.2 s)
21. factory: started doing as vm.
22. coder: The tester made both changes from the review (entry 20), and `make check` is green again. It ends with `test: green (109.8 s)` and `check: green`, with total coverage at 99.21 %.

    What I built: `_MARKER_TEXTS` in `src/factory/agents/domain/prompts.py:42` now also holds `"<context"` and `CONTEXT_CLOSE`. That change is already on the branch from an earlier run (bae1a49ee). `_escape_markers` applies the tuple to the body and to each start fact's whole text: its output, the cut line and the `failed:` line. The new criterion 6, the cut path, is therefore covered without any code change. I changed no code in this run.

    Main choice: `<context` is escaped as a bare prefix, like the other markers, as the human decided in entry 8. Rejected: a matcher that escapes it only when `>` or whitespace follows.

    Refactor: I read the diff again. It is two tuple entries, and nothing needs changing.

    Description: the reviewer's added criterion 6 is already in it. The journal changed nothing else, so the Description stays as it is.

    Noticed, not touched: nothing.

    `check`: check: green

    `check`: check: green
    `duplicates`: duplicates: 7 new, 39 known, 4 gone
23. factory: started review as vm.
24. reviewer: no findings

    Checked and fine:
    - Code: `_MARKER_TEXTS` (`src/factory/agents/domain/prompts.py:42-49`) holds six markers. `_escape_markers` applies them to the body (`compose_prompt`, line 170) and to the whole text `_context_text` returns (`_context_block`, line 140): the output, the cut line from `_cut` and the `failed: <reason>` line. The role's instructions go through `_block` unescaped (line 172). The escape runs after the cut, so a marker in the kept part is escaped, and a marker split by the cut is left as harmless partial text. `<context` cannot match inside `</context>`, and an `&lt;` that is already escaped is never matched again. `compose_prompt`, `PromptFacts` and `StartFact` keep their signatures and fields. The docstring of `compose_prompt` says "its marker texts escaped" without counting them, so it is still true.
    - Criteria 1–6, each against its test in `tests/agents/domain/test_prompts_context_markers.py`:
      - 1: two start facts, with `<context name="x">` and `</context>` as rows. The test checks one opening and one closing per fact, plus the escaped text.
      - 2: the same rows for the body. The test checks that no `<context` and no `</context>` stands before `&lt;/work-item>`, which is stricter than "between the two markers" because the work item block comes first. It also checks the escaped text.
      - 3: checks the exact `failed: … &lt;/context> …` line and one `</context>`.
      - 4: rows `near` and `plain`, each used as the body and as an output. The test checks both byte for byte inside their blocks. The `near` row holds none of the six markers, as the human's answer in entry 8 asks.
      - 5: instructions that hold both markers reach the message unescaped.
      - 6: an output 5 characters over `CONTEXT_LIMIT` with `</context>` in the kept part. The test checks the escaped marker, the `[5 more characters cut here` line and one `</context>`.
      - Each rule's both sides (escaped vs. byte for byte, escaped vs. unescaped role) are covered as rows or by their own criterion. The tester's run passed (entry 20), and the coder's `make check` after it was green (entry 22: `check: green`, coverage 99.21 %).
    - Architecture: the change is domain-only. It adds no I/O, no dependency and no new module under `src/`, and the test mirrors the package under `tests/agents/domain/`.
    - Security: no markers that silence a check, no secrets. The change makes the prompt's block boundaries harder to forge from data, which is what it is for.
    - Quality: two tuple entries reuse the existing `CONTEXT_CLOSE`, with no duplicate logic. The test builds its facts from `CODER_FACTS` in `tests/support/first_message_support.py`, so the copied helper from round 0 is gone.
    - Work item hygiene: the main choice (`<context` escaped as a prefix) and the rejected matcher are in entries 7, 8 and 14. The Description matches what was built. Docs criterion 8 names the two guide files, the six markers and the reason.
    - Smoke test: the output's `</context>` becomes `&lt;/context>`, so only the block's own closing marker is left and the count is 1.

    Earlier tests: none changed. The diff only adds `tests/agents/domain/test_prompts_context_markers.py`, so no leave was needed. The leave to edit `MARKERS` in `tests/agents/domain/test_prompts.py` and `tests/pipeline/application/test_stage_context.py` was not used.
25. factory: started docs as vm.
26. documenter: Updated the project guide so that it names all six escaped marker texts (docs criterion 8).

    Files changed:
    - `docs/project-guide/agents.md`, *The system prompt and the first message*: the escape bullet now lists all six marker texts (`<work-item`, `</work-item>`, `<role-instructions`, `</role-instructions>`, `<context`, `</context>`). It says the same escape applies to every start fact's text, and says why the context markers are among them: an output holding `</context>` (a diff of `prompts.py`) would close its block early, and a body holding `<context name="...">` would look like a start fact inside the work item. It also says that each text is escaped as a prefix (`<context-free>` too, as the human decided in entry 8), that a text without any of the six reaches the message byte for byte, and that the role's instructions stay unescaped.
    - `docs/project-guide/pipeline.md`, *The first message*: step 1 said "four marker texts". It now says six and points to the list in agents.md.
    - `docs/project-guide/pipeline.md`, *Start facts*: replaced the stale bullet "`<context` and `</context>` are not among them". It now says each block's whole text, the cut line and the `failed:` line included, has the six texts escaped, gives the reason, and says the escape runs after the cut. I checked this against `_context_block` and `_MARKER_TEXTS` in `src/factory/agents/domain/prompts.py`.

    `make documents`: documents ok (59.8 s). I changed only documents, so I did not run `make check`. The factory's checks decide.

    Cross-read and found current: the rest of `docs/project-guide/agents.md` (the system prompt text, the context block bullet at line 34) and the rest of `docs/project-guide/pipeline.md` (the context key, the lease, `CONTEXT_LIMIT` and the cut line, the `failed:` reasons). I grepped `README.md`, `docs/operator-guide/` and `docs/decisions.md` for the escape and the markers and found nothing that describes the marker list. I added no entry to the decision log, because the story asks for none.

    Stale text not mine to fix: none seen.

    `check`: check: green
    `secrets`: secrets: green (1.1 s)
    `documents`: documents ok (60.2 s)
27. factory: started smoke-test as vm.
28. smoke-tester: I ran the smoke test once, as written, from the repository root.

    Command 1 (`uv run python -c "... print(compose_prompt(f).count('</context>'))"`):
    ```
    Bytecode compiled 4164 files in 86ms
    1
    ```
    It met its `Expect: 1` line. The first line is uv's own bytecode notice, not output from the program. The program printed `1`. So the start fact's output `x = "</context>"` no longer closes its block early: only the block's own `</context>` is left in the message, and the marker in the output must have been escaped.

    Against the acceptance criteria: the smoke test contradicts none of them. It touches criterion 1 (one `</context>` per start fact), and its result agrees. Criteria 2–6 have their own tests in `tests/agents/domain/test_prompts_context_markers.py`. The coder's `make check` was green and the factory's check after the docs stage was green (criterion 7). The documenter covered the docs criterion (8) in entry 26.

    Findings: none.
