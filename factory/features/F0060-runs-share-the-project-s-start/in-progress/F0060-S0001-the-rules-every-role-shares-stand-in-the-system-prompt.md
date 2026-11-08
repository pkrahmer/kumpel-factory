---
stage: approval
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 678
comments_read: [6726852112, 6726967345]
handed_over: approval
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T19:45:08.261833Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T19:45:08.268924Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T19:45:37.261010Z'
  stage: intake
  run: 70fe01b7f4d6433fbeb39c13168ec3ce
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T19:45:42.085191Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-08T19:48:43.831153Z'
  stage: tests
  run: 733b412fd5fe4a4fab2a3aeddf2ead65
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T19:48:51.380168Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-08T19:58:20.008021Z'
  stage: doing
  run: 3c549c6c944448dc9594aa41b18819af
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T19:58:27.527037Z'
  stage: tests
- number: 9
  speaker: tester
  kind: result
  at: '2026-11-08T19:59:22.156363Z'
  stage: tests
  run: 6a2b8433f41b4594a9cc3bc4500d0321
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T19:59:27.078510Z'
  stage: doing
- number: 11
  speaker: coder
  kind: result
  at: '2026-11-08T20:01:50.401924Z'
  stage: doing
  run: 2e4965ab7028488982ad51be96a1a32d
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T20:01:55.535722Z'
  stage: review
- number: 13
  speaker: reviewer
  kind: result
  at: '2026-11-08T20:03:09.771809Z'
  stage: review
  run: 370e643accc546d8b8c1849bc04300b4
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-08T20:03:14.932893Z'
  stage: doing
- number: 15
  speaker: coder
  kind: result
  at: '2026-11-08T20:03:33.758330Z'
  stage: doing
  run: fea8230c66e1478186a5f93d03736523
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-08T20:03:39.008330Z'
  stage: tests
- number: 17
  speaker: tester
  kind: result
  at: '2026-11-08T20:04:24.554960Z'
  stage: tests
  run: 2ad6ecb0d92647418ca55e4a9c27b46b
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-08T20:04:30.080172Z'
  stage: doing
- number: 19
  speaker: coder
  kind: result
  at: '2026-11-08T20:06:47.229654Z'
  stage: doing
  run: 5bc162de88dd4c1c9c5b1a74a4aebc7d
- number: 20
  speaker: factory
  kind: started
  at: '2026-11-08T20:06:52.410837Z'
  stage: review
- number: 21
  speaker: reviewer
  kind: result
  at: '2026-11-08T20:07:27.596050Z'
  stage: review
  run: b60e354c7e9e44e59338285c2a7e0808
- number: 22
  speaker: factory
  kind: started
  at: '2026-11-08T20:07:32.674317Z'
  stage: docs
- number: 23
  speaker: documenter
  kind: result
  at: '2026-11-08T20:22:08.077690Z'
  stage: docs
  run: 7e245a97bda343f0afe6f22a1e899d9d
- number: 24
  speaker: factory
  kind: stall
  at: '2026-11-08T20:22:08.443422Z'
  stage: docs
  run: 7e245a97bda343f0afe6f22a1e899d9d
  reason: check_red
- number: 25
  speaker: factory
  kind: started
  at: '2026-11-08T20:22:16.174925Z'
  stage: docs
- number: 26
  speaker: documenter
  kind: question
  at: '2026-11-08T20:30:19.397062Z'
  stage: docs
  run: 9c9a706daf4047c6ab53e352b4e3b2b7
  blocked: question
- number: 27
  speaker: human
  kind: comment
  at: '2026-11-08T20:42:19.653270Z'
  stage: docs
- number: 28
  speaker: factory
  kind: started
  at: '2026-11-08T20:42:22.042825Z'
  stage: docs
- number: 29
  speaker: documenter
  kind: result
  at: '2026-11-08T20:48:18.072540Z'
  stage: docs
  run: fa48475be9ab499b83e11e83c4e4b432
- number: 30
  speaker: factory
  kind: stall
  at: '2026-11-08T20:48:18.524514Z'
  stage: docs
  run: fa48475be9ab499b83e11e83c4e4b432
  reason: check_red
- number: 31
  speaker: factory
  kind: question
  at: '2026-11-08T20:48:25.018918Z'
  stage: docs
  blocked: attempts_cap
- number: 32
  speaker: human
  kind: comment
  at: '2026-11-08T20:54:14.008161Z'
  stage: docs
- number: 33
  speaker: factory
  kind: started
  at: '2026-11-08T20:54:16.565731Z'
  stage: docs
- number: 34
  speaker: documenter
  kind: result
  at: '2026-11-08T20:57:51.704031Z'
  stage: docs
  run: 84729ca4d2f4418192bfcaa597f1593d
- number: 35
  speaker: factory
  kind: started
  at: '2026-11-08T20:57:56.774986Z'
  stage: smoke-test
- number: 36
  speaker: smoke-tester
  kind: result
  at: '2026-11-08T21:00:20.278300Z'
  stage: smoke-test
  run: bab73604256845da8f0f702e09f574b0
---

# The rules every role shares stand in the system prompt

## Description

Every shipped agent file under `agents/agents/` carries the same `## Rules` section (the opening paragraphs and the rules R1 to R15), and the factory sends an agent file's body in the run's first message, which no later run reads from the prompt cache. The system prompt, which every run of both runtimes receives and which later runs read from the cache, holds only a short orientation. After this story the shared rules stand once, in the shipped system prompt `agents/system-prompt.md` and in the built-in fallback `SYSTEM_PROMPT`, and the seven agent files keep only what is their own: the lines before the rules, `## Role` where there is one, `## Stage` and `## Lessons`. The words of the rules stay as they are, except where they point to a place that moves: the opening paragraph now says that the stage's and the role's instructions come in the `<role-instructions>` block of the first message. The system prompt's own opening says that the rules below apply to every role, and that the `<role-instructions>` block holds the instructions of the agent's role. Both runtimes already send the system prompt file, so neither changes. A project agent under `<project>/factory/agents/` that is a copy of an earlier shipped file still carries the rules; that only repeats them, and the operator guide says that such a copy may drop its `## Rules` section.

## Interface

- `agents/system-prompt.md` and `src/factory/agents/domain/prompts.py` (`domain`), `SYSTEM_PROMPT`: the same text, which is the system prompt's orientation followed by the `## Rules` section.
  - The orientation says that the rules below apply to every agent in every stage, and that the `<role-instructions>` block of the first message holds the instructions of the agent's role, to be followed with the same weight; the sentences on the `<work-item>` block and the `<context>` blocks stay.
  - The `## Rules` section holds the opening paragraphs and R1 to R15 as the shipped agent files hold them today, word for word, except the opening paragraph's sentence on where the stage's and the role's instructions stand: they stand under `Stage` and `Role` in the `<role-instructions>` block.
- `agents/agents/<name>.md` for the seven roles (`intake`, `tester`, `coder`, `reviewer`, `documenter`, `smoke-tester`, `acceptance-reviewer`): no `## Rules` section; everything else unchanged.
- The leave for earlier tests (the human, 2026-11-08, in `feature.md`, decision 1): "the tests that read the `## Rules` section, a rule `R1.` to `R15.` or the order of sections from a shipped agent file (`tests/agent_files/test_claude_agent_refusal.py`, `test_claude_agent_skills.py`, `test_claude_agent_texts.py`, `test_claude_agent_texts_check_red.py`, `test_claude_agent_texts_docs_slip.py`, and any other test whose only failure is this move) read them from `agents/system-prompt.md` instead and check the same text; the order of sections in an agent file loses `## Rules`."
- Tests: the changed modules above, and `tests/agent_files/test_shared_rules_system_prompt.py` for the criteria below.

## Acceptance criteria

1. `agents/system-prompt.md` holds a `## Rules` section with each of the rules R1 to R15 exactly once, in that order, after the orientation.
2. No shipped agent file under `agents/agents/` holds a `## Rules` heading or a line starting with `R1. ` to `R15. `.
3. Every shipped agent file's body has its sections in the order `## Role` (where present), `## Stage`, `## Lessons`, and each keeps, word for word, the text it held in those sections and before its first section.
4. Each of R1 to R15 in `agents/system-prompt.md` is word for word the rule as the shipped coder's file held it before this story, except that the opening paragraph's sentence on `Stage` and `Role` says that they stand in the `<role-instructions>` block.
5. The orientation of `agents/system-prompt.md` says that the rules apply to every agent in every stage and that the `<role-instructions>` block holds the instructions of the agent's role; it keeps the sentences on the `<work-item>` and `<context>` blocks.
6. `SYSTEM_PROMPT` equals the text of `agents/system-prompt.md`.
7. A run under each runtime (the Claude runtime's instructions file, the opencode runtime's agent `prompt`), started with the shipped agent home, receives the text of `agents/system-prompt.md` with the rules, and the run's first message holds no `## Rules` section: rows of one parametrized test, one per runtime.
8. `make check` stays green.
9. docs: the operator guide (`docs/operator-guide/agent-runtime.md`, the agent file and the system prompt) says that the rules every role shares stand in the system prompt file of the agent home, that an agent file holds only its role's own instructions, and that a project agent copied from an earlier shipped file may drop its `## Rules` section; the project guide's file on the agents area (`docs/project-guide/agents.md`) says where the shared rules stand and that `SYSTEM_PROMPT` equals the shipped file.

## Smoke test

```bash
grep -c '^## Rules' agents/system-prompt.md agents/agents/*.md
```
Expect: `agents/system-prompt.md:1`, then one line per agent file ending in `:0`.

```bash
grep -c '^R15\. ' agents/system-prompt.md
```
Expect: `1`

```bash
uv run python -c "from pathlib import Path; from factory.agents.domain.prompts import SYSTEM_PROMPT; print(SYSTEM_PROMPT == Path('agents/system-prompt.md').read_text(encoding='utf-8'))"
```
Expect: `True`

```bash
uv run pytest tests/agent_files/test_shared_rules_system_prompt.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names concrete files and their contents: `agents/system-prompt.md` and `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py`, both the orientation followed by `## Rules`; the seven `agents/agents/<name>.md` files without `## Rules`; the one reworded sentence (Stage/Role now stand in the `<role-instructions>` block); and the new test module `tests/agent_files/test_shared_rules_system_prompt.py`. The leave to change earlier tests is the human's decision 1 in `feature.md`. It names the five test files plus "any other test whose only failure is this move", which also covers `tests/agents/adapters/test_shipped_agents_effect.py`. Neither runtime changes: both already read `system_prompt_file` through `system_prompt_text` (`agent_launch.py`).
   - Criteria: each one is testable by one test function. 1: rules R1 to R15 exactly once each and in order. 2: no rules heading or `R<n>. ` line in an agent file. 3: section order and word-for-word bodies. 4: rule texts word for word, with the one sentence reworded; the existing pinned-text tests, moved to read from the system prompt by the leave, carry most of this. 5: what the orientation says. 6: `SYSTEM_PROMPT` equals the file, which decision 2 also requires. 7: one parametrized test with one row per runtime. The failing side of each "no `## Rules`" and "exactly once" rule is the same assertion. No Interface rule raises an error or validates input, so there are no further failing sides to cover. 8 (make check) and 9 (docs) come last.
   - Smoke test: four runnable commands: two `grep -c`, a `uv run python -c` that prints a boolean, and pytest on the new file. Each `Expect:` can be checked against the output. The pytest command passes no `-q`, which is right because `pyproject.toml` already has `addopts = "-q ..."`, so a summary line is printed.
   - Docs criterion: names what the operator and project-guide readers must know without dictating sentences: where the shared rules stand, what an agent file holds, that a copied project agent may drop `## Rules`, and that `SYSTEM_PROMPT` equals the shipped file. It names `docs/operator-guide/agent-runtime.md` and `docs/project-guide/agents.md`. The latter currently describes `## Rules` in every body (lines 280–281, 352) and will need updating.
   - Architecture: the text constant stays in the `agents` area's `domain` layer, and the shipped files stay in `agents/`. No new interface, dependency or wiring is needed; `wiring.py` already passes `agent_home / system-prompt.md` to both runtimes. The change to `CLAUDE.md`'s first paragraph is listed in `feature.md` as the human's own change after the merge, so it is not part of this story.
   - Scope: within F0060's first scope line (S0001). It does not touch the out-of-scope items: no story text in the system prompt and no `CLAUDE.md` carrying, which is S0002's. Route: `tests`, because the Interface changes `src/` and `agents/`, which the documenter may not write.
4. factory: started tests as vm.
5. tester: Wrote the tests for the shared rules moving into the system prompt. I also moved the earlier rule tests to read from `agents/system-prompt.md`, under the human's leave (decision 1 in `feature.md`).

   Criteria → tests (all in `tests/agent_files/test_shared_rules_system_prompt.py`):
   - criterion 1: `test_the_system_prompt_holds_each_rule_once_in_order_after_the_orientation`
   - criterion 2: `test_no_shipped_agent_file_holds_the_shared_rules` (one row per agent file)
   - criterion 3: `test_every_agent_file_keeps_its_own_sections_word_for_word_in_order` (one row per agent file). It checks the headings are `## Role` (where present), `## Stage`, `## Lessons`. It also checks a crc32 checksum of the text before the first section and of each section the file keeps, against values computed from the files before this story. I used crc32 integers rather than hex digests so that `make secrets` stays green without a baseline entry.
   - criterion 4: `test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word`. Every paragraph after the first must equal the coder's pre-story `## Rules` text. In the first paragraph, everything before and after the old sentence ("Stage-specific instructions are under `Stage` below; …") must be unchanged. The old sentence must be gone, and the sentence that replaces it must name `Stage`, `Role` and `<role-instructions>`.
   - criterion 5: `test_the_orientation_says_whom_the_rules_bind_and_where_the_role_stands`, four rows:
     - a sentence says the rules apply to every agent in every stage;
     - a sentence says the `<role-instructions>` block holds the role's instructions with the same weight;
     - the `<work-item>` sentence is kept word for word;
     - the `<context>` sentence is kept word for word.
   - criterion 6: `test_the_fallback_system_prompt_equals_the_shipped_file`. It passes today, since both texts are still the old ones, and it pins the change.
   - criterion 7: `test_a_run_gets_the_rules_in_the_system_prompt_and_none_in_its_first_message`, rows `claude` and `opencode`. Both use stand-ins, the shipped coder file and `system_prompt_file=SYSTEM_PROMPT_FILE`. The Claude row reads the instructions file and `-p`; the opencode row reads the agent `prompt` in the configuration and the message argument.
   - criteria 8 and 9: no test (`make check`; docs).

   Files created:
   - `tests/agent_files/test_shared_rules_system_prompt.py`
   - `tests/support/shared_rules_support.py`: the coder's `## Rules` paragraphs before the story, the old sentence, and the checksums of each agent file's own parts.

   Earlier tests changed under the leave. Each reads the rules from the system prompt through a new helper, `shared_rules()` in `tests/support/shipped_agents.py`, and checks the same text. Where a test was parametrized by agent name only to read the rules, it now takes no parameter and keeps its name.
   - `tests/agent_files/test_claude_agent_refusal.py` (the R14 line, once)
   - `tests/agent_files/test_claude_agent_skills.py` (R15 right after R14)
   - `tests/agent_files/test_claude_agent_texts.py`: the section order loses `## Rules`, and the two anchor tests now read the system prompt.
   - `tests/agent_files/test_claude_agent_texts_check_red.py` (no `check_red` in the shared rules)
   - `tests/agent_files/test_claude_agent_texts_docs_slip.py` (the R12 text, once)
   - `tests/agent_files/test_claude_settings_git.py` (the "You do not commit either" rule; the leave covers it as a test whose only failure is this move)

   `tests/agents/adapters/test_shipped_agents_effect.py` still passes after the move, so I did not change it.

   Test run (`uv run pytest -q` on the new file and the six changed files): the failures are what the coder must fix.
   - The agent files still hold `## Rules`.
   - The section order still includes `## Rules`.
   - The checksums don't match, because the opening text currently runs into the rules.
   - The system prompt has no `## Rules` section yet; in both runtime rows the system prompt's headings are `[]`.

   Every module imported; there were no collection errors. `make lint` is green. I skipped the type check, as the stage allows.

   Open: none.

   `lint`: lint: green (0.1 s)
6. factory: started doing as vm.
7. coder: Built the move. Four earlier test modules the tester did not change still fail, and each fails only because the rules left the agent files. The human's leave (decision 1 in `feature.md`, "any other test whose only failure is this move") covers them, so I end with `tests` and leave those changes to the tester.

   What I built (in the working tree):
   - `agents/system-prompt.md`: the orientation, then `## Rules`, then the coder's former rules word for word. The opening paragraph's sentence now reads: "Stage-specific instructions are under `Stage`, role-specific instructions under `Role`, both in the `<role-instructions>` block of your first message." The orientation now says that "The rules below apply to every agent in every stage." It also says that "The `<role-instructions>` block holds the instructions of your role, which add to these rules: follow them with the same weight." The `<work-item>` and `<context>` sentences are unchanged.
   - `src/factory/agents/domain/prompts.py`: `SYSTEM_PROMPT` is the same text, which I generated from the file.
   - `agents/agents/*.md` (all seven): the `## Rules` section is removed and nothing else changes. Before removing it I checked that the section was identical in all seven files.

   Main choice: in the orientation, the role sentence says the role's instructions "add to these rules", so that one sentence (split at `:`) names both `role-instructions` and `rules`. That keeps `test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is` passing. Alternative rejected: "holds the instructions of your role: follow them with the same weight as these rules". It breaks that earlier test, which would then need a change outside the leave.

   State: the new test module `tests/agent_files/test_shared_rules_system_prompt.py` and the six test modules the tester changed all pass. In `make check`, lint, types, layers, sast, secrets and licenses are green. `make test` is red only on these:

   1. `tests/agent_files/test_shipped_agents_r14.py::test_each_agent_holds_the_take_s_r14_once_and_no_kernel_promise` (all 7 rows): it reads `WRITE_PATHS_RULE` from each agent file. Change needed: check that line once in `shared_rules()` (the system prompt), and keep the "no kernel promise" and `$TMPDIR` checks on each agent file.
   2. `tests/agent_files/test_first_message_agent_files.py::test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message` (6 rows; coder passes): the sentence with "work item" and "first message" came from R6. Change needed: keep the READ_FIRST check on each agent file, and look for the "work item … first message" sentence in the system prompt's rules.
   3. `tests/agent_files/test_claude_agent_texts.py::test_body_names_every_decision_of_its_stage_in_inline_code` (reviewer, documenter, smoke-tester): `` `question` `` was named in those bodies only by R2/R8 (`E AssertionError: assert ['question'] == []`, test_claude_agent_texts.py:198). Change needed: count a decision as named when it appears in the body or in `shared_rules()`.
   4. `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: it pins the whole reviewer body by crc32 (`E AssertionError: assert 1092243890 == 3903663111`, test_claude_agent_texts_review_groups.py:97). Change needed: drop the `## Rules` section from the reconstructed earlier body before taking the checksum, or pin the new value.

   After those changes no code needs to change. Refactor: nothing to change. The constant was generated from the file, and the agent files lost only their section.

   Noticed, not touched: `docs/project-guide/agents.md` and `docs/operator-guide/agent-runtime.md` still describe `## Rules` in every agent file. The documenter handles that under criterion 9.
8. factory: started tests as vm.
9. tester: Made the four test changes that the coder's entry 7 names, under the human's leave (decision 1 in `feature.md`, "any other test whose only failure is this move"). Every test keeps its name and checks the same text. The only difference is that the shared rules are now read from `agents/system-prompt.md`, through `shared_rules()` in `tests/support/shipped_agents.py`.

   Earlier test files changed:
   - `tests/agent_files/test_shipped_agents_r14.py::test_each_agent_holds_the_take_s_r14_once_and_no_kernel_promise`: `WRITE_PATHS_RULE` must now appear exactly once in `shared_rules()`. The checks for no kernel promise and no `$TMPDIR` run on each agent file and on the shared rules, so they cover the same text as before.
   - `tests/agent_files/test_first_message_agent_files.py::test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message`: the `READ_FIRST` patterns are still checked on each agent file. The sentence naming "work item" and "first message", which came from R6, is now looked for in `shared_rules()`.
   - `tests/agent_files/test_claude_agent_texts.py::test_body_names_every_decision_of_its_stage_in_inline_code`: a decision counts as named when it appears in inline code in the agent's body or in `shared_rules()`.
   - `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: before the earlier body is rebuilt, the pre-move `## Rules` section (`RULES_BEFORE` from `tests/support/shared_rules_support.py`) is put back right before `## Role`. The pinned CRC-32 (3903663111) did not change and still matches.

   Rejected: pinning a new CRC value for the reviewer body. Putting the old rules back keeps the test checking against the same earlier text.

   Run: `uv run pytest -q tests/agent_files/ tests/agents/adapters/test_shipped_agents_effect.py` all passed. `make lint` is green. No files were created, and no module failed to import.

   Open: none. The coder's entry says no code needs to change after these tests.

   `lint`: lint: green (0.1 s)
10. factory: started doing as vm.
11. coder: The build from entry 7 is unchanged and was already committed on the branch. The tester's four test changes from entry 9 now pass against it, and no code needed to change.

    What I built (from entry 7, checked again in this run):
    - `agents/system-prompt.md`: the orientation, then `## Rules` with the opening paragraphs and R1 to R15, word for word as the coder's file held them. The one exception is the opening sentence, which now reads: "Stage-specific instructions are under `Stage`, role-specific instructions under `Role`, both in the `<role-instructions>` block of your first message."
    - `src/factory/agents/domain/prompts.py`: `SYSTEM_PROMPT` matches the file byte for byte (checked with `diff` against the imported constant).
    - `agents/agents/{intake,tester,coder,reviewer,documenter,smoke-tester,acceptance-reviewer}.md`: the `## Rules` section is removed and nothing else changed.

    Run:
    - `uv run pytest -q tests/agent_files/ tests/agents/adapters/test_shipped_agents_effect.py`: all passed.
    - `make check`: green (lint, types, layers, sast, secrets, licenses, test at 99.21 % coverage).

    Main choice (from entry 7): the orientation's role sentence says the role's instructions "add to these rules: follow them with the same weight". That way one sentence names both blocks, and `test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is` keeps passing unchanged. Rejected: "follow them with the same weight as these rules" after a colon, because it would have broken that test outside the leave.

    Refactor: nothing to change. The diff is the moved section, the constant generated from the file and the reworded orientation.

    Noticed, not touched:
    - The orientation now says "The rules below apply to every agent in every stage." The rules' first paragraph, kept word for word, repeats "These rules apply to every agent in every stage." The repetition is deliberate: criteria 4 and 5 each ask for one of the two sentences.
    - `docs/operator-guide/agent-runtime.md` and `docs/project-guide/agents.md` still say every agent file holds `## Rules`. Criterion 9 leaves that to the documenter.

    The journal did not change the meaning of the task, so `## Description` stays as it is.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
12. factory: started review as vm.
13. reviewer: Round 0 review of `git diff develop...HEAD -- . ':!factory'`. Groups 1 to 5 and item 6 are all checked below.

    Group 1 (criteria): each of criteria 1 to 7 has a test in `tests/agent_files/test_shared_rules_system_prompt.py`, and each test checks the criterion it is named after:
    - Criterion 1: R1 to R15 appear once, in order, after a non-empty orientation.
    - Criterion 2: one row per agent file.
    - Criterion 3: the section order, plus a crc32 of the opening and of each section the file keeps.
    - Criterion 4: the paragraphs after the first are equal to `RULES_BEFORE`, and the first paragraph is checked around the replaced sentence.
    - Criterion 5: four rows.
    - Criterion 6: the fallback text equals the file.
    - Criterion 7: one parametrized test with a `claude` row and an `opencode` row.

    I checked the pinned data against `develop`. For all seven files, `own_parts` of each body on `develop` equals `PARTS_BEFORE`, and each file's `## Rules` section on `develop` equals `"\n\n".join(RULES_BEFORE)`. So criteria 3 and 4 pin the real earlier text. The "exactly once" limit fails on both sides through `numbers == list(range(1, 16))`. The journal (entry 11) says `make check` was green after the coder.

    Group 2 (architecture): `SYSTEM_PROMPT` stays a constant in `factory.agents.domain.prompts`. There is no new import, interface or wiring, and no runtime changes. Nothing to report.

    Group 3 (security): no markers, secrets or command building. The hex-like values are crc32 integers. Nothing to report.

    Group 4 (quality), `src/`: the constant matches the file, and the comment at `prompts.py:29` is still true. Nothing to report.

    Group 5 (hygiene): the journal names the main choice for the role sentence and the rejected wording. The Description matches what was built, and criterion 9 still says what the documenter must write.

    Findings (round 0, so copied helpers in the new test module still count):
    1. `tests/agent_files/test_shared_rules_system_prompt.py:71` `_rules()`: a second copy of `shared_rules()` in `tests/support/shipped_agents.py:170`, which this same diff adds. Fix: drop `_rules()` and use `shared_rules()`.
    2. `tests/agent_files/test_shared_rules_system_prompt.py:83` `_headings` and `:36` `_WITHOUT_ROLE`: copies of `_headings` (`tests/agent_files/test_claude_agent_texts.py:151`) and `_WITHOUT_ROLE` (`test_claude_agent_texts.py:17`). Fix: move both to `tests/support/shipped_agents.py` under the standing leave, and use them from there in both modules.
    3. `tests/agent_files/test_shared_rules_system_prompt.py:47` `_CLAUDE_REPLY` copies `REPLY` from `tests/support/claude_stand_in.py:16`; only the numbers differ, and the test does not depend on them. In the same file, `:208` `Step(stdout=REPLY_EVENTS)` is `REPLY` from `tests/support/opencode_stand_in.py:364`. Fix: import `REPLY` from each support module, as `tests/support/container_extra_support.py:17,22` does.

    Earlier tests changed by the diff:
    - `tests/agent_files/test_claude_agent_refusal.py`: the human's leave (story Interface, decision 1 of `feature.md`).
    - `tests/agent_files/test_claude_agent_skills.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts_check_red.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts_docs_slip.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts_review_groups.py`: the human's leave, "any other test whose only failure is this move" (journal entries 7 and 9).
    - `tests/agent_files/test_claude_settings_git.py`: the human's leave, "any other test whose only failure is this move" (journal entry 5).
    - `tests/agent_files/test_first_message_agent_files.py`: the human's leave, "any other test whose only failure is this move" (journal entries 7 and 9).
    - `tests/agent_files/test_shipped_agents_r14.py`: the human's leave, "any other test whose only failure is this move" (journal entries 7 and 9).
    - `tests/support/shipped_agents.py`: none needed; it only adds the helper `shared_rules()`.
14. factory: started doing as vm.
15. coder: Round 1. All three of the reviewer's findings in entry 13 are copied test helpers. Fixing them means changing tests, which the coder may not do. `CLAUDE.md` gives a standing leave to move a shared test helper, so I am handing these to the tester and changing no code. Each copy is still at the line the reviewer named.

    Changes for the tester (every test keeps its name and checks the same thing):
    1. In `tests/agent_files/test_shared_rules_system_prompt.py`, remove `_rules()` (line 71) and call `shared_rules()` from `tests/support/shipped_agents.py:170` in its place.
    2. Move `_headings` (`tests/agent_files/test_claude_agent_texts.py:151`) and `_WITHOUT_ROLE` (`test_claude_agent_texts.py:17`) into `tests/support/shipped_agents.py`. Then use them from there in `test_claude_agent_texts.py` and in `test_shared_rules_system_prompt.py`, and delete the copies at lines 36 and 83 of `test_shared_rules_system_prompt.py`. This is the standing leave; the tester's entry names `test_claude_agent_texts.py` as an earlier test file it changed.
    3. In `test_shared_rules_system_prompt.py`, remove `_CLAUDE_REPLY` (line 47) and import `REPLY` from `tests/support/claude_stand_in.py:16` instead. Replace `Step(stdout=REPLY_EVENTS)` (line 203) with `REPLY` from `tests/support/opencode_stand_in.py:364`, the way `tests/support/container_extra_support.py:17,22` does. Both modules export the name `REPLY`, so one of them needs an import alias.

    Rejected: changing these tests myself, because the coder never edits tests (R9).

    Code: no change. The build from entries 7 and 11 (`agents/system-prompt.md`, `src/factory/agents/domain/prompts.py`, the seven `agents/agents/*.md`) stays as it is. The reviewer found nothing in groups 2 to 5. I did not run the tests or `make check` this round, because I changed no files.

    What the journal changed: nothing in the task's meaning, so `## Description` stays.

    Noticed, not touched: the docs for criterion 9 are still the documenter's.
16. factory: started tests as vm.
17. tester: Round 1. Made the three moves that the coder's entry 15 names, which answer the reviewer's findings in entry 13. All three fall under CLAUDE.md's standing leave to move a shared test helper. Every test keeps its name and checks the same thing.

    1. `tests/agent_files/test_shared_rules_system_prompt.py`: removed `_rules()` and now uses `shared_rules()` from `tests/support/shipped_agents.py`. With it, the now-unused `section_text` import is gone.
    2. Moved `_headings` and `_WITHOUT_ROLE` into `tests/support/shipped_agents.py` as `headings()` and `WITHOUT_ROLE`. Both test modules now use them from there, and the copies in each are deleted. In the first test of the new module, the local variable `headings` became `found` so that it no longer shadows the helper.
    3. `test_shared_rules_system_prompt.py`: removed `_CLAUDE_REPLY` and now imports `REPLY as CLAUDE_REPLY` from `tests/support/claude_stand_in.py`. Replaced `Step(stdout=REPLY_EVENTS)` with `REPLY as OPENCODE_REPLY` from `tests/support/opencode_stand_in.py`, the way `tests/support/container_extra_support.py` does it.

    Earlier test file changed under the standing leave: `tests/agent_files/test_claude_agent_texts.py`, which now uses `headings` and `WITHOUT_ROLE` from support. Also changed: `tests/agent_files/test_shared_rules_system_prompt.py` (this story's) and `tests/support/shipped_agents.py` (gains the helper and the constant). No files created.

    Criteria → tests: unchanged from entry 5, all in `tests/agent_files/test_shared_rules_system_prompt.py`:
    - criterion 1: `test_the_system_prompt_holds_each_rule_once_in_order_after_the_orientation`
    - criterion 2: `test_no_shipped_agent_file_holds_the_shared_rules`
    - criterion 3: `test_every_agent_file_keeps_its_own_sections_word_for_word_in_order`
    - criterion 4: `test_the_rules_in_the_system_prompt_are_the_coders_rules_word_for_word`
    - criterion 5: `test_the_orientation_says_whom_the_rules_bind_and_where_the_role_stands`
    - criterion 6: `test_the_fallback_system_prompt_equals_the_shipped_file`
    - criterion 7: `test_a_run_gets_the_rules_in_the_system_prompt_and_none_in_its_first_message`

    Run: `uv run pytest -q tests/agent_files/` together with the shared-helper guards (`tests/guards/test_shared_test_helpers.py`, `test_shared_imports.py`, `test_shared_constants.py`): all passed. Every module imported. Type check skipped, as the stage allows. Open: none.

    `lint`: lint: green (0.1 s)

    `lint`: lint: green (0.2 s)
18. factory: started doing as vm.
19. coder: Round 1. The tester's entry 17 moved the three copied test helpers that the reviewer found in entry 13. No code needed to change, and I changed none.

    What I built: the build from entries 7 and 11 is unchanged.
    - `agents/system-prompt.md`: the orientation, then `## Rules` with R1 to R15. The text is word for word the coder's earlier rules, except for the sentence on `Stage` and `Role`, which now says they stand in the `<role-instructions>` block.
    - `src/factory/agents/domain/prompts.py`: `SYSTEM_PROMPT` is the same text as the file.
    - `agents/agents/*.md` (all seven): the `## Rules` section is removed and nothing else changed.

    Run:
    - `uv run pytest -q tests/agent_files/test_shared_rules_system_prompt.py tests/agent_files/test_claude_agent_texts.py`: all passed.
    - `make check`: green, with coverage at 99.21 %.

    Main choice (from entry 7): the orientation's role sentence says the role's instructions "add to these rules: follow them with the same weight". That keeps `test_first_message_agent_files.py::test_the_system_prompt_names_both_blocks_and_what_each_one_is` passing unchanged. I rejected "follow them with the same weight as these rules" after the colon, because that wording breaks the same test, and the human's leave does not cover a change to it.

    Refactor: nothing to change, since this round left the code diff as it was.

    What the journal changed: nothing in the task's meaning, so `## Description` stays.

    Noticed, not touched: `docs/operator-guide/agent-runtime.md` and `docs/project-guide/agents.md` still say that every agent file holds `## Rules`. Criterion 9 leaves those changes to the documenter.

    `duplicates`: duplicates: 7 new, 39 known, 4 gone
20. factory: started review as vm.
21. reviewer: Round 1 review of `git diff develop...HEAD -- . ':!factory'`. I read the full diff of `src/`, the new test module, `tests/support/` and every earlier test file the diff changes.

    no findings

    - Round 0 findings (entry 13): all three are fixed. `tests/agent_files/test_shared_rules_system_prompt.py` now uses `shared_rules()`, `headings()` and `WITHOUT_ROLE` from `tests/support/shipped_agents.py`. It also imports `REPLY` from `tests/support/claude_stand_in.py` and `tests/support/opencode_stand_in.py` under aliases. The local copies are gone, and `test_claude_agent_texts.py` uses the moved helpers too.
    - Group 1 (criteria): criteria 1 to 7 still each have their test, and each test checks what its criterion says. `SYSTEM_PROMPT` in `src/factory/agents/domain/prompts.py` is the same text as `agents/system-prompt.md`: the orientation, then `## Rules`, with only the Stage/Role sentence reworded. Entry 19 records `make check` green after the coder.
    - Group 2 (architecture): nothing to report. The constant stays in `factory.agents.domain`, and no runtime, interface or wiring changed.
    - Group 3 (security): nothing to report. There are no markers and no secrets, and the checksums are crc32 integers.
    - Group 4 (quality): nothing to report. The comment at `prompts.py:29` is still true.
    - Group 5 (hygiene): nothing to report. The journal names the main choice (the "add to these rules" wording) and the wording that was rejected. The Description matches what was built. Criterion 9 still says what the documenter must write, and `docs/project-guide/agents.md:280-281,352` still describes `## Rules` in every body for the documenter to change.

    Notes:
    1. `tests/agent_files/test_shared_rules_system_prompt.py:59` `_sentences`: a near-copy of `_sentences` in `tests/agent_files/test_first_message_agent_files.py:17` and `tests/agent_files/test_context_system_prompt.py:11`. It splits only at `.`, where the others also split at `;` and `:`. That is needed because the kept `<work-item>` sentence contains a colon, so this is a variant, not a second copy.

    Earlier tests changed by the diff:
    - `tests/agent_files/test_claude_agent_refusal.py`: the human's leave (story Interface, decision 1 in `feature.md`).
    - `tests/agent_files/test_claude_agent_skills.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts.py`: the human's leave (same), and the standing leave to move a shared test helper for `headings` and `WITHOUT_ROLE` (entry 17).
    - `tests/agent_files/test_claude_agent_texts_check_red.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts_docs_slip.py`: the human's leave (same).
    - `tests/agent_files/test_claude_agent_texts_review_groups.py`: the human's leave, "any other test whose only failure is this move" (entries 7 and 9).
    - `tests/agent_files/test_claude_settings_git.py`: the human's leave, "any other test whose only failure is this move" (entry 5).
    - `tests/agent_files/test_first_message_agent_files.py`: the human's leave, "any other test whose only failure is this move" (entries 7 and 9).
    - `tests/agent_files/test_shipped_agents_r14.py`: the human's leave, "any other test whose only failure is this move" (entries 7 and 9).
    - `tests/support/shipped_agents.py`: the standing leave to move a shared test helper (it gains `headings`, `WITHOUT_ROLE` and the new `shared_rules()`; no earlier test it held changed).
22. factory: started docs as vm.
23. documenter: Round 1 docs. I wrote the docs that criterion 9 asks for and fixed the text the cross-read found stale. I changed only documents, so I did not run `make check`, as the lesson says.

    Files changed:
    - `docs/operator-guide/agent-runtime.md`:
      - *The agent files*: an agent file's body now holds only its role's own instructions (role, stage, lessons). The rules every role shares (the opening paragraphs and R1 to R15) stand once, in the `## Rules` section of the agent home's `system-prompt.md`.
      - *A project's own agents*: a project agent copied from an earlier shipped file still carries `## Rules`. That only repeats the rules, so the copy may drop the section.
      - *The shipped agents and settings*: the system prompt is an orientation followed by the shared `## Rules`. Each agent file reaches the run in the `<role-instructions>` block.
    - `docs/project-guide/agents.md`:
      - *The system prompt and the first message*: the system prompt now holds the orientation and then the shared `## Rules`. The `<role-instructions>` block holds the role's instructions, which add to the rules and carry the same weight. `SYSTEM_PROMPT` equals the shipped file byte for byte, and a change to one is made to the other in the same story.
      - *The shipped agents*: the list of body sections loses `## Rules`. A new paragraph says no body holds `## Rules`. The bullets on the rules' opening paragraphs, R14 and R15 moved under it and now say the rules stand in the system prompt. A bullet names `tests/agent_files/test_shared_rules_system_prompt.py` and what it checks.
      - The sentence "Among the lessons that go beyond those two" now reads "the two every body has", since the rules block now stands between it and the list it refers to.
      - The settings bullet on `git commit` now says the shared `## Rules` in the system prompt say "You do not commit either".
    - `docs/decisions.md`, the introduction only: "the agents' `## Rules`" now adds that they stand in `agents/system-prompt.md`. I added no new decision entry and no "Why" or "Rejected" line.

    Cross-read and found current:
    - The rest of `docs/operator-guide/agent-runtime.md`. *The cached start* already says every run begins with the common system prompt, and the fallback paragraph still holds.
    - `docs/project-guide/agents.md`: the runtime sections (instructions file, opencode `prompt`) and the test list of the system-prompt section.
    - `docs/project-guide/style.md`: its `## Rules for all documents` is a different heading.
    - `README.md`.

    `make documents` is red, and not because of this story. Every run ends with `docs/project-guide/agents.md:224: the example did not end in 60 s` and `docs/project-guide/watching.md:152: the example did not end in 60 s`, followed by `Report (not checked yet)`.
    - I ran it three times. One of those runs was with my three edits stashed (develop's docs text): same two lines.
    - Both examples are unchanged by this story. Both finish in under a second when run by hand, including under `env -i` with an empty HOME. So the time-out is in this machine's run of the document check, not in the documents.
    - I did not look further. The factory runs `make documents` after this stage, and that run decides.

    Stale text noticed, not mine: none.

    Findings: none.

    `guides`: guides: green (9.6 s)
    `secrets`: secrets: green (2.1 s)
24. factory: Stage docs stalled (attempt 1 of 2): a check is red after the stage: `documents`
    Bytecode compiled 4164 files in 85ms
    sync: green (0.1 s)
    Bytecode compiled 4164 files in 60ms
25. factory: started docs as vm.
26. documenter: Round 1 docs, second attempt after the `documents` stall (entry 24). I changed no files in this run. The docs from entry 23 already meet criterion 9:
    - `docs/operator-guide/agent-runtime.md:328,334,359`: the shared rules stand in the agent home's `system-prompt.md`, an agent file holds only its role's instructions, and a copied project agent may drop `## Rules`.
    - `docs/project-guide/agents.md:30,284,289,356`: where the shared rules stand, and that `SYSTEM_PROMPT` equals the shipped file byte for byte.
    - `docs/decisions.md`: introduction only.

    I cross-read these again and found them current.

    Question: `make documents` is red, and the cause is this machine's network, not the documents. How should the stage go on?

    What I found:
    - `make documents` ran again in this run and failed with `docs/operator-guide/machine.md:187`, `docs/project-guide/README.md:401` and `docs/project-guide/watching.md:152: the example did not end in 60 s`. Entry 23's runs timed out on different examples (`agents.md:224`, `watching.md:152`). This story changed none of these examples.
    - The cause is the check's setup on this machine. `ProcessExampleRunner` (`src/factory/shared/adapters/document_examples.py`) runs each document's examples in a new `git export` of HEAD (`CheckoutFixture`), under `env -i` with an empty HOME. So the first `uv run` of each document builds a new `.venv` from an empty uv cache and downloads every dependency.
    - I reproduced this by hand: the `watching.md:152` example in a fresh `git archive HEAD` copy with an empty HOME took 3 min 10 s wall time (user CPU 6.5 s, so almost all of it was download wait), against the 60 s `EXAMPLE_TIME_LIMIT`. In the warm checkout the same command takes 0.2 s.
    - Entry 23 saw the same failure with the story's docs edits stashed, so `develop`'s documents fail in the same way.

    Options:
    (a) Retry the docs stage later, when the network or uv's package source is fast enough for a cold `uv sync` within 60 s. Nothing in the branch changes.
    (b) You run `make documents` on a machine with a fast package source, or confirm the docs by reading them, and let the story move on to the smoke test.
    (c) A separate story makes the document check's examples reuse a warm uv cache or `.venv`, or raises the limit for the first command. That changes code, so it is outside this story and outside my write paths.

    I would choose (b) for this story and (c) as a backlog story. With (b) the story moves on, and (c) stops the docs stage of every later story from failing in the same way. I ended with `question` rather than `smoke-test` because another forward decision would only be held red again by the same check (this is attempt 2 of 2).

    Stale text noticed, not mine: none.
27. 2026-11-08 human: (a) Retry. The cause is the package index's speed, not the documents: a cold `uv run` in a fresh copy took 99 s at one moment and 7 s a few minutes later on the VM. The fix (the examples share the check's uv cache) is F0061, kept in the backlog for later.
28. factory: started docs as vm.
29. documenter: Round 1 docs, third run, after the human's answer in entry 27 to retry. I changed no files in this run. The docs from entry 23 already meet criterion 9, and I checked them again on the branch:
    - `docs/operator-guide/agent-runtime.md:328,334,359`: the shared rules stand once in the agent home's `system-prompt.md`, an agent file holds only its role's own instructions, and a project agent copied from an earlier shipped file may drop its `## Rules` section.
    - `docs/project-guide/agents.md:30,284,289,356`: the shared rules stand in the system prompt and in no agent file, and `SYSTEM_PROMPT` equals the shipped file byte for byte.
    - `docs/decisions.md`: the introduction only, as in entry 23 (no new entry, no "Why" or "Rejected" line).

    `make documents` is still red. I ran it twice in this run. Both runs failed on the same line and nothing else: `docs/project-guide/README.md:401: the example did not end in 60 s`. The earlier runs (entries 23 and 26) timed out on other examples. This story changed none of them. The cause is the one the human named in entry 27: a cold `uv` cache in each example's fresh copy has to download packages, and the download speed varies (F0061 holds the fix). Following the human's choice (a), I end forward and leave the decision to the factory's own run of `make documents` after this stage.

    I did not run `make check`, because this run changed no files and the earlier runs changed only documents.

    Cross-read and found current: the rest of `docs/operator-guide/agent-runtime.md` and of `docs/project-guide/agents.md`, `docs/project-guide/style.md`, `README.md`.

    Stale text I noticed that is not mine to fix: none.

    Findings: none.

    `guides`: guides: green (9.7 s)
    `secrets`: secrets: green (2.1 s)
30. factory: Stage docs stalled (attempt 2 of 2): a check is red after the stage: `documents`
    Bytecode compiled 4164 files in 88ms
    sync: green (0.1 s)
    Bytecode compiled 4164 files in 50ms
31. factory: Stage docs stalled 2 times. The last time: Stage docs stalled (attempt 2 of 2): a check is red after the stage: `documents`
    Bytecode compiled 4164 files in 88ms
    sync: green (0.1 s)
    Bytecode compiled 4164 files in 50ms

    Comment anything to retry: the attempts go back to 0 and the stage runs again. Close the pull request to discard the story instead: it goes back to the backlog as you wrote it, and its branch and bill are deleted.
32. 2026-11-08 human: Retry. The package index is fast again at the moment (a cold `uv run` took 3 to 5 s at 21:55 UTC; 70 to 99 s at other times this evening).
33. factory: started docs as vm.
34. documenter: Round 1 docs, fourth run, after the human's retry in entry 32. I changed no files in this run. The docs from entry 23 still meet criterion 9, and I checked them again on the branch:
    - `docs/operator-guide/agent-runtime.md:328,334,359`: the rules every role shares stand once, in the `## Rules` section of the agent home's `system-prompt.md`. An agent file holds only its role's own instructions, and a project agent copied from an earlier shipped file may drop its `## Rules` section.
    - `docs/project-guide/agents.md:30,284,289,356`: the shared rules stand in the system prompt and in no agent file, and `SYSTEM_PROMPT` equals the shipped file byte for byte.
    - `docs/decisions.md`: only the introduction changed, as in entry 23. There is no new entry, so no "Why" or "Rejected" line was written.

    `make documents` is now green and ended with `documents ok (118.0 s)`. Its only other output was the usual `not run (vm)` / `not run (suite)` lines for `install.md:27,35`, `records.md:53` and `pipeline.md:142`. The red runs in entries 23 to 30 timed out because the package index was slow, as the human said in entry 27 (F0061 holds the fix). This run did not time out.

    I did not run `make check`, because this run changed no files and the earlier runs changed only documents.

    Cross-read and found current: the rest of `docs/operator-guide/agent-runtime.md` and of `docs/project-guide/agents.md`, `docs/project-guide/style.md`, and `README.md`.

    Stale text noticed that is not mine to fix: none.

    Findings: none.

    `guides`: guides: green (10.0 s)
    `secrets`: secrets: green (2.2 s)
    `documents`: documents ok (65.8 s)
35. factory: started smoke-test as vm.
36. smoke-tester: Smoke test, round 1. I ran the four commands from the repository root, as written and in order. Each output met its `Expect:` line.

    1. `grep -c '^## Rules' agents/system-prompt.md agents/agents/*.md`: met. `system-prompt.md:1`, then one line per agent file, each ending in `:0`.
    ```
    agents/system-prompt.md:1
    agents/agents/acceptance-reviewer.md:0
    agents/agents/coder.md:0
    agents/agents/documenter.md:0
    agents/agents/intake.md:0
    agents/agents/reviewer.md:0
    agents/agents/smoke-tester.md:0
    agents/agents/tester.md:0
    ```

    2. `grep -c '^R15\. ' agents/system-prompt.md`: met.
    ```
    1
    ```

    3. `uv run python -c "... print(SYSTEM_PROMPT == Path('agents/system-prompt.md').read_text(encoding='utf-8'))"`: met.
    ```
    Bytecode compiled 4164 files in 88ms
    True
    ```

    4. `uv run pytest tests/agent_files/test_shared_rules_system_prompt.py`: met. The summary line shows only `passed`.
    ```
    .......................                                                  [100%]
    23 passed in 0.07s
    ```

    I checked the criteria against the files once more:
    - `agents/system-prompt.md` holds the orientation and then `## Rules`, with R1 to R15 once each and in order (lines 13 to 41).
    - The orientation says that "The rules below apply to every agent in every stage" and that the `<role-instructions>` block holds the instructions of the role, to be followed with the same weight.
    - The opening rule sentence now places `Stage` and `Role` in the `<role-instructions>` block.
    - Every agent file's headings are `## Role` (where present), `## Stage`, `## Lessons`.

    The smoke test contradicts none of the criteria.

    Observation, not a finding: this run's own `<role-instructions>` still held `## Rules`. That is expected, because the factory sends the agent files from its installed agent home, which does not hold this branch's change yet.

    Findings: none.

    `check`: check: green
