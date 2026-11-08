---
stage: done
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 648
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T01:42:27.764900Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T01:52:02.901047Z'
  stage: acceptance
  run: cf8170776cca40408d78b64cfa62fcff
- number: 3
  speaker: factory
  kind: done
  at: '2026-11-08T01:55:58.472953Z'
  stage: done
stories: [F0057-S0001, F0057-S0002, F0057-S0003, F0057-S0004, F0057-S0005]
outcome: accepted
---

# Acceptance of The factory works on develop

## Recommendation

**Accepted with stories.** Every scope item has its story, `make check` is green, and the feature's smoke test passes end to end. On a fresh remote with only `main`, the factory names `develop` and waits for it. Once `develop` exists it archives a merged story there and leaves `main` alone. Kumpel archives the feature as itself and promotes `develop` to `main` with a merge commit, and only when the switch is on. The findings do not break what the feature promised:
- `archive-feature.sh` archives a feature whose last acceptance was refused.
- `promote.sh` cannot reuse a promotion pull request that is still open.
- The playbook still archives by hand.
- The code still has some names that say `main`.

Four stories are proposed for them.

## 1 Scope

None. Each scope line of `feature.md` maps to an archived story, and the code those stories name matches:
- One constant: `WORK_BRANCH` in `src/factory/shared/domain/paths.py` (S0001). The guard `tests/guards/test_work_branch_search.py` keeps the literals out of `src/` and `tests/`.
- The constant says `develop` (S0002). The agent files, `operator/template/` and the todo demo follow it (guard `tests/guards/test_working_branch_in_agent_texts.py`). The waiter and the preflight name `develop`.
- Kumpel works on `develop` (S0003): `start-story.sh`, `next-story.sh`, `approval.sh`, `status.sh`, `merge.sh` and `reset-to-tag.sh`. The new `archive-feature.sh` and `promote.sh` sit behind the switch `promote`, and every Kumpel commit goes through `kumpel-commit.sh`.
- The operator's documents name `develop` (S0004) and so does the project guide (S0005).

No story goes beyond the scope. S0004's one code change, taking `promote`/`promoted` out of `GLOSSARY_FORBIDDEN`, served its documents and was the human's decision (S0004 journal 11).

Out of scope was respected:
- No setting names the branch.
- `main_branch_failing` keeps its name, and `stops.md` and `pipeline.md` say it means the working branch.
- Old `docs/decisions.md` entries and `docs/runs/` are untouched.

The goal's last conditions are the human's own acts and cannot be seen from the repository: the factory running on `develop`, and `main` protected. That the factory runs on `develop` is shown indirectly: this branch was cut from `develop`, and S0003 to S0005 were merged into `develop`.

## 2 Feature smoke test

The walk: a new project gets `develop`, the factory works there, and Kumpel promotes to `main`. It is one pytest module, written in a `mktemp -d` folder and removed after the run. It used the repository's `tests/conftest.py` fixtures as a plugin and called only the real entry points: `RepositoryWaiter`/`CheckoutPreparer` and `MergedHandler` on real git remotes, and the real Kumpel scripts with the suite's `curl` stand-in for the hosting API. It has four parts:
1. A remote with only `main` gets a stop, then `develop` is created from `main` as `install.md` step 1 says.
2. A merged story is archived on `develop` while `main` stays where it was.
3. `archive-feature.sh` runs, then `promote.sh` with the switch off and then on.
4. A probe: `archive-feature.sh` on a feature whose last acceptance in `done/` is booked `outcome: refused`.

```console
$ PYTHONPATH=tests uv run pytest -p conftest -p no:xdist -p no:cacheprovider -s -q --rootdir=. -o addopts="" --tb=short "$d/test_feature_f0057_walk.py" | grep -E "^E |WALK|passed|failed|error"
WALK WORK_BRANCH: develop
WALK only main: prepared: False
WALK only main: stop: ['the repository has no develop branch yet']
WALK with develop: prepared: True
WALK with develop: stops left: []
.WALK develop log: ['work item F0001-S0001: merged, archived', 'merge work-item/F0001-S0001', 'start F0001-S0001-first.md']
WALK done/ on develop: True
WALK main moved: False
.WALK archive-feature.sh: (0, '05d69ea F0001: archived', '')
WALK develop tip: F0001: archived | Kumpel <kumpel@noreply.invalid> | Kumpel
WALK archive on develop: ['F0001-example']
WALK promote.sh (switch off): (0, 'promotion opened: #4711, for the human to merge', '')
WALK promote.sh (switch on): (0, 'promoted #4711', '')
WALK request: POST /pulls {"head": "develop", "base": "main", "title": "F0001: promoted to main", "body": "The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story"}
WALK request: POST /pulls {"head": "develop", "base": "main", "title": "F0001: promoted to main", "body": "The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story"}
WALK request: PUT /pulls/4711/merge {"merge_method": "merge", "commit_title": "Merge pull request #4711 from develop", "commit_message": "Promoted by Kumpel after F0001's acceptance."}
.WALK archive-feature.sh after a refused acceptance: (0, '35f23da F0001: archived', '')
4 passed in 0.69s
```

The walk is green: every assertion of the feature's promise held. Two observations from it:
- **The probe.** `archive-feature.sh` archived a feature whose last acceptance is `refused`. The script checks only that the last acceptance is in `done/`, but the factory books a closed acceptance in `done/` too (`src/factory/work/application/acceptance.py:334`, "Books a closed acceptance `refused` in `done/`"). From there `promote.sh` would promote it, so a refused feature could reach `main`. Kumpel's procedure (`references/approving.md`, "When the merge accepted a feature's acceptance") is what stands in the way today; the script does not. Proposed: S0006.
- **The second POST.** With the switch off, `promote.sh` opens the promotion. Running it again opens a second pull request from `develop` to `main`, which is what happens when the human turns the switch on, or when the next feature is accepted before the human merged the first promotion. The `curl` stand-in accepted the second POST. GitHub refuses a second open pull request for the same head and base (422), so on the real host the script stops at `hosting: POST ...: 422`. Proposed: S0007.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- **Names that still say `main` (S0001 coder entries 10, 14 and 21; S0002 entries 41, 45 and 47, and the human's entry 39: "anything else that still says main in words goes to the journal as a note for a later story"):**
  - `stage_file_on_main` (`src/factory/entry/wiring.py:437`), `_main_report_paths`/`_main_reports` (`work/application/acceptance_reading.py:108`, `:202`), `_main_commit` (`watching/application/watcher.py`) and `EvaluationInput.main_commit` (`pipeline/domain/evaluation.py:39`).
  - The local variables named `main` in `machine/application/preflight.py` and `pipeline/domain/evaluation.py`, and the comment at `entry/check_story.py:68`.
  - In tests: the constant `NO_MAIN` (`tests/pipeline/application/test_repository_waiter.py:33`), which now holds `develop`, and the test docstrings and names that say `main` for the working branch, for example the `remote` fixture's docstring in `tests/conftest.py:155` and `tests/pipeline/application/handlers/test_merged.py`'s module docstring.

  None of these is in the records contract. The stamp fields `main_failed`/`main_probed` are stored in `preflight-stamp.json`, and `main_branch_failing` is kept by decision 6. Proposed: S0009, leaving the stored fields and the stop out.
- **`f"origin/{WORK_BRANCH}"` with the remote's name written out** in `hand_over.py` and `stage.py` (S0001 coder entries 10, 14, 18 and 21). The human deferred it to S0002 (entry 19), and S0002 did not take it up. It is included in S0009.
- **`tests/pipeline/application/test_repository_waiter.py` copied `make_remote`**: S0002 fixed it under the standing leave. Closed.
- **The test of S0002's criterion 5 duplicates the one above it** (`tests/machine/application/test_preflight_run.py:82`, reviewer entry 47). It is a note, and no story is proposed for it.
- **`stage.py:162`'s merge-conflict text has no test that pins it** (S0002 tester entry 43). The human chose no criterion (entry 39). It is listed in check 6.
- **`settings.sh set promote` on an old settings file** (S0003 coder entry 16): fixed in S0003 round 1. Closed.
- **The name `test_a_settings_file_without_the_promote_switch_reads_it_as_off` now covers four rows** (S0003 reviewer entries 30 and 38). It is a note, and no story is proposed.
- **`tests/agent_files/test_claude_agent_texts.py:144` still forbids `promote` in the agent files** (S0004 tester entry 10, coder entry 15). The human said leave it (entry 11), so it is listed under 6.
- **`docs/operator-guide/stops.md` said "on `main`"** (S0003 documenter entry 40): S0004 fixed it. Closed.

## 5 The documentation as a whole

I read `README.md`, `docs/operator-guide/` and `docs/project-guide/` for a `main` that means the working branch, with `grep -rnw main` minus the entry-point functions. Every remaining `main` either means the line of accepted features (`install.md` *The branches*, `operator/README.md`, `operator.md:133`) or is a code name. No two stories contradict each other: `install.md`, `operator/README.md`, `SKILL.md` and `references/approving.md` describe the archive and the promotion the same way. The gaps:
- **`docs/operator-playbook.md:203` still says a finished feature is moved to `factory/archive/` "by hand (`git mv`)".** Since decision 8 that is `archive-feature.sh`, which commits as Kumpel. Step 8, the acceptance, says nothing of the promotion that now follows it. S0004's Interface named the playbook, but its documenter only fixed the branch names. This does not mislead in behaviour, because a hand-made `git mv` still satisfies `promote.sh`, but the playbook contradicts the scripts and decision 8.
- **`docs/operator-guide/work-items.md:221` (turn off *Automatically delete head branches*)** gives only the story reason. With the setting on, merging a promotion would also delete `develop` itself, the head of every promotion. That is a stronger reason, and nobody wrote it.
- **`install.md` does not say which branch is the repository's default.** The feature keeps `main` as the default (*The human's changes*, step 5), so a fresh clone starts on `main`. The scripts and the factory all check out `develop` explicitly, so nothing breaks, but the newcomer's question is not answered.
- **`install.md` step 1 says "the preflight names a missing `origin/develop`".** On a remote with only `main`, the operator actually sees the waiter's `repository_unavailable` stop, "the repository has no develop branch yet" (smoke test, part 1), not the preflight's finding. `health.md` lists both rows correctly. The text follows S0004's criterion 2 word for word, so it is imprecise rather than wrong.

Proposed: S0008, one documentation repair for these four.

## 6 Decisions taken for the human

From `feature.md`: decisions 1 to 9 (develop/main; `WORK_BRANCH`; the switch `promote` off by default; a promotion carries `develop`'s tip; a merge commit only, and `main` is never fixed directly; `main_branch_failing` keeps its name; every Kumpel commit names Kumpel; Kumpel archives with a script; the tests' change first). Decisions 1 to 7 are recorded in `docs/decisions.md`.

From the journals (the human's answers):
- **S0001 j4:** the guard has one failing row per literal.
- **S0001 j19/j24:** criterion 5 sends the documenter to `work.md`'s `paths` table, not `shared.md`.
- **S0002 j4:** criterion 3 is widened to one row per form, and every prose `main` in the agent files and the template, R10 included, says `develop`.
- **S0002 j9:** the Kumpel scripts stayed on `main` in S0002, with their tests on a constant of their own, and moved in S0003.
- **S0002 j14:** the coder could write `demo/todo-service/project/Makefile` and `CLAUDE.md`, and the human changed `factory/pipeline.yml` for that one story.
- **S0002 j21:** the repository stop's text follows `WORK_BRANCH`, the private names and docstrings are reworded, and there is a new criterion.
- **S0002 j28:** one test change, `OTHER_BRANCH` in `test_repository_waiter.py`.
- **S0002 j39:** the texts the operator sees follow `WORK_BRANCH`. Everything else that still says `main` became a note, and only blocking points were asked about after that.
- **S0002 j50:** the human gave the text of the `docs/decisions.md` entry. Rejected options are recorded only for decisions 1 and 4.
- **S0003 j4:** the intake's added criteria were accepted.
- **S0003 j14:** `DEFAULT_BRANCH` in `test_operator_merge_reset.py`. The coder could write `operator/README.md`. A settings file without `promote` reads it as `off`, which S0003's review widened to `set`.
- **S0004 j4:** criteria 2 and 3 were split and sharpened.
- **S0004 j11:** `promote` and `promoted` left `GLOSSARY_FORBIDDEN`. `tests/agent_files/test_claude_agent_texts.py` still forbids `promote` in the agent files: worth a look, since `promote` is now the switch's name.
- **Defaults nobody asked about:**
  - `archive-feature.sh` treats any acceptance in `done/` as finished, whatever its outcome (S0006 proposes otherwise).
  - `promote.sh` titles a promotion after one feature, though it carries all of `develop`'s tip (decision 4).
  - `reset-to-tag.sh` leaves `main` alone.

Earlier tests changed, each with its leave:
- **S0001:** 163 test modules, only to replace the literal branch with the constant. Leave: the human, 2026-11-07, in its Interface. The reviewer's entries 12 and 23 list them, and four went beyond a plain replacement (named in tester entry 8, within the leave).
- **S0002, the agent-text tests and the tests whose only failure was the new value:** under the Interface's leave of 2026-11-07.
- **S0002, the Kumpel script tests:** j9.
- **S0002, `test_repository_waiter.py`, `tests/entry/test_health.py` and `test_run_waiter.py`:** j21, plus j28 for `OTHER_BRANCH`.
- **S0002, the pinned visible texts:**
  - `test_preflight_run.py`, `test_preflight_run_environment.py` and `test_preflight_stale_main_stop.py`
  - `test_preflight_stop_detail.py`, `test_acceptance_merged.py`, `test_acceptance_no_state_refusals.py` and `test_stall_edges.py`
  - `test_acceptance_closed.py`, `test_acceptance_description.py` and `test_stall_texts.py`

  Leave: j39. `make_remote` gained a `branch` parameter under the standing leave.
- **S0003:**
  - `tests/support/operator_skill_support.py`, `test_operator_merge_reset.py` and `test_operator_skill_scripts.py`: under the Interface's leave of 2026-11-07, with j14 for `DEFAULT_BRANCH`.
  - `test_operator_skill_signature.py`: `KUMPEL` moved under the standing leave.
- **S0004:** `tests/pipeline/domain/test_documents.py::test_the_v1_words_are_the_sixteen_in_their_order`, with its list and its name changed from eighteen, under j11 ("with your leave for the pinned test").

No earlier test changed without a named leave.

## 7 The slow checks

Nothing beyond `make check` is offered today, and `make mutants` is outside this stage (check 3). `make check` ran green here: `test: green (102.5 s)`, coverage 99.22 %, `check: green`. The JUnit report holds 10969 tests summing to 937.8 s. The slowest are the time-limit tests at their ten-second `ROOMY_LIMIT`, by design, for example:
- `tests/machine/adapters/test_podman_timeout_status.py::test_podman_s_timeout_status_at_the_limit_is_a_timed_out_run[137-at-the-limit]`
- `tests/shared/adapters/test_process_session.py::test_time_limit_ends_every_process_of_the_group[run_process-own-session]`

Both took 10.0 s. None of the feature's tests stands out.

Disk: at the acceptance, `/srv/factory/vm` has 15.7 GB free and 1.5 GB used. At the previous record line, "disk start", it had 16.4 GB free and 1.5 GB used. `/srv/factory/vm/state` and `/tmp` show the same free figure, so they share one pool. Free space fell by 0.7 GB while the used figure did not change, so the space went to something these three records do not measure, such as other datasets, snapshots or images in the pool. The feature's changes do not explain it: no dependency, `uv.lock` or `operator/vm/Dockerfile` change. Two notes: the 0.7 GB is unexplained, and the "start" line does not say whose start it is.

## 8 Cost

The stories cost 69 runs, 133.6 min, 717 turns and $24.34:
- S0001: 13 runs, 18.9 min, $3.79
- S0002: 23 runs, 41.0 min, $8.06
- S0003: 19 runs, 54.8 min, $9.68
- S0004: 9 runs, 13.1 min, $1.91
- S0005: 5 runs, 5.8 min, $0.89

**S0003 stands out in time and money.** It stalled once on a red `lint` after the tests stage (j9) and went through three review rounds. Round 0's two findings were the settings table and the commit helper. Round 1 found that `promote.sh` read a story's title as `---`, the front matter of a story in `done/`, plus the unknown-switch rows on an old settings file. Each round went coder, then tester, then coder.

The human answered 14 questions, all of cause `question`, and the stories waited 0.5 h for them:

| Story | Questions | Journal entries |
|---|---|---|
| S0001 | 3 | 3, 18, 23 |
| S0002 | 7 | 3, 8, 13, 20, 27, 38, 49 |
| S0003 | 2 | 3, 13 |
| S0004 | 2 | 3, 10 |
| S0005 | 0 | – |

**S0002 needed the human most.** Its Interface said "`src/factory/` otherwise unchanged", so each further text that still said `main` had to be asked about: the Kumpel scripts, the demo project outside the write paths, the scheduler's message, two tests disagreeing, and the visible texts. The documenter also had no source for the rejected options of the decisions. The human's j39 ("ask only for something that blocks") ended the loop.

## Proposed stories

- `backlog/F0057-S0006-archive-feature-refuses-a-feature-whose-acceptance-was-refused.md`: the walk archived a refused feature, and from there it can be promoted to `main`.
- `backlog/F0057-S0007-promote-reuses-an-open-promotion.md`: a second `promote.sh` while a promotion is open stops at the host's 422, which happens when the switch is turned on or when two features are accepted before the human merges.
- `backlog/F0057-S0008-the-operators-documents-on-archive-promotion-and-the-default-branch.md`: the playbook's hand archive, the reason to keep auto-delete off, the default branch and the stop a new project sees.
- `backlog/F0057-S0009-the-code-names-the-working-branch-by-its-role.md`: the code names and test texts that still say `main`, which the human sent to a later story (S0002 j39).

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted with stories; 4 stories proposed (F0057-S0006 to S0009)

   1 Scope: none. Each scope line has its story, no story goes beyond the scope, and the out-of-scope items were respected. The factory running on `develop` and `main` being protected are the human's acts and cannot be checked here.
   2 Feature smoke test: green, 4 passed. A remote with only `main` gets the stop "the repository has no develop branch yet", and creating `develop` clears it. A merged story is archived on `develop` and `main` does not move. `archive-feature.sh` commits as Kumpel, and `promote.sh` opens develop→main and merges with `merge_method: merge` only when the switch is on. Two probes found gaps: `archive-feature.sh` archives a feature whose last acceptance was refused (→ S0006), and a second `promote.sh` opens a second promotion, which GitHub refuses with 422 (→ S0007).
   3 Mutation testing: by sweep, not run here.
   4 Noticed: names in the code and tests that still say `main` for the working branch, and `origin/` written out in `hand_over.py` and `stage.py`, which the human sent to a later story in S0002 j39 (→ S0009). The other notes were closed or were left as they are by the human's choice.
   5 Documentation: no contradictions between stories. Gaps: the playbook still archives by hand and has no promotion step; the auto-delete setting would delete `develop` when a promotion is merged; the default branch is not stated; `install.md` names the preflight where a new project actually sees the waiter's stop (→ S0008).
   6 Decisions: feature decisions 1 to 9, the human's 14 answers across S0001 to S0004, and three defaults nobody asked about. Every earlier test change has a named leave.
   7 Slow checks: nothing beyond `make check`, which is green (`test: green (102.5 s)`, 99.22 %). The slowest tests are the 10 s `ROOMY_LIMIT` ones. Free disk fell 0.7 GB with the used figure unchanged, which the feature's changes do not explain (no dependency or image change).
   8 Cost: $24.34 over 69 runs. S0003 cost the most ($9.68, 54.8 min: a lint stall and three review rounds). S0002 needed the human most: 7 of the 14 questions, because its narrow Interface had to be widened text by text until the human's j39. The stories waited 0.5 h in total.
3. factory: done (pull request merged); cost: 1 runs, 9.5 min, 55 turns, 170040 tokens in (5143179 more from cache), 43362 out, $2.75
