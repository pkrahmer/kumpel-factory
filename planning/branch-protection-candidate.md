# Candidate: Kumpel works under branch protection on main

Written 2026-11-07 from the code on `main` (47f1df69f) and the operator skill. Nothing was changed. The aim is a protected `main`: "Require a pull request before merging", no direct pushes.

## 1. Every direct write to main

### The factory (pushed by the factory process with the hosting token, author `factory`)

All five go through `WorkItemRecorder.publish(MAIN_BRANCH, ...)` in `src/factory/pipeline/application/handlers/recording.py`, which commits and calls `push_with_retries`.

| # | Where | Commit subject | What it writes | Why on main |
| :-- | :-- | :-- | :-- | :-- |
| F1 | `pipeline/application/handlers/merged.py` | `work item <id>: merged, archived` | Moves the story from `in-progress/` to `done/` with its cost records, adds the `done` entry with the bill, sets the stage to done. Then deletes the branch. | The board, the next story and the feature's acceptance read the story's place on `origin/main`. `merge.sh` and `start_next` wait for this commit. |
| F2 | `pipeline/application/handlers/closed.py` (`_discard`) | `work item <id>: closed before the approval, back in the backlog` | Moves the story file back to `backlog/`. | A close before approval discards the work; main must show the story as not started. |
| F3 | `work/application/acceptance.py` (`AcceptanceMerged._book`) | `work item <id>: merged, archived` | Moves the acceptance report to `done/` with its bill. | The feature is complete only when its acceptance is in `done/` on main. |
| F4 | `work/application/acceptance.py` (`AcceptanceClosed._book`) | `work item <id>: closed, refused` | Writes the refused report under `done/`. | Same: the refusal must count for the feature. |
| F5 | `pipeline/application/stops.py` (`StopPublisher`, called each tick by `tick.py`) | `stops recorded` | Appends raised and cleared stops to `factory/stops.jsonl`. | The stops' history is shared and survives a machine; `stops.py` reads it back from `origin/main`. |

Everything else the factory pushes goes to a `work-item/...` branch, which is unaffected: claims (`claims.py`), stage results (`stage.py`), answers and questions (`handlers/comments.py`, `handlers/questions.py`), recovery and stalls, the hand-over, and the opening of an acceptance (`acceptance.py` `open`, a new branch from `origin/main`). Disk records and the take's candidate lists stay on the machine and are not pushed.

### Kumpel, the operator skill (the human's token, author Kumpel or the human)

| # | Where | What it writes | Why on main |
| :-- | :-- | :-- | :-- |
| K1 | `scripts/start-story.sh` | `<id>: start`: moves the story from `backlog/` to `in-progress/`. | The factory starts a story when it finds it in `in-progress/` on `origin/main`. |
| K2 | `references/standing-orders.md`, *The log* | `.kumpel/log/<UTC date>.md`, one line per act, committed with the act's files or alone (`operator log: ...`). | The trail of what Kumpel did and why, next to the files it changed. |
| K3 | `references/answering.md` (lines 10, 17), `approving.md` (line 20), `shaping.md` (line 18) | Small fixes on main: files outside every role's write paths (`pyproject.toml`'s ignores, `.secrets.baseline`, `security/`), a document slip after a merge, a correction to a story still in `backlog/`, and new features and stories. | A fix the stage needs at its next start, or a fix too small for a round. |
| K4 | `docs/operator-playbook.md`, line 203 (by hand today, by the human or Kumpel) | Moves a finished feature's folder to `factory/archive/`. | The factory reads only `factory/features/`. |
| K5 | `scripts/reset-to-tag.sh` | Moves `main` to a tag's commit by force (`PATCH /git/refs/heads/main`, `force: true`). | Repeats a trial on the site's trial repository. |

`scripts/merge.sh` merges through the API (`PUT /pulls/<n>/merge`). That is a pull request merge and stays allowed.

## 2. What breaks under "require a pull request before merging"

- **F1, F3 (the archive after a merge):** the push is refused. As `docs/operator-guide/work-items.md` (line 155) describes for a rejected archive push, nothing is archived and the branch is kept, and the next tick tries again, so it fails on every tick. The story stays in `in-progress/` on main. `merge.sh` waits for the archive commit forever, `start_next` never fires, and the feature never becomes due for its acceptance. **The whole cycle stops after the first merge.**
- **F2, F4 (closes):** the discard or the refusal never reaches main. The story stays shown as in progress, and the feature cannot complete.
- **F5 (stops):** the records stay on the machine, retried on every tick. The stops still work locally, but their shared history and the Timeline's reading of it are lost.
- **K1 (start):** no story can start at all.
- **K2 (log):** each log commit is refused. Because the log is committed together with the act's files, the act's own commit fails with it.
- **K3, K4:** each needs its own pull request. That is the intent of the protection, not a break, but the skill's texts say "on `main` yourself".
- **K5:** also needs the force-push rule lifted. It is meant for a trial repository, which can stay unprotected.
- **Approvals:** if the rule also requires one approving review, nothing can merge, because the factory, Kumpel and the human all use **one identity** (the human's token). GitHub does not let an author approve their own pull request (already found on 2026-10-05). Only "require a pull request" with zero required approvals works with one identity.

**Would a bypass for the factory's token be needed?** For F1 to F5, yes, unless the factory changes how it records (option B or C below). But today the factory's token is the human's token. A bypass for it is a bypass for the human, so the protection would protect nothing. Any bypass first needs **a separate identity for the factory**.

## 3. Designs, weighed

**A. A separate factory identity with a bypass (recommended).** The factory pushes with its own identity, and that identity alone may push to `main`. Its five commits stay as they are today. Kumpel and the human go through pull requests.
- Trail: better than today. Main's history separates the factory's mechanical commits from the human's merges, where today all of them are one account.
- Approvals: the factory's pull requests would come from its own identity, so the human could approve them. That makes a required review possible later.
- Code: none for F1 to F5. Only the identity changes.
- **To verify first:** which identities a ruleset on a user-owned repository may name as bypass actors. A GitHub App or a deploy key is likely possible; a second user is likely not, and the "repository admin" role would include the human. This is one probe on a trial repository.
- Risk: the bypass identity can push anything to main, not only records. A GitHub App with contents permission on this one repository keeps that narrow, and push rules for file paths (if the plan offers them) could narrow it further.

**B. Everything through pull requests, no bypass.** The factory opens a small pull request for each archive, close and stop record, and merges it itself. Kumpel does the same for starts.
- Trail: complete, but noisy. There would be about three pull requests per story instead of one, and a merge conflict between two small pull requests would become a new failure mode.
- Code: large. Every `publish(MAIN_BRANCH)` becomes open, wait and merge, and every reader that waits for the archive commit must wait for a merge instead.
- It works only with zero required approvals, unless A's identity exists too.

**C. Records move off main.** Stop records (F5) and Kumpel's log (K2) move to an unprotected branch, for example `factory/records` and `kumpel/log`, written as today. The archive of a story is written on its own branch at the approval stage, so that the merge itself archives it and F1 needs no commit after the merge.
- Trail: kept, but in two places. The archive-before-merge changes what a close after approval must undo.
- Code: medium. It also changes what "done" means before the merge.

**Recommendation:** A for the factory (F1 to F5), with pull requests for Kumpel's and the human's own writes (K1, K3, K4), and C's log branch for K2. A pull request per log line would bury the real ones. K5 stays for unprotected trial repositories only.

## 4. Candidate feature: "Kumpel works under a protected main"

Before it starts: the human's probe on a trial repository (`pkrahmer/factory-demo` or a new one). Add a ruleset "require a pull request, zero approvals", then try a bypass for a GitHub App and for a deploy key with one push each. Write down which works on a user-owned repository.

Stories, if the probe confirms A:

- **S1. The factory may push with an identity of its own.** Today the token file holds the human's token. The factory must accept a GitHub App installation, or the identity the probe allows, for its git pushes and its API calls, and refresh a token that expires. The preflight checks that the identity can push to `main`, and the operator guide's *The hosting-service token* says how to set it up. Clear once the probe names the identity kind. With a deploy key, the git side changes to SSH, while the API side keeps a token.
- **S2. Kumpel starts a story through a pull request.** `start-story.sh` pushes the move to a `kumpel/start-<id>` branch, opens a pull request, and merges it with `merge.sh`'s message form. `next-story.sh` and `wait.sh` keep reading `main`. Clear.
- **S3. Kumpel's log lives on its own branch.** `.kumpel/log/<date>.md` is committed to an unprotected `kumpel/log` branch. The act's own files go into the act's pull request. `standing-orders.md`, *The log*, says where the log is read. Clear.
- **S4. Kumpel's fixes on main become pull requests.** `answering.md`, `approving.md` and `shaping.md` say "open a pull request and merge it" instead of "on `main` yourself", and the stage merges `origin/main` at its next start as today. Clear; text only.
- **S5. The factory moves a finished feature to the archive.** After a feature's last acceptance is booked (F3), the factory moves the feature's folder to `factory/archive/` in the same commit. This removes the manual K4 and its pull request. Optional, but it closes the last human write that the protection would otherwise make a pull request.
- **Docs, in each story:** `docs/operator-guide/` (the token, the stops file, what needs a protected main), `operator/README.md` and the playbook's archive rule. `reset-to-tag.sh` says that it needs an unprotected repository.

If the probe shows no bypass actor that fits a user-owned repository, the choice is B, or moving the repository to an organisation, where a team or an App can be named. That is the human's decision.
