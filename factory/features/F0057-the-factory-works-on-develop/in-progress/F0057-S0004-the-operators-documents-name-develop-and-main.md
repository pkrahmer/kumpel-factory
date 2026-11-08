---
stage: docs
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 646
comments_read: [6715370076, 6715449873]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T00:59:32.597955Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T00:59:32.605075Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T00:59:49.265142Z'
  stage: intake
  run: 666d05e36618439fa27c8bb4c515b704
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T01:03:40.357080Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T01:03:42.716682Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T01:04:04.291193Z'
  stage: intake
  run: 2435763283c24c4da595bcada092ae31
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T01:04:09.458261Z'
  stage: docs-only
- number: 8
  speaker: documenter
  kind: result
  at: '2026-11-08T01:08:05.344884Z'
  stage: docs-only
  run: b9fcb1c5395e49419b8ab84aa87bc1da
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T01:08:10.450023Z'
  stage: tests
- number: 10
  speaker: tester
  kind: question
  at: '2026-11-08T01:08:40.216532Z'
  stage: tests
  run: 62794c19435f4faf8aa5e3216a099317
  blocked: question
- number: 11
  speaker: human
  kind: comment
  at: '2026-11-08T01:10:28.785314Z'
  stage: tests
- number: 12
  speaker: factory
  kind: started
  at: '2026-11-08T01:10:31.265788Z'
  stage: tests
- number: 13
  speaker: tester
  kind: result
  at: '2026-11-08T01:11:20.978493Z'
  stage: tests
  run: b9680d04450a486598f4610a2724c551
- number: 14
  speaker: factory
  kind: started
  at: '2026-11-08T01:11:25.936867Z'
  stage: doing
- number: 15
  speaker: coder
  kind: result
  at: '2026-11-08T01:16:56.121489Z'
  stage: doing
  run: 6067e4ffa80b427a9d0302a90a7c4c39
- number: 16
  speaker: factory
  kind: started
  at: '2026-11-08T01:17:01.678738Z'
  stage: review
- number: 17
  speaker: reviewer
  kind: result
  at: '2026-11-08T01:18:42.755478Z'
  stage: review
  run: 98ef0014253e4e9c963c22489444f0e8
---

# The operator's documents name develop and main

## Description

After F0057-S0002 and S0003 the factory and Kumpel work on `develop`, and `main` is the protected line of accepted features. The operator's documents still name `main` as the branch the factory works on, about 130 times. This story corrects them, so that an operator knows which branch holds what, how to create `develop` for a new project, how to protect `main`, and how a feature reaches `main`. Its one code change, decided by the human (journal entry 11), takes `promote` and `promoted` out of the v1 words of the document check (`GLOSSARY_FORBIDDEN` in `src/factory/shared/domain/documents.py`), so that the guide can name the switch `promote`; the earlier test that pins that list changes with the human's leave.

## Interface

- The documents: `docs/operator-guide/*.md`, `docs/operator-playbook.md`, the root `README.md` and `operator/README.md`. Every mention of the factory's working branch says `develop`; a mention of the line of accepted features says `main`. `docs/runs/` and the entries of `docs/decisions.md` stay as they are.
- `docs/operator-guide/install.md`: a new project needs `develop`, created from `main`; the preflight names a missing `origin/develop`.
- A section, in the operator guide page the documenter judges right, on protecting `main`: a ruleset that requires a pull request with zero approvals and blocks force pushes and deletion, and why zero (one identity for the factory, Kumpel and the human; GitHub refuses an author's own approval). The promotion: after a feature's acceptance, Kumpel archives the feature and promotes `develop` to `main` with a merge commit, behind the switch `promote`; `main` is never fixed directly.
- The stop `main_branch_failing` keeps its name and means the working branch (F0057 decision 6); `docs/operator-guide/stops.md` says so.
- The documenter finds the mentions by script (`grep -nE` for `main` as a branch in the files above) and quotes the script's list of the mentions left as `main` in its entry, each meaning the line of accepted features; the reviewer checks with the same script. The story took the docs route; the one code change and its tests are those of journal entry 11.

## Acceptance criteria

1. No document of the Interface names `main` as the branch the factory works on; every remaining `main` as a branch means the line of accepted features (the script of the Interface, its output quoted).
2. `install.md` tells a new project to create `develop` from `main`, and says that the preflight names a missing `origin/develop`.
3. The operator guide tells how to protect `main`: a ruleset that requires a pull request with zero approvals and blocks force pushes and deletion, and why zero approvals (one identity for the factory, Kumpel and the human; GitHub refuses an author's own approval).
4. The operator guide tells that after a feature's acceptance Kumpel archives the feature and then promotes `develop` to `main` with a merge commit, behind the switch `promote`.
5. The operator guide tells that `main` is never fixed directly: a fix goes to `develop` and reaches `main` with the next promotion.
6. `stops.md` says that `main_branch_failing` means the working branch.
7. `make documents` ends with `documents ok (<seconds> s)`.
8. `promote` and `promoted` are no longer v1 words: the document check accepts them in a checked document, and the other v1 words stay forbidden.
9. `make check` stays green.
10. docs: the files of the Interface; the reader knows which branch holds what, how to set up and protect them, and how a feature is promoted.

## Smoke test

```bash
uv run python -m factory.entry.check_documents | tail -1
```
Expect: `documents ok (<seconds> s)`

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Questions (the format check passed; the Interface, scope, architecture and route are fine, but two Interface behaviours have no criterion):

   1. The Interface says `install.md` states that the preflight names a missing `origin/develop`. Criterion 2 only covers "create `develop` from `main`". Should criterion 2 also require that `install.md` says the preflight names a missing `origin/develop`? I would choose yes: extend criterion 2.

   2. The Interface lists several separate behaviours of the promotion section: the ruleset blocks force pushes and deletion, the promotion is a merge commit, it runs behind the switch `promote`, Kumpel archives the feature first, and `main` is never fixed directly (a fix goes to `develop`). Criterion 3 says only "how to protect `main`, why zero approvals, how a feature reaches `main`". Each stated behaviour needs its own checkable criterion, or the documenter and reviewer will read criterion 3 two ways. I would choose to split criterion 3 into: (a) protecting `main`, with the ruleset's three rules and why zero approvals; (b) promotion after acceptance, as a merge commit behind the switch `promote`, after Kumpel archives the feature; (c) `main` is never fixed directly.

   Everything else is accepted as written. The smoke test is runnable and its Expect line is checkable. The docs criterion names what the reader must know and dictates no sentences. The story is within F0057's scope.
4. 2026-11-08 human: 1. Yes. 2. Yes, split criterion 3 into (a), (b) and (c) as you wrote them.
5. factory: started intake as vm.
6. intake: accepted, with the human's answer (journal entry 4) carried into the story: criterion 2 now also requires that `install.md` says the preflight names a missing `origin/develop`; criterion 3 is split into 3 (protecting `main`: the ruleset's three rules and why zero approvals), 4 (promotion after acceptance: Kumpel archives first, then a merge commit, behind the switch `promote`) and 5 (`main` is never fixed directly). The later criteria are renumbered (6 stops, 7 documents, 8 `make check`, 9 docs, the last two kept last).
   - Interface: names concrete documents only (`docs/operator-guide/*.md`, `docs/operator-playbook.md`, `README.md`, `operator/README.md`); no code or signatures change. All of these are paths the documenter may write, apart from `docs/operator-playbook.md`, which the Interface and criterion 9 name explicitly.
   - Criteria: each is checkable by reading the documents or by the quoted script. Every stated behaviour of the Interface has its own criterion. Failing sides do not apply, because the story states no validation rule.
   - Smoke test: `uv run python -m factory.entry.check_documents | tail -1` is runnable. It does not run pytest, so the `-q` rule does not apply. The `Expect:` line is checkable.
   - Docs criterion: names what the reader must know and dictates no sentences.
   - Architecture: no code is touched, so the layers are unaffected. `main_branch_failing` keeps its name as `CLAUDE.md` and decision 6 require.
   - Scope: within F0057 (S0004 is the operator's documents), and `docs/runs/` and decision-log entries are excluded as the feature says.
   Route: docs-only.
7. factory: started docs-only as vm.
8. documenter: I wrote the documents, but `make documents` fails, and the cause is code. So I end with `tests`, as the docs-only route says for a change outside the documents.

   **The blocker.** `GLOSSARY_FORBIDDEN` in `src/factory/shared/domain/documents.py:77-78` lists `promote` and `promoted` as v1 words. `_uses_word` matches the whole word case-insensitively, backticks included. Criterion 4 and the Interface require the operator guide to name the switch `promote`. Every operator-guide page is in `docs/checked-documents.txt`, so `docs/operator-guide/install.md` fails with `uses the v1 word 'promote'`. It is the only finding of `make documents`; the rest of the output is `not run` lines. I did not touch `docs/checked-documents.txt` or write around the switch's name.
   - The change needed is to remove `promote` from `GLOSSARY_FORBIDDEN` (or exempt the switch's name). That is code, so the tester and then the coder do it.
   - `promoted` I would also remove: a promotion is now a real term (`operator/skill/kumpel/scripts/promote.sh`, title `<id>: promoted to main`).
   - The existing test of that list will need the same change, as the coder's route requires. I have not looked at it.
   - After the fix, run `make documents` again; I expect `documents ok`. My text keeps `promote` in `install.md` as criterion 4 asks.

   **Files changed, one line each.**
   - `docs/operator-guide/install.md`:
     - Install step 1: a new project needs `develop`, created from `main`; the preflight names a missing `origin/develop`. The later steps are renumbered 2 to 6.
     - New section *The branches*: what `develop` and `main` hold.
     - *Protect `main`*: a ruleset with a required pull request with zero approvals, blocked force pushes and blocked deletion, and why zero (one identity for the factory, Kumpel and the human; GitHub refuses an author's own approval).
     - *The promotion*: after acceptance Kumpel archives the feature, then `promote.sh` opens the `develop` to `main` pull request and merges it with a merge commit when `promote` is on. It is never a squash or rebase. With `promote` off, you merge it.
     - *Fixes go to `develop`*: `main` is never fixed directly.
     - The facts come from `operator/skill/kumpel/scripts/promote.sh` and `operator/README.md`.
   - `docs/operator-guide/stops.md`: the `main-branch-failing` row says it means the working branch `develop` and keeps its name. The other `origin/main` mentions became `develop`.
   - `docs/operator-guide/health.md`, `agent-runtime.md`, `machine.md`, `pipeline.md`, `records.md`, `work-items.md`: `main` as the working branch became `develop`. This includes the quoted messages `merging the develop branch conflicts...` and `no report on the branch or the develop branch`, which I checked against `WORK_BRANCH` in `src/factory/shared/domain/paths.py` and `post_texts.py` and `acceptance.py`. `work-items.md` also lists `main` among the branches the tick never touches.
   - `docs/operator-guide/site.md`: `reset-to-tag.sh` moves `develop`, not `main`, and leaves `main` alone (its real output lines are in `reset-to-tag.sh`). The merge polling reads `develop`.
   - `docs/operator-playbook.md`, `README.md`: `main` as the working branch became `develop`.
   - `operator/README.md`: already correct, no edit.

   **The script and the mentions left as `main`.** The script is `grep -nwE "main" docs/operator-guide/*.md docs/operator-playbook.md README.md operator/README.md`. It lists these, each meaning the line of accepted features or the code repository's own branch, not the factory's working branch:
   - `cloud-run.md:54`, `site.md:99`, `machine.md:297` and `machine.md:314`: `main` is the code repository's ref, as in `--ref main` and `SITE_CODE_REF`.
   - `records.md:25`: schemas fetched from the code's `main`, which holds accepted code.
   - `stops.md:20`: only the stop's name, `main-branch-failing`, explained as the working branch.
   - `site.md:237`: "`main` is left alone".
   - `work-items.md:139`: `main` among the branches never touched.
   - `install.md:11`, `45`, `47`, `49`, `55`, `59`, `63`: the new text on creating `develop` from `main`, protecting `main`, the promotion and fixes.
   - `operator/README.md:84`, `111` and `131`: the promotion and the switch.

   **Cross-read and found current.** `operator/README.md` and the `docs/operator-guide` pages `README.md` and `cloud-run.md` (apart from the code ref).

   **Stale text I noticed and left.**
   - `docs/runs/` and the decision log stay as the Interface says.
   - `docs/project-guide/` was not in the Interface. I did not check it for `main`.
   - `docs/operator-guide/README.md` is not word-checked differently; nothing in it names the working branch.
9. factory: started tests as vm.
10. tester: Question. I wrote no tests and changed no files. I stopped at step 1 because the work needs a code change and a test change that the description rules out.

    **The conflict.** The description says "It changes no code and no test". Criterion 7 needs `make documents` to end with `documents ok`, and criterion 4 needs the operator guide to name the switch `promote`. Those cannot all hold today. `GLOSSARY_FORBIDDEN` in `src/factory/shared/domain/documents.py:70-89` lists `promote` and `promoted` as v1 words, so `docs/operator-guide/install.md` fails the check (documenter, journal entry 8). No criterion covers changing that list, so I have nothing to test. An earlier story's test also pins the list as it is: `tests/pipeline/domain/test_documents.py::test_the_v1_words_are_the_eighteen_in_their_order`. Changing that test is a change to a test I did not write, which needs your leave (CLAUDE.md, *Not without asking*).

    **Options:**
    - (a) Widen the story. Add a criterion before the last two: "`promote` and `promoted` are no longer v1 words: the document check accepts them in a checked document." Give leave to edit the pinned test so it holds the sixteen remaining words in their order. I would then add a parametrized test: a guide line holding `promote` or `promoted` gives no finding, and `ticket` still gives one, as the control row.
    - (b) Same as (a), but remove only `promote` and keep `promoted` forbidden. The documenter argues for removing both, because "promoted to main" is now a real term (the PR title `promote.sh` writes).
    - (c) Keep the story docs-only. The documenter rewrites the guide without the word, for example "the promotion switch". That conflicts with criterion 4 as written, so you would need to reword criterion 4.

    **My choice: (a).** A promotion is now a real thing in the factory (`operator/skill/kumpel/scripts/promote.sh`). Keeping either word forbidden would make the documents talk around it.

    Not touched: `tests/agent_files/test_claude_agent_texts.py:144` also forbids `promote`, but in the agent files, not the operator documents. I would leave it as it is unless you say otherwise.

    Criterion → test mapping: none yet. Files created: none. Modules the test run could not import: none, because I did not run the tests.
11. 2026-11-08 human: (a), with your leave for the pinned test; the coder removes both words from GLOSSARY_FORBIDDEN. The agent-file test stays as it is.
12. factory: started tests as vm.
13. tester: I wrote the test for the criterion the human added in journal entry 11 (option (a)) and changed the earlier test that pins the v1-word list, which the human gave leave for. `make lint` is green.

    **Description updated (R5):**
    - The new criterion 8 goes before the two closing ones: "`promote` and `promoted` are no longer v1 words: the document check accepts them in a checked document, and the other v1 words stay forbidden." `make check` is now 9 and docs is 10.
    - The sentence "It changes no code and no test" and the Interface's "No test changes" line now name the one code change (`GLOSSARY_FORBIDDEN` in `src/factory/shared/domain/documents.py`) and the human's leave for the pinned test.

    **Criterion → test:**
    - criteria 1–7, 9, 10: documents and checks only; no test of mine (docs route, `make documents`, `make check`).
    - criterion 8: `tests/shared/domain/test_documents_promotion_words.py::test_the_words_of_a_promotion_are_no_v1_words`. It is one parametrized test. Rows `promote`, `` `promote` `` (backticks, as `install.md` writes the switch) and `promoted` in the guide's `install.md` must give no finding. A control row, `ticket`, must still give `uses the v1 word 'ticket'`.
    - criterion 8, the list itself: `tests/pipeline/domain/test_documents.py::test_the_v1_words_are_the_sixteen_in_their_order`. This is the earlier test, changed with the human's leave (journal entry 11):
      - it no longer has `promote` and `promoted` in the list it expects;
      - I renamed it from `..._the_eighteen_...` to `..._the_sixteen_...` so the name stays true.

    **Files:**
    - Created: `tests/shared/domain/test_documents_promotion_words.py`.
    - Changed: `tests/pipeline/domain/test_documents.py`, only the pinned list test, under the human's leave.
    - Left as the human said: `tests/agent_files/test_claude_agent_texts.py`.

    **Test run** (`uv run pytest -q` on the two files): 4 tests fail, for the right reason, and the rest pass.
    - The three promotion rows fail because the check still returns a `uses the v1 word` finding.
    - The pinned-list test fails because `GLOSSARY_FORBIDDEN` still has 18 words.
    - The `ticket` control row and the other tests in `test_documents.py` pass. `test_every_v1_word_alone_on_its_line_is_one_finding` takes its rows from `GLOSSARY_FORBIDDEN`, so it follows the coder's change by itself.

    Modules the test runner could not import: none.

    For the coder: remove `promote` and `promoted` from `GLOSSARY_FORBIDDEN`. Then `make documents` should pass on the documenter's `install.md`.

    The factory left out changes outside the write paths: factory/features/F0057-the-factory-works-on-develop/in-progress/F0057-S0004-the-operators-documents-name-develop-and-main.md.

    `lint`: lint: green (0.1 s)
14. factory: started doing as vm.
15. coder: I removed `promote` and `promoted` from `GLOSSARY_FORBIDDEN` in `src/factory/shared/domain/documents.py`, as the human decided in journal entry 11. That is the only code change. The other sixteen v1 words stay, in their order.

    **Checks**
    - `make test` passes, including `tests/shared/domain/test_documents_promotion_words.py` and the renamed `test_the_v1_words_are_the_sixteen_in_their_order`.
    - `make documents` now ends `documents ok (58.2 s)` on the documenter's `install.md`.
    - `make check` ends `check: green`.

    **Choice:** I removed both words from the list. The alternative was an exemption for just the switch's name, written `` `promote` ``. I rejected it because the human's answer asks for both words to go, and because "promoted to main" is now a real term: it is in the pull request title that `promote.sh` writes.

    **Refactor:** the change is two deleted lines, so nothing needed changing.

    **What the journal changed in the task:** the work now includes this one code change and the pinned-list test changed with the human's leave, and the new criterion is that `promote` and `promoted` are no longer v1 words. The tester's rewrite of `## Description` was left out by the factory because it is outside the tester's write paths. I did not rewrite the Description either. It still says "It changes no code and no test", so the reviewer should read it together with journal entries 11 and 13.

    **Noticed, not touched:** `tests/agent_files/test_claude_agent_texts.py:144` still forbids `promote` in the agent files. The human said to leave it as it is.

    `check`: check: green
    `duplicates`: duplicates: 6 new, 39 known, 4 gone
16. factory: started review as vm.
17. reviewer: no findings

    What I reviewed: `git diff develop...HEAD -- . ':!factory'` (eleven documents, `src/factory/shared/domain/documents.py`, two test files) and the work item.

    - Criterion 1: I ran the Interface's script myself, `grep -nwE "main" docs/operator-guide/*.md docs/operator-playbook.md README.md operator/README.md`. Every hit left is one of these:
      - the code repository's own ref: `cloud-run.md:54`, `site.md:99`, `machine.md:297` and `machine.md:314`;
      - accepted code: `records.md:25`;
      - the stop's name: `stops.md:20`;
      - `main` left alone by the reset: `site.md:237`;
      - a branch the tick never touches: `work-items.md:139`;
      - the new text on branches, protection and promotion: `install.md:11`, `45`, `47`, `49`, `55`, `59` and `63`;
      - the promotion: `operator/README.md:84`, `111` and `131`.
      None of them names the working branch.
    - Criteria 2 to 6: the new section of `install.md` (*The branches*, *Protect `main`*, *The promotion*, *Fixes go to `develop`*) and the `main-branch-failing` row of `stops.md` cover each criterion. I checked the claims against the code:
      - `operator/skill/kumpel/scripts/promote.sh`: the pull request from `develop` to `main`, `merge_method: merge`, and with the switch off the pull request is left for the human;
      - `operator/README.md:131`: `/kumpel promote on`;
      - `operator/skill/kumpel/scripts/reset-to-tag.sh:77-93`: the `moved develop to` and `left main alone` lines;
      - `operator/skill/kumpel/scripts/merge.sh:38`: it polls `develop`;
      - `preflight.py`: `_NO_WORK_BRANCH_TO_PREPARE`, `find_open_pull_request(WORK_BRANCH)` and the messages of the `develop` probe;
      - `scheduler.py:135-137`;
      - `post_texts.py:37`;
      - `acceptance.py:298` and `acceptance.py:353`.
      Every quoted message the documents changed matches the code.
    - Criterion 7: the coder's journal entry 15 reports `make documents` as `documents ok (58.2 s)`. Criterion 9: the factory's `make check` after the coder was `check: green`.
    - Criterion 8 (the human's, journal entry 11): `src/factory/shared/domain/documents.py` drops only `promote` and `promoted`, and the other sixteen words keep their order. The test `tests/shared/domain/test_documents_promotion_words.py::test_the_words_of_a_promotion_are_no_v1_words` is one parametrized test with these rows:
      - `promote`, `` `promote` `` and `promoted` give no finding;
      - the control row `ticket` still gives a finding.
      `tests/pipeline/domain/test_documents.py::test_the_v1_words_are_the_sixteen_in_their_order` pins the new list. Both sides of the rule are tested.
    - Architecture, security, quality: the code change deletes two entries from a constant. It adds no marker that silences a check, no secret and no new helper.

    Work item corrected (the tester's rewrite, journal entry 13, was left out by the factory; journal entry 11 settles what it should say):
    - description corrected: "It changes no code and no test." -> the one code change (`promote` and `promoted` out of `GLOSSARY_FORBIDDEN`) and the human's leave for the pinned test, journal entry 11.
    - description corrected (Interface): "No test changes; the story takes the docs route." -> "The story took the docs route; the one code change and its tests are those of journal entry 11."
    - description corrected (criteria): the human's criterion from journal entry 11 is now criterion 8, "`promote` and `promoted` are no longer v1 words: the document check accepts them in a checked document, and the other v1 words stay forbidden". `make check` is renumbered 9 and docs 10. Its test already exists (see above), so it is no finding.

    Earlier tests:
    - `tests/pipeline/domain/test_documents.py`: changed under the human's leave, journal entry 11. Only the pinned-list test changed: its list and its name, from eighteen to sixteen.
