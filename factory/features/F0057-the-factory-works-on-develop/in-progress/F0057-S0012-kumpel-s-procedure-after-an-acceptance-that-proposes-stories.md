---
stage: review
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 654
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T07:06:57.307308Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T07:06:57.314688Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-08T07:07:14.483687Z'
  stage: intake
  run: 9dad4a913c754b45aa882da848d11ed2
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-08T07:07:19.213414Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-08T07:08:00.554677Z'
  stage: tests
  run: acaa28d195ef47b0b77c79899ef096e3
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-08T07:08:05.884095Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-08T07:12:51.934616Z'
  stage: doing
  run: 787c10b5fc90469b8149bb4fe7bbcd2d
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-08T07:12:56.723571Z'
  stage: review
- number: 9
  speaker: reviewer
  kind: result
  at: '2026-11-08T07:13:40.665588Z'
  stage: review
  run: f81fd80a92854fb9b6c5f5b745bd757f
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-08T07:13:45.561099Z'
  stage: doing
- number: 11
  speaker: coder
  kind: result
  at: '2026-11-08T07:14:05.590554Z'
  stage: doing
  run: c418071a3e884fe981f0da4c398240b2
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T07:14:10.556131Z'
  stage: tests
- number: 13
  speaker: tester
  kind: result
  at: '2026-11-08T07:14:36.580773Z'
  stage: tests
  run: 85e795127956455a905a7ccb95af2610
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-08T07:14:41.611300Z'
  stage: doing
- number: 15
  speaker: coder
  kind: result
  at: '2026-11-08T07:18:57.542142Z'
  stage: doing
  run: 34ee3c2fdaec48548291088be5e5cf96
---

# Kumpel's procedure after an acceptance that proposes stories


## Description

An acceptance merged as "accepted with stories" leaves its proposed stories in the feature's `backlog/`. `archive-feature.sh` then refuses with `<id> is not finished: <path> is in backlog/`. `promote.sh` refuses a feature that is not archived, so the promotion waits until the proposed stories are done and a further acceptance is merged. That is what happened to F0057 after its first acceptance, and its second acceptance's smoke test showed it.

The documents say otherwise:
- `docs/operator-playbook.md`, step 8, archives and promotes right after an accepted feature and only then turns to the proposed stories.
- `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 makes Kumpel report the refusal to the human as a fault.
- Its step 2 does not know that `promote.sh` reuses an open promotion and then prints `promotion open: #<number>, for the human to merge`.
- `docs/operator-guide/install.md`, *The promotion*, does not say when the promotion waits.

This story brings Kumpel's procedure and the operator's documents in line with the scripts. It changes no script. Whether a feature accepted with stories should be promoted at once, without archiving, is the human's choice when refining. Unless the human chooses that, the story describes the behaviour as it is.

## Interface

- `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance* (the coder writes it; `operator/skill/*` is its path):
  - **Step 1:** when the accepted acceptance proposed stories, so that the feature's `backlog/` holds them, the archive's refusal `is in backlog/` is expected. Kumpel tells the human that the archive and the promotion wait for the feature's next accepted acceptance, and starts nothing else for it.
  - **Step 2:** names the reuse of an open promotion and its line `promotion open: #<number>, for the human to merge`.
- Tests: a new module `tests/operator_scripts/test_operator_approving_after_acceptance.py`. It reads only the lines of `approving.md` under `## After a feature's acceptance`, up to the next `## ` heading.
- No script changes, and no earlier test changes.

## Acceptance criteria

1. Under `## After a feature's acceptance` in `approving.md`, step 1 contains `is in backlog/` and `next accepted acceptance`, and step 2 contains `promotion open: #`. These are rows of one test. The same text placed outside that section does not satisfy a row: the test reads only the section.
2. `make check` stays green.
3. docs:
   - `docs/operator-playbook.md`, step 8: after an acceptance with proposed stories, the archive and the promotion follow the feature's next accepted acceptance, not this one.
   - `docs/operator-guide/install.md`, *The promotion*: when a feature's promotion waits, and why.
   - `docs/decisions.md`: an entry only if the human chooses a change of behaviour when refining; otherwise none.

## Smoke test

```bash
uv run pytest tests/operator_scripts/test_operator_approving_after_acceptance.py 2>&1 | tail -1
```
Expect: a line ending in `passed in <seconds>s` with no `failed`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names concrete paths: `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, steps 1 and 2 (both exist today), and the new test module `tests/operator_scripts/test_operator_approving_after_acceptance.py`. No script changes.
   - Criteria: criterion 1 is one parametrized test with rows for step 1 (`is in backlog/`, `next accepted acceptance`) and step 2 (`promotion open: #`). The section-only reading is covered: the same text outside the section does not satisfy a row. That is the failing side. The two closing criteria are in place. The behaviours the Interface states, "tells the human" and "starts nothing else", are checked only through those phrases. Judged acceptable: the section is prose for an agent.
   - Smoke test: the pytest command is runnable. It passes no `-q`, correct because `pyproject.toml` `addopts` already sets `-q`. The `Expect:` line (`passed in <seconds>s`, no `failed`) can be checked against the output.
   - Docs criterion: it names what the reader must know. In the playbook's step 8, the archive and promotion follow the next accepted acceptance. In install.md, when the promotion waits and why. The `decisions.md` entry applies only if the human chooses a behaviour change. It dictates no sentences.
   - Architecture: it fits. Docs and Kumpel's skill text only, with a test under `tests/operator_scripts/` as CLAUDE.md lays out. No code or script is touched.
   - Scope: it is within F0057, which covers Kumpel's procedure and the operator's documents on `develop` and `main`. Nothing in "Out of scope" is touched. Route is `tests`, because `operator/skill/*` is not a path the documenter may write.
4. factory: started tests as vm.
5. tester: Wrote the test for criterion 1. It reads only the lines of `operator/skill/kumpel/references/approving.md` under `## After a feature's acceptance`, up to the next `## ` heading. It splits them into numbered steps (each step with its continuation lines). Each row checks one phrase in one step, so the same text outside the section, or in the other step, does not satisfy a row.

   - criterion 1: tests/operator_scripts/test_operator_approving_after_acceptance.py::test_steps_after_an_acceptance_name_the_waits_of_the_scripts. Three rows: step 1 contains `is in backlog/`, step 1 contains `next accepted acceptance`, step 2 contains `promotion open: #`.
   - criterion 2 (`make check` stays green): no test; the factory's check covers it.
   - criterion 3 (docs): no test; it is the documenter's.

   Files created: `tests/operator_scripts/test_operator_approving_after_acceptance.py`.

   Modules the test run could not import: none. The test runs on the existing file. The run of the new module failed all three rows on the assertion, which is the right reason: today's step 1 says "still in `backlog/`" and does not name the next acceptance, and step 2 does not name the reuse of an open promotion. `make lint` is green.

   Rejected: moving the section-reading lines of `test_operator_archive_outcome.py::test_approving_names_the_refusal_of_a_feature_whose_acceptance_was_not_accepted` into `tests/support/`. Its four inline lines find only the first line of a step, and this story says to change no earlier test. The new module holds its own small reader that also takes a step's continuation lines. No earlier test file was changed.

   `lint`: lint: green (0.2 s)
6. factory: started doing as vm.
7. coder: Built: `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*. This is a text change only. No script or test changed.
   - Step 1 has a new continuation line. When the accepted acceptance proposed stories, the feature's `backlog/` holds them. The refusal `<feature id> is not finished: <path> is in backlog/` is then expected and is not a fault. Kumpel tells the human that the archive and the promotion wait for the feature's next accepted acceptance, and starts nothing else for the feature.
   - Step 2 now says that `promote.sh` reuses an open promotion: it adds the feature's stories to the open pull request and opens no second one. With the switch off it prints `promotion open: #<number>, for the human to merge`, and Kumpel tells the human the same. I checked the wording against `operator/skill/kumpel/scripts/archive-feature.sh` (`refuse "$story is in $folder/"`) and `promote.sh` (`echo "promotion $state: #$number, for the human to merge"`).

   Main choice: I put the new case for step 1 on a continuation line under step 1, not inside step 1's first line. `tests/operator_scripts/test_operator_archive_outcome.py::test_approving_names_the_refusal_of_a_feature_whose_acceptance_was_not_accepted` reads only that first line and checks `is not finished: its last acceptance`. Keeping the first line as it was leaves that test untouched. The new test reads a step together with its continuation lines. The alternative I rejected was rewriting step 1's first line into a longer list of refusals. That would make the other refusals harder to read and would put the existing test's phrase at risk.

   Refactor: I read the diff and found nothing to change.

   Noticed, not touched: step 1's first line still says "report that to the human" for every refusal. The continuation line narrows that for the `backlog/` case. The documenter still has the docs criterion: `docs/operator-playbook.md` step 8 and `docs/operator-guide/install.md` *The promotion*. The journal did not change the task's meaning, so the Description stays as it is.

   `make check`: check: green (test: green, 109.5 s).

   `check`: check: green
   `duplicates`: duplicates: 6 new, 39 known, 4 gone
8. factory: started review as vm.
9. reviewer: Reviewed `git diff develop...HEAD -- . ':!factory'`, which changes `operator/skill/kumpel/references/approving.md` and adds `tests/operator_scripts/test_operator_approving_after_acceptance.py`, against the work item. I checked the new wording against the scripts. The refusal `<id> is not finished: <path> is in backlog/` matches `operator/skill/kumpel/scripts/archive-feature.sh:23,29`. The open promotion being patched or kept, and the line `promotion open: #<number>, for the human to merge` printed only with the switch off, match `operator/skill/kumpel/scripts/promote.sh:47-52,61-77`. Criterion 1 is one parametrized test with three rows. It reads only the `## After a feature's acceptance` section, step by step, so text outside the section or in the other step cannot satisfy a row. The coder's journal entry 7 records `make check` green. The Description, the Interface and the docs criterion match what was built. No architecture or security findings: the change is skill text and one test, with no new suppression marker.

   1. `tests/operator_scripts/test_operator_approving_after_acceptance.py:16-18` (`section_steps`): the lines that find the section copy code that already exists. They repeat the inline lines of `tests/operator_scripts/test_operator_archive_outcome.py:121-124` and do the job of `factory.shared.domain.sections.section_text` (`src/factory/shared/domain/sections.py:128`, already used by `tests/support/shipped_agents.py:162`). Fix: the tester gets the section with `section_text(APPROVING.read_text(encoding="utf-8"), "After a feature's acceptance")` and keeps only the code that splits the result into numbered steps. This is a test-only change, and the coder hands it to the tester.

   Earlier tests: none. The diff adds one test file (`A`) and changes, renames or deletes no test file that `develop` holds.
10. factory: started doing as vm.
11. coder: Round 1. I changed no code. The reviewer's one finding, entry 9 item 1, asks for a change only to this story's own test, so it goes to the tester.

    The change: in `tests/operator_scripts/test_operator_approving_after_acceptance.py`, `section_steps` should stop finding the section itself (the `lines.index(SECTION)` / `startswith("## ")` lines, and the `SECTION` constant). It should get the section from `factory.shared.domain.sections.section_text(APPROVING.read_text(encoding="utf-8"), "After a feature's acceptance")` (`src/factory/shared/domain/sections.py:128`, already used by `tests/support/shipped_agents.py:162`). It keeps only the code that splits that text into numbered steps with their continuation lines. The three rows and the test's name stay the same. `section_text` returns `str | None`, so the test must handle `None` to satisfy mypy.

    Main choice: I hand it to the tester rather than editing the test myself, because the coder never edits tests (R9). The alternative I rejected was a `question`: the finding concerns a test written in this story, so no other story's test changes and the human's leave is not needed.

    `operator/skill/kumpel/references/approving.md` stays as it was in entry 7. The journal did not change the task's meaning, so the Description stays as it is. I did not run `make check` this round because nothing in the working tree changed.

    Noticed, not touched: `tests/operator_scripts/test_operator_archive_outcome.py:121-124` still finds the section with its own inline lines. Changing that test would need the human's leave or the standing leave to move a shared helper, and this story says no earlier test changes.
12. factory: started tests as vm.
13. tester: Mode: the test change the coder's entry 11 names, which carries out the reviewer's finding in entry 9 item 1. It is a change to this story's own test only. No earlier test file changed.

    Changed `tests/operator_scripts/test_operator_approving_after_acceptance.py`, `section_steps`:
    - It no longer finds the section itself. The `lines.index(...)` and `startswith("## ")` lines are gone.
    - It now gets the section from `factory.shared.domain.sections.section_text(APPROVING.read_text(encoding="utf-8"), "After a feature's acceptance")`.
    - It asserts that the result is not `None`, with a message naming the file and the heading, which handles `str | None` for mypy.
    - It keeps only the code that splits the text into numbered steps with their continuation lines.

    The test's name and its three rows are unchanged.

    One departure from entry 11: the coder asked for the `SECTION` constant to be removed. I kept it, now holding only the heading name (`After a feature's acceptance`, without `## `), because it is used twice: in the call and in the assertion message. It no longer feeds a heading search of the test's own.

    Mapping, unchanged:
    - criterion 1: tests/operator_scripts/test_operator_approving_after_acceptance.py::test_steps_after_an_acceptance_name_the_waits_of_the_scripts
    - criterion 2 (`make check` green): no test, the factory's check.
    - criterion 3 (docs): no test, the documenter's.

    Files created: none this round. Changed: the file above.

    Modules the test run could not import: none.

    Run: `uv run pytest -q tests/operator_scripts/test_operator_approving_after_acceptance.py` passed all three rows. That is expected, because the coder's skill text from entry 7 is already on the branch.

    `make lint`: lint: green (0.1 s).

    `lint`: lint: green (0.2 s)
14. factory: started doing as vm.
15. coder: Round 1, after the tester's change. I changed no code this round. The reviewer's one finding (entry 9, item 1) was a change to this story's own test only. The tester made it in entry 13: `section_steps` in `tests/operator_scripts/test_operator_approving_after_acceptance.py` now gets the section from `factory.shared.domain.sections.section_text`. Nothing else is left for the coder.

    Built (unchanged since entry 7): `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*.
    - Step 1 has a continuation line for the case where the accepted acceptance proposed stories. The refusal `is in backlog/` is then expected, and Kumpel tells the human that the archive and the promotion wait for the feature's next accepted acceptance.
    - Step 2 names the reuse of an open promotion and its line `promotion open: #<number>, for the human to merge`.

    Main choice (from entry 7): the new step-1 case is a continuation line, not part of step 1's first line. `test_operator_archive_outcome.py` reads only that first line, so it stays untouched. Rejected: rewriting the first line into a longer list of refusals.

    Refactor: there is no new diff this round, so nothing to change.

    Noticed, not touched:
    - `tests/operator_scripts/test_operator_archive_outcome.py:121-124` still finds the section with its own inline lines. Changing it needs the human's leave, and this story changes no earlier test.
    - The docs criterion is the documenter's: `docs/operator-playbook.md` step 8 and `docs/operator-guide/install.md` *The promotion*.
    - The journal did not change the task's meaning, so the Description stays as it is.

    `make check`: check: green (test: green, 108.4 s).

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
