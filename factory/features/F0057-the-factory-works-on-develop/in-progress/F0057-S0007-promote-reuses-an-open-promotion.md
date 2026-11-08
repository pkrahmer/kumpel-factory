---
stage: doing
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: 650
comments_read: [6716086925]
handed_over: null
claim:
  instance: vm
  stage: doing
  started_at: '2026-11-08T02:20:58.296499Z'
  lease_duration: 60
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-08T02:16:31.512122Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-08T02:16:31.520234Z'
  stage: intake
- number: 3
  speaker: intake
  kind: question
  at: '2026-11-08T02:16:48.532578Z'
  stage: intake
  run: 40a8811e5a60492ab15f3efd03e88684
  blocked: question
- number: 4
  speaker: human
  kind: comment
  at: '2026-11-08T02:18:37.663661Z'
  stage: intake
- number: 5
  speaker: factory
  kind: started
  at: '2026-11-08T02:18:40.055174Z'
  stage: intake
- number: 6
  speaker: intake
  kind: result
  at: '2026-11-08T02:19:00.111456Z'
  stage: intake
  run: 022fac1620484f3e9c3b769fee6272d0
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-08T02:19:07.772920Z'
  stage: tests
- number: 8
  speaker: tester
  kind: result
  at: '2026-11-08T02:20:53.337784Z'
  stage: tests
  run: a69a5b7f309f44cf915e3ddd96fda161
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-08T02:20:58.296499Z'
  stage: doing
---

# promote.sh reuses an open promotion

<!-- proposed by feature acceptance of 2026-11-08; refine before starting -->

## Description

`operator/skill/kumpel/scripts/promote.sh` always opens a new pull request from `develop` to `main`. With the switch `promote` off, the human merges that pull request at their own pace. When `promote.sh` runs again while it is open, the hosting service refuses a second open pull request for the same head and base (GitHub answers 422), and the script stops with `hosting: POST ...: 422`. That happens when the human turns the switch on and Kumpel promotes, or when a next feature is accepted first (F0057-A0001, smoke test). A promotion carries `develop`'s tip (F0057 decision 4), so the open pull request already holds the new feature's commits. This story makes `promote.sh` find an open promotion and reuse it: it adds the feature's stories to its body, and then merges it or prints its number as today. The title, the merge method and the refusal of a feature that is not archived stay as they are.

## Interface

- `operator/skill/kumpel/scripts/promote.sh <feature id>`, after the archive check:
  - It asks for the open promotion with `GET /repos/<repository>/pulls?state=open&base=main&head=<owner>:develop&per_page=1`. `<owner>` is the part of `SITE_REPOSITORY` before its `/`.
  - **None open:** it opens one with `POST /pulls` as today, same title and body.
  - **One open:** no `POST`. It sends `PATCH /pulls/<number>` with a `body` equal to the open pull request's body, a blank line, and the new feature's block `The stories of <id>:` followed by its story lines, as today. The title stays.
  - **When the feature's block is already in the body** (a rerun for the same feature), no `PATCH` is sent.
  - Then, in every case: with the switch on it merges `<number>` with `merge_method: merge` and the message `Promoted by Kumpel after <id>'s acceptance.`, as today. With the switch off it prints `promotion opened: #<number>, for the human to merge` for a new one and `promotion open: #<number>, for the human to merge` for a reused one.
- A failed `GET` stops the script with the hosting client's message and exit status, and nothing is opened.
- Tests: a new module `tests/operator_scripts/test_operator_promote_reuse.py` with the `curl` stand-in.
- The human's leave (journal entry 4): `tests/operator_scripts/test_operator_develop.py::test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on` answers the new `GET` route with an empty list, so far as the new request requires. It keeps its name and what it checks.

## Acceptance criteria

1. With no open promotion (the `GET` answers `[]`), `promote.sh F0001` sends `POST /pulls` with the title and body of today. With the switch off it prints `promotion opened: #4711, for the human to merge`. The stand-in also sees the `GET /repos/<repository>/pulls` with the query parameters `state=open`, `base=main`, `head=<owner>:develop` (`<owner>` the part of `SITE_REPOSITORY` before its `/`) and `per_page=1` (one test).
2. With an open promotion #4711 whose body lists F0001's stories, `promote.sh F0002` sends no `POST`. It sends one `PATCH /pulls/4711` whose body is the old body, a blank line and F0002's block, and which carries no `title`. The rows of one test:
   - Switch off: it prints `promotion open: #4711, for the human to merge`.
   - Switch on: it then sends `PUT /pulls/4711/merge` with `merge_method: merge` and `Promoted by Kumpel after F0002's acceptance.`.
3. With an open promotion #4711 whose body already holds F0001's block, `promote.sh F0001` sends neither `POST` nor `PATCH`, and with the switch off prints `promotion open: #4711, for the human to merge` (one test).
4. When the `GET` fails with 500, `promote.sh` exits non-zero, prints `hosting: GET ...: 500 ...` on stderr and sends no `POST`, `PATCH` or `PUT` (one test).
5. `make check` stays green.
6. docs: `operator/README.md` and `docs/operator-guide/install.md` (*The promotion*) say that a promotion still open is reused and gains the next feature's stories; `docs/decisions.md`: none.

## Smoke test

```bash
uv run pytest tests/operator_scripts/test_operator_promote_reuse.py 2>&1 | tail -1
```
Expect: a line ending in `passed in <seconds>s` with no `failed`.

## Journal

1. 2026-11-08 human: created.
2. factory: started intake as vm.
3. intake: Questions before this story can be accepted. The format check passed.

   1. The Interface changes a test another story wrote: `tests/operator_scripts/test_operator_develop.py::test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on` must answer the new `GET` route with an empty list. The line says the leave is "to be given when refining", and the journal holds no answer from the human. Do you give the leave for exactly that change (the test keeps its name and what it checks)? I would choose yes. Without your word the tester cannot touch that test, and the old test would fail on the new `GET`.

   2. The Interface fixes the `GET` request: `state=open&base=main&head=<owner>:develop&per_page=1`, with `<owner>` taken from `SITE_REPOSITORY`. No criterion tests it. Criteria 1 to 4 would also pass if a coder queried a different base or head, or took the wrong owner. Please add a criterion that the stand-in sees the `GET` with those query parameters and the owner from `SITE_REPOSITORY`. I would add it to criterion 1's test.

   3. The Interface says "The title stays" on reuse, and no criterion tests it. Criterion 2 only checks the `PATCH` body. Please add that the `PATCH` sends no `title`, or that it sends the open title unchanged. I would choose "no `title` in the `PATCH`". Add it to criterion 2.
4. 2026-11-08 human: 1. Yes, that leave, exactly that change.
   2. Yes, in criterion 1's test.
   3. Yes: no `title` in the PATCH, in criterion 2.
5. factory: started intake as vm.
6. intake: accepted
   - Interface: names `operator/skill/kumpel/scripts/promote.sh <feature id>`, the exact GET route and the PATCH/POST/PUT requests, the printed lines, the new test module. Human's leave (journal entry 4) for the one old test in `test_operator_develop.py`; I changed the Interface line from "to be given when refining" to "(journal entry 4)".
   - Criteria: carried in from the human's answer (journal entry 4): criterion 1 now also checks the GET query parameters and the owner from `SITE_REPOSITORY` (answer 2); criterion 2 now has the PATCH carry no `title` (answer 3). Each criterion is one test or one parametrized test. Both sides of each rule are covered: no promotion open, one open, block already present, GET failure.
   - Smoke test: runs pytest without `-q`, which is right because `addopts` already sets it. The `Expect:` line (ends in `passed in <seconds>s`, no `failed`) is checkable.
   - Docs criterion: names the two documents and what the reader must know (an open promotion is reused and gains the next feature's stories). It dictates no sentences.
   - Architecture: the change is in the operator's script and its tests under `tests/operator_scripts/`, which fits the project layout.
   - Scope: within F0057's Kumpel promotion (S0003, decisions 3 to 5). It is not in "Out of scope". The route is `tests`, because the Interface changes a script and a test.
7. factory: started tests as vm.
8. tester: Wrote the tests of `promote.sh` reusing an open promotion. They fail as intended: all 5 new rows fail because the script still sends `POST /pulls` and prints "promotion opened"/"promoted". The changed old test still passes. `make lint` is green.

   Each criterion and its test:
   - criterion 1: tests/operator_scripts/test_operator_promote_reuse.py::test_promote_without_an_open_promotion_asks_for_it_and_opens_one. It checks one GET `/pulls` with `state=open`, `base=main`, `head=owner:develop` and `per_page=1`, compared with parse_qs. It checks one POST `/pulls` with today's head, base, title and body, and the line `promotion opened: #4711, …`.
   - criterion 2: tests/operator_scripts/test_operator_promote_reuse.py::test_promote_adds_the_next_feature_to_the_open_promotion, with rows switch-off and switch-on. It checks that no POST is sent and that one PATCH `/pulls/4711` is sent whose body is the old body, `\n\n` and F0002's block, with no `title`. With the switch off it checks `promotion open: #4711, …`. With the switch on it checks PUT `/pulls/4711/merge` with `merge_method: merge` and the message for F0002.
   - criterion 3: tests/operator_scripts/test_operator_promote_reuse.py::test_promote_again_for_a_feature_already_in_the_open_promotion_changes_nothing
   - criterion 4: tests/operator_scripts/test_operator_promote_reuse.py::test_promote_stops_when_the_query_for_the_open_promotion_fails. The switch is on. It checks a non-zero exit, `hosting: GET <route>: 500 ` on stderr, and that no POST, PATCH or PUT is sent.
   - criteria 5 and 6 (make check, docs) have no test.

   Files:
   - Created: tests/operator_scripts/test_operator_promote_reuse.py.
   - Changed under the human's leave (journal entry 4): tests/operator_scripts/test_operator_develop.py::test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on now answers the `OPEN_PROMOTION` route with `[]`. Its name and what it checks are unchanged.
   - Changed under the standing leave to move shared test helpers: `write_switches` and `requests_that_change` moved from tests/operator_scripts/test_operator_develop.py to tests/support/operator_skill_support.py, and test_operator_develop.py now imports them from there.
   - Added to tests/support/operator_skill_support.py: the constant `OPEN_PROMOTION`. It is the GET route with the query in the Interface's order, and the owner comes from `REPOSITORY` (`owner/repo`).

   Notes for the coder:
   - The curl stand-in matches an answer on the exact path with its query, or on the bare path. So the script's GET must use the query string exactly as the Interface gives it, in that order and with the colon not encoded. Otherwise the GET gets the POST's answer.
   - No module was left unimported. The code under test is a shell script.

   Open: nothing.

   `lint`: lint: green (0.1 s)
9. factory: started doing as vm.
