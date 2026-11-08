---
stage: docs
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 659
comments_read: [6720500729, 6720585535, 6720667293]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T10:42:00.039045Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T10:42:00.046925Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T10:42:16.102298Z'
  stage: intake
  run: ef6a83a45f83442b91a5a7273813c5ae
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T10:46:05.246265Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T10:46:07.615751Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T10:46:24.851541Z'
  stage: intake
  run: 734c7f7de2b54a51aaefde992fbd6480
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T10:46:29.787251Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T10:48:57.214337Z'
  stage: tests
  run: 4c6da60ae0044da8970b9f09db42c606
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T10:49:02.487923Z'
  stage: doing
- number: 10
  speaker: coder
  kind: question
  at: '2026-11-08T10:51:50.121166Z'
  stage: doing
  run: 71fcd213f30341aaaf7b09b71e7742c5
  blocked: question
- number: 11
  speaker: human
  kind: comment
  at: '2026-11-08T10:53:39.699791Z'
  stage: doing
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T10:53:41.983215Z'
  stage: doing
- number: 13
  speaker: coder
  kind: result
  at: '2026-11-08T10:53:56.852963Z'
  stage: doing
  run: f4cab83a8891427fb6efd955e90255c5
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-08T10:54:01.785742Z'
  stage: tests
- number: 15
  speaker: tester
  kind: result
  at: '2026-11-08T10:54:25.661729Z'
  stage: tests
  run: 1d07528cd8d64d279f81965af1aa484b
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-08T10:54:30.308599Z'
  stage: doing
- number: 17
  speaker: coder
  kind: result
  at: '2026-11-08T10:58:44.030886Z'
  stage: doing
  run: 0d8cb5f27a574e24b0302ea5c813d10b
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-08T10:58:49.307162Z'
  stage: review
- number: 19
  speaker: reviewer
  kind: result
  at: '2026-11-08T11:00:27.645324Z'
  stage: review
  run: 6491af38877846cdb5e08a92324b6933
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-08T11:00:33.105592Z'
  stage: doing
- number: 21
  speaker: coder
  kind: question
  at: '2026-11-08T11:00:55.134280Z'
  stage: doing
  run: 4d63c5d3f0ff4e41be322a398a56fa8c
  blocked: question
- number: 22
  speaker: human
  kind: comment
  at: '2026-11-08T11:02:41.898827Z'
  stage: doing
- number: 23
  speaker: factory
  kind: started
  at: '2026-11-08T11:02:44.316765Z'
  stage: doing
- number: 24
  speaker: coder
  kind: result
  at: '2026-11-08T11:03:02.111047Z'
  stage: doing
  run: 96608464d6504ed6aaf11e87e2305996
- number: 25
  speaker: factory
  kind: started
  at: '2026-11-08T11:03:07.318514Z'
  stage: tests
- number: 26
  speaker: tester
  kind: result
  at: '2026-11-08T11:03:58.933950Z'
  stage: tests
  run: 271f7c6ceaee450ea12ee18e2d083753
- number: 27
  speaker: factory
  kind: started
  at: '2026-11-08T11:04:04.161441Z'
  stage: doing
- number: 28
  speaker: coder
  kind: result
  at: '2026-11-08T11:08:24.380590Z'
  stage: doing
  run: 6ca378092de3412d91b33cef0fe9d269
- number: 29
  speaker: factory
  kind: started
  at: '2026-11-08T11:08:29.408868Z'
  stage: review
- number: 30
  speaker: reviewer
  kind: result
  at: '2026-11-08T11:09:45.845384Z'
  stage: review
  run: 633d5568b559475e9daabbf026ca492e
---

# Every role has the same tools and the same decision tool

## Description

A Claude Code request begins with its tool list, so two runs share a cached start only if their tools are the same. The cache is also per model, and a change of effort between requests invalidates the cached messages. Today the roles differ in four ways:
- Intake, the reviewer and the smoke tester have no `Write` tool.
- The decision tool's schema lists the stage's allowed decisions, so it differs from stage to stage.
- Intake and the documenter run on Sonnet, the other roles on Opus.
- Intake runs at low effort, the reviewer and the acceptance reviewer at high, the others at medium.

After this story, every role has the tools `Read, Grep, Glob, Edit, Bash, Write, Skill`. Intake and the documenter run on Opus at medium effort, so that they, the tester, the coder and the smoke tester share one model and one effort. The reviewer and the acceptance reviewer stay on Opus at high effort (the feature's decision 3). The decision tool's schema is the same for every request. The factory's write paths still decide what each role may write, as today. The runtime still refuses a decision outside the stage's allowed ones, as it does today after the run. The run's message still names the allowed decisions.

## Interface

- `agents/agents/*.md`: every agent file's `tools` is `[Read, Grep, Glob, Edit, Bash, Write, Skill]`.
- `agents/agents/intake.md` and `agents/agents/documenter.md`: `model: opus`, `effort: medium`. The other agent files keep their model and effort.
- `factory.agents.adapters.claude_runtime`: the `--json-schema` argument no longer depends on the request. `decision` is a string, and its description says the run's message names the allowed decisions.
- A decision outside the request's `allowed_decisions` is handled as today: the run's result is refused.
- No other launch argument changes.

## Acceptance criteria

1. Every agent file under `agents/agents/` has exactly the tools `Read, Grep, Glob, Edit, Bash, Write, Skill`, in this order (rows of one test over the files).
2. Every agent file has `model: opus`. Intake, the tester, the coder, the documenter and the smoke tester have `effort: medium`; the reviewer and the acceptance reviewer have `effort: high` (rows of one test over the files).
3. Two requests with different `allowed_decisions` give the same `--json-schema` argument.
4. A run whose decision is not in the request's `allowed_decisions` is refused, as before (an earlier test may change only in how it builds the schema).
5. Intake, the reviewer and the smoke tester still cannot write outside `{work_item}`: the factory's write-path verdict refuses a written file outside it, with `Write` as with `Edit` (rows of one test).
6. The `--json-schema` argument's `decision` property has type `string` and no `enum`, and its description says the run's message names the allowed decisions.
7. The message built for a request contains each of its `allowed_decisions`.
8. The launch arguments of a request, with the `--json-schema` value removed, equal those before this story (the model and effort of intake and the documenter come from their agent files and are covered by criterion 2).
9. `make check` stays green.
10. docs: the project guide's description of the agent files and of the launch arguments says that every role has the same tools and the same decision tool, and why (the shared cached start). `docs/decisions.md`: one entry, every role has the same tools, and five roles share one model and one effort, for the prompt cache; the write paths, not the tool list, limit what a role writes.

## Smoke test

```bash
grep -h '^tools:' agents/agents/*.md | sort -u
```
Expect: exactly one line, `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]`

```bash
grep -h '^model:' agents/agents/*.md | sort -u
```
Expect: exactly one line, `model: opus`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Format check passed. Questions:

   1. The Interface says the `--json-schema` `decision` is a string and "its description says the run's message names the allowed decisions". No criterion tests that. Criterion 3 only compares two schemas. Please add one, for example: "the schema's `decision` property has type `string` and no `enum`, and its description mentions the allowed decisions". I would choose that.

   2. The Description says "The run's message still names the allowed decisions". Nothing tests it. Please add a criterion, for example: "the message built for a request contains each of its `allowed_decisions`". This matters most because the schema no longer lists them.

   3. The Interface says "No other launch argument changes". No criterion pins it, and two coders could read it differently. Please add a criterion, for example: "the launch arguments of a request, with the `--json-schema` value removed, equal those before this story". Alternatively, say it is not tested and drop the line. I would add the criterion.

   Everything else is fine: criteria 1, 2, 4 and 5 each have one test, and the refused side is covered by criteria 4 and 5. The smoke commands are runnable and their Expect lines are checkable. The docs criterion names what the reader must know and dictates no sentences. The architecture fits, because only the `agents` adapters and `agents/agents/*.md` change. The scope fits S0001 in `feature.md`.
4. 2026-11-08 human: Agreed on all three, as you propose:
   1. Add the criterion: the schema's `decision` property has type `string` and no `enum`, and its description says the run's message names the allowed decisions.
   2. Add the criterion: the message built for a request contains each of its `allowed_decisions`.
   3. Add the criterion: the launch arguments of a request, with the `--json-schema` value removed, equal those before this story (the model and effort of intake and the documenter come from their agent files and are covered by criterion 2).
5. factory: started intake as vm.
6. intake: accepted. I carried in the human's answer (journal entry 4) by adding three criteria before the two closing ones: new 6 (the schema's `decision` is a string with no `enum`, and its description says the message names the allowed decisions), new 7 (the message contains each of the request's `allowed_decisions`) and new 8 (launch arguments other than `--json-schema` are unchanged). `make check` and `docs:` are now criteria 9 and 10. The Description did not change.
   - Interface: it names concrete paths (`agents/agents/*.md` with their `tools`, `model` and `effort` values, and `factory.agents.adapters.claude_runtime`'s `--json-schema` argument). Every behaviour it states now has a criterion.
   - Criteria: each is testable by one test function. The failing sides are covered: criterion 4 refuses a decision outside `allowed_decisions`, criterion 5 refuses a write outside `{work_item}`, and criterion 6 requires no `enum`. Each effort value has its own row in criterion 2.
   - Smoke test: both `grep ... | sort -u` commands are runnable, and each `Expect:` line is checkable against the output. The commands run no pytest.
   - Docs criterion: it names what the reader must know (same tools and decision tool for every role, and why) and the one decisions entry. It dictates no sentences.
   - Architecture: only the `agents` adapters and the agent files change. The write paths stay in the factory.
   - Scope: this matches S0001 in `feature.md` and decisions 1 to 3. Route: `tests`, because the Interface changes code.
7. factory: started tests as vm.
8. tester: I wrote the tests for criteria 1 to 8. They are red on purpose: the agent files still hold the old tools, model and effort, and the runtime still writes the decision `enum` into the schema.

   - criterion 1: tests/agent_files/test_shared_start_agent_files.py::test_every_agent_file_has_the_same_tools_in_the_same_order (one row per file under `agents/agents/`)
   - criterion 2: tests/agent_files/test_shared_start_agent_files.py::test_every_agent_file_runs_on_opus_at_its_roles_effort (one row per file). tests/agent_files/test_shared_start_agent_files.py::test_the_shipped_agents_are_the_seven_with_an_effort checks that the effort table covers every agent file.
   - criterion 3: tests/agents/adapters/test_claude_runtime_shared_schema.py::test_requests_with_different_decisions_get_the_same_json_schema
   - criterion 4: tests/agents/adapters/test_claude_runtime.py::test_reply_without_a_usable_decision_is_no_result (row "decision not allowed"). This test already exists and I left it unchanged; its stand-in does not read the schema.
   - criterion 5: tests/pipeline/application/test_take_refuses_write_and_edit.py::test_a_file_written_outside_the_work_item_is_refused. The rows are intake, reviewer and smoke-tester, each with Write and Edit. Each role's write paths come from the template pipeline definition and go through `take.is_refused`. A Write row is a new file and an Edit row is an existing one. Each row also checks that the work item itself is not refused. The verdict does not depend on the tool, so this test already passes.
   - criterion 6: tests/agents/adapters/test_claude_runtime_shared_schema.py::test_the_decision_is_any_string_described_as_named_in_the_message. The decision must be type `string` with no `enum`, and its description must contain "message" and "allowed decisions".
   - criterion 7: tests/agents/domain/test_prompt_names_decisions.py::test_the_message_names_each_allowed_decision. I read "the message built for a request" as the prompt that `compose_prompt` builds, which the runtime passes as `-p`.
   - criterion 8: tests/agents/adapters/test_claude_runtime_shared_schema.py::test_the_other_launch_arguments_are_as_before. Two rows with different `allowed_decisions`. With the `--json-schema` value removed, the arguments must equal today's list.

   Files I created: tests/agent_files/test_shared_start_agent_files.py, tests/agents/adapters/test_claude_runtime_shared_schema.py, tests/agents/domain/test_prompt_names_decisions.py, tests/pipeline/application/test_take_refuses_write_and_edit.py.

   Earlier test files I changed, because they pinned what this story changes:
   - tests/support/shipped_agents.py: in the shared table of shipped agents, intake is now opus/medium with all seven tools, documenter is now opus, and reviewer and smoke-tester now have all seven tools. I removed `_TOOLS_WITHOUT_WRITE`. The values now say what the Description states, and the test names and what they check are unchanged. Without this, test_shipped_agents_effect.py and test_claude_files.py would stay red after the coder's change.
   - tests/agents/adapters/test_claude_runtime.py::test_json_schema_asks_for_an_allowed_decision_and_an_entry: it compared the whole schema, `enum` included. It now checks that `decision` is a string and takes the decision property from the schema itself; the rest of the schema is compared exactly as before. I took this change as covered by criterion 4's "an earlier test may change only in how it builds the schema".

   If the human sees either change to an earlier test as beyond that leave, the reviewer can raise it.

   Test run, before implementation: the new tests and the earlier tests that read the agent files fail on wrong values, for example test_claude_files.py::test_front_matter_holds_the_four_applied_keys_with_their_values[intake|reviewer|documenter|smoke-tester] and test_shipped_agents_effect.py::test_call_passes_exactly_the_agent_tools[smoke-tester]. Every module imported; nothing failed to import. `make lint` is green.

   `lint`: lint: green (0.2 s)
9. factory: started doing as vm.
10. coder: I stopped with the implementation done and `make check` red on one test that no code can make pass.

    What I built:
    - `agents/agents/intake.md`, `documenter.md`, `reviewer.md` and `smoke-tester.md` now match the Interface. All seven agent files have `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]` and `model: opus`. Intake is now at `effort: medium`. The reviewer and the acceptance reviewer keep `high`.
    - In `src/factory/agents/adapters/claude_runtime.py`, `_decision_schema(request)` is replaced by one module constant, `_DECISION_SCHEMA`. Its `decision` is a string with no `enum`, and its description says the decision is one of the allowed decisions the run's message names. `_answered` still refuses a decision outside `request.allowed_decisions`, and the other launch arguments are unchanged.
    - Main choice: build the schema once at import, because it no longer depends on the request. I rejected keeping a function that ignores its argument. I made the names private because nothing outside the module uses them.

    The blocking test: `tests/agents/adapters/test_claude_runtime_shared_schema.py::test_requests_with_different_decisions_get_the_same_json_schema` fails before it reaches the runtime. Its helper `_arguments` calls `work.mkdir()` on `tmp_path / "first" / "work"`, and `tmp_path / "first"` does not exist. Output from `uv run pytest -q tests/agents/adapters/test_claude_runtime_shared_schema.py --tb=short`:
    ```
    tests/agents/adapters/test_claude_runtime_shared_schema.py:32: in _arguments
        work.mkdir()
    E   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pytest-of-factory/pytest-1/test_requests_with_different_d0/first/work'
    ```
    The other three tests in that file pass, because they give `_arguments` the bare `tmp_path`. In `make check`, every earlier step and every other test passed (total coverage 99.22 %). This test is the only failure.

    Options:
    1. The tester changes the helper's `work.mkdir()` to `work.mkdir(parents=True)` in that test file. The test still checks the same thing. I recommend this.
    2. The tester changes the test to create `tmp_path / "first"` and `tmp_path / "second"` before calling `_arguments`.

    With either answer I will end with `tests` and name the change. No code change is needed on my side.

    Refactor: I read my diff and nothing else needs changing.

    Noticed but not touched: the comment above `__all__` in `claude_runtime.py` keeps old names exported for earlier callers. It is unrelated to this story. The journal changed nothing in the Description; it only added criteria 6 to 8, which intake already carried in.
11. 2026-11-08 human: Option 1: the tester changes the helper's `work.mkdir()` to `work.mkdir(parents=True)`; the test keeps checking the same thing.
12. factory: started doing as vm.
13. coder: The human's answer in entry 11 calls for a test change. In `tests/agents/adapters/test_claude_runtime_shared_schema.py`, the helper `_arguments` (line 32) should call `work.mkdir(parents=True)` instead of `work.mkdir()`. That lets `test_requests_with_different_decisions_get_the_same_json_schema` create `tmp_path / "first" / "work"` and `tmp_path / "second" / "work"`, and the test still checks the same thing.

    I changed no code in this round. The implementation from the last round is already committed: the four agent files under `agents/agents/` and the shared `_DECISION_SCHEMA` constant in `src/factory/agents/adapters/claude_runtime.py`. In that round's `make check`, this test was the only failure. When the tester sends the work item back, I will run `make check` and hand it to review.

    The journal added nothing new to the Description. Entry 11 only picks option 1 from my question.
14. factory: started tests as vm.
15. tester: I made the test change the human approved in entry 11, which the coder named in entry 13. In `tests/agents/adapters/test_claude_runtime_shared_schema.py`, the helper `_arguments` (line 32) now calls `work.mkdir(parents=True)` instead of `work.mkdir()`. Before, `test_requests_with_different_decisions_get_the_same_json_schema` failed with `FileNotFoundError`, because it passes `tmp_path / "first"` and `tmp_path / "second"` to the helper and those folders did not exist. The helper can now create them. No test name or assertion changed, and every test checks the same thing as before.

    Criterion → test mapping is unchanged from entry 8. The fix affects only criterion 3: tests/agents/adapters/test_claude_runtime_shared_schema.py::test_requests_with_different_decisions_get_the_same_json_schema.

    Files changed: tests/agents/adapters/test_claude_runtime_shared_schema.py. Files created: none. Modules the test run could not import: none.

    I ran `uv run pytest -q tests/agents/adapters/test_claude_runtime_shared_schema.py` once: all 4 tests pass with the coder's implementation. `make lint`: lint: green (0.1 s).

    `lint`: lint: green (0.1 s)
16. factory: started doing as vm.
17. coder: The tester applied the test fix the human approved in entry 11 (`work.mkdir(parents=True)` in `tests/agents/adapters/test_claude_runtime_shared_schema.py`). With that fix, `make check` is green (`check: green`, total coverage 99.22 %). No code changed in this round.

    What I built (the change committed in the first doing round):
    - `agents/agents/intake.md`, `documenter.md`, `reviewer.md` and `smoke-tester.md`: every agent file now has `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]` and `model: opus`.
      - Intake moves from sonnet at low effort to opus at medium.
      - The documenter moves from sonnet to opus and stays at medium.
      - The reviewer and the acceptance reviewer keep `effort: high`.
    - `src/factory/agents/adapters/claude_runtime.py`: the per-request `_decision_schema(request)` is replaced by one module constant, `_DECISION_SCHEMA`.
      - Its `decision` is a string with no `enum`. Its description, `_DECISION_DESCRIPTION`, says the decision is one of the allowed decisions that the run's message names.
      - A comment gives the reason: the shared cached start.
      - `_answered` still refuses a decision outside `request.allowed_decisions`.
      - No other launch argument changed.

    Main choice: build the schema once at import, because it no longer depends on the request. I rejected the alternative of keeping a function that takes the request and ignores it.

    Refactor: I read the diff against `develop` again; nothing needs changing.

    Noticed but not touched: the comment above `__all__` in `claude_runtime.py` keeps old names exported for earlier callers; it is unrelated to this story. The journal changed nothing in the Description: the human's answers added criteria 6 to 8, which intake already carried in, and picked the test fix.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
18. factory: started review as vm.
19. reviewer: Findings:

    1. `tests/support/shipped_agents.py` (rows intake, reviewer, documenter and smoke-tester, and the removed `_TOOLS_WITHOUT_WRITE`): another story wrote this support module, and the tester changed its values without leave. The change does not move a shared helper (the standing leave), the story does not name the file, and no human answer in the journal allows it. Criterion 4's leave covers only how a test builds the schema. Fix: the coder ends with `question` and asks the human for leave to change this file's four rows to the Interface's values. With that leave the change can stay as it is.
    2. `tests/agents/adapters/test_claude_runtime_shared_schema.py:14-54`: `REPLY`, `_arguments` and `_schema` copy existing helpers in `tests/agents/adapters/test_claude_runtime.py`. `REPLY` copies `_reply` (lines 33-51), `_arguments` copies `_request`, `_runtime` and `_only_call` (lines 61-107), and `_schema` copies `_after` (lines 110-111). Fix: the tester moves those helpers to a module in `tests/support/` under the standing leave and both files use it. Or the tester writes the three tests into `test_claude_runtime.py` with its own helpers, which adds tests only and needs no leave.
    3. `tests/agents/domain/test_prompt_names_decisions.py:25`: `decision in message` is a substring check over the whole prompt. In the row `["doing", "question"]`, `doing` is always found in `Stage: doing`, so for that decision the test passes whatever the `Allowed decisions:` line says. Criterion 7 is not really tested for it. Fix: take the prompt's `Allowed decisions:` line, split its list after the colon, and assert that each requested decision is in that list.
    4. `tests/agents/domain/test_prompt_names_decisions.py:13-21`: the `PromptFacts` it builds copies `VALID` and `_facts` from `tests/agents/domain/test_prompts.py:13-25`. Fix: write the test into `test_prompts.py` with `_facts(allowed_decisions=decisions)`, or move `VALID` and `_facts` to a module in `tests/support/` under the standing leave.

    Checked and found sound:
    - Criteria 1, 2, 3, 5, 6 and 8 each have a test that checks what the criterion says.
    - Criterion 4 is still tested by `test_claude_runtime.py::test_reply_without_a_usable_decision_is_no_result[decision not allowed]`, and `claude_runtime.py:226` still refuses such a decision.
    - The source change in `claude_runtime.py` (one module constant, `_DECISION_SCHEMA`, with a comment that gives the reason) changes no other launch argument.
    - Architecture: holds.
    - Security: holds; the diff adds no silencing marker.
    - The Description matches what was built.
    - The journal gives the main decision (one constant, not a function that ignores the request) and the rejected alternative.
    - The docs criterion still describes what the reader must know.
    - Coder entry 17 reports `make check` green.
    - I did not read the `duplicates: 6 new` report: no report file is in the checkout, and the `src` change is one constant that replaces a function.

    Earlier tests:
    - `tests/agents/adapters/test_claude_runtime.py` (`test_json_schema_asks_for_an_allowed_decision_and_an_entry`): the human's leave in criterion 4 ("an earlier test may change only in how it builds the schema"). Only the expected `decision` property changed.
    - `tests/support/shipped_agents.py`: none; see finding 1.
20. factory: started doing as vm.
21. coder: I changed no code this round. All four review findings are about tests, and the first one needs the human's leave before anything else can move.

    **Question (finding 1):** The tester changed `tests/support/shipped_agents.py` in its first run. That support module belongs to an earlier story. The tester changed four rows (intake, reviewer, documenter, smoke-tester) to the Interface's values and removed `_TOOLS_WITHOUT_WRITE`. The reviewer found that no leave covers this change: it is not a move of a shared helper, the story does not name the file, and criterion 4's leave is only about how a test builds the schema. Without the change, `test_shipped_agents_effect.py` and `test_claude_files.py` stay red against the agent files the Interface asks for. So the old values cannot stay unless those tests change some other way. Options:
    1. Give leave for the change as it is: the four rows take the Interface's tools, model and effort, and `_TOOLS_WITHOUT_WRITE` is removed. Test names and what they check stay the same. **I recommend this.**
    2. Give leave for a narrower change that you name, for example keeping `_TOOLS_WITHOUT_WRITE` unused.
    3. Refuse the change. The earlier tests would then pin the old tools and model, which contradicts the Interface. The story's agent-file change could not pass, and the Interface would have to change.

    **What happens after your answer:** I will end with `tests`. The tester will then make findings 2 to 4 together with whatever your answer needs:
    - Finding 2: move the copied helpers `REPLY`, `_arguments` and `_schema` from `tests/agents/adapters/test_claude_runtime_shared_schema.py` into a `tests/support/` module under the standing leave. The other way is to put those tests into `test_claude_runtime.py` and use its helpers there.
    - Finding 3: in `tests/agents/domain/test_prompt_names_decisions.py`, check each decision against the prompt's `Allowed decisions:` list, not as a substring of the whole prompt.
    - Finding 4: either write that test into `tests/agents/domain/test_prompts.py` using `_facts(allowed_decisions=...)`, or move `VALID` and `_facts` into a `tests/support/` module.

    Finding 3 changes a test this story wrote, and findings 2 and 4 fall under the standing leave, so none of them needs another question.

    **State of the code:** the implementation from the first doing round is unchanged. That is the four agent files under `agents/agents/` and the `_DECISION_SCHEMA` constant in `src/factory/agents/adapters/claude_runtime.py`. The reviewer judged the source change sound, and `make check` was green in entry 17.

    The journal changed nothing in the Description.
22. 2026-11-08 human: Option 1: leave given for the change to `tests/support/shipped_agents.py` as it is. The four rows take the Interface's tools, model and effort, and `_TOOLS_WITHOUT_WRITE` is removed; test names and what they check stay the same. Findings 2 to 4 as you describe.
23. factory: started doing as vm.
24. coder: I changed no code in this round. All the open findings are test changes, so I am sending the work item to the tester.

    The human's answer (entry 22) gives leave for the change to `tests/support/shipped_agents.py` exactly as it stands: the four rows (intake, reviewer, documenter, smoke-tester) take the Interface's tools, model and effort, and `_TOOLS_WITHOUT_WRITE` is removed. That settles review finding 1, and the tester has nothing more to do on it.

    Test changes for the tester (review findings 2 to 4, which the human approved as described in entry 21):
    - Finding 2: `tests/agents/adapters/test_claude_runtime_shared_schema.py` copies helpers from `tests/agents/adapters/test_claude_runtime.py`:
      - `REPLY` copies `_reply`.
      - `_arguments` copies `_request`, `_runtime` and `_only_call`.
      - `_schema` copies `_after`.
      Either move the shared helpers into one `tests/support/` module under the standing leave, so both files use it and keep their test names and checks, or write the three tests into `test_claude_runtime.py` and use its helpers there.
    - Finding 3: in `tests/agents/domain/test_prompt_names_decisions.py`, `decision in message` is a substring check over the whole prompt. Instead, take the prompt's `Allowed decisions:` line, split the list after the colon, and assert that each requested decision is in that list. Today `doing` is always found because the prompt also says `Stage: doing`.
    - Finding 4: the `PromptFacts` that the same file builds copies `VALID` and `_facts` from `tests/agents/domain/test_prompts.py`. Either write the test into `test_prompts.py` with `_facts(allowed_decisions=...)`, or move `VALID` and `_facts` into a `tests/support/` module under the standing leave.

    State of the code: unchanged since the first doing round, and the reviewer judged it sound. It covers the four agent files under `agents/agents/` and the `_DECISION_SCHEMA` constant in `src/factory/agents/adapters/claude_runtime.py`. `make check` was green in entry 17. When the tester sends the work item back, I will run `make check` and hand it to review.

    The journal changed nothing in the Description: entry 22 only gives leave for an existing test change.
25. factory: started tests as vm.
26. tester: I made the test changes for review findings 2 to 4, as the coder's entry 24 names them and the human approved in entry 22. Finding 1 is settled by that answer, so I left `tests/support/shipped_agents.py` as it is.

    - Finding 2: I took the second option the reviewer offered. The three tests from `tests/agents/adapters/test_claude_runtime_shared_schema.py` now live in `tests/agents/adapters/test_claude_runtime.py` and use its own helpers (`_request`, `_runtime`, `_reply`, `_only_call`, `_after`). One small private helper, `_arguments_allowing`, changes only the request's `allowed_decisions` through `model_copy`. I deleted the copied `REPLY`, `_arguments` and `_schema` with the old file. No earlier test changed; I only added tests to that file. Because those helpers build a sonnet / high / `Read,Edit` request, the launch-arguments test now expects those values. It checks the same thing as before: everything apart from the `--json-schema` value is the earlier list, whatever the decisions are. I renamed it to `test_the_other_launch_arguments_do_not_depend_on_the_decisions`.
    - Finding 3: the prompt test now finds the single `Allowed decisions:` line in the message, splits the list after the colon and checks that each requested decision is in that list. `Stage: doing` can no longer make it pass.
    - Finding 4: that test now lives in `tests/agents/domain/test_prompts.py` and uses its `_lines` and `_facts`. I deleted `tests/agents/domain/test_prompt_names_decisions.py`.

    Criterion → test, after this change:
    criterion 3: tests/agents/adapters/test_claude_runtime.py::test_requests_with_different_decisions_get_the_same_json_schema
    criterion 6: tests/agents/adapters/test_claude_runtime.py::test_the_decision_is_any_string_described_as_named_in_the_message
    criterion 7: tests/agents/domain/test_prompts.py::test_the_message_names_each_allowed_decision
    criterion 8: tests/agents/adapters/test_claude_runtime.py::test_the_other_launch_arguments_do_not_depend_on_the_decisions
    Criteria 1, 2, 4 and 5 keep their tests from the first tests round, unchanged.

    Files changed: tests/agents/adapters/test_claude_runtime.py and tests/agents/domain/test_prompts.py (tests added only). Files deleted: tests/agents/adapters/test_claude_runtime_shared_schema.py and tests/agents/domain/test_prompt_names_decisions.py (both written by this story).

    I ran `uv run pytest -q` once on the two changed files. Every test passed, because the code already exists, and every module imported. `make lint`: lint: green.

    `lint`: lint: green (0.2 s)
27. factory: started doing as vm.
28. coder: I changed no code in this round. The open review findings were all about tests: finding 1 got the human's leave in entry 22, and the tester settled findings 2 to 4 in entry 26. With the tester's changes in place, I ran `make check` in the foreground and it is green: `test: green (108.8 s)`, `check: green`, total coverage 99.22 %.

    What I built (unchanged since the first doing round):
    - `agents/agents/intake.md`, `documenter.md`, `reviewer.md` and `smoke-tester.md`: every agent file now has `tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]` and `model: opus`. Intake moved to `effort: medium`. The reviewer and the acceptance reviewer keep `high`.
    - `src/factory/agents/adapters/claude_runtime.py`: one module constant, `_DECISION_SCHEMA`, replaces the per-request `_decision_schema(request)`. Its `decision` is a string with no `enum`. Its description, `_DECISION_DESCRIPTION`, says the decision is one of the allowed decisions that the run's message names. A comment gives the reason (the shared cached start). `_answered` still refuses a decision outside `request.allowed_decisions`, and no other launch argument changed.

    Main choice: the schema is built once, when the module loads, because it no longer depends on the request. I rejected keeping a function that takes the request and ignores it.

    Refactor: I read the diff against `develop` again. Nothing needs changing.

    Noticed but not touched: the comment above `__all__` in `claude_runtime.py` keeps old names exported for earlier callers. That is unrelated to this story.

    The journal did not change the Description: entries 21 to 26 only settled test findings.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
29. factory: started review as vm.
30. reviewer: no findings

    Checked in this round:
    - Round 0 findings are settled.
      - Finding 1: the human gave leave in entry 22.
      - Finding 2: the copied `REPLY`, `_arguments` and `_schema` are gone. The tests for criteria 3, 6 and 8 are now in `tests/agents/adapters/test_claude_runtime.py:190-248` and use that file's `_request`, `_runtime`, `_reply`, `_only_call` and `_after`.
      - Finding 3: `tests/agents/domain/test_prompts.py:32-44` now splits the `Allowed decisions:` line, so `Stage: doing` can no longer satisfy it.
      - Finding 4: that test uses `_lines` and `_facts` from `test_prompts.py`.
    - Criteria:
      - 1 and 2: `tests/agent_files/test_shared_start_agent_files.py` (rows over the files, plus a guard that the effort table covers every agent file).
      - 3, 6 and 8: `test_claude_runtime.py`.
      - 4: `test_reply_without_a_usable_decision_is_no_result[decision not allowed]`, and `claude_runtime.py:226` still refuses such a decision.
      - 5: `tests/pipeline/application/test_take_refuses_write_and_edit.py`, with rows over role × tool.
      - 7: `test_prompts.py::test_the_message_names_each_allowed_decision`.
      - Each test checks what its criterion says.
    - `make check`: the coder reports it green in entry 28.
    - Source: `claude_runtime.py:160-173` is one module constant, `_DECISION_SCHEMA`. Its `decision` is a string with no `enum` and a description that names the run's message. A comment gives the reason (the cached start). No other launch argument changes.
    - Architecture: holds. Only the `agents` adapter and the agent files change.
    - Security: holds. No silencing marker and no string-built command.
    - Quality: holds.
    - `make duplicates` (I ran it): 6 new, 39 known, 4 gone. None comes from this diff. The `claude_runtime`/`opencode_runtime` similar-code finding is the known `finished_run` block at shifted lines (it shows as gone/new). The other five are in modules the diff does not touch.
    - Work item: the Description matches what was built. The journal gives the main choice (one constant, not a function that ignores the request) and what was rejected. The docs criterion still says what the reader must know. The diff changes no document.

    Earlier tests:
    - `tests/agents/adapters/test_claude_runtime.py`: criterion 4's leave ("an earlier test may change only in how it builds the schema") covers `test_json_schema_asks_for_an_allowed_decision_and_an_entry`. Only its expected `decision` property changed. Everything else in the file is added tests only.
    - `tests/agents/domain/test_prompts.py`: none needed. It only adds a test.
    - `tests/support/shipped_agents.py`: the human's leave, journal entry 22.

    Notes:
    - `tests/agents/adapters/test_claude_runtime.py:218-248`: the expected argument list in `test_the_other_launch_arguments_do_not_depend_on_the_decisions` repeats the one in `test_call_passes_every_flag_in_order` (lines 118-150). It is a test-quality point only. That unchanged earlier test already pins the arguments as they were before this story.
