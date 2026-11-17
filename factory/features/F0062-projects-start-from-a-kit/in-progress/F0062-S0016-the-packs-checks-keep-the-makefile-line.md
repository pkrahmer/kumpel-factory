---
stage: docs
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 710
comments_read: [6942486584]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T08:06:54.230208Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T08:06:54.237439Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T08:07:18.171476Z'
  stage: intake
  run: 9c414dde64ce440f911031b60381cd1e
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-17T08:07:23.290770Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-17T08:10:30.583385Z'
  stage: tests
  run: 8b19930b2bae430094fa7962dac2d838
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-17T08:10:38.059115Z'
  stage: doing
- number: 7
  speaker: coder
  kind: question
  at: '2026-11-17T08:11:20.370706Z'
  stage: doing
  run: 2cb1bb3ea7974de390c3a9d8c5701a2f
  blocked: question
- number: 8
  speaker: human
  kind: comment
  at: '2026-11-17T08:12:05.662885Z'
  stage: doing
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T08:12:08.180010Z'
  stage: doing
- number: 10
  speaker: coder
  kind: result
  at: '2026-11-17T08:12:19.604833Z'
  stage: doing
  run: 240dfe9e1b094504841da50dbf96bce4
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T08:12:24.756754Z'
  stage: tests
- number: 12
  speaker: tester
  kind: result
  at: '2026-11-17T08:13:21.090411Z'
  stage: tests
  run: 6a47329c4d7d412ea43a1c1f20424641
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-17T08:13:26.494157Z'
  stage: doing
- number: 14
  speaker: coder
  kind: result
  at: '2026-11-17T08:15:58.640620Z'
  stage: doing
  run: 30af8e4a770243b5bc17f8aa365f20e1
- number: 15
  speaker: factory
  kind: started
  at: '2026-11-17T08:16:04.712005Z'
  stage: review
- number: 16
  speaker: reviewer
  kind: result
  at: '2026-11-17T08:16:32.364023Z'
  stage: review
  run: 22700e4797a64bc3801d1e7cd461c4da
---

# Each pack's checks section keeps the line that names the factory's makefile


## Description

The kit's `CLAUDE.md` says under `## Checks` where the factory's targets are: "The factory's targets are in `factory/Makefile`", followed by two wordings to choose from. The first is that the root `Makefile` forwards every target. The second, for a repository that keeps a root `Makefile` of its own, is that every target is run as `make -f factory/Makefile <target>`. That line is the only place that tells an agent in such a repository not to run the root's `make check`. But the guide's step 5 (`docs/operator-guide/start-a-project.md`) and the packs' README step 4 (`operator/packs/README.md`) both tell the reader to replace the skeleton's whole `## Checks` section with the pack's section, and no pack's `## Checks` section holds the line. A project assembled as written, and as `pack_claude_md` of `tests/support/kit_support.py` assembles it, has a `CLAUDE.md` that never names `factory/Makefile`. The two guides ask in the same step to "keep" the kit's line, which the replacement has just removed. The factory's own gates are not affected, because they run `make -f factory/Makefile` through `make_file`. An agent's own `make check` in a repository with its own root `Makefile` runs the wrong makefile. After this story, each pack's `## Checks` section carries the kit's line word for word as its second bullet, so the replacement keeps it, and the guides say to keep the wording that fits. The packs' files are copies of the human's drafts (feature decision 23), so the human's seat adds the line to each `planning/packs-draft/<pack>/CLAUDE.sections.md` before the story starts, and the story copies the three files. Nothing else in the packs or the kit changes.

## Interface

- No module under `src/factory/` changes.
- `operator/packs/python/CLAUDE.sections.md`, `operator/packs/c-host/CLAUDE.sections.md`, `operator/packs/java-gradle/CLAUDE.sections.md`: copies of the human's drafts. The second bullet of each `## Checks` section is the kit's line from `operator/kit/CLAUDE.md`, byte for byte: the line that starts with "- The factory's targets are in `factory/Makefile`." and holds both wordings in its `<Either: ... Or: ...>` placeholder.
- Rules:
  - in the `CLAUDE.md` that `pack_claude_md(pack)` assembles, for each of the three packs, the `## Checks` section holds the kit's line exactly once;
  - every other line of each pack's `CLAUDE.sections.md` is as before;
  - the kit's `CLAUDE.md` is unchanged.
- Tests: `tests/operator_scripts/test_pack_checks_line.py`, new, built on `pack_claude_md`, `KIT` and `PACKS` of `tests/support/kit_support.py`.
- Leave for earlier tests: "the tester may change `TEMPLATE_RULES_LINES` in `tests/agent_files/test_claude_files.py`, and any other earlier test whose only failure is the added line in the packs' `## Checks` sections, to hold that line; each test keeps its name and what it checks."

## Acceptance criteria

1. For each pack (`python`, `c-host`, `java-gradle`, one row each), the `## Checks` section of `pack_claude_md(pack)` holds exactly one line that starts with "- The factory's targets are in `factory/Makefile`.", and that line is equal to the line of `operator/kit/CLAUDE.md` that starts the same way. A section without the line, or with a different wording of it, fails the row; before the drafts are copied, every row fails.
2. For each pack, removing that one line from the pack's `CLAUDE.sections.md` gives the file as it was before this story: no other line changed. The test compares against the text at the commit before the story, or against an expected list of the section's other bullets.
3. `operator/kit/CLAUDE.md` still holds the line once, under `## Checks`.
4. `make check` stays green.
5. docs: in `docs/operator-guide/start-a-project.md` step 5 and `operator/packs/README.md` step 4, the reader learns that the pack's `## Checks` section replaces the kit's together with the line about `factory/Makefile`, and that they keep the one wording of that line that fits their repository. Neither page asks the reader to keep a line that the replacement removes.

## Smoke test

```bash
for p in python c-host java-gradle; do awk '/^## Checks/{f=1;next} /^## /{f=0} f' "operator/packs/$p/CLAUDE.sections.md" | grep -c "The factory's targets are in \`factory/Makefile\`"; done
```
Expect: three lines, each `1`.

```bash
uv run pytest tests/operator_scripts/test_pack_checks_line.py tests/operator_scripts/test_packs.py tests/agent_files/test_claude_files.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: accepted
   - Interface: concrete. No module under `src/factory/` changes. The three `operator/packs/<pack>/CLAUDE.sections.md` files are copied from the human's drafts. I checked that each draft in `planning/packs-draft/<pack>/CLAUDE.sections.md` holds the kit's line byte for byte as the second bullet of `## Checks`, and that it differs from today's pack file by that line alone. The new test `tests/operator_scripts/test_pack_checks_line.py` builds on `pack_claude_md`, `KIT` and `PACKS`, which exist in `tests/support/kit_support.py`. The leave for earlier tests names `TEMPLATE_RULES_LINES` in `tests/agent_files/test_claude_files.py`, and any other test that fails only because of the added line.
   - Criteria: each can be tested by one test function. Criterion 1 has one row per pack and covers both failing sides: the line missing, and a different wording. It also checks that the line appears exactly once. Criterion 2 pins every other line, against the text before the story or an expected list. Criterion 3 checks that the kit is unchanged. Each of the three Interface rules has its own criterion.
   - Smoke test: both commands can run. The pytest command passes no `-q`, and `addopts` already sets `-q`, so the summary line still prints. The expectations can be checked: three lines that each say `1`, and a summary with only `passed`.
   - Docs criterion: it says what the reader must know in the guide's step 5 and the packs README's step 4. That is: the pack's `## Checks` section replaces the kit's section together with the line about `factory/Makefile`, the reader keeps the wording that fits their repository, and no step asks them to keep a line the replacement removed. It dictates no sentences.
   - Architecture: the change is pack data under `operator/packs/` plus one test in `tests/operator_scripts/`. No code changes and no layer is touched.
   - Scope: within F0062, which covers the kit and the packs. The packs are copies of the human's drafts (feature decision 23), and the change touches nothing listed under Out of scope. The route is `tests`, because the pack files are outside the documenter's write paths.
4. factory: started tests as self.
5. tester: Wrote the tests for the packs' `## Checks` line that names `factory/Makefile`, and changed one earlier test under the story's leave.

   - criterion 1: `tests/operator_scripts/test_pack_checks_line.py::test_each_assembled_checks_section_holds_the_kit_makefile_line_once`, one row per pack. In `section_texts(pack_claude_md(pack))["Checks"]`, the lines that start with "- The factory's targets are in `factory/Makefile`." must be exactly `[kit line]`. A missing line, a second copy or a different wording fails the row.
   - criterion 2: `tests/operator_scripts/test_pack_checks_line.py::test_each_pack_sections_file_differs_from_before_only_by_the_kit_line`, one row per pack, with three checks:
     - the kit's line is the second bullet of `## Checks`;
     - the section's other bullets equal an expected list (`OTHER_CHECKS_BULLETS`);
     - the whole file with the kit's line removed has the sha256 of today's pack file (`SECTIONS_BEFORE_SHA256`), so every other line of the file is pinned without reading git history.
     
     I checked the drafts: each `planning/packs-draft/<pack>/CLAUDE.sections.md` with the line removed by grep gives exactly those three hashes.
   - criterion 3: `tests/operator_scripts/test_pack_checks_line.py::test_the_kit_holds_the_makefile_line_once_under_checks`. The kit holds the line once in the whole file, and that one copy is under `## Checks`. This passes today, as it should.
   - criterion 4 (`make check`) and criterion 5 (docs) are not tested here.

   Files: created `tests/operator_scripts/test_pack_checks_line.py`.

   Earlier test changed under the story's leave: `tests/agent_files/test_claude_files.py`. `TEMPLATE_RULES_LINES` now holds the kit's line as the second bullet of `## Checks`. `test_template_rules_file_is_the_python_project_text` keeps its name and what it checks. It fails until the python draft is copied.

   I did not copy the drafts to see the tests go green. That copy is the coder's work, and my attempt to do it was refused.

   `make test`: 7 failures, all for the right reason, and no import or collection errors:
   - the 3 rows of criterion 1: the line is missing (`assert [] == [...]`);
   - the 3 rows of criterion 2: the second bullet is not the kit's line;
   - `test_template_rules_file_is_the_python_project_text`.

   `make lint` is green. The coder's work: copy the three `planning/packs-draft/<pack>/CLAUDE.sections.md` files to `operator/packs/<pack>/CLAUDE.sections.md`.

   `lint`: lint: green (0.2 s)
6. factory: started doing as self.
7. coder: Copied the three drafts: `operator/packs/python/CLAUDE.sections.md`, `operator/packs/c-host/CLAUDE.sections.md` and `operator/packs/java-gradle/CLAUDE.sections.md` are now byte-for-byte copies of `planning/packs-draft/<pack>/CLAUDE.sections.md`. Before the copy, each pack file differed from its draft by the kit's line alone. I did not change anything else, and no code was needed.

   Tests: `uv run pytest -q tests/operator_scripts/test_pack_checks_line.py tests/agent_files/test_claude_files.py tests/operator_scripts/test_packs.py` passes; all seven earlier failures are now green.

   Blocker: `make check` is red. `lint`, `types`, `layers` and `sast` pass, but `make secrets` fails on the tester's own test file, so I cannot hand forward. Its output:
   ```
   Secret Type: Hex High Entropy String
   Location:    tests/operator_scripts/test_pack_checks_line.py:57
   Location:    tests/operator_scripts/test_pack_checks_line.py:58
   Location:    tests/operator_scripts/test_pack_checks_line.py:59
   make: *** [Makefile:65: secrets] Error 1
   ```
   Those three lines are the sha256 values in `SECTIONS_BEFORE_SHA256`. `CLAUDE.md` asks for low-entropy hex in tests so that `make secrets` stays green without a baseline entry. Adding a `pragma: allowlist secret` or a `.secrets.baseline` entry needs your leave, and I may not edit the test.

   Options:
   (a) The tester replaces the sha256 pin in `test_each_pack_sections_file_differs_from_before_only_by_the_kit_line` with an expected list of the whole file's lines without the kit's line. The files are only 18–19 lines each, and criterion 2 already allows "an expected list". The pin can then go, or it can be merged into `OTHER_CHECKS_BULLETS`.
   (b) Add `# pragma: allowlist secret` to the three hash lines.
   (c) Add the three findings to `.secrets.baseline`.

   I would choose (a): it keeps the test readable, needs no secrets exception, and matches what criterion 2 already allows. On an answer of (a), I end the next run with `tests` naming that change.
8. 2026-11-17 human: (a). No marker and no baseline entry.
9. factory: started doing as self.
10. coder: The human answered (a), which needs a test change. I changed no code and no test. The three pack copies from the previous run are already in place and stay as they are.

    The change for the tester, under option (a): in `tests/operator_scripts/test_pack_checks_line.py::test_each_pack_sections_file_differs_from_before_only_by_the_kit_line`, replace the sha256 pin `SECTIONS_BEFORE_SHA256` with an expected list of each pack file's lines once the kit's line is removed. That list may be merged with `OTHER_CHECKS_BULLETS`. This gets the high-entropy hex values out of the test, so `make secrets` goes green with no `pragma: allowlist secret` and no `.secrets.baseline` entry.

    `make check` is still red on `make secrets` until the tester makes this change. When the work item comes back to doing, I will run `make check` again and hand forward to review.
11. factory: started tests as self.
12. tester: I made the test change the human approved (option (a), journal entries 8 and 10). It is in `tests/operator_scripts/test_pack_checks_line.py::test_each_pack_sections_file_differs_from_before_only_by_the_kit_line`, and no other test changed.

    - I removed the sha256 pin `SECTIONS_BEFORE_SHA256` and the `hashlib` import. The three high-entropy hex values that made `make secrets` red are gone. I added no `pragma: allowlist secret` and no `.secrets.baseline` entry.
    - In their place come two expected lists:
      - `LINES_BEFORE_CHECKS`: each pack file's lines up to and including `## Checks`.
      - `LINES_AFTER_CHECKS`: each pack file's lines from the blank line that ends the section through the end of the file.
    - The `## Checks` bullets in between are not repeated. The new lists reuse `OTHER_CHECKS_BULLETS`, as the coder's entry allowed.
    - The test now checks that the file split on `\n`, with the kit's line removed, equals `(*LINES_BEFORE_CHECKS, *OTHER_CHECKS_BULLETS, *LINES_AFTER_CHECKS)`. That pins every other line, and the trailing newline too, without reading git history.
    - The other two checks of the test are unchanged: the kit's line is the second bullet, and the other bullets equal `OTHER_CHECKS_BULLETS`.

    I generated the expected lines from the current pack files with the kit's line taken out. Before this story each pack file differed from its draft by that line alone (entries 3 and 5), so these are the lines as they were. I split long strings by implicit concatenation to stay within the line limit.

    Criterion mapping, unchanged:
    - criterion 1: `tests/operator_scripts/test_pack_checks_line.py::test_each_assembled_checks_section_holds_the_kit_makefile_line_once`
    - criterion 2: `tests/operator_scripts/test_pack_checks_line.py::test_each_pack_sections_file_differs_from_before_only_by_the_kit_line`
    - criterion 3: `tests/operator_scripts/test_pack_checks_line.py::test_the_kit_holds_the_makefile_line_once_under_checks`

    Files created: none. The only file changed is `tests/operator_scripts/test_pack_checks_line.py`, a test of this story. There were no import failures.

    Runs:
    - `uv run pytest -q tests/operator_scripts/test_pack_checks_line.py`: 7 passed. The pack copies are already in place.
    - `detect-secrets scan` on the file: 0 findings.
    - `make lint`: lint: green (0.1 s).

    Next, the coder runs `make check` and hands forward to review.

    `lint`: lint: green (0.1 s)
13. factory: started doing as self.
14. coder: The tester replaced the sha256 pin with expected line lists (entry 12), so I changed nothing in this run. The work is the three pack copies I made in entry 7. They are still byte-for-byte copies of `planning/packs-draft/<pack>/CLAUDE.sections.md`:
    - `operator/packs/python/CLAUDE.sections.md`
    - `operator/packs/c-host/CLAUDE.sections.md`
    - `operator/packs/java-gradle/CLAUDE.sections.md`

    Each copy differs from the earlier pack file only by the kit's `factory/Makefile` line, which is the second bullet of its `## Checks` section. No module under `src/factory/` changed.

    Runs:
    - `uv run pytest -q tests/operator_scripts/test_pack_checks_line.py`: 7 passed.
    - `make check guides`: `check: green` (test: green, 109.3 s; coverage 99.14 %) and `guides: green` (9.4 s). `make secrets` is green now that the high-entropy hex values are gone, with no marker and no baseline entry, as the human answered in entry 8.

    Main choice: copy the human's drafts unchanged. I rejected adding the line to each pack file by hand, because the packs are copies of the drafts (feature decision 23).

    Refactor: the diff is three data-file copies, so there was nothing to change.

    The journal did not change the meaning of the task: the human's answer (a) changed only how the test pins the other lines. The Description stays as it is.

    Noticed but did not touch: the docs criterion (5), the edits to `docs/operator-guide/start-a-project.md` step 5 and `operator/packs/README.md` step 4. That is the documenter's work.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
15. factory: started review as self.
16. reviewer: no findings

    I reviewed `git diff develop...HEAD -- . ':!factory'` and checked the parts that matter against the repository.

    - Pack copies: `operator/packs/{python,c-host,java-gradle}/CLAUDE.sections.md` are byte-for-byte copies of `planning/packs-draft/<pack>/CLAUDE.sections.md` (checked with `cmp`). In each, the diff adds one line, and that line is the second bullet of `## Checks`. It is identical to line 22 of `operator/kit/CLAUDE.md`. The diff does not touch `operator/kit/`, and no module under `src/factory/` changes.
    - Criterion 1: `test_each_assembled_checks_section_holds_the_kit_makefile_line_once` has one row per pack. It reads the `## Checks` section of `pack_claude_md(pack)` and requires the lines that start with the kit line's opening to equal `[kit line]`. That fails a missing line, a second copy and a different wording.
    - Criterion 2: `test_each_pack_sections_file_differs_from_before_only_by_the_kit_line` has one row per pack. It removes the kit's line and compares the whole file, split on `\n`, with the expected lines before the section, the section's other bullets and the lines after it. That pins every other line and the trailing newline. It also checks that the kit's line is the second bullet. The hex pins are gone, so `make secrets` has nothing to flag, and no marker or baseline entry was added, as the human answered in entry 8.
    - Criterion 3: `test_the_kit_holds_the_makefile_line_once_under_checks` checks that the kit holds the line once in the whole file and that this one copy is under `## Checks`.
    - Criterion 4: the coder's entry 14 reports `make check guides` green.
    - Criterion 5: this is the documenter's work, and the criterion still says what the reader must learn in both guide steps.
    - The Interface rule "the kit's `CLAUDE.md` is unchanged" holds by the diff; criterion 3 and the assembly test pin the line it carries.
    - Architecture, security and quality: there is no code change. The new test reuses `section_texts`, `pack_claude_md`, `KIT`, `PACKS`, `PACKS_FOLDER`, `PACK_SECTIONS` and `Pack` from `tests/support/kit_support.py`, and `split_lines` from `factory.shared.domain.sections`. It copies no helper, and the module carries its docstring.
    - Hygiene: the Description matches what was built, and the journal names the main choice (copy the drafts unchanged) and what was rejected (adding the line by hand; options (b) and (c) for the secrets finding).

    Earlier tests:
    - `tests/agent_files/test_claude_files.py`: changed under the leave in the story's Interface, which the human wrote at creation (entry 1). `TEMPLATE_RULES_LINES` gains only the kit's line, and `test_template_rules_file_is_the_python_project_text` keeps its name and what it checks.
