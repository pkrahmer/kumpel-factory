---
stage: review
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 693
comments_read: [6936126509]
handed_over: null
claim:
  instance: self
  stage: review
  started_at: '2026-11-17T02:42:57.242378Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T02:25:48.924110Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T02:25:48.931095Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-17T02:26:51.270261Z'
  stage: intake
  run: ba8d80ed90db4e33a8a27f9049a0d235
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-17T02:28:39.782462Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-17T02:28:42.279205Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-17T02:29:04.235495Z'
  stage: intake
  run: 495090b8960d49aea1413564509964ae
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T02:29:09.082028Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-17T02:35:21.326828Z'
  stage: tests
  run: 86142f22a5964ec8a1358ec89afc5f9f
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T02:35:28.741326Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T02:38:42.559238Z'
  stage: doing
  run: 753fd95047b5433f9ab721bfd8f82eb8
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T02:38:48.311041Z'
  stage: review
- number: 12
  speaker: reviewer
  kind: result
  at: '2026-11-17T02:39:39.418589Z'
  stage: review
  run: e92c960c46854719a2b19879e1f29392
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-17T02:39:45.169023Z'
  stage: tests
- number: 14
  speaker: tester
  kind: result
  at: '2026-11-17T02:40:18.386544Z'
  stage: tests
  run: 5b1290fb2abb46eb823ded521f49e3f1
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-17T02:40:24.061381Z'
  stage: doing
- number: 16
  speaker: coder
  kind: result
  at: '2026-11-17T02:42:51.688521Z'
  stage: doing
  run: f2e07c4a11884461b30b1c3c94538bfd
- number: 17
  speaker: factory
  kind: started
  at: '2026-11-17T02:42:57.242378Z'
  stage: review
---

# The installed builder

## Description

A small project runs the thin line: one builder that writes tests, code and documents, one reviewer, the approval. The factory ships no `builder`, so each of the three templates carries its own copy of a builder and of a reviewer under `factory/agents/`, and the copies have drifted. After this story the factory's installed agents hold `builder`, written for any stack, and the installed reviewer also checks the review points a project writes in the section `## Review` of its `CLAUDE.md`. A project of the thin line then needs no agent file at all, and what is special about its stack lives in `CLAUDE.md`. A project's own agent file still wins over the installed one, file by file; nothing changes for the full line.

## Interface

- `agents/agents/builder.md`, new, with exactly this front matter and text:

```markdown
---
model: opus
effort: medium
budget_usd: 6
tools: [Read, Grep, Glob, Edit, Bash, Write, Skill]
---
Never change the build files, the makefile or `factory/`; a story that needs a change there is a question.

Your entry says what you built (the paths), the decisions you took where the story left something open, and what you noticed but did not touch.

## Role

You build the whole story alone: its tests, its code and its documents, inside the architecture `CLAUDE.md` describes. No other role writes tests, code or documents in this pipeline; a reviewer reads your work after you.

- Meet every acceptance criterion and cover it with tests. Write the tests first, see them fail, then write the code.
- Implement where the `## Interface` puts it; the rules of `CLAUDE.md` are binding, and `make check` enforces the ones it can.
- You write only inside your role's write paths; the factory takes nothing else from you. The build files, the makefile and `factory/` are the human's unless `CLAUDE.md` says otherwise: a story that seems to need a change there, a new dependency included, ends with `question`.
- Update the documents the story's docs criterion names, and nothing it does not name.
- Small functions, explicit names, no clever one-liners. Comments say why, never what, and they are timeless: no work item ids, no criterion numbers, no stage names.
- Where the story leaves something open, decide yourself and say so in your entry; ask only what you cannot decide without the human.
- Leave your work in the working tree; the factory commits it under the work item's subject after you. Never commit and never push.

## Stage

1. The work item is in your first message: its Description, Interface, criteria and smoke test. `CLAUDE.md` is already in your context. Read the code and documents the story touches; not other work items, not `feature.md`, not `factory/`, not `.claude/`. If the prompt's round is greater than 0, address exactly the findings in the reviewer's latest entry, nothing more.
2. Write the tests for every criterion, then the code, until `make check` is green.
3. Update the documents the docs criterion names.
4. Run the smoke test's commands as written and check each against its `Expect:` line. A command that does not meet its line is work still to do, not a remark.
5. With everything green, read your own diff and the new files (`git status --short`) the way a reviewer would: rename what is unclear, simplify what is convoluted, remove duplication and dead code. Chain the final `make check` with your last edit in one command.
6. End with `review` and an entry: what you built (paths), the decisions you took and the alternatives you rejected, the smoke test's results, anything you noticed but did not touch. The factory runs `make check` after you; red holds the work item here.

## Lessons

- Run `make check` and every other make target in the foreground and read its output. Never start one in the background, and never wait for a process with `pgrep -f`: it matches its own command line, so the wait never ends.
- Give a project command that can take minutes, such as `make check`, the shell tool's largest timeout (600000 ms), so that the tool does not move it to the background.
- Before you write a helper, search the code and the tests for one that does the same, and reuse or extend it.
```

- `agents/agents/reviewer.md` gains, as its last part before any `## Lessons` section, or at its end when it has none, exactly:

```markdown
### The project's review points

When the project's `CLAUDE.md` holds a section `## Review`, each of its points is a checklist item of every review, beside the groups above. Check each point against the diff and report a broken one as a finding that names the point. Without that section there is nothing more to check.
```

- Where another shipped file lists the installed agents or the roles by name (the system prompt `agents/system-prompt.md`, `agents/README.md` is the documenter's), the coder adds `builder` only where the list claims to be complete.
- No module under `src/factory/` changes: `ProjectAgentDefinitions` already reads a project's file first and the installed one otherwise.
- Tests: `tests/agent_files/test_installed_builder.py`. `feature.md` gives this leave (decision 11): "S0004 may change earlier tests under `tests/agent_files/`, and any other earlier test, that pin the list or the number of the shipped agents or the text or a checksum of `reviewer.md`, where their only failure is the eighth agent `builder` or the reviewer's new part." Journal entry 4 extends it: the tester may add rows for `builder` to the per-agent tables of `tests/support/shipped_agents.py` and of the tests under `tests/agent_files/` (boundary, anchors, lessons, efforts, the pinned role lists), and may take the builder's stage and decisions from a thin-line pipeline definition written in the test instead of `operator/template/factory/pipeline.yml`. Every earlier test keeps its name and still checks the seven agents as before.

## Acceptance criteria

1. The installed agents' reader (`FrontmatterAgentDefinitionReader` on the repository's `agents/` folder) names `builder` among its agents and reads it: model `opus`, effort `medium`, a budget of 6, the seven tools of the Interface.
2. The builder's text holds the three headings `## Role`, `## Stage` and `## Lessons`, ends its stage with `review`, and names no stack: none of the words `gradle`, `pytest`, `cmake` appears in it (compared without case).
3. The installed reviewer's text holds the heading `### The project's review points` and names the section `## Review` of `CLAUDE.md`.
4. A pipeline definition of the thin line (roles `builder` and `reviewer`; stages `doing`, `review`, `approval`, `done`) on a repository without `factory/agents/` loads through `PipelineLoader` with the installed agents, and `ProjectCheck.run` gives its point `agents` no fault.
5. A project's own `factory/agents/builder.md` is the one that is read when it exists, and the installed one when it does not: rows of one parametrized test.
6. Every earlier test of the shipped agent files passes with the eighth agent.
7. `make check` stays green.
8. docs: the operator guide's page on the agents (`docs/operator-guide/agent-runtime.md` or the page that lists the installed agents) names `builder` and says that the thin line (one builder, one reviewer) needs no agent file in the project, that a project's own file under `factory/agents/` still replaces the installed one file by file, and that a project gives the reviewer its own review points in the section `## Review` of its `CLAUDE.md`; the project guide (`docs/project-guide/agents.md`) lists the eighth agent; `agents/README.md` lists `builder.md`; `docs/decisions.md` records the decision of 2026-11-16 that the installed agents are the default, a kit copies no agent file, and a stack's review points live in the project's `CLAUDE.md`.

## Smoke test

```bash
uv run python -c "
from pathlib import Path
from factory.agents.adapters.agent_files import FrontmatterAgentDefinitionReader as R
reader = R(Path('agents').resolve())
print('builder' in reader.names(), len(reader.names()))
reader.read('builder'); print('read')
"
grep -c '^### The project.s review points$' agents/agents/reviewer.md
```
Expect: `True 8`, then `read`, then `1`.

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
git init -q "$d/p"; mkdir -p "$d/p/factory" "$d/p/src"
cat > "$d/p/factory/pipeline.yml" <<'EOF'
contract: "1.1"
project_commands:
  check: {time_limit: 10}
  sync: {time_limit: 5}
roles:
  builder: {write_paths: ["src/*"]}
  reviewer: {write_paths: ["{work_item}"]}
stages:
  doing: {role: builder, next: [review], checks: [check]}
  review: {role: reviewer, next: [approval, doing], round_cap: 3}
  approval: {approval: true, next: [done, doing]}
  done: {}
EOF
cp factory/story-form.md factory/feature-form.md "$d/p/factory/"
printf 'check:\n\techo "check: green"\nsync:\n\techo "sync: green (0.0 s)"\n' > "$d/p/Makefile"
touch "$d/p/src/a.c"
git -C "$d/p" add -A; git -C "$d/p" -c user.name=t -c user.email=t@example.com commit -q -m one
uv run python -m factory.entry.check_project --agent-home agents "$d/p" | grep -E '^(agents|project):'
```
Expect: `agents: ok` and `project: ready`.

```bash
uv run pytest tests/agent_files/
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: Questions before the tests stage. The format check passed. The Interface, the placement (agents/agents/, no change under src/factory/), the scope against feature.md, the smoke tests (runnable; pytest is called without `-q`, which `addopts` already sets, so the summary line is printed) and the docs criterion (it names what the reader must know) are all fine. Two points block the build, because the exact builder text in the Interface cannot pass criterion 6 under leave 11 as it is worded now:

   1. The builder's step 1 reads "1. Read the work item: its Description, Interface, …". `tests/agent_files/test_no_agent_file_reads_its_work_item_first_and_each_finds_it_in_the_first_message` (test_first_message_agent_files.py) fails any shipped agent that matches `^\d+\. Read (the work item|the story)\b`. The step also goes against the shared rule R6: the work item is in the first message and is not read first. This failure is about the text, not about the list or the number of agents, so leave 11 does not cover it. Options: (a) reword step 1 in the Interface, for example "1. The work item is in your first message: its Description, Interface, criteria and smoke test. `CLAUDE.md` is already in your context. Read the code and documents the story touches; …". (b) Add a leave that excludes `builder` from that test. I would choose (a).

   2. The per-agent tables in `tests/support/shipped_agents.py` and `tests/agent_files/` need more than a new name for `builder`:
      - Every `ShippedAgent` has a `boundary` sentence. `test_body_starts_with_the_boundary_and_the_entry_sentence` (test_claude_files.py) and `test_body_still_opens_with_the_boundary_and_the_entry_sentence` (test_claude_agent_texts.py) both require the body to open with "<boundary>\n\n<entry>". The builder text opens with its entry sentence and has no boundary sentence.
      - `test_body_names_every_decision_of_its_stage_in_inline_code` looks up each role's stage in `operator/template/factory/pipeline.yml` and asserts exactly one. The template has no `builder` stage, so the test fails.
      - Builder rows are also needed in `ROLE_AND_STAGE_ANCHORS`, `LESSONS` and `EFFORTS`. The pinned role list of `test_template_pipeline_definition_is_valid_with_the_shipped_roles` would also change.

      Does leave 11 cover these changes? Options: (a) Add a boundary line to the builder's Interface text, for example "You build the story; what you cannot decide you ask." Extend leave 11 so the tester may add builder rows to those tables and take builder's decisions (`review`, `question`) from a thin-line definition in the test, not from the template. (b) Leave the builder text as it is, and let the tester make the boundary optional, with builder's row having none. I would choose (a): the builder then follows the same shape as the seven agents, and the tests change only by data rows and the source of one role's decisions.
4. 2026-11-17 human: 1: (a), with your wording of step 1. 2: (a). The builder's text opens with this boundary sentence, a blank line, then its entry sentence: "Never change the build files, the makefile or `factory/`; a story that needs a change there is a question." Leave 11 is extended: the tester may add rows for `builder` to the per-agent tables of `tests/support/shipped_agents.py` and of the tests under `tests/agent_files/` (boundary, anchors, lessons, efforts, the pinned role lists), and may take the builder's stage and decisions from a thin-line pipeline definition written in the test instead of `operator/template/factory/pipeline.yml`. Every earlier test keeps its name and still checks the seven agents as before.
5. factory: started intake as self.
6. intake: accepted
   I carried the human's answer from journal entry 4 into the story. I made no other edits.
   - The builder text in the Interface now opens with the boundary sentence "Never change the build files, the makefile or `factory/`; a story that needs a change there is a question." Then come a blank line and the entry sentence.
   - Step 1 of the builder text is reworded to "1. The work item is in your first message: its Description, Interface, criteria and smoke test. …". This is the wording from option (a) of question 1.
   - The Tests line of the Interface now carries the extended leave 11. The tester may add rows for `builder` to the per-agent tables of `tests/support/shipped_agents.py` and `tests/agent_files/` (boundary, anchors, lessons, efforts, pinned role lists). The tester may take the builder's stage and decisions from a thin-line definition written in the test. Every earlier test keeps its name and still checks the seven agents.

   Interface: it names concrete files: `agents/agents/builder.md` with its exact text, and the exact section added to `agents/agents/reviewer.md`. Nothing under `src/factory/` changes. The test file is named, and the system prompt adds `builder` only where a list claims to be complete. With the reworded step 1 and the boundary sentence, the builder text now fits the existing shape tests.
   Criteria: each one can be tested by one test function. Criterion 5 has both rows: the project's file is read when it exists, the installed one when it does not. Criterion 2 covers both sides of the stack-word rule. Criterion 4 covers the thin line on a repository with no agent files. Criterion 6 is now coverable under the extended leave.
   Smoke test: the commands can be run. Each Expect line can be checked: `True 8`, `read`, `1`, `agents: ok` / `project: ready`, and a pytest summary with only `passed`. pytest is called without `-q`.
   Docs criterion: it names what the reader must know: `builder`, that the thin line needs no agent file, that the replacement works file by file, the `## Review` section, the project guide's list, `agents/README.md` and the decision of 2026-11-16. It dictates no sentences.
   Architecture: the change is agent files plus tests and docs only. `ProjectAgentDefinitions` already resolves the project's file first, then the installed one. No layer moves.
   Scope: the story is within F0062: the installed agents become the default and kits copy no agent file. Its test changes are covered by leave 11 as extended in entry 4. Route: `tests`, because `agents/agents/` and tests change, which the documenter alone may not write.
7. factory: started tests as self.
8. tester: Tests for the installed builder are written. Each criterion maps to a test:
   - criterion 1: tests/agent_files/test_installed_builder.py::test_the_installed_agents_name_and_read_the_builder
   - criterion 2: tests/agent_files/test_installed_builder.py::test_the_builder_has_role_stage_and_lessons_and_ends_its_stage_with_review and ::test_the_builder_names_no_stack (one row each for gradle, pytest and cmake, compared without case)
   - criterion 3: tests/agent_files/test_installed_builder.py::test_the_installed_reviewer_checks_the_projects_review_points
   - criterion 4: tests/agent_files/test_installed_builder.py::test_the_thin_line_loads_with_the_installed_agents_alone (`PipelineLoader` with `ProjectAgentDefinitions` over the repository's `agents/`) and ::test_the_thin_line_without_agent_files_passes_the_agents_point (`ProjectCheck.run` on a committed repository that has no `factory/agents/`)
   - criterion 5: tests/agent_files/test_installed_builder.py::test_a_projects_builder_wins_over_the_installed_one, with the rows project-builder and installed-builder
   - criterion 6: the earlier tests under tests/agent_files and tests/agents/adapters/test_shipped_agents_effect.py now carry the builder through `SHIPPED_AGENTS`. Each one keeps its name.
   - criteria 7 and 8: no test from me; `make check` and the docs stage cover them.

   Files created: tests/agent_files/test_installed_builder.py.

   Support changed (leave 11 as extended in entry 4): tests/support/shipped_agents.py.
   - New `ShippedAgent` row for `builder`, with the boundary and entry sentences from the Interface.
   - New `THIN_LINE_ONLY = {"builder"}`.
   - New `THIN_LINE_PIPELINE`, the smoke test's thin-line definition, and `thin_line_definition()` to parse it.
   - New `full_line_names()`, the seven agents of the template's full line.
   - The module docstring now says eight agents.

   Earlier test files I changed, all under leave 11 as extended in entry 4. Every test keeps its name and still checks the seven agents as before.
   - tests/agent_files/test_claude_files.py: `test_template_pipeline_definition_is_valid_with_the_shipped_roles` now compares the template's roles with `full_line_names()`, because the template is the full line and has no builder.
   - tests/agent_files/test_claude_agent_texts.py:
     - `_decisions` takes the builder's stage from `thin_line_definition()`.
     - New builder rows in `LESSONS` (the three lessons of the Interface) and in `ROLE_AND_STAGE_ANCHORS` (two sentences of its Role and Stage).
   - tests/agent_files/test_shared_start_agent_files.py: new `builder: medium` row in `EFFORTS`.
   - tests/agent_files/test_shared_rules_system_prompt.py: `test_every_agent_file_keeps_its_own_sections_word_for_word_in_order`
     - It now runs only over the agents in `PARTS_BEFORE`. Those checksums record each file before the shared rules moved, and the builder did not exist then.
     - It strips the reviewer's new subsection `### The project's review points` before taking the checksum.
   - tests/agent_files/test_claude_agent_texts_review_groups.py: `test_the_rest_of_the_reviewer_body_is_unchanged` strips the same new subsection, the way it already strips `### docs-review`.

   How I checked them:
   - In a throwaway copy of the repository I added `agents/agents/builder.md` and the reviewer's new part, both exactly as the Interface gives them. Without my test changes, these 8 tests failed there and nothing else did (I ran tests/agent_files, tests/agents, tests/guards and tests/entry/test_tick_shipped_agent_file.py): the template role list, the builder's decisions, anchors and lessons, `PARTS_BEFORE` for reviewer and builder, the reviewer CRC, and `EFFORTS`.
   - With my changes, all of tests/agent_files passed in that copy, the new file included.
   - In the copy, `mypy` could not resolve the `factory` package, so the type check of these tests is left to the coder's `make check`.

   Red on the branch on purpose: `make test` fails because `agents/agents/builder.md` does not exist. That includes the fixture of tests/agents/adapters/test_shipped_agents_effect.py, which copies every shipped agent, so all of its rows error with FileNotFoundError. The reviewer's earlier checksum tests and the review-points test fail until the new part is added to `agents/agents/reviewer.md`.

   `make lint`: green.

   No module failed to import.

   The throwaway copy is still in a `mktemp -d` directory under /tmp: removing it was refused, and it goes with the stage.

   `lint`: lint: green (0.2 s)
9. factory: started doing as self.
10. coder: I added the installed builder and the reviewer's review points. `make check guides` is green.

    Built:
    - New `agents/agents/builder.md`. Its front matter and text are exactly as the Interface gives them: it opens with the boundary sentence from entry 4, and step 1 is reworded as entry 4 decided.
    - `agents/agents/reviewer.md`: the subsection `### The project's review points` now sits directly before `## Lessons`, after `### docs-review`, with the Interface's wording.
    - No module under `src/factory/` changed. I changed no tests.

    Checked:
    - The tester's files, `uv run pytest -q tests/agent_files/ tests/agents/adapters/test_shipped_agents_effect.py`: all pass.
    - `make check guides`: lint, types, layers, sast, secrets, licenses and test are each green, then `check: green` and `guides: green`.

    Smoke test, all three blocks run as written:
    - The reader prints `True 8`, then `read`. The `grep -c` gives `1`.
    - The thin-line project, checked with `check_project --agent-home agents`, prints `agents: ok` and `project: ready`.
    - `pytest tests/agent_files/` passed, part of the run above.

    Main choice: I put the reviewer's new part as the last subsection before `## Lessons`, as the Interface says. I rejected putting it inside the Role's checklist, because the Interface fixes its place and the tester's checksum tests strip it as one block.

    The Interface asks to add `builder` to the system prompt only where a list there claims to be complete. `agents/system-prompt.md` has no such list (it names roles only in passing, in R9 and R13), so I left it unchanged.

    Not touched: the documents of criterion 8 (`docs/operator-guide/`, `docs/project-guide/agents.md`, `agents/README.md`, `docs/decisions.md`). They belong to the documenter.

    Refactor: nothing to change. The diff is one new agent file and one inserted subsection, both fixed word for word by the Interface.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
11. factory: started review as self.
12. reviewer: Review, round 0: one finding, and it touches only this story's tests. So the work item goes to `tests`.

    I read the diff against every criterion and the Interface:
    - `agents/agents/builder.md` matches the Interface word for word: the front matter, the boundary sentence and the reworded step 1 from entry 4.
    - `agents/agents/reviewer.md` has the new subsection as its last part before `## Lessons`, word for word.
    - Nothing under `src/` changed.
    - Criteria 1 to 5 each have a test that checks what the criterion says. Criterion 4 is checked twice: through `PipelineLoader` on the `remote` fixture, whose `REMOTE_FILES` hold no `factory/agents/`, and through `ProjectCheck.run` on a committed repository with no `factory/agents/`. Criterion 5 is two rows of one parametrized test.
    - The coder reports `make check guides` green (entry 10).

    I found no architecture, security or hygiene problem.
    - The system prompt has no complete list of roles, so leaving it unchanged is right.
    - The Description and the docs criterion still describe what was built.

    Findings:
    1. `tests/agent_files/test_claude_agent_texts_review_groups.py:29` and `tests/agent_files/test_shared_rules_system_prompt.py:84`: the same regex `_REVIEW_POINTS_SUBSECTION` (`^### The project's review points\n(?:(?!#).*\n|\n)*`) is written twice. That is a second copy of one helper. Fix: define it once in `tests/support/shipped_agents.py`, with the comment of the first file, and import it in both test files.

    Notes:
    - `tests/agent_files/test_installed_builder.py:65`: the first assertion (the heading in `f"\n{body}\n"`) adds nothing to the next one, which finds the heading in the `## Stage` section. One of them could go.

    Earlier tests changed:
    - `tests/agent_files/test_claude_agent_texts.py`: entry 4. It adds builder rows to `LESSONS` and `ROLE_AND_STAGE_ANCHORS`, and takes the builder's decisions from the thin-line definition.
    - `tests/agent_files/test_claude_agent_texts_review_groups.py`: leave 11 of feature.md, as the Interface cites it. The test strips the reviewer's new part before its checksum.
    - `tests/agent_files/test_claude_files.py`: entry 4. The template's pinned role list is now `full_line_names()`.
    - `tests/agent_files/test_shared_rules_system_prompt.py`: leave 11 and entry 4. It strips the reviewer's new part, and its rows stay the seven agents of `PARTS_BEFORE`.
    - `tests/agent_files/test_shared_start_agent_files.py`: entry 4. A `builder` row in `EFFORTS`.
    - `tests/support/shipped_agents.py`: entry 4. A builder `ShippedAgent` row, plus `THIN_LINE_ONLY`, `THIN_LINE_PIPELINE`, `thin_line_definition()` and `full_line_names()`.
13. factory: started tests as self.
14. tester: Round 1: I fixed the reviewer's one finding from entry 12. It needed changes to the tests only.

    Finding 1 (the regex `_REVIEW_POINTS_SUBSECTION` was written twice). It is now defined once in `tests/support/shipped_agents.py` as `REVIEW_POINTS_SUBSECTION`, with the comment from the first file. Both tests that used it now import it from there:
    - `tests/agent_files/test_claude_agent_texts_review_groups.py::test_the_rest_of_the_reviewer_body_is_unchanged`: its local copy is gone and it uses the shared one.
    - `tests/agent_files/test_shared_rules_system_prompt.py::test_every_agent_file_keeps_its_own_sections_word_for_word_in_order`: its local copy is gone and it uses the shared one. Its old comment now sits above the parametrize: the agents `PARTS_BEFORE` lists predate the builder and the reviewer's review points.
    Every test keeps its name and checks the same thing. This uses leave 11 as extended in entry 4, and this story's own earlier changes to these files.

    I left the reviewer's note on `tests/agent_files/test_installed_builder.py:65` (two assertions that check the same heading) as it is. It is a note, not a finding.

    Files created: none. Files changed: `tests/support/shipped_agents.py`, `tests/agent_files/test_claude_agent_texts_review_groups.py`, `tests/agent_files/test_shared_rules_system_prompt.py`.

    Checked:
    - `uv run pytest -q` on those two test files and `tests/agent_files/test_installed_builder.py`: all 44 passed.
    - `make lint`: lint: green (0.1 s).
    - I did not run the type check. When I ran `mypy` on these files alone, it could not analyse the `factory` package (`import-untyped`), so the coder's `make check` covers types.

    Every test module imported.

    `lint`: lint: green (0.2 s)
15. factory: started doing as self.
16. coder: Round 1: no code change was needed. The reviewer's one finding (entry 12) was the copied regex in the tests. The tester has fixed it (entry 14) by moving it to `REVIEW_POINTS_SUBSECTION` in `tests/support/shipped_agents.py`.

    Checked:
    - I ran the tester's named files with `uv run pytest -q tests/agent_files/test_claude_agent_texts_review_groups.py tests/agent_files/test_shared_rules_system_prompt.py tests/agent_files/test_installed_builder.py`. All 44 passed.
    - `make check guides`: every target is green, ending with `check: green` and `guides: green`. Coverage is 99.14 %. Types now cover the tester's changed files, which the tester could not check alone.

    Built: nothing new this round. `agents/agents/builder.md` and the reviewer's subsection in `agents/agents/reviewer.md` are unchanged since entry 10. I changed no tests and no module under `src/factory/`.

    Main choice: I left the agent files as they are. The finding touched only the tests. I rejected touching the reviewer's note on `tests/agent_files/test_installed_builder.py:65`: it is a note, and the file is a test.

    Refactor: nothing to change. The diff outside the tests is still the two agent files, whose wording the Interface fixes word for word.

    Not touched: the documents of criterion 8 (`docs/operator-guide/`, `docs/project-guide/agents.md`, `agents/README.md`, `docs/decisions.md`). They belong to the documenter.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
17. factory: started review as self.
