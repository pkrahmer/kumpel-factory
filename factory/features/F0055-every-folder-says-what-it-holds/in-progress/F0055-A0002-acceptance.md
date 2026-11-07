---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 642
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-07T15:30:39.222612Z'
  stage: acceptance
- number: 2
  speaker: factory
  kind: crash
  at: '2026-11-07T15:33:12.524162Z'
  stage: acceptance
- number: 3
  speaker: factory
  kind: started
  at: '2026-11-07T15:33:14.141297Z'
  stage: acceptance
- number: 4
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-07T15:43:15.534170Z'
  stage: acceptance
  run: 6b356d4dff354841be19be59251228f5
stories: [F0055-S0001, F0055-S0002, F0055-S0003, F0055-S0004, F0055-S0005, F0055-S0006, F0055-S0007, F0055-S0008, F0055-S0009]
outcome: null
---

# Acceptance of Every folder says what it holds

## Recommendation

**accepted with stories.** The feature now does what `feature.md` promised. The two stories from the first acceptance closed both holes it found:

- a listed README with no file now fails the guard (S0008)
- a link line, or an opening that carries a link, now keeps its limits (S0009)

All 22 READMEs are clean and on the checked list, every module and script carries the SPDX line, and `make check` and `make documents` are green. Two small findings are worth a story each, and neither breaks a promise to a user:

- Four sentences of the documents still describe the time before S0008 and before the human's three READMEs (F0055-S0010).
- Only 3 of the 22 listed READMEs are pinned to `docs/checked-documents.txt`, so the feature's done condition can quietly stop holding (F0055-S0011).

## 1 Scope

No story is missing for any item in the Scope, and no story falls outside it. The first acceptance (F0055-A0001) mapped S0001 to S0007 to the Scope. S0008 and S0009 are its two proposed stories, and both stay inside the Scope's guard (S0001) and feature decision 6. I read the code they changed:

- `tests/guards/test_folder_readmes.py`: `_listed_readme_problems` and the unskipped `test_a_folder_readme_agrees_with_its_folder`
- `src/factory/shared/domain/folder_readmes.py`: `LINK_LINE_SENTENCES`, `LINK_LINE_WORDS`, `_read_line_past_opening` and `_is_longer_than`

The Goal's done condition holds: every README on the list exists and is on the checked list, and `make check` is green.

One step of *The human's changes* went differently from the plan. The human wrote `factory/README.md`, `factory/features/README.md` and `docs/runs/README.md` (commit 35a1d50da). `feature.md` says the human "adds them to the list and the checked list", but none of the three is on `FOLDER_READMES` or on `docs/checked-documents.txt`. The human's run log (`docs/runs/2026-11-05-f0052/log.md:227`) says this was on purpose:

- adding them needs a code change
- S0004's test pins 22 paths
- `factory/features/` holds feature folders that come and go, so its README names them by kind

My smoke test confirms the last reason: `readme_problems` on `factory/features/README.md` gives `factory/features: F0055-every-folder-says-what-it-holds/ is not named`. The other two READMEs give `[]`. This is the human's choice and is listed under 6. The text of `feature.md` still describes the old plan, and it is the human's to update.

## 2 The feature's smoke test

The walk-through a reader and a maintainer of the repository would do:

1. Does every listed folder have a README in its form, on the checked list?
2. Where do the human's READMEs stand?
3. Does every module and script name its license?
4. Is the document check green?
5. Does a slip get caught? In a clone, I deleted a README, added a new area subfolder, appended a long link line and wrote an opening of three sentences that carries a link.

The script ran from a `mktemp -d` that removes itself:

```bash
repo=/work/checkout; cd "$repo"
echo "== 1 every listed folder has a README in its form, on the checked list"
uv run --quiet python - <<'PY'   # readme_problems over FOLDER_READMES with the real subfolders, membership of docs/checked-documents.txt, areas under src/factory
...
print("== 1b the human's three READMEs (feature.md: added to the list and the checked list after S0005)")
...
PY
echo "== 2 every module and script names its license"
uv run --quiet python - <<'PY'   # git ls-files: src/factory/*.py line 1, operator/ shebang scripts outside template/ line 2
...
PY
echo "== 3 the document check on the repository"
make documents 2>&1 | tail -1
echo "== 4 slips in a clone: a deleted README, a new subfolder, a long link line, a long opening with a link"
c=$(mktemp -d); git clone --quiet "$repo" "$c/r"; cd "$c/r"
rm security/README.md
mkdir src/factory/watching/charts && touch src/factory/watching/charts/x.py
printf '\nThe board is described at length here, and the reader is told all about it in [the guide](../../../docs/project-guide/watching.md). And more.\n' >> src/factory/watching/README.md
python3 - <<'PY'   # agents/README.md: its opening becomes "One. Two. Three, see [the guide](../docs/project-guide/README.md)."
...
PY
uv run --quiet --project "$repo" pytest -o addopts= -q -p no:cacheprovider tests/guards/test_folder_readmes.py 2>&1 | grep -E "^E  .*(no README|not named|long link|opening)" | sed 's/^E *//' | sort -u
uv run --quiet --project "$repo" pytest -o addopts= -q -p no:cacheprovider tests/guards/test_folder_readmes.py 2>&1 | tail -1
rm -rf "$c"
```

Output:

```
== 1 every listed folder has a README in its form, on the checked list
22 READMEs, 0 with problems; areas without README: []
== 1b the human's three READMEs (feature.md: added to the list and the checked list after S0005)
factory/README.md exists | on FOLDER_READMES: False | on checked list: False | form: []
factory/features/README.md exists | on FOLDER_READMES: False | on checked list: False | form: ['factory/features: F0055-every-folder-says-what-it-holds/ is not named']
docs/runs/README.md exists | on FOLDER_READMES: False | on checked list: False | form: []
== 2 every module and script names its license
188 modules, 0 without header; 15 scripts, 0 without; tests with header: 1
== 3 the document check on the repository
documents ok (60.1 s)
== 4 slips in a clone: a deleted README, a new subfolder, a long link line, a long opening with a link
AssertionError: assert ['security: no README.md'] == []
Left contains 2 more items, first extra item: 'src/factory/watching: charts/ is not named'
Left contains one more item: 'agents: the opening is longer than two sentences'
Left contains one more item: 'security: no README.md'
3 failed, 28 passed in 0.06s
```

The result is green for every promise:

- All four slips were caught, including the two that the first acceptance found slipping through. In `watching`, the second item, which pytest hid behind "2 more items", is the long link line. Running that row alone shows `['src/factory...ng link line']`.
- The one "test with header" is `tests/guards/test_license_headers.py`, which names the line it looks for, not a header.
- The 15 scripts are those that start with a shebang. A0001 counted 18 by another rule, and the guard `tests/guards/test_license_headers.py` is green either way.

The smoke test also showed one gap that no guard covers. In a clone, I deleted `src/factory/agents/README.md` and `security/README.md` from `docs/checked-documents.txt` and ran `tests/guards` together with the two check-documents test modules. Every test passed except the same 130 errors that an unchanged clone shows, which come from the clone's environment. So 19 of the 22 READMEs can leave the checked list with `make check` green, and the feature's done condition then fails without notice (F0055-S0011).

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

What S0008 and S0009 noticed:

- **S0008, coder, documenter and smoke tester:** `tests/guards/test_test_folder_readmes.py` is now redundant: S0008's guard proves for all 22 that a listed README exists. The name of its first test, `test_a_test_folder_readme_is_written_so_its_guard_does_not_skip_it`, describes a skip that no longer exists. Its second test is the only pin of the checked list, and it covers only 3 of 22. Taken up in F0055-S0011.
- **S0009, coder (entries 7, 15):** a subfolder line written right under the opening, with no blank line between, still ends the opening. This was true before S0009, and the style page's form puts a blank line there. It is not worth a story.
- **S0009, reviewer note (entry 17):** `f"{FOLDER}: line 9 is a long link line"` is written out in two rows, while line 5 has the constant `LONG_LINK_LINE_5`. This is cosmetic.
- **S0009, reviewer (entry 9):** the reviewer could not read `make duplicates`' new findings, because no report is in the checkout. The round-1 reviewer ran it by hand.

Items from A0001 that are still open, all small:

- `_run` is still copied in `tests/entry/test_check_documents_checked_files.py:50` and `tests/entry/test_check_documents_folder_readmes.py:30`. The standing leave allows the move.
- `tests/README.md` still writes its subfolder sentences in lower case.
- `tests/vm/test_stage_image.py::test_the_first_line_names_the_build_command_with_the_runtime` reads line 2.
- `readme_problems` is still reported unused by vulture (`make duplicates`: 6 new, 39 known, 4 gone, the same as at A0001). Its baseline entry is the human's.
- The root README still names `agents/` in both of its folder lists.

Mine: the human's three READMEs exist, but the root README's `factory/` line and `docs/README.md`'s `runs/` line do not link them. See check 5 and F0055-S0010.

## 5 The documentation as a whole

I read `README.md`, `docs/README.md` and the human's three new READMEs. In the project guide I read `style.md`, *Folder READMEs*, and `shared.md`, *The folder READMEs*. S0009's text in both places agrees with the code:

- the opening is the first paragraph
- a link line is one sentence of at most 25 words
- `line <n> is a long link line`

`make documents` is green. Findings, all for F0055-S0010:

- `docs/project-guide/style.md`, *Folder READMEs*, says the guard "checks each one that exists". That was the skip S0008 removed. `shared.md` says correctly that a missing listed README fails. The two pages contradict each other, and the style page is the stale one.
- `docs/project-guide/shared.md` says `FOLDER_READMES` lists "every folder README of the repository, 22 in all". Six folder READMEs are outside the list: the human's `factory/`, `factory/features/`, `docs/runs/` and `planning/`, plus `demo/` and `operator/`. The section names only `operator/README.md` as an exception.
- The root `README.md`, `## The folders`, gives `factory/` no link. S0005 criterion 6 required a link to "each folder's README that exists", and `factory/README.md` exists now.
- `docs/README.md` gives `runs/` no link to `runs/README.md`.

None of these misleads a user into breaking anything: they are one sentence each, in the agents' guide and in two link lists. `docs/decisions.md:1653` still says "the 23 paths", which the human kept as a record (S0004 entry 12).

## 6 Decisions taken for the human

To accept or revisit:

1. Feature decisions 1 to 11 in `feature.md`, and the ten answers and defaults that A0001 listed under its check 6. Nothing new was added to them. Still to revisit from there: the root README names `agents/` both in *Where to read next* and in *The folders*, while S0005 entry 4 asked for no repeat.
2. **New, the human's own:** `factory/README.md`, `factory/features/README.md` and `docs/runs/README.md` stay off `FOLDER_READMES` and off the checked list, against the text of `feature.md` (*The human's changes*, "after S0005's merge"). The reasons are in `docs/runs/2026-11-05-f0052/log.md:227`. As a result, the document check does not read these three: a broken link or name in them blocks nothing. Options I see:
   - **(a)** Keep them off and correct `feature.md`. This is what I would choose, and F0055-S0010 documents it.
   - **(b)** Add `factory/README.md` and `docs/runs/README.md` to the list, a one-line code change plus the checked list. `docs/runs/` then fails the guard on every new run folder until its README names it.
   - **(c)** A second constant of READMEs that are checked for names and links but not for their subfolders. That is a story with code.
3. S0008: `tests/guards/test_test_folder_readmes.py` was left in place as the human's call. F0055-S0011 proposes removing it and needs the human's leave, which its Interface names.
4. S0009: the human kept the opening's word limit and the number of link lines unchanged (its Description, 2026-11-07). The human also shortened `docs/README.md`'s long link line on `main` before the story started.

Earlier tests changed, each with its leave:

- `tests/guards/test_folder_readmes.py::test_a_folder_readme_agrees_with_its_folder` and its module docstring: S0008, under the human's leave of 2026-11-07 that its Interface quotes. The test kept its name, and only its skip was dropped.
- `tests/shared/domain/test_folder_readmes.py::test_a_readme_out_of_its_form_gives_one_line_per_rule`: S0009, under the human's leave of 2026-11-07 that its Interface quotes. Nine rows were added and no row was changed.

The four earlier tests that A0001 listed for S0001 to S0007 each had their leave. Both S0008 and S0009 reviewers confirmed that no other earlier test changed. No earlier test was changed without a leave.

## 7 The slow checks

The slow checks were as follows:

- `make documents`: green, `documents ok (60.1 s)`.
- `make duplicates`: `6 new, 39 known, 4 gone`, the same six as at A0001. One of them is this feature's: `readme_problems` is reported unused, by design.
- Image scan and SBOM: none offered.
- `make mutants`: not run (check 3).

The JUnit report of my `make check` run (`.reports/junit.xml`) counts 10,912 tests with 922.5 s of summed test time. The slowest are the 10-second time-limit tests, none of them this feature's:

- `tests/machine/adapters/test_podman_timeout_status.py::test_podman_s_timeout_status_at_the_limit_is_a_timed_out_run`, 10.02 s for each of two rows
- `tests/agents/adapters/test_claude_runtime_resume.py`, 10.0 s for each of two tests

The feature's 114 tests (folder READMEs, license headers, heading references) sum to 0.4 s. `make check` ended `test: green (101.1 s)` and `check: green`, with 99.22 % coverage.

Disk: free space on the pool fell from 17.2 GB at `disk start` to 16.6 GB at `disk acceptance`, a drop of 0.6 GB. Used space on `/srv/factory/vm` stayed at 1.5 GB, and `/srv/factory/vm/state` and `/tmp` show 0.0 GB used. Between those two records the feature changed nothing but this report. The 0.6 GB lies outside the dataset: images, snapshots or caches on the pool, perhaps from this stage's crashed first run, its clones and `uv` runs. A0001 saw the same pattern with 0.7 GB. Two acceptances in a row lost about 0.6 GB that no work explains, so the human should look at what is filling the pool.

## 8 Cost

The nine stories took 97 runs, 139.5 min and 683 turns, with 2,258,730 tokens in (15,026,917 more from cache) and 270,581 out, for $23.15.

Of that, S0001 to S0007 took $19.54 (81 runs), as A0001 reported. S0001 stands out at $6.48 and 19 runs, a third of the feature. The causes were two counts the Interface left open, three review rounds over edge cases of the form and the round cap. The two new stories were cheap:

- S0008: 6 runs, 5.4 min, $1.40. Its whole change was in a test module, so the coder handed on an empty diff.
- S0009: 10 runs, 11.9 min, $2.21. It needed one review round, where the reviewer added criteria 4 and 5, whose rows passed without any code change.

The human answered 13 questions (11 questions, 2 at the round cap), and the stories waited 0.6 h for them. S0008 and S0009 asked none: their leaves were written into the Interfaces when the human refined them. S0001 and S0003 needed the human most, three answers each:

- S0001: the form's counts, then the round cap.
- S0003: on the tests route no role could write `tests/README.md`, so the human opened the coder's write paths for that one story.

## Proposed stories

- **F0055-S0010, The guides name the folder READMEs as they are now:** a docs-only repair. `style.md` still describes the guard's removed skip, `shared.md` calls the 22 paths every folder README, and the root README and `docs/README.md` do not link the human's new READMEs.
- **F0055-S0011, Every listed folder README is on the checked list:** a test-only story. Only 3 of 22 listed READMEs are pinned to `docs/checked-documents.txt`. The story pins all 22 in the folder-README guard and removes the now-redundant `tests/guards/test_test_folder_readmes.py`, under a leave the human gives.

## Journal

1. factory: started acceptance as vm.
2. factory: crash 1: the run of stage acceptance ended without a result. Its work is discarded back to commit 06ac7902f94be1ba673cd99e48fea05afb1f0dce.
3. factory: started acceptance as vm.
4. acceptance-reviewer: accepted with stories; 2 stories proposed
   1 Scope: no gap. S0008 and S0009, the first acceptance's two proposals, stay inside the Scope, and the done condition holds: 22 READMEs exist and are on the checked list, and make check is green. The human wrote factory/README.md, factory/features/README.md and docs/runs/README.md but kept all three off the list and the checked list, on purpose (docs/runs/2026-11-05-f0052/log.md:227). feature.md still describes the old plan.
   2 Smoke test: green. 22 READMEs have no problems, 188 modules and 15 shebang scripts carry the SPDX line, and make documents is ok. In a clone the guard caught all four slips: a deleted README, a new subfolder, a long link line and a three-sentence opening with a link. It also showed a gap: two READMEs taken off docs/checked-documents.txt break no test, so 19 of the 22 are unpinned.
   3 Mutation testing: by sweep, not run here.
   4 Noticed: test_test_folder_readmes.py is now redundant, and its first test's name describes the removed skip (F0055-S0011). Still open from A0001: the _run test helper is copied in two modules, tests/README.md writes its subfolder lines in lower case, the first-line test of test_stage_image reads line 2, the duplicates baseline entry for readme_problems is the human's to add, and the root README names agents/ twice. Also, a subfolder line right under the opening ends it.
   5 Docs: style.md still says the guard checks each README "that exists", against shared.md and the code. shared.md calls the 22 "every folder README of the repository". The root README's factory/ line and docs/README.md's runs/ line do not link the human's new READMEs (F0055-S0010).
   6 Decisions: feature decisions 1 to 11 and A0001's list are unchanged. New, for the human: their three READMEs stay off the list. Options: (a) keep them off and correct feature.md, my choice; (b) add factory/ and docs/runs/; (c) a constant of READMEs that are checked but not guarded. S0008 and S0009 changed earlier tests, each under the leave its Interface quotes. No earlier test was changed without a leave.
   7 Slow checks: make documents ok (60.1 s); make duplicates 6 new, 39 known, 4 gone, the same as at A0001. There is no scan and no SBOM. The slowest tests are the 10 s time-limit tests, and the feature's 114 tests take 0.4 s. Free disk fell 0.6 GB between disk start and disk acceptance while dataset use stayed at 1.5 GB. Nothing this feature did explains it, and it is the second such drop in a row.
   8 Cost: 97 runs, 139.5 min, $23.15. S0001 still stands out ($6.48, 19 runs). S0008 cost $1.40 (6 runs) and S0009 $2.21 (10 runs, one review round). The human answered 13 questions (11 questions, 2 at the round cap) and the stories waited 0.6 h; S0008 and S0009 asked none. S0001 and S0003 needed the human most, 3 answers each.
   Proposed: F0055-S0010 (docs repair: the guides name the folder READMEs as they are now) and F0055-S0011 (every listed README is pinned to the checked list, and the redundant test module goes, under the human's leave). Both pass factory-check-story, and their smoke tests are red today.
