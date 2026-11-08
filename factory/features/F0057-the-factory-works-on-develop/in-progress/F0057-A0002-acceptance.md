---
stage: approval
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 653
comments_read: []
handed_over: approval
claim: null
journal:
- number: 1
  speaker: factory
  kind: started
  at: '2026-11-08T03:23:01.202893Z'
  stage: acceptance
- number: 2
  speaker: acceptance-reviewer
  kind: result
  at: '2026-11-08T03:31:42.319049Z'
  stage: acceptance
  run: b83a59bab6e94c448e2bbdbebcc18b0d
stories: [F0057-S0001, F0057-S0002, F0057-S0003, F0057-S0004, F0057-S0005, F0057-S0006, F0057-S0007, F0057-S0008, F0057-S0009]
outcome: null
---

# Acceptance of The factory works on develop

## Recommendation

**Accepted with stories.** `make check` is green, and the feature's smoke test passes end to end:
- A new project names and waits for `develop`.
- A merged story is archived on `develop` and `main` does not move.
- Kumpel refuses to archive a refused feature, archives an accepted one as itself, opens one promotion and adds the next feature to it, and merges it with a merge commit only when the switch is on.

The four stories that the first acceptance proposed (S0006 to S0009) did what they promised, and nothing in the feature's promise is broken. Three findings remain, each worth a small story:
- The project guide does not name Kumpel's new scripts.
- After an acceptance that proposes stories, the archive and the promotion behave differently from what the playbook and Kumpel's procedure say.
- `origin/develop` is built in sixteen places.

## 1 Scope

None. The scope lines of `feature.md` (S0001 to S0005) were checked in F0057-A0001 and still hold:
- `WORK_BRANCH` in `src/factory/shared/domain/paths.py:13` says `develop`.
- Its guard `tests/guards/test_work_branch_search.py` passes.

The four later stories came from that acceptance's proposals. Each stays within the feature's Kumpel and documents scope, and none goes beyond it:
- **S0006:** `operator/skill/kumpel/scripts/archive-feature.sh:36-44` reads `outcome: accepted` between the first two `---` lines.
- **S0007:** `promote.sh` asks for an open promotion and reuses it, sending `PATCH` with the body only.
- **S0008:** the four documentation gaps are closed:
  - `docs/operator-playbook.md:203` names `archive-feature.sh`.
  - `docs/operator-guide/work-items.md:224` gives the `develop` reason for keeping auto-delete off.
  - `install.md:45` names the default branch.
  - `install.md:11` names the waiter's stop.
- **S0009:** the code names say the working branch. The only identifiers left with a `main` part are the kept ones (`main_branch_failing`, `_MAIN_FAILING`, `main_failed`, `main_probed`).

Out of scope was still respected: no branch setting, `main_branch_failing` kept, no old decision entries and no `docs/runs/` touched. `feature.md`'s Stories list still names only S0001 to S0005. That is the human's file, and the intakes treated the proposed stories as in scope.

The goal's last conditions are the human's acts and cannot be seen from the repository:
- `main` is protected.
- The first promotion (*The human's changes*, "After the feature's acceptance").

That the factory runs on `develop` is shown indirectly: this branch and S0006 to S0009 were cut from `develop` and merged into it.

## 2 Feature smoke test

The walk is a user's path through the feature: a new project, a story merged, then Kumpel after two acceptances. It also replays this feature's own history: the first accepted acceptance proposed stories into the feature's `backlog/`, and a second one followed them.

The script is one pytest module, written in a `mktemp -d` folder and removed after the run. It uses the repository's `tests/conftest.py` fixtures as a plugin and calls only the real entry points:
- `RepositoryWaiter`/`CheckoutPreparer` and `MergedHandler` on real git remotes.
- The real `archive-feature.sh` and `promote.sh`, with the suite's `curl` stand-in for the hosting API.

It has three parts:
1. A remote with only `main`, then `develop` created from it.
2. A story merged and archived. A `main` branch sits at the start commit and must not move.
3. Kumpel:
   - F0001's only acceptance is refused.
   - F0002 is accepted but has a proposed story in its `backlog/`.
   - The human then merges an accepted A0002 for F0001 and finishes F0002's story.
   - Kumpel archives both features and promotes F0001 with the switch off. It promotes F0002 into the open promotion, runs that again, and runs it once more with the switch on.

```console
$ PYTHONPATH=tests uv run pytest -p conftest -p no:xdist -p no:cacheprovider -s -q --rootdir=. -o addopts="" --tb=short "$d/test_feature_f0057_walk.py" 2>&1 | grep -E "^E |WALK|passed|failed|error|Error"
WALK WORK_BRANCH: develop
WALK only main: prepared: False
WALK only main: stops: ['the repository has no develop branch yet']
WALK with develop: prepared: True
WALK with develop: stops left: []
.WALK develop tip: work item F0001-S0001: merged, archived
WALK done/ on develop: True
WALK main moved: False
.WALK archive F0001 after a refused acceptance: 1 archive-feature.sh: F0001 is not finished: its last acceptance factory/features/F0001-example/done/F0001-A0001-acceptance.md is not accepted
WALK archive F0002 with a proposed story in backlog/: 1 archive-feature.sh: F0002 is not finished: factory/features/F0002-other/backlog/F0002-S0003-proposed.md is in backlog/
WALK archive F0001 after A0002 accepted: 0 0fcf417 F0001: archived 
WALK develop tip author: F0001: archived | Kumpel <kumpel@noreply.invalid>
WALK main tip: seed
WALK promote F0001 (off, none open): 0 promotion opened: #4711, for the human to merge 
WALK archive F0002: 0 b07954d F0002: archived 
WALK promote F0002 (off, F0001's open): 0 promotion open: #4711, for the human to merge 
WALK promote F0002 again (off): 0 promotion open: #4711, for the human to merge 
WALK promote F0002 (on): 0 promoted #4711 
WALK request: POST /pulls {"head": "develop", "base": "main", "title": "F0001: promoted to main", "body": "The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story"}
WALK request: PATCH /pulls/4711 {"body": "The stories of F0001:\n\n- F0001-S0001: First story\n- F0001-S0002: Second story\n\nThe stories of F0002:\n\n- F0002-S0001: First story\n- F0002-S0002: Second story\n- F0002-S0003: Proposed"}
WALK request: PUT /pulls/4711/merge {"merge_method": "merge", "commit_title": "Merge pull request #4711 from develop", "commit_message": "Promoted by Kumpel after F0002's acceptance."}
WALK POSTs in all: 1
3 passed in 0.83s
```

The walk is green. Both probes of F0057-A0001 now hold:
- A refused feature is not archived, so it cannot be promoted.
- A second promotion reuses the open pull request: one `POST`, one `PATCH`, a rerun that sends nothing, and the merge.

Two observations:
- **An acceptance that proposes stories.** The archive refuses it with `... is in backlog/`, so the promotion waits until the proposed stories and a further acceptance are done. That is what happened to F0057 itself after A0001. `docs/operator-playbook.md:31` says the opposite order: "After an accepted feature is archived, its promotion follows ... Proposed stories land in `backlog/` ... A further acceptance follows them". `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 makes Kumpel report the refusal to the human as if something had failed. Nothing breaks, because the refusal is fail-safe, but the documents tell the operator to expect a promotion that does not come. Proposed: S0012.
- **The promotion's title stays `F0001: promoted to main`** when it also carries F0002. S0007 decided this ("The title stays"). It is listed under 6.

## 3 Mutation testing

By sweep, not run here.

## 4 What the stories noticed

- **`origin/develop` is built in sixteen places** (S0009 coder entries 10 and 14, reviewer entry 16):
  - `_WORK_REF = f"{REMOTE}/{WORK_BRANCH}"` is defined again in nine modules: `tick`, `scheduler`, `preflight`, `work_items`, `acceptance`, `acceptance_reading`, `wiring`, `watcher` and `opening`.
  - `FORM_REF` (`pipeline/application/task.py:31`) and `PIPELINE_REF` (`pipeline/application/pipeline_loading.py:15`) hold the same value.
  - Five calls spell it inline: `handlers/hand_over.py:78`, `stops.py:120` and `:142`, `stage.py:488`, `watching/application/costs.py:229`.

  `CLAUDE.md` counts a second copy of a helper as a finding, and this one has fifteen. Proposed: S0010.
- **The front matter's opening `---` need not be the file's first line** in `archive-feature.sh`'s check (S0006 coder entry 13, reviewer 15, documenter 17, smoke-tester 19). It is what the Interface says, and the factory always writes front matter at the top. Note, no story.
- **An open promotion whose body is `null`** gets a `PATCH` body that starts with a blank line (S0007 coder entries 10 and 18). `promote.sh` always writes a body. Note, no story.
- **The coder's Description edits are dropped by the take** (S0007 entries 14 to 24; S0009 entries 14 and 16). In S0007 the coder rewrote criterion 4 ("exits non-zero" to the hosting client's 22), and the factory left it out because the work item is outside the coder's write paths. The archived criterion still says "exits non-zero", which is true of 22. In S0009 the reviewer had to write the coder's dropped criterion 6 edit again. The coder's instructions ask it to correct the Description, while its write paths refuse it. That is a pipeline matter (`factory/pipeline.yml` and the agent files are the human's), listed under 6.
- **The guard `tests/guards/test_project_guide_files.py::test_no_file_names_a_removed_guide_file`** failed S0008's first docs run on the bare name `work-items.md` in the playbook (S0008 entries 6 and 8). The name belongs to a live operator-guide file and also to a removed project-guide file, so the guard refuses a correct mention of the operator guide. The documenter worked around it by rewording the link text. Note for the human, no story.
- **The playbook's archive paragraph** opens with a sentence of about 40 words (S0008 reviewer entry 14). The playbook is the human's document. Note.
- **The playbook's older change list and its step 26** still use the archive wording of their time (S0008 documenter entries 5, 8 and 12). History, not rules. Closed.
- **Test names and test-support docstrings that still say `main`:**
  - `red_main` and `push_main` are named in `docs/decisions.md:1235`, `docs/project-guide/README.md:174` and `machine.md` (S0009 documenter entry 18).
  - The human chose not to rename the test functions (S0009 j4).
  - I also found helper docstrings outside S0009's leave that say `main` for the working branch: `tests/support/human_clone.py:22` and `:50`, `tests/support/acceptance_walk.py:109` and `:179`, `tests/support/container_support.py:131` and `:160`, and `tests/support/preflight_support.py:1`, `:174` and `:184`.

  They are of the same kind as the test names the human kept, so this is a note and no story.
- **`make duplicates` reports "6 new, 39 known, 4 gone" after every coder of S0006 to S0009.** S0009's reviewer found four of the six in files the story did not touch (`claude_runtime`/`opencode_runtime`, `folder_readmes`, `cost_records`). Of the other two, the `hand_over`/`acceptance` pair is a known finding listed with its modules in reverse order. So `security/duplicates-baseline.txt`, the human's file, is stale, and every reviewer has to sort that out again. Note for the human.

## 5 The documentation as a whole

I read `README.md`, `docs/operator-guide/` (`install.md`, `work-items.md`, `health.md`), `docs/project-guide/operator.md`, `operator/README.md`, the Kumpel skill's `SKILL.md` and `references/approving.md`, and the playbook's steps 8 and *Finished features*.

The four gaps of F0057-A0001 are closed (S0008). The outcome rule and the reuse are told the same way in `install.md` *The promotion*, `operator/README.md:110-111` and the playbook. Three gaps remain:
- **The project guide does not know Kumpel's archive and promotion.** `docs/project-guide/operator.md`, *The skill's scripts*, lists only `comment.sh` and `reset-to-tag.sh`. It does not name:
  - `archive-feature.sh`, `promote.sh`, or `kumpel-commit.sh`, through which every Kumpel commit names Kumpel (decision 7).
  - In *Test modules by script*: `test_operator_develop.py`, `test_operator_archive_outcome.py` and `test_operator_promote_reuse.py`.
  - Among the helpers: `tests/support/archive_feature_support.py`.

  An agent changing these scripts finds nothing about them in its guide. S0003, S0006 and S0007 each had a docs criterion that named only the operator's documents. Proposed: S0011.
- **An acceptance with proposed stories** (check 2): the playbook's step 8 and `approving.md` step 1 promise an archive and a promotion that the script refuses until the proposed stories and a further acceptance are done. `install.md` *The promotion* does not say it either. Proposed: S0012.
- **`approving.md` step 2** still says `promote.sh` "opens the pull request" and makes no mention of the reuse or of the line `promotion open: #<number>, for the human to merge`. It is not wrong in effect, since Kumpel tells the human the number either way, but it is behind the script. Included in S0012.

No example in these documents runs against changed behaviour. The commands named (`git switch -c develop origin/main`, `/kumpel promote on`, `archive-feature.sh <feature id>`) match the scripts.

## 6 Decisions taken for the human

From `feature.md`, decisions 1 to 9, as listed in F0057-A0001 (accepted by its merge).

From the journals of S0006 to S0009 (the human's answers):
- **S0006 j4:**
  - The leave for `finished_feature` in `test_operator_develop.py`.
  - The coder writes `approving.md`, with a test that step 1 names the refusal.
  - The refused rows also check a clean `develop` checkout.
  - An unclosed front matter and an `outcome: accepted` only in the body are both refused.
  - The earlier refusal texts get rows of their own.
- **S0007 j4:**
  - The leave for `test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on`.
  - The `GET` query parameters are tested.
  - The `PATCH` carries no `title`.
- **S0009 j4:**
  - The `REMOTE` form gets a guard row.
  - Bare `main` locals are left untested, so the reviewer reads them.
  - The `check_story` comment is an untested change.
  - No test function is renamed.
  - The guard keeps three failing rows.

Defaults nobody asked about:
- **S0006:** the front matter is "the block between the first two `---` lines", wherever they stand.
- **S0007:** a reused promotion keeps its first feature's title (`F0001: promoted to main` while it carries F0002). Its merge message names only the last feature.
- **S0007:** criterion 4 in `done/` still says "exits non-zero" while its test pins 22, because the take dropped the coder's rewrite.
- **S0008:** `main` stays the default branch. The Interface left it to the human when refining, and no answer changed it.
- **S0009:** the coder renamed beyond the Interface's list as the guard required: `on_main` became `on_work_branch`, `_follow_main` became `_follow_work_branch`, and `opening.py`'s `_MAIN` became `_WORK_REF`. It also built `hand_over.py`'s branch side from `REMOTE`.

Open for the human:
- **An acceptance that proposes stories defers its feature's archive and promotion** until the stories and a further acceptance are done (check 2). S0012 documents this as it is. The alternative is the human's choice: promote at once, without archiving, since a promotion carries `develop`'s tip anyway (decision 4).
- **The coder is asked to correct the Description but may not write the work item** (check 4). Either the coder's write paths include its own work item outside the front matter and journal, as R14 allows, or its instructions send such corrections to the reviewer.
- From F0057-A0001, still open:
  - `tests/agent_files/test_claude_agent_texts.py:144` forbids `promote` in the agent files.
  - `reset-to-tag.sh` leaves `main` alone.

Earlier tests changed, each with its leave:
- **S0006, `tests/operator_scripts/test_operator_develop.py`:**
  - Under the standing leave: `finished_feature`, `tree` and the feature constants moved to `tests/support/archive_feature_support.py`.
  - Under the human's leave in j4: `ACCEPTANCE` gains `stage: done`/`outcome: accepted`.
- **S0007, `test_operator_develop.py`:**
  - Under the human's leave in j4: `test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on` answers `OPEN_PROMOTION` with `[]`.
  - Under the standing leave: `write_switches`, `requests_that_change`, `PULL_NUMBER` and `OLD_SWITCHES` moved to `tests/support/operator_skill_support.py`.
- **S0008:** none.
- **S0009,** under the human's leave of 2026-11-08 in its Interface (j4):
  - `tests/conftest.py`: the `remote` docstring.
  - `tests/pipeline/application/handlers/test_merged.py`: the module docstring.
  - `tests/pipeline/application/test_repository_waiter.py`: `NO_MAIN` became `NO_WORK_BRANCH`.
  - `tests/pipeline/domain/test_evaluation_due.py`, `test_evaluation_reject.py` and `tests/support/evaluation_support.py`: `main_commit` became `work_commit`.
  - `tests/guards/test_work_branch_search.py` only gained tests.

No earlier test changed without a named leave.

## 7 The slow checks

Nothing beyond `make check` is offered, and `make mutants` is outside this stage (check 3). `make check` ran green here: `test: green (109.6 s)`, coverage 99.22 %, `check: green`. The JUnit report holds 11004 tests summing to 944.0 s, 35 more than at F0057-A0001. The slowest are the ten-second `ROOMY_LIMIT` tests, as designed:
- `tests/machine/adapters/test_podman_timeout_status.py::test_podman_s_timeout_status_at_the_limit_is_a_timed_out_run[255-at-the-limit]` (10.02 s)
- `tests/machine/adapters/test_podman_images.py::test_a_build_that_reaches_its_time_limit_has_not_passed` (10.01 s)

The 44 tests of S0006, S0007 and S0009's new modules take 2.39 s together. The slowest of them is `test_operator_promote_reuse.py::test_promote_adds_the_next_feature_to_the_open_promotion[switch-on]` at 0.21 s.

Disk: now `/srv/factory/vm` has 15.2 GB free and 1.5 GB used. At the previous record, "disk acceptance" (F0057-A0001), it had 15.7 GB free and 1.5 GB used. `/srv/factory/vm/state` and `/tmp` show the same free figure, so they share one pool. Free space fell by 0.5 GB again while the used figure stayed the same; at F0057-A0001 it fell by 0.7 GB, so 1.2 GB over the feature. The feature's changes since F0057-A0001 do not explain it: `git diff --stat` against A0001's merge shows no change to `uv.lock`, `pyproject.toml`, `Makefile` or `operator/vm`. The space goes to something these records do not measure, such as datasets, snapshots or images elsewhere in the pool. This is unexplained and growing, and worth a look by the human.

## 8 Cost

The stories cost 103 runs, 172.6 min, 958 turns and $31.15. S0001 to S0005 were $24.34 of that (69 runs, 133.6 min; see F0057-A0001). The four later stories cost 34 runs, 39.0 min and $6.81:

| Story | Runs | Minutes | Cost |
|---|---|---|---|
| S0006 | 8 | 9.4 | $1.59 |
| S0007 | 11 | 11.9 | $2.24 |
| S0008 | 6 | 5.6 | $0.83 |
| S0009 | 9 | 12.0 | $2.15 |

None stands out against S0003 ($9.68), still the costliest of the feature. Among the four, S0007 cost the most: one review round with two test findings (a copied constant and an exit status checked only as non-zero), which went coder, then tester, then coder. Most of the rest of the later stories' extra runs were stalls:
- S0006's intake stalled once on a criterion number it left behind.
- S0008's docs stage stalled once on the guide-file guard (check 4) and went through one docs-review round with three findings.

The human answered 17 questions, all of cause `question`, and the stories waited 0.6 h in total. 14 of them, and 0.5 h, were S0001 to S0005. The three new ones are one intake question each, in S0006 j4, S0007 j4 and S0009 j4: the intake asked for a leave for an earlier test, or for a criterion where the Interface had a rule without one. S0008 needed no answer. **S0002 still needed the human most over the whole feature** (7 of 17), for the reason F0057-A0001 gives: its narrow Interface had to be widened text by text until the human's j39.

## Proposed stories

- `backlog/F0057-S0010-the-working-branch-s-remote-ref-is-one-constant.md`: `origin/develop` is built in sixteen places, nine of them copies of the same private constant. One `WORK_REF` in `factory.shared.domain.paths` ends the copies, and a guard keeps them out.
- `backlog/F0057-S0011-the-project-guide-names-kumpel-s-archive-and-promotion.md`: `docs/project-guide/operator.md` does not name `archive-feature.sh`, `promote.sh`, `kumpel-commit.sh`, their three test modules or their test helper.
- `backlog/F0057-S0012-kumpel-s-procedure-after-an-acceptance-that-proposes-stories.md`: after an accepted acceptance that proposed stories, the archive refuses and the promotion waits. The playbook, `install.md` and `approving.md` promise otherwise, and `approving.md` step 2 does not know the reuse.

## Journal

1. factory: started acceptance as vm.
2. acceptance-reviewer: accepted with stories; 3 stories proposed (F0057-S0010 to S0012)

   1 Scope: none. The scope lines of S0001 to S0005 still hold. S0006 to S0009 came from the first acceptance's proposals and stay within the feature's Kumpel and documents scope. Out of scope was respected. Protecting `main` and the first promotion are the human's acts, which I cannot see from the repository.
   2 Feature smoke test: green, 3 passed. A new project waits for `develop`. A merged story is archived on `develop` and `main` does not move. Kumpel refuses to archive a refused feature and archives an accepted one as Kumpel. It opens one promotion, adds the next feature to it with `PATCH` (one `POST` in all), and merges it with a merge commit only when the switch is on. After an acceptance that proposed stories, the archive refuses ("is in backlog/") and the promotion waits, which the playbook and `approving.md` do not say (→ S0012).
   3 Mutation testing: by sweep, not run here.
   4 Noticed: `origin/develop` is built in 16 places, nine of them copies of the same `_WORK_REF` constant (→ S0010). The take drops the coder's corrections to the Description (S0007, S0009). The guide-file guard refuses the bare name `work-items.md`. `make duplicates` reports stale new findings every time. The front-matter and `null`-body edge cases, and the test-support docstrings that still say `main`, are notes with no story.
   5 Documentation: the four gaps from A0001 are closed. `docs/project-guide/operator.md` does not name `archive-feature.sh`, `promote.sh`, `kumpel-commit.sh` or their tests and test helper (→ S0011). The playbook, `install.md` and `approving.md` promise an archive and a promotion that an acceptance with proposed stories defers, and `approving.md` step 2 does not mention reusing an open promotion (→ S0012).
   6 Decisions: the human's answers in S0006 j4, S0007 j4 and S0009 j4. Defaults nobody asked about: a reused promotion keeps its first feature's title; criterion 4 of S0007 still says "exits non-zero"; `main` stays the default branch; S0009 renamed beyond its list. Open for the human: whether an acceptance that proposes stories should defer the promotion, and the coder's missing write path for Description corrections. Every earlier test change names its leave.
   7 Slow checks: nothing beyond `make check`, which is green (`test: green (109.6 s)`, 99.22 %, 11004 tests). The slowest are the 10 s `ROOMY_LIMIT` tests. Free disk fell another 0.5 GB with used space unchanged (1.2 GB over the feature). No dependency or image change explains it.
   8 Cost: $31.15 over 103 runs. S0006 to S0009 cost $6.81 over 34 runs, and S0007 the most of them ($2.24, one review round). S0003 is still the costliest of the feature ($9.68). 17 questions were answered and the stories waited 0.6 h; the 3 new questions were one intake question each in S0006, S0007 and S0009. S0002 needed the human most (7 questions).
