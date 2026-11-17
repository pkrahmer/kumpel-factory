---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 710
comments_read: []
handed_over: null
claim:
  instance: self
  stage: doing
  started_at: '2026-11-17T08:10:38.059115Z'
  lease_duration: 60
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
