---
stage: intake
blocked: null
round: 0
attempts: 0
crashes: 0
pull_request: null
comments_read: []
handed_over: null
claim:
  instance: vm
  stage: intake
  started_at: '2026-11-08T02:16:31.520234Z'
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
- The human's leave, to be given when refining: `tests/operator_scripts/test_operator_develop.py::test_promote_opens_the_promotion_and_merges_it_only_with_the_switch_on` answers the new `GET` route with an empty list, so far as the new request requires. It keeps its name and what it checks.

## Acceptance criteria

1. With no open promotion (the `GET` answers `[]`), `promote.sh F0001` sends `POST /pulls` with the title and body of today. With the switch off it prints `promotion opened: #4711, for the human to merge` (one test).
2. With an open promotion #4711 whose body lists F0001's stories, `promote.sh F0002` sends no `POST`. It sends one `PATCH /pulls/4711` whose body is the old body, a blank line and F0002's block. The rows of one test:
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
