# Kumpel's procedure after an acceptance that proposes stories


## Description

An acceptance merged as "accepted with stories" leaves its proposed stories in the feature's `backlog/`. `archive-feature.sh` then refuses with `<id> is not finished: <path> is in backlog/`. `promote.sh` refuses a feature that is not archived, so the promotion waits until the proposed stories are done and a further acceptance is merged. That is what happened to F0057 after its first acceptance, and its second acceptance's smoke test showed it.

The documents say otherwise:
- `docs/operator-playbook.md`, step 8, archives and promotes right after an accepted feature and only then turns to the proposed stories.
- `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance*, step 1 makes Kumpel report the refusal to the human as a fault.
- Its step 2 does not know that `promote.sh` reuses an open promotion and then prints `promotion open: #<number>, for the human to merge`.
- `docs/operator-guide/install.md`, *The promotion*, does not say when the promotion waits.

This story brings Kumpel's procedure and the operator's documents in line with the scripts. It changes no script. Whether a feature accepted with stories should be promoted at once, without archiving, is the human's choice when refining. Unless the human chooses that, the story describes the behaviour as it is.

## Interface

- `operator/skill/kumpel/references/approving.md`, *After a feature's acceptance* (the coder writes it; `operator/skill/*` is its path):
  - **Step 1:** when the accepted acceptance proposed stories, so that the feature's `backlog/` holds them, the archive's refusal `is in backlog/` is expected. Kumpel tells the human that the archive and the promotion wait for the feature's next accepted acceptance, and starts nothing else for it.
  - **Step 2:** names the reuse of an open promotion and its line `promotion open: #<number>, for the human to merge`.
- Tests: a new module `tests/operator_scripts/test_operator_approving_after_acceptance.py`. It reads only the lines of `approving.md` under `## After a feature's acceptance`, up to the next `## ` heading.
- No script changes, and no earlier test changes.

## Acceptance criteria

1. Under `## After a feature's acceptance` in `approving.md`, step 1 contains `is in backlog/` and `next accepted acceptance`, and step 2 contains `promotion open: #`. These are rows of one test. The same text placed outside that section does not satisfy a row: the test reads only the section.
2. `make check` stays green.
3. docs:
   - `docs/operator-playbook.md`, step 8: after an acceptance with proposed stories, the archive and the promotion follow the feature's next accepted acceptance, not this one.
   - `docs/operator-guide/install.md`, *The promotion*: when a feature's promotion waits, and why.
   - `docs/decisions.md`: an entry only if the human chooses a change of behaviour when refining; otherwise none.

## Smoke test

```bash
uv run pytest tests/operator_scripts/test_operator_approving_after_acceptance.py 2>&1 | tail -1
```
Expect: a line ending in `passed in <seconds>s` with no `failed`.

## Journal
