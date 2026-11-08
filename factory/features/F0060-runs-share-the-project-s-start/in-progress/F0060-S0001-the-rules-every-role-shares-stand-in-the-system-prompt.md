---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 678
comments_read: []
handed_over: null
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
