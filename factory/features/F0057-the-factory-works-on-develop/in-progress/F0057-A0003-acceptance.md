---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 657
comments_read: []
handed_over: null
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T07:52:49.342174Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T07:58:52.469022Z'
  stage: acceptance
  run: 83ee91ca64a54d348fa75202b2dc3f3c
stories: [F0057-S0001, F0057-S0002, F0057-S0003, F0057-S0004, F0057-S0005, F0057-S0006, F0057-S0007, F0057-S0008, F0057-S0009, F0057-S0010, F0057-S0011, F0057-S0012]
outcome: null
---

# Acceptance of The factory works on develop

## Recommendation

**Accepted.** `make check` is green and the feature's smoke test passes end to end. A new project waits for `develop`, and a merged story is archived on `develop` while `main` stays where it was. Kumpel refuses to archive a refused feature or one with proposed stories in `backlog/`. It archives an accepted feature as Kumpel, opens one promotion and adds the next feature to it, and merges it with a merge commit only when the switch is on.

The three stories that F0057-A0002 proposed (S0010 to S0012) did what they promised, and what is left is notes. One reason not to propose a story for any of them: by the behaviour S0012 documented, a proposed story would itself hold back F0057's archive and its first promotion. That promotion, and protecting `main`, are the goal's last open steps.

## 1 Scope

None. The scope lines of `feature.md` (S0001 to S0005) were checked in F0057-A0001 and F0057-A0002 and still hold. `WORK_BRANCH` in `src/factory/shared/domain/paths.py` says `develop`, and its guard `tests/guards/test_work_branch_search.py` passes in `make check`.

The three later stories came from F0057-A0002's proposals. Each stays within the feature's one-constant, Kumpel and documents scope:
- **S0010:** `WORK_REF = f"{REMOTE}/{WORK_BRANCH}"` sits at `src/factory/shared/domain/paths.py:14`. `grep -rn '{REMOTE}/{WORK_BRANCH}' src/factory` finds that one line, and no `_WORK_REF` is left under `src/factory`. `PIPELINE_REF` and `FORM_REF` are set to it. The guard `tests/guards/test_work_ref_search.py` keeps it that way.
- **S0011:** `docs/project-guide/operator.md` names `archive-feature.sh`, `promote.sh`, `kumpel-commit.sh`, the three test modules and `tests/support/archive_feature_support.py`.
- **S0012:** `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 expects the `is in backlog/` refusal after an acceptance that proposed stories. Step 2 names the reuse of an open promotion. The playbook's step 8 and `install.md`, *The promotion*, follow.

Out of scope was still respected: there is no branch setting, `main_branch_failing` is kept, and no old decision entry or `docs/runs/` file was touched. `feature.md`'s Stories list still names only S0001 to S0005. That is the human's file.

The goal's last conditions are the human's acts, and I cannot see them from the repository:
- `main` is protected.
- The first promotion (*The human's changes*, "After the feature's acceptance").

That the factory runs on `develop` shows in this branch and in S0010 to S0012, which were cut from `develop` and merged into it.

## 2 Feature smoke test

The walk is a user's path through the whole feature:
1. A new project with only `main`, then `develop` created from it.
2. A story merged and archived, with a `main` branch that must not move.
3. Kumpel after two features' acceptances:
   - F0001's only acceptance is refused.
   - F0002 is accepted but has a proposed story in its `backlog/`.
   - The human then merges an accepted A0002 for F0001.
   - Kumpel archives F0001 and promotes it with the switch off.
   - The human finishes F0002's proposed story and merges its accepted A0002.
   - Kumpel archives F0002 and promotes it into the open promotion, then runs that again with the body already up to date. Then it runs once more with the switch on.

The walk also reads `approving.md`'s section through `factory.shared.domain.sections.section_text` and checks that it names both waits.

The script is one pytest module. I wrote it into a `mktemp -d` folder and removed the folder after the run. It uses the repository's `tests/conftest.py` fixtures as a plugin and calls only the real entry points:
- `RepositoryWaiter` and `CheckoutPreparer` on a real bare remote.
- `MergedHandler` on the `remote`, `human` and `checkout` fixtures.
- The real `archive-feature.sh` and `promote.sh`, with the suite's `curl` stand-in for the hosting API.

```console
$ PYTHONPATH=tests uv run pytest -p conftest -p no:xdist -p no:cacheprovider -s -q --rootdir=. -o addopts="" --tb=short "$d/test_feature_f0057_walk.py" 2>&1 | grep -E "^E |WALK|passed|failed|rror"
WALK WORK_BRANCH, WORK_REF, PIPELINE_REF, FORM_REF: ('develop', 'origin/develop', 'origin/develop', 'origin/develop')
WALK only main: prepared: False
WALK only main: stops: ['the repository has no develop branch yet']
WALK with develop: prepared: True
WALK with develop: stops left: []
.WALK develop tip: work item F0001-S0001: merged, archived
WALK done/ on develop: True
WALK main moved: False
.WALK archive F0001 after a refused acceptance: 1 archive-feature.sh: F0001 is not finished: its last acceptance factory/features/F0001-example/done/F0001-A0001-acceptance.md is not accepted
WALK archive F0002 with a proposed story in backlog/: 1 archive-feature.sh: F0002 is not finished: factory/features/F0002-other/backlog/F0002-S0003-proposed.md is in backlog/
WALK promote F0002 before its archive: 1 promote.sh: F0002 is not archived on develop
WALK archive F0001 after A0002 accepted: 0 08ab0ed F0001: archived
WALK develop tip, author, committer: F0001: archived | Kumpel <kumpel@noreply.invalid> | Kumpel <kumpel@noreply.invalid>
WALK main tip: seed
WALK promote F0001 (off, none open): 0 promotion opened: #4711, for the human to merge
WALK archive F0002 after A0002 accepted: 0 b59452f F0002: archived
WALK promote F0002 (off, F0001's open): 0 promotion open: #4711, for the human to merge
WALK promote F0002 again (off, body already holds F0002): 0 promotion open: #4711, for the human to merge
WALK promote F0002 (on): 0 promoted #4711
WALK request: POST /pulls {'head': 'develop', 'base': 'main', 'title': 'F0001: promoted to main', 'body': 'The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story'}
WALK request: PATCH /pulls/4711 {'body': 'The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story\n\nThe stories of F0002:\n\n- F0002-S0001: First story\n- F0002-S0002: Second story\n- F0002-S0003: Third story'}
WALK request: PUT /pulls/4711/merge {'merge_method': 'merge', 'commit_title': 'Merge pull request #4711 from develop', 'commit_message': "Promoted by Kumpel after F0002's acceptance."}
WALK POSTs in all: 1
WALK approving: backlog wait: True
WALK approving: reuse: True
3 passed in 0.89s
```

The walk is green, and every step matches what `install.md`, *The promotion*, the playbook's step 8 and `approving.md` now say. One note from the run: in a first version of the walk, I did not update the stand-in's answer for the open promotion before the run with the switch on. The script then sent a second, identical `PATCH`. That is correct, since it compares against the body the hosting service reports. The version above answers with the patched body, and the rerun sends nothing.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- **`test_operator_archive_outcome.py:121-124` finds the `approving.md` section with its own inline lines** (S0012 coder entries 11 and 15). That is the copy S0012's reviewer had removed from the new test in favour of `section_text`. Replacing it changes an earlier test, which needs the human's leave. It is four lines in one test, so it is a note and no story.
- **The name `text` in `tests/operator_scripts/test_operator_approving_after_acceptance.py:27`** shadows the section text read on line 17 (S0012 reviewer entry 17). Note.
- **`approving.md` step 1's first line still says "report that to the human"** for every refusal, and the continuation line narrows it for the `backlog/` case (S0012 coder entry 7). Read in order, the two lines agree. Note.
- **`make duplicates` still reports "6 new, 39 known, 4 gone"** after both coders (S0010 entry 7, S0012 entries 7 and 15). F0057-A0002 traced this to a stale `security/duplicates-baseline.txt`, which is the human's file. S0010 only removed duplication. Still open for the human.
- **S0011's docs reviewer** rejected two possible findings itself: a 33-word list sentence, and bullets of several sentences. Closed.
- Earlier notes that F0057-A0002 kept as notes stay as they were. These are the front matter's opening `---`, an open promotion with a `null` body, the guide-file guard on the bare `work-items.md`, and the test-support docstrings that say `main`.

## 5 The documentation as a whole

I read `README.md`'s branch lines, `docs/operator-guide/install.md` (*The branches*, *The promotion*, *Fixes go to `develop`*), the playbook's step 8 and *Finished features*, `docs/project-guide/work.md` (the `paths` table), `operator.md` (*The skill's scripts* and its test tables), `pipeline.md` and `agents.md` on `PIPELINE_REF`, and the Kumpel skill's `approving.md`.

The three gaps of F0057-A0002 are closed:
- The project guide names Kumpel's scripts, tests and helper (S0011).
- `install.md`, the playbook and `approving.md` agree on the wait after an acceptance that proposes stories. All three say the same refusal text and the same "next accepted acceptance" (S0012).
- `approving.md` step 2 names the reuse (S0012).

My walk ran the commands and messages these documents name, and they match.

Remarks, none of weight:
- **`docs/project-guide/work.md:397-398` explain the ref twice.** Line 397, written before S0010, says the code builds `origin/<branch>` "from `REMOTE` and `WORK_BRANCH`". Line 398 says it builds the working branch's ref only through `WORK_REF`. They do not contradict each other, since `WORK_REF` is built from those two, but a newcomer reads two rules. It could be one sentence at the next touch of `work.md`. Note.
- **The playbook's step 8** carries the new case as a long parenthesis inside a sentence. The playbook is the human's document. Note.
- A search of `README.md`, `docs/` (besides `docs/decisions.md`'s dated entries and `docs/runs/`) and `operator/` finds no stale `origin/main` and no `_WORK_REF`. The only `origin/main` outside the dated entries is `install.md:11`, the command that creates `develop` from `main`, which is right.

## 6 Decisions taken for the human

From `feature.md`: decisions 1 to 9, as listed in F0057-A0001. They were accepted by its merge.

From the journals of S0010 to S0012: no question was asked, so there were no answers. Defaults nobody asked about:
- **S0010:** `PIPELINE_REF` and `FORM_REF` stay as public aliases of `WORK_REF`, as the Description said, and are not replaced at their call sites.
- **S0012:**
  - The new step-1 case is a continuation line, so that the earlier test, which reads only step 1's first line, stays untouched.
  - No change of behaviour: an acceptance that proposes stories defers the archive and the promotion. The Description left the alternative, promoting at once, to the human when refining. No answer chose it, and no `docs/decisions.md` entry was written.
- **S0012's tester** kept a `SECTION` constant that the coder had asked it to remove (entry 13). It is used twice. Harmless.

Still open for the human, from the earlier acceptances:
- **An acceptance that proposes stories defers its feature's archive and promotion** (F0057-A0002). It is now documented as it is. Changing it is a product question.
- **The coder may not write its own work item**, while its instructions ask it to correct the Description. `factory/pipeline.yml:23` still has no `{work_item}` for the coder. S0010 to S0012 needed no correction, so it did not bite this time.
- **`tests/agent_files/test_claude_agent_texts.py:144` forbids `promote` in the agent files**, and **`reset-to-tag.sh` leaves `main` alone** (F0057-A0001).
- **`security/duplicates-baseline.txt` is stale** (check 4).

Earlier tests changed: none in S0010, S0011 or S0012. Each reviewer's entry says so (S0010 entry 9, S0012 entries 9 and 17), and S0011 changed only a document. No earlier test changed without a named leave.

## 7 The slow checks

Nothing beyond `make check` is offered, and `make mutants` is outside this stage (check 3). `make check` ran green here: `test: green (107.7 s)`, coverage 99.22 %, `check: green`.

The JUnit report holds 11020 tests summing to 939.1 s, 16 more than at F0057-A0002. The slowest are the ten-second `ROOMY_LIMIT` tests, as designed:
- `tests/machine/adapters/test_podman_timeout_status.py::test_podman_s_timeout_status_at_the_limit_is_a_timed_out_run[255-at-the-limit]` (10.02 s)
- the same test's `[137-at-the-limit]` row (10.02 s)
- `tests/shared/adapters/test_document_examples.py::test_the_folder_and_the_home_are_gone_once_the_document_has_run[past-the-limit]` (10.01 s)

The 12 tests of S0010's and S0012's new modules take 0.03 s together. The slowest of them is the repository guard of `test_work_ref_search.py`, at 0.014 s.

Disk: now `/srv/factory/vm` has 15.0 GB free and 1.5 GB used. At the previous record, "disk start", it had 15.8 GB free and 1.5 GB used. `/srv/factory/vm/state` and `/tmp` show the same free figures, so they share one pool. Free space fell by 0.8 GB while the used figure stayed the same. That continues the trend F0057-A0001 and F0057-A0002 reported: 0.7 GB, then 0.5 GB. The feature's changes since F0057-A0002 do not explain it. `git diff --stat` against F0057-A0002's archive commit (`88484da91`) shows no change to `uv.lock`, `pyproject.toml`, `Makefile`, `operator/vm` or a stage Containerfile. The changes were constants, documents, one skill text and tests. The space goes to something these records do not measure, such as datasets, snapshots or images elsewhere in the pool. It is still unexplained and still growing, and it is worth a look by the human.

## 8 Cost

The stories cost 124 runs, 192.0 min, 1089 turns and $34.85. S0001 to S0009 were $31.15 of that (103 runs, 172.6 min; see F0057-A0002). The three later stories cost 21 runs, 19.3 min and $3.69:

| Story | Runs | Minutes | Cost |
|---|---|---|---|
| S0010 | 6 | 5.7 | $1.16 |
| S0011 | 5 | 4.6 | $0.85 |
| S0012 | 10 | 9.0 | $1.68 |

None stands out. S0003 ($9.68) is still the costliest of the feature. Among the three, S0012 cost the most: one review round on a copied section reader in its own new test, which went coder, then tester, then coder, then review again (entries 9 to 17). S0010 and S0011 went straight through, apart from one docs-review round in S0011 on four style findings.

The human answered 17 questions, all of cause `question`, and the stories waited 0.6 h in total. S0010 to S0012 asked none. **S0002 still needed the human most over the whole feature** (7 of 17), for the reason F0057-A0001 gives: its narrow Interface had to be widened text by text until the human's answer in its journal entry 39.

## Proposed stories

None. Every remaining item is a note, or the human's file or choice (check 6). A proposed story would also hold back F0057's archive and first promotion until it and a further acceptance were done (check 2).

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted; 0 stories proposed

   1 Scope: none. The scope lines of S0001 to S0005 still hold. S0010 added `WORK_REF`, S0011 added the project guide's Kumpel scripts and S0012 added the procedure after an acceptance that proposes stories. All three stay within scope, and out of scope was respected. Protecting `main` and the first promotion are the human's acts, which I cannot see from the repository.
   2 Feature smoke test: green, 3 passed. A new project waits for `develop`. A merged story is archived on `develop` and `main` does not move. Kumpel refuses to archive a refused feature or one with proposed stories in `backlog/`, and refuses to promote one that is not archived. It archives an accepted feature as Kumpel, sends one `POST` and one `PATCH`, and merges with `merge_method: merge` only when the switch is on. `approving.md` names both waits.
   3 Mutation testing: by sweep, not run here.
   4 Noticed: `test_operator_archive_outcome.py:121-124` still has an inline section reader, and changing it needs the human's leave. A shadowed name `text` in S0012's test. `approving.md` step 1's first line is broader than its continuation line. `make duplicates` still reports 6 stale new findings against the human's baseline. All are notes.
   5 Documentation: the three gaps from A0002 are closed, and `install.md`, the playbook and `approving.md` agree with the scripts and with the walk. Two small notes: `work.md:397-398` state the ref rule twice, and playbook step 8 has a long parenthesis.
   6 Decisions: no questions in S0010 to S0012. Defaults: `PIPELINE_REF` and `FORM_REF` are kept as aliases, S0012 changed no behaviour, and its new case sits on a continuation line. Still open for the human: the deferred promotion after proposed stories, no coder write path for corrections to the Description, the agent-file guard on `promote`, `reset-to-tag.sh` leaving `main` alone, and the stale duplicates baseline. No earlier test was changed.
   7 Slow checks: nothing beyond `make check`, which is green (`test: green (107.7 s)`, 99.22 %, 11020 tests). The slowest are the 10 s `ROOMY_LIMIT` tests. Free disk fell another 0.8 GB with used space unchanged, the third drop in a row, and no dependency or image change explains it.
   8 Cost: $34.85 over 124 runs. S0010 to S0012 cost $3.69 over 21 runs, and S0012 the most of them ($1.68, one review round on its own test). S0003 is still the costliest ($9.68). 17 questions were answered and the stories waited 0.6 h; S0010 to S0012 asked none. S0002 needed the human most (7).
