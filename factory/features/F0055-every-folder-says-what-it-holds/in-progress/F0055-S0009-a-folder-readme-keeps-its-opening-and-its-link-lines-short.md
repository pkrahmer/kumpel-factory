---
stage: smoke-test
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 641
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-07T15:06:28.399880Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-07T15:06:28.406925Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-07T15:06:50.924801Z'
  stage: intake
  run: 162835f69b1e4918a5ba14b8dbd1b009
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-07T15:06:55.954507Z'
  stage: tests
- number: 5
  speaker: tester
  kind: result
  at: '2026-11-07T15:07:33.654163Z'
  stage: tests
  run: 51afc1090c0240be85ad5b71de1a994f
- number: 6
  speaker: factory
  kind: started
  at: '2026-11-07T15:07:38.705306Z'
  stage: doing
- number: 7
  speaker: coder
  kind: result
  at: '2026-11-07T15:14:05.770029Z'
  stage: doing
  run: 135c25bb765449199275e7124de72eaf
- number: 8
  speaker: factory
  kind: started
  at: '2026-11-07T15:14:10.702703Z'
  stage: review
- number: 9
  speaker: reviewer
  kind: result
  at: '2026-11-07T15:15:30.312823Z'
  stage: review
  run: cf32733647be4e6cba3840f08cefb1af
- number: 10
  speaker: factory
  kind: started
  at: '2026-11-07T15:15:35.398669Z'
  stage: doing
- number: 11
  speaker: coder
  kind: result
  at: '2026-11-07T15:15:54.564907Z'
  stage: doing
  run: cc10a00b7fa2466eb9a9eb90808346de
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-07T15:15:59.509728Z'
  stage: tests
- number: 13
  speaker: tester
  kind: result
  at: '2026-11-07T15:16:29.893680Z'
  stage: tests
  run: 4e04f2d0413946098b040b6551197792
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-07T15:16:35.043846Z'
  stage: doing
- number: 15
  speaker: coder
  kind: result
  at: '2026-11-07T15:20:45.739022Z'
  stage: doing
  run: 6c803c1d776a4ea3b72d43efd729a86d
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-07T15:20:50.915746Z'
  stage: review
- number: 17
  speaker: reviewer
  kind: result
  at: '2026-11-07T15:21:39.668134Z'
  stage: review
  run: 7177beae61604b6db9eb360df3470bc2
- number: 18
  speaker: factory
  kind: started
  at: '2026-11-07T15:21:44.956647Z'
  stage: docs
- number: 19
  speaker: documenter
  kind: result
  at: '2026-11-07T15:26:11.936282Z'
  stage: docs
  run: 7629bc6bb47740fb84a6746c72629510
---

# A folder README keeps its opening and its link lines short

## Description

Feature decision 6 says a folder README stays a pointer: an opening of at most two sentences and nothing beside the links and the subfolder lines. `readme_problems` lets two things past it. A line that carries a relative link is taken as a link line and never counted, so an opening that carries a link escapes the two-sentence limit (`One. Two. Three. Four. Five, see [g](g.md).` gives `[]`), and a link line may hold any number of sentences of any length, after the subfolder list too (eight lines of 200 words, each with a link, give `[]`). Only the line limit bounds them. `docs/project-guide/style.md` already says "no other prose", so the code is laxer than the documents. This story closes both: the opening is the first paragraph after the title and counts its sentences whether or not it carries a link, and every other line that is no subfolder line and carries a relative link holds one sentence of at most 25 words. The word limit of the opening itself and the number of link lines stay as they are (the human, 2026-11-07). No README changes in this story: the human shortened `docs/README.md`'s one long link line on main before it started, so all 22 READMEs keep to the new rules.

## Interface

- `factory.shared.domain.folder_readmes` (domain), changed:

```python
LINK_LINE_SENTENCES: Final = 1
LINK_LINE_WORDS: Final = 25

def readme_problems(folder: str, readme: str | None, subfolders: Sequence[str]) -> list[str]
```

- The opening is the paragraph right after the title: its consecutive non-blank lines, up to the first blank line. Its sentences are counted whether or not a line of it carries a relative link; more than `OPENING_SENTENCES` (two) gives `<folder>: the opening is longer than two sentences`, as today. A link in the opening still counts as the README's link to a guide.
- A link line is a line after the opening, outside code blocks, that is no subfolder line and carries a relative link (by `relative_link_targets`, as today). It holds at most `LINK_LINE_SENTENCES` sentence and at most `LINK_LINE_WORDS` words, words separated by whitespace with the link's markdown counted as written; past either limit it gives `<folder>: line <n> is a long link line`, `<n>` the 1-based line number in the whole README, blank lines counted.
- A line after the opening that is no subfolder line and carries no relative link stays `<folder>: line <n> is no part of the form`; a README without a title keeps having no opening.
- The tests are new rows of `tests/shared/domain/test_folder_readmes.py::test_a_readme_out_of_its_form_gives_one_line_per_rule` (written by F0055-S0001). The human's leave (2026-11-07): the tester adds rows to that test and changes none of its rows; every existing row keeps its result.

## Acceptance criteria

1. An opening that carries a relative link counts its sentences, rows of the test of the form: an opening of two sentences with a link gives no line; one of three sentences with a link gives `<folder>: the opening is longer than two sentences`.
2. A link line keeps its limits, rows of the same test: a link line of one sentence of 25 words gives no line; one of 26 words gives `<folder>: line <n> is a long link line`; one of two sentences gives the same line; a link line of 26 words after the subfolder list gives it too.
3. Every existing row of the test of the form keeps its result.
4. The opening ends at its first blank line, a row of the same test: a line without a relative link in the paragraph right after the opening (`line 5` of the test's README) gives `<folder>: line 5 is no part of the form`.
5. A link in the opening counts as the README's link to a guide, a row of the same test: a README whose only relative link is in its opening gives no `<folder>: links to no guide`.
6. `make check` stays green.
7. docs: `docs/project-guide/style.md`, *Folder READMEs*: the reader learns that the opening is the first paragraph and counts its sentences with or without a link, and that a line with a link outside it is one sentence of at most 25 words. `docs/project-guide/shared.md`, *The folder READMEs*: the new finding of `readme_problems`.

## Smoke test

```bash
uv run python -c "from factory.shared.domain.folder_readmes import readme_problems; print(readme_problems('w', '# W\n\nOne. Two. Three, see [g](g.md).\n\n- \`a/\` One sentence.\n', ['a']))"
```
Expect: `['w: the opening is longer than two sentences']`

```bash
uv run python -c "from factory.shared.domain.folder_readmes import readme_problems; print(readme_problems('w', '# W\n\nOne.\n\n- \`a/\` One sentence.\n\nMore here, see [g](g.md). And more.\n', ['a']))"
```
Expect: `['w: line 7 is a long link line']`

```bash
uv run pytest tests/guards/test_folder_readmes.py 2>&1 | tail -1 | grep -c failed
```
Expect: `0`

## Journal

1. 2026-11-07 human: created.
2. factory: started intake as vm.
3. intake: accepted
   - Interface: names `factory.shared.domain.folder_readmes`, the two constants `LINK_LINE_SENTENCES` and `LINK_LINE_WORDS`, and the `readme_problems` signature. It also states the opening as the paragraph up to the first blank line, the new finding text `line <n> is a long link line`, and how words and line numbers are counted.
   - Criteria: each is testable as a row of the existing parametrized test.
     - The opening is covered on both sides (two sentences with a link pass, three fail).
     - The link line is covered on both sides: 25 words pass, 26 words fail, two sentences fail, and 26 words after the subfolder list fail.
     - Criterion 3 keeps the existing rows' results. The Interface names the human's leave to add rows to that test and change none (2026-11-07).
     - The unchanged rules (a line without a link is "no part of the form", no title means no opening) stay pinned by the existing rows.
   - Smoke test: the commands are runnable. In the second one, `More here…` falls on line 7, so the expected `line 7` is right. The pytest command passes no `-q`, and the project's `addopts` already sets it. Its `grep -c failed` on the summary line gives `0`, so the Expect line can be checked.
   - Docs criterion: it names what the reader must know, in `style.md` *Folder READMEs* and `shared.md` *The folder READMEs*. It dictates no sentences.
   - Architecture: the change is confined to a pure `shared.domain` module with no I/O, as CLAUDE.md requires.
   - Scope: it fits feature decision 6 (a README stays a pointer) and is not in the feature's out-of-scope list. The route is `tests` because the Interface changes code under `src/`.
4. factory: started tests as vm.
5. tester: Added seven rows to `test_a_readme_out_of_its_form_gives_one_line_per_rule` in `tests/shared/domain/test_folder_readmes.py`, as the human allowed on 2026-11-07. I did not change any existing row. I also added a constant `GUIDE_LINK`, a constant `LONG_LINK_LINE_5` and a helper `_link_line(words)` to the same module. The helper builds one sentence with a relative link; the link `[the guide](../docs/README.md)` counts as two words, as written.

   - criterion 1: tests/shared/domain/test_folder_readmes.py::test_a_readme_out_of_its_form_gives_one_line_per_rule, rows `opening-of-two-sentences-with-a-link` (no line) and `opening-of-three-sentences-with-a-link` (the opening line)
   - criterion 2: the same test, rows `link-line-of-25-words` (no line), `link-line-of-26-words` and `link-line-of-two-sentences` (both `line 5 is a long link line`), `link-line-of-26-words-after-the-list` (`line 9 is a long link line`). The row `link-line-of-25-words-after-the-list` (no line) is the accepted side of that limit after the list.
   - criterion 3: the existing rows of the same test and of `test_a_readme_and_its_subfolders_give_what_they_disagree_on`, unchanged. All of them pass today.
   - criterion 4: `make check`, the coder's to keep green. `make lint` is green.
   - criterion 5: docs, not tested.

   Files: no new files. The only file changed is `tests/shared/domain/test_folder_readmes.py`, which F0055-S0001 wrote, under the leave quoted in the Interface.

   Run (`uv run pytest -q tests/shared/domain/test_folder_readmes.py`): four rows fail because the result is wrong. They are `opening-of-three-sentences-with-a-link`, `link-line-of-26-words`, `link-line-of-two-sentences` and `link-line-of-26-words-after-the-list`; each gets `[]` where one line is expected. Every other row passes. The test runner imported every module, since `factory.shared.domain.folder_readmes` already exists. The rows do not import the new constants `LINK_LINE_SENTENCES` and `LINK_LINE_WORDS`.

   `lint`: lint: green (0.1 s)
6. factory: started doing as vm.
7. coder: Built: `src/factory/shared/domain/folder_readmes.py`. No other file changed, and no test changed.

   - New constants `LINK_LINE_SENTENCES` (1) and `LINK_LINE_WORDS` (25).
   - The opening is now one paragraph: the first blank line after an opening line ends it (`past_opening`). A line in the opening that carries a relative link stays in the opening, so its sentences are counted. The link still counts as the README's link to a guide.
   - `_read_line_past_opening` sorts each line after the opening that is no subfolder line. A line without a relative link still gives `line <n> is no part of the form`. A line with one is checked against the new limits and gives `line <n> is a long link line`, `<n>` the 1-based line number.
   - `_form_problems` adds the new finding.

   Main choice: the opening ends at its blank line, which follows the Interface's "first paragraph". I rejected the other option, keeping the old rule where a link line ends the opening. Under that rule an opening of three sentences with a link on its first line would still slip past the limit.

   Refactor: the subfolder check and the new link-line check were the same sentence-and-word test. I merged them into one helper, `_is_longer_than(text, sentences, words)`. Behaviour is unchanged.

   Checks:
   - `make check` is green.
   - The tests in `tests/shared/domain/test_folder_readmes.py` and `tests/guards/test_folder_readmes.py` pass, so all 22 real READMEs keep to the new rules.
   - The first two smoke commands print the expected lines.

   The journal did not change the meaning of the task, so I left `## Description` as it was.

   Noticed, not touched: a subfolder line written right under the opening with no blank line between still ends the opening, as before.

   `check`: check: green
   `duplicates`: duplicates: 6 new, 39 known, 4 gone
8. factory: started review as vm.
9. reviewer: Reviewed `git diff main...HEAD -- . ':!factory'` (`src/factory/shared/domain/folder_readmes.py`, `tests/shared/domain/test_folder_readmes.py`) against the work item. The code matches the Interface. The opening now ends at its first blank line (`_read_line`), so a link inside it no longer ends it. A link line after the opening is checked by `_read_line_past_opening` through `_is_longer_than`. The finding text and the line numbers match the Interface. The new rows cover criteria 1 and 2 on both sides of each limit: 2/3 sentences with a link, 25/26 words before and after the list, and 1/2 sentences. Each row's README is built so that the line numbers 5 and 9 are right. The coder's `make check` was green (journal 7). Architecture holds: the change stays in a pure `shared.domain` module with no I/O. Security is clean: no markers and no strings handed to a shell. Quality is fine: the shared `_is_longer_than` removes the old copied sentence-and-word check. There is no dead code, and the one comment says why.

   Findings:
   1. criterion 4 added: it needs its test. `folder_readmes.py:_read_line` makes a new behaviour that no row pins. A line without a relative link in the paragraph after the opening used to count as part of the opening. It now gives `line <n> is no part of the form`. The existing rows show this only after the subfolder list (`free-prose-after-the-list`). The row `only-link-a-web-address` now also gives `line 5 is no part of the form`, but it does not assert it. Fix: a row of `test_a_readme_out_of_its_form_gives_one_line_per_rule`, for example `_readme(links=(FREE_PROSE,))` expecting `operator: line 5 is no part of the form` once.
   2. criterion 5 added: it needs its test. The Interface says "A link in the opening still counts as the README's link to a guide", and `_read_line` was rewritten around `has_link`. Every row still carries the default `LINK` line, so no row has its only relative link in the opening. Fix: a row such as `_readme(opening=(f"What it holds, see {GUIDE_LINK}.",), links=())` expecting `operator: links to no guide` zero times.

   description corrected: "All 22 READMEs of today keep to these rules (measured at the feature's acceptance), so no README changes." -> removed. The Description's last sentence already says what is true: the human shortened `docs/README.md`'s long link line before this story started.

   I renumbered the closing criteria: `make check` is now 6 and docs is now 7.

   I could not read the new findings that `make duplicates` reported (journal 7: "6 new"): no report is in the checkout. The diff is small and adds no copied logic.

   Earlier tests:
   - `tests/shared/domain/test_folder_readmes.py` (written by F0055-S0001): changed under the human's leave named in the Interface (2026-11-07). It only adds rows, plus the module-level `GUIDE_LINK`, `LONG_LINK_LINE_5` and `_link_line` that they use. No existing test or row changed.
10. factory: started doing as vm.
11. coder: Round 1: the reviewer's latest entry added two criteria, and both need only their test rows. I changed no code and no test, and I did not run `make check` this round.

    - criterion 4: a line without a relative link in the paragraph right after the opening gives `<folder>: line 5 is no part of the form`. Add it as a row of `tests/shared/domain/test_folder_readmes.py::test_a_readme_out_of_its_form_gives_one_line_per_rule`, for example `_readme(links=(FREE_PROSE,))` expecting that line once.
    - criterion 5: a README whose only relative link is in its opening gives no `<folder>: links to no guide`. Add it as a row of the same test, for example `_readme(opening=(f"What it holds, see {GUIDE_LINK}.",), links=())` expecting that line zero times.

    I checked both against `src/factory/shared/domain/folder_readmes.py` as it stands:
    - `'# W\n\nOne.\nTwo.\n\nFree prose here.\n\n- \`a/\` One sentence.\n'` gives `w: line 6 is no part of the form` (and `links to no guide`, since it has no link at all).
    - `'# W\n\nWhat it holds, see [g](../docs/README.md).\n\n- \`a/\` One sentence.\n'` gives `[]`.

    So the new rows should pass without a code change. What the journal changed: the reviewer added criteria 4 and 5 and renumbered the closing ones. The Description already says this, so I did not rewrite it.
12. factory: started tests as vm.
13. tester: I added the two rows that the coder's entry 11 named, for the two criteria the reviewer added. Both are new rows of `test_a_readme_out_of_its_form_gives_one_line_per_rule` in `tests/shared/domain/test_folder_readmes.py`. The human's leave of 2026-11-07, quoted in the Interface, allows adding rows to that test. I changed no existing row.

    - criterion 4: `tests/shared/domain/test_folder_readmes.py::test_a_readme_out_of_its_form_gives_one_line_per_rule`, row `prose-in-the-paragraph-after-the-opening`. The README is `_readme(links=(FREE_PROSE,))`, and the test expects `operator: line 5 is no part of the form` once.
    - criterion 5: the same test, row `only-link-in-the-opening`. The README is `_readme(opening=(f"What it holds, see {GUIDE_LINK}.",), links=())`, and the test expects `operator: links to no guide` zero times.

    Mapping of the other criteria, unchanged from entry 5:
    - criterion 1: the rows `opening-of-two-sentences-with-a-link` and `opening-of-three-sentences-with-a-link`.
    - criterion 2: the `link-line-*` rows.
    - criterion 3: the existing rows.
    - criterion 6: `make check`.
    - criterion 7: docs, not tested.

    Files: no new files were created. The only file changed is `tests/shared/domain/test_folder_readmes.py`, which F0055-S0001 wrote.

    Results:
    - `uv run pytest -q tests/shared/domain/test_folder_readmes.py`: 32 passed and none failed. The new rows pass because the coder's code already handles them, as entry 11 predicted, so they were never red.
    - The test runner imported every module.
    - `make lint`: green.

    `lint`: lint: green (0.2 s)
14. factory: started doing as vm.
15. coder: Round 1: the tester added rows for the two criteria the reviewer added. They are `prose-in-the-paragraph-after-the-opening` (criterion 4) and `only-link-in-the-opening` (criterion 5) in `tests/shared/domain/test_folder_readmes.py`. Both pass against `src/factory/shared/domain/folder_readmes.py` as entry 7 left it. So this round has nothing to fix and no code changed: no file under `src/` and no test.

    - Built: nothing new this round. The implementation is still the one entry 7 describes, in `src/factory/shared/domain/folder_readmes.py`.
    - Main choice (unchanged): the opening ends at its first blank line, so a link inside it no longer ends it. I rejected keeping the old rule, where a link line ended the opening.
    - Refactor: I left it alone. The diff is the same one the reviewer read in entry 9.
    - Description: the journal changed nothing here beyond the reviewer's criteria 4 and 5, which the Description already holds, so I did not rewrite it.
    - Noticed, not touched: as in entry 7, a subfolder line written right under the opening with no blank line between still ends the opening.

    `make check`: green, run this round. The final lines were `test: green (102.6 s)` and `check: green`.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
16. factory: started review as vm.
17. reviewer: Round 1 review of `git diff main...HEAD -- . ':!factory'`, which changes `src/factory/shared/domain/folder_readmes.py` and `tests/shared/domain/test_folder_readmes.py`. I read the diff against the work item.

    no findings

    What I checked:
    - **Group 1, the acceptance criteria.** Every criterion has a row of `test_a_readme_out_of_its_form_gives_one_line_per_rule`, and I worked out each row's README line by line.
      - Criterion 1: the rows `opening-of-two-sentences-with-a-link` (0) and `opening-of-three-sentences-with-a-link` (1).
      - Criterion 2: the rows `link-line-of-25-words` and `link-line-of-26-words` at line 5, `link-line-of-two-sentences`, and `link-line-of-25-words-after-the-list` and `link-line-of-26-words-after-the-list` at line 9.
        - `_link_line(25)` is 25 words with the link's markdown counted as written.
        - It is one sentence, because `_SENTENCE_END` does not match the `.md)` inside the link.
        - So both sides of both limits (25/26 words, 1/2 sentences) are tested.
      - Criterion 3: the diff only adds rows and module-level helpers. No existing row changed.
      - Criterion 4: `prose-in-the-paragraph-after-the-opening` expects line 5.
      - Criterion 5: `only-link-in-the-opening`.
      - The coder's `make check` was green (journal 15). Both of the reviewer's earlier findings now have rows.
    - **The code against the Interface.**
      - `_read_line` ends the opening at the first blank line after it, and sets `has_link` before it sorts the line, so a link in the opening counts as the link to a guide.
      - `_read_line_past_opening` keeps `line <n> is no part of the form` for a line without a link and adds `line <n> is a long link line` through `_is_longer_than` with `LINK_LINE_SENTENCES`/`LINK_LINE_WORDS`.
      - Line numbers are 1-based over the whole README. Code blocks are skipped as before.
      - A README without a title still starts `past_opening`.
    - **Group 2, architecture:** the change stays in a pure `shared.domain` module, with no I/O and no new imports.
    - **Group 3, security:** no markers, secrets or shell strings.
    - **Group 4, quality.**
      - `_is_longer_than` replaces the sentence-and-word check that the subfolder line used to carry inline, so the new rule copies nothing.
      - There is no dead code, and the one new comment says why.
      - I ran `make duplicates` myself because the earlier review could not read it: `6 new, 39 known, 4 gone`.
        - The one new finding in this diff's module is vulture's `unused function 'readme_problems'` (60 %). That was already true on main: only tests call the function, and the baseline does not carry it.
        - The other five are in modules this diff does not touch.
    - **Group 5, work item hygiene:**
      - The journal gives the main choice (the opening ends at its blank line) and the option rejected (a link line ending the opening).
      - The Description matches what was built.
      - Docs criterion 7 names what the reader of `style.md` and `shared.md` must learn.

    Earlier tests:
    - `tests/shared/domain/test_folder_readmes.py` (written by F0055-S0001): changed under the human's leave of 2026-11-07 that the Interface quotes. It adds rows to `test_a_readme_out_of_its_form_gives_one_line_per_rule` and the module-level `GUIDE_LINK`, `LONG_LINK_LINE_5` and `_link_line` that they use, and changes no existing row or test.

    Notes:
    - `tests/shared/domain/test_folder_readmes.py`: the string `f"{FOLDER}: line 9 is a long link line"` is written out in two rows, while line 5 has the constant `LONG_LINK_LINE_5`. This is a naming point and does not send the work item back.
18. factory: started docs as vm.
19. documenter: Docs for the new `readme_problems` rules. I read `src/factory/shared/domain/folder_readmes.py` on the branch before writing, and `make documents` ended with `documents ok (61.4 s)`. I did not run `make check`, because I changed only documents.

    Files changed:
    - `docs/project-guide/style.md`, *Folder READMEs*:
      - The opening is the first paragraph after the title, up to the first blank line.
      - Its sentences are counted with or without a link, and a link in it counts as the link to a guide.
      - A line outside the opening that carries a relative link and is no subfolder line is one sentence of at most 25 words, the link's markdown counted as written.
    - `docs/project-guide/shared.md`, *The folder READMEs*: a new bullet on `readme_problems`.
      - It gives the opening's limit.
      - It gives `line <n> is no part of the form` for a line with no relative link.
      - It gives the new `line <n> is a long link line` for a link line past `LINK_LINE_SENTENCES` (1) or `LINK_LINE_WORDS` (25).
      - `<n>` is the 1-based line number in the whole README.

    Cross-read and found current:
    - The `tests/guards/test_folder_readmes.py` description in `docs/project-guide/README.md` line 66.
    - The rest of `style.md` and `shared.md`.
    - `docs/decisions.md`: it has no entry on folder READMEs or `readme_problems`, so I wrote nothing there.

    Stale text I noticed: none. No finding for the coder: the code matches the Interface.

    `check`: check: green
    `secrets`: secrets: green (0.5 s)
    `documents`: documents ok (61.0 s)
