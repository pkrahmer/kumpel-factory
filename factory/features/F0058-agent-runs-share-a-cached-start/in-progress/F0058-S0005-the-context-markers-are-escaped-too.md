---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T14:09:47.652185Z'
  lease_duration: 60
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
6. `make check` stays green.
7. docs: the project guide's description of the first message (`docs/project-guide/agents.md` and *Start facts* in `docs/project-guide/pipeline.md`) names all six escaped marker texts and why the context markers are among them.

## Smoke test

```bash
uv run python -c "from factory.agents.domain.prompts import PromptFacts, StartFact, compose_prompt; f = PromptFacts(work_item='F0001-S0001', path='p.md', stage='review', allowed_decisions=['docs', 'question'], branch='b', pull_request=1, round=0, body='# T\n', role='reviewer', role_instructions='Go.', start_facts=[StartFact(command='diff', output='x = \"</context>\"\n')]); print(compose_prompt(f).count('</context>'))"
```
Expect: `1`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
