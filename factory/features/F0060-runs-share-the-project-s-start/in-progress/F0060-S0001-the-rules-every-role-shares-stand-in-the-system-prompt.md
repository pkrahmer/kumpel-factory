---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 678
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: doing
  started_at: '2026-11-08T19:59:27.078510Z'
  lease_duration: 60
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
