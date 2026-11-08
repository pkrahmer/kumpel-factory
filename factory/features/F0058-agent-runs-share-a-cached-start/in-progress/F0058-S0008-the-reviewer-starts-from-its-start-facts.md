---
stage: tests
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 669
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: tests
  started_at: '2026-11-08T15:24:42.349120Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T15:24:09.916753Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T15:24:09.924510Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T15:24:37.662734Z'
  stage: intake
  run: 16e40619ab6f4346b69c103c362767f9
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T15:24:42.349120Z'
  stage: tests
---

# The reviewer starts from its start facts

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

Since F0058-S0004 and the human's change after it, the stages `review` and `docs-review` get the branch's diff as a start fact: a `<context>` block in the first message, gathered by the factory before the agent starts. The common system prompt says the agent need not gather these facts again. The shipped reviewer's instructions still say the opposite. *Stage* step 1 of `agents/agents/reviewer.md` reads "Read the diff in your first command", and step 1 of its *docs-review* subsection reads "Read `git diff develop...HEAD -- README.md docs operator/README.md` in your first command". A reviewer that follows its rules spends the turn the start fact was built to save. The human's measurement run against the 2026-11-08 baseline would count that turn. After this story, both steps tell the reviewer to read the diff from its `<context>` block when the first message holds one. The reviewer runs the diff command itself only in three cases: no block holds the diff, the block says `failed:`, or the block ends in the cut line. The command stays in each step as that fallback, since a project may give its stages no `context`. Everything else in the reviewer's instructions stays as it is, and so do the other agents. The documenter gets only the changed files' names (`facts-changes`) and still reads the diff itself. The tester's "`git ls-files` lists them" is a hint, not an order.

## Interface

No module under `src/factory/` changes. The story changes one shipped agent file, `agents/agents/reviewer.md` (the coder's write path `agents/*`):

- *Stage* step 1 keeps its scope (`git diff develop...HEAD -- . ':!factory'`), its rules on generated and lock files, and its sentences on the Makefile and `make check`. It no longer says "Read the diff in your first command". It says instead that the diff is in the first message's `<context>` block when one holds it, and that the reviewer runs the command only when no block holds it, when its block says `failed:`, or when its block is cut.
- *docs-review* step 1 says the same of `git diff develop...HEAD -- README.md docs operator/README.md`, and no longer says "in your first command".
- Neither step names a project's command (`facts-diff`): the shipped agent file serves every project, and the factory knows only the names a stage's `context` lists.

Tests, mirroring the files under `tests/agent_files/`: a new `tests/agent_files/test_reviewer_start_facts.py`.

Earlier tests this story changes: `tests/agent_files/test_claude_agent_texts_review_groups.py` (the strings `review_reads_the_diff` and `docs_review_reads_the_diff`, through which it rebuilds the earlier text of the reviewer) and `tests/agent_files/test_claude_agent_texts_docs_route.py` (`DOCS_DIFF` and the steps that quote it). `feature.md` gives no leave for them. The human gives it, or refuses it, when refining this story, and the leave's words then stand here.

The human's leave for earlier tests: this story may change `tests/agent_files/test_claude_agent_texts_review_groups.py` (the strings `review_reads_the_diff` and `docs_review_reads_the_diff`) and `tests/agent_files/test_claude_agent_texts_docs_route.py` (`DOCS_DIFF` and the steps that quote it) as far as the reviewer's new wording needs, and nothing else in them.

## Acceptance criteria

1. In `agents/agents/reviewer.md`, *Stage* step 1 and *docs-review* step 1 each name the `<context>` block as where the diff is. Each also names the three cases in which the reviewer runs the command itself: no block holds the diff, the block says `failed:`, or the block is cut. Each row checks one step for `<context>`, `failed:` and `cut`.
2. Neither step still says "in your first command", and each still holds its own diff command (`git diff develop...HEAD -- . ':!factory'` and `git diff develop...HEAD -- README.md docs operator/README.md`). The two steps are the rows of one parametrized test, which also holds the rows of criteria 1 and 3.
3. Neither step names `facts-diff` or any other project command.
4. `make check` stays green.
5. docs: the project guide's agent table (`docs/project-guide/agents.md`, the `reviewer` rows for `review` and `docs-review`) says that the reviewer reads the diff from its start fact and runs it only as the fallback; the operator guide and `docs/decisions.md` need nothing, since the start facts' reason is already there.

## Smoke test

```bash
grep -c 'in your first command' agents/agents/reviewer.md
```
Expect: `0`.

```bash
grep -c '<context>' agents/agents/reviewer.md
```
Expect: a number of at least `2`.

```bash
uv run pytest tests/agent_files/test_reviewer_start_facts.py 2>&1 | tail -1
```
Expect: a line ending in `passed` with no `failed`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names the one file that changes, `agents/agents/reviewer.md` (the coder's write path `agents/*`). I checked both passages: *Stage* step 1 (line 81, "Read the diff in your first command") and *docs-review* step 1 (line 91, "... in your first command"). It says what each step keeps (the scope command, the generated/lock-file rules, the Makefile and `make check` sentences), what each loses, and the three fallback cases. No module under `src/factory/` changes. It names the new test `tests/agent_files/test_reviewer_start_facts.py` and the two earlier tests it changes. The human's leave for them is written into the story (`review_reads_the_diff` and `docs_review_reads_the_diff` in `test_claude_agent_texts_review_groups.py` lines 70-92; `DOCS_DIFF` in `test_claude_agent_texts_docs_route.py` line 13). Route: `tests`, because the changed path is outside the documenter's paths.
   - Criteria: one parametrized test over the two steps can check each of 1-3. A row checks for `<context>`, `failed:` and `cut`, for the absence of "in your first command", for its own diff command, and for the absence of `facts-diff`. The refused sides are stated as absences (2, 3) and pass with the current text only for 3, so the rule has both sides. 4 and 5 close the list.
   - Smoke test: runnable. `grep -c` gives counts that can be checked (`0`, and at least `2`; the file will hold the literal `<context>`, which is only escaped in this message). The pytest command passes no `-q`, since `addopts` already sets `-q`, so the `passed` summary line prints.
   - Docs criterion: names what the reader must know (the reviewer reads the diff from its start fact and runs the command only as the fallback) and dictates no sentences. Note for the documenter: `docs/project-guide/agents.md` has a `reviewer | docs-review` row in the docs-route table (line 324). It has no `reviewer | review` row; the only other `reviewer` rows are the tools table (line 273) and the Documents checklist row (line 341). So the documenter places the `review` side where it fits. I judge this the documenter's choice, not a gap in the story.
   - Architecture: one shipped agent file and tests under `tests/agent_files/`, mirroring the agent files as CLAUDE.md asks. The story names no project command in the shipped file (R8, the factory knows only `context` names). `factory/` and `src/` are not touched.
   - Scope: inside F0058's scope item S0004 (start facts save the agent's turns): this makes the reviewer use the facts S0004 gives it. It changes neither the reviewer's effort nor its edits to criteria, both of which are out of scope. Other agents stay unchanged as the Description says.
4. factory: started tests as vm.
