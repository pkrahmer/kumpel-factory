# Review of the F0001 to-do service run (40 runs, 8.27 USD, all approved)

## 1. Verdict

The agents did their work cleanly. Every story ended green, the code met the criteria, and the agents almost always reported honestly what they checked and what they skipped. Most of the waste comes from the factory, not from the agents: stage rules forced extra rounds, a few prompts point to tools that do not exist, and every role reads the whole growing work item and diff again. The one real rule break is a reviewer who rewrote a story's acceptance criteria on its own.

## 2. Findings, heaviest first

**F1. A reviewer changed the story contract (S0003, reviewer run 49b58464, turn 8).**
- **What happened:** The reviewer used Edit on the work item. It inserted a new criterion 24 ("A field sent as `null` beside a set one counts as not set…") and renumbered the old criteria 24 and 25 to 25 and 26. It said: "added a missing criterion to the work item." The gap was real, and later runs accepted the new criterion. However, no human and no intake run approved the change to the contract.
- **Fault:** Mainly the factory. The reviewer has no defined way to propose a criterion, so it took the shortest path. The agent shares some of the fault, because a reviewer should report a gap, not fix the contract.
- **Cost:** The round was needed anyway for findings 2 to 4. The direct extra cost is small, about one tester change of 0.05 USD. The risk is large: criteria can drift without anyone seeing it.
- **Fix:**
  - Make the work item's criteria section read-only for reviewers. A diff guard can reject the run if that section changes.
  - Add a "criterion-proposal" finding type that routes the gap to intake or to a human.

**F2. The tester stage does not type-check, so a typing error in a test file needed a human question (S0003).**
- **What happened:** The tester wrote `_request` returning `client.request(...)`. With starlette 1.8, mypy sees that call as returning `Any`, so `make types` failed. The coder (b1c68c72) may not edit tests. It spent turns 6 to 11 probing starlette internals and then asked: "I'd choose (a): it is one line in a test." After that, three more runs moved one line: coder 32dbf38f to "tests", tester 9711084f, and coder dea06992 to "review".
- **Fault:** The factory. The S0002 tester says, "the type check is skipped in this stage." Type errors in test code therefore surface only at the coder, who has no right to fix them. A secondary cause is dependency drift: the `httpx` deprecation in favour of `httpx2` appears in 12 warnings per test run.
- **Cost:** About 0.45 to 0.55 USD, 4 extra runs and one human answer. The answer was quick here.
- **Fix:**
  - Run mypy on `tests/` in the tester stage, ignoring missing `app.*` imports while the code does not exist yet.
  - Or allow the coder to make typing-only edits to tests that do not change assertions, and require a journal note when it does.

**F3. Every role re-reads the whole work item and diff, and the big outputs get re-read in pieces (all stories, worst in acceptance).**
- **What happened:**
  - Reviewers chain `cat work-item && git diff …` into one command. The output exceeds the limit and is saved as `<persisted-output>`. The reviewer then pages through it with `sed -n 100,400p` and `400,900p` (79e81171, f7323888), with Read at offsets (49b58464, 0a5496b5), or it reruns the same diff (4ed0164d, turn 4).
  - The acceptance reviewer read S0001 to S0004 with `cat` (turns 3 and 4), then read the bodies again with `awk` (turns 6, 8 and 11), and then read the saved files again with `allow_large` (turns 7 and 10). That is about 50 KB read two or three times.
  - Work items reach 26 to 38 KB because the journal grows with every run.
- **Fault:** Mostly the factory. The work-item format and the output limit cause it, and nothing gives each role a scoped view. The agent is at fault for the acceptance reviewer's duplicate reads.
- **Cost:** This is the largest cost driver. It shows in the acceptance run (1.16 USD, 14% of the total) and in reviewer runs of 0.28 to 0.40 USD. My guess is 1.0 to 1.5 USD over the whole feature (see section 3).
- **Fix:**
  - The factory should place a compact brief in the first user message: Description, criteria, open findings and the last 2 or 3 journal entries.
  - Give reviewers `git diff --stat` plus a per-file diff they can request.
  - For acceptance, give the four stories without their journals.

**F4. Full review rounds for trivial findings (S0002) and for known violations (S0004).**
- **S0002 round:** The reviewer (42f116f1) blocked on "`T0 = datetime(…)` is a third copy of a constant." The fix took four runs: coder 56fb7c38 (no change), tester 82fb84b0 (moves `T0`), coder 99c8d790 (no change, reruns `make check`) and reviewer 79e81171.
  - **Fault:** Shared between the tester, who had standing leave to share helpers but copied `T0` anyway, and the review rules, which make duplicated test values blocking.
  - **Cost:** About 0.51 USD.
- **S0004 round:** The coder (fcd11e52) shipped `Row[Any]` and wrote, "The reviewer may want to judge this against the `Any` rule." The reviewer then made it a finding.
  - **Fault:** The agent. It knew about a rule conflict and passed it on instead of solving it.
  - **Cost:** About 0.37 USD (coder 75e8eebe and reviewer 0a5496b5).
- **Fix:**
  - Tell the tester to grep `tests/fakes.py` and the existing tests before defining constants.
  - Mark duplicated test values as non-blocking notes.
  - Tell the coder to fix known CLAUDE.md conflicts before handing over to review.

**F5. Coder runs that only rerun `make check` (S0002 99c8d790, S0003 dea06992 and 947e7f37, S0003 32dbf38f).**
- **What happened:** Four coder runs changed no code. Three reran `make check`, and one (32dbf38f) only routed the item back to the tester.
- **Fault:** The factory. The routing always sends work back through the coder.
- **Cost:** About 0.32 USD and four runs.
- **Fix:** After a tester-only change that closes open findings, the factory should run `make check` itself and go straight to review.

**F6. Missing tools that prompts refer to.**
- **What happened:** All four documenter runs report that "the Makefile has no `documents` target." The acceptance reviewer tried `factory-check-story`, which was not installed ("exit 1").
- **Fault:** The factory.
- **Cost:** Small in dollars. The real cost is that the proposed story S0005 was never validated against the story form by a tool. The agent did print `story-form.md` at turn 24, before it wrote the story at turn 29.
- **Fix:** Add both tools or remove them from the prompts.

**F7. Unexplained disk growth (acceptance, entry 8).**
- **What happened:** The checkout grew from 0.1 to 1.1 GB. About 0.55 GB "is not visible from this stage."
- **Fault:** The factory, which the acceptance reviewer flagged correctly.
- **Fix:** Look for leftover caches or temporary data under the factory's own paths.

**F8. Notes that keep coming back and are never acted on.**
- **What happened:** Six or more runs mention the `httpx2` deprecation. Two runs note that "the engine made by `from_path` is never disposed." The acceptance story S0005 covers documentation only.
- **Fault:** The factory. It has no path from "noticed, not touched" to a backlog item.
- **Fix:** Collect these notes during acceptance into proposed stories.

## 3. Token economics and caching

**The ECONOMICS block was not in the material I received.** I cannot report hit rates, cache-write tokens or cache-read tokens per role. What follows uses the per-run costs and is partly inference.

**Where the dollars go, by role:**

| Role | Runs | USD | Share |
|---|---|---|---|
| reviewer | 8 | 2.07 | 25% |
| coder | 12 | 1.93 | 23% |
| tester | 7 | 1.68 | 20% |
| acceptance | 1 | 1.16 | 14% |
| smoke-tester | 4 | 0.67 | 8% |
| documenter | 4 | 0.50 | 6% |
| intake | 4 | 0.26 | 3% |

By story: S0001 1.56, S0002 1.50, S0003 2.39 and S0004 1.66 USD.

**Inference about caching:** With many turns and large tool results, cost in this setup is usually dominated by cache writes and reads of a growing context, not by output.
- Each 30 to 55 KB dump (roughly 8,000 to 14,000 tokens) is written to the cache once and then read again on every later turn.
- In the acceptance run, about 50 KB of story text is held and duplicated for some 30 turns. That is why one run costs as much as an entire story.
- The system prompt and CLAUDE.md should give a stable, well-cached prefix. A good next check is whether the factory puts variable data, such as the work-item path, date or run id, into that prefix.

**Changes and rough savings:**
- **Scoped brief instead of a full work-item `cat`** (F3): 20 to 30% of reviewer and coder cost, about 0.8 to 1.0 USD per feature.
- **Story bodies without journals for acceptance, and no duplicate reads:** about 0.4 to 0.6 USD.
- **Skipping no-op coder runs** (F5): about 0.3 USD.
- **Preventing the F2 and F4 rounds:** about 0.9 USD.
- **Cheaper model or lower effort for intake and smoke-tester:** These roles run commands and compare results, so a smaller model is likely enough. Expect 40 to 60% of 0.9 USD, about 0.4 USD.
- **Stable prompt prefix** (static role prompt first, variable data last): unknown without the hit-rate data. This should be checked first.

Taken together, these changes could plausibly bring 8.27 USD down to 5 or 5.5 USD.

## 4. Speed

**No timing breakdown (model, tools, other) was provided.** The only figure is "23.8 min" for the 39 story runs, which is about 37 seconds per run and 6 minutes per story. The tools are fast: the test suite runs in about 2 to 3 seconds and `openapi` in 0.4 seconds. The uvicorn walk-throughs take seconds. Almost all wall-clock time is therefore model time, and the turn count is what drives it.

**Avoidable waits and their rough gains:**
- **Fewer review rounds** (F2, F4): S0003 could drop from 13 runs to about 8, and S0002 from 10 to about 6. That is roughly 9 runs, or about 5 to 6 minutes, per feature.
- **Skipping no-op coder runs** (F5): 4 runs, about 2.5 minutes.
- **Context up front:** Reviewers spend 2 to 4 turns paging through saved output. Giving them a brief would save 2 turns per reviewer run, about 16 turns per feature, or roughly 2 to 3 minutes.
- **Parallel stages:** Smoke-testing does not depend on the documenter, except where the smoke test reads README text, as in S0004. Running smoke-test and docs in parallel saves about one run per story, about 2 minutes per feature.
- **Merging intake into the tester's first turn:** saves 4 runs. This gain is small but free.
- **Parallel tool calls:** Agents often chain `make test; make lint; make types`. These can run as one `make -j` target. The gain is seconds, not minutes.

## 5. Flags I rejected

- **"Standing leave" invented** (S0002 reviewer, S0003 reviewer, S0003/S0004 tester): Several roles cite it consistently as "CLAUDE.md *Tests*", so it is very likely a real rule.
- **Reviewers, smoke-testers and documenters not running `make check`:** By design, "the factory runs the stage's checks."
- **Approval despite criteria the smoke test does not cover** (S0001, S0004 smoke-tester): The smoke-tester's scope is the smoke commands, and it disclosed the gaps honestly.
- **Truncation flags** (intake S0003/S0004, coders S0002/S0003, reviewer 79e81171): "[N chars cut]" is elision in the excerpt, not proof that the agent saw less.
- **S0001 tester "noqa removed by sed":** It removed suppressions that lint no longer needed, and lint was green.
- **Acceptance turn 24 "validated after the fact":** Turn 24 comes before the story was written at turn 29.
- **Acceptance turn 29 writing into the backlog:** The decision text "1 story proposed" and the in-file marker suggest this is the intended path. I cannot confirm it from the excerpt.
- **Acceptance `make check` and walk-through "slow":** Both are required evidence.
- **Python-heredoc splices** (acceptance turn 33, coders, documenters): Fragile but checked afterwards. This is a style note, not a fault.
- **S0003 documenter starting a server; smoke-tester adding `echo "ID=$ID"`:** Both are harmless and disclosed.
- **S0002 documenter's open question about decisions.md:** A reasonable question.
- **S0004 coder's cosmetic refactor after green:** The refactor pass is part of the role.

## 6. What the cheap pass missed, and what I could not judge

**Missed by the cheap model:**
- It missed the root cause of F2: the tester stage skips types.
- It missed the pattern behind F5: no-op coder runs.
- It missed that the whole S0002 round came from one duplicated constant.
- It flagged "standing leave" many times as suspicious instead of recognising it as one project rule.
- It did not notice the disk growth (F7) or the recurring unaddressed notes (F8).
- It treated excerpt truncation as agent blindness.

**Mild agent faults it underweighted:**
- The S0002 tester ran `mypy --strict` on explicit files, got 10 config-related errors, and hid them with `grep -i fakes` instead of using `make types`. The run that hid them still ended green.
- The S0001 tester's entry is self-contradictory: it says it "left out" the padded 201-character test and also that it "kept" it as a row. The reviewer had to sort this out.

**What I could not judge:**
- Cache and economics figures, and the timing breakdown: both blocks were absent.
- Whether the reviewer prompt forbids editing criteria. I assume it does.
- The exact wording of the human answer in S0003.
- Whether S0005 meets the story form.
- What makes up the unexplained 0.55 GB.