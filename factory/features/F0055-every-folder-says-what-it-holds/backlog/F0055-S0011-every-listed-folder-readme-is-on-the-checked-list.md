# Every listed folder README is on the checked list

<!-- proposed by feature acceptance of 2026-11-07; refine before starting -->

## Description

The feature's done condition says every README on `FOLDER_READMES` is on `docs/checked-documents.txt`, so a wrong name or link in it blocks. Today that holds, but only the three test-folder READMEs are pinned to it, by F0055-S0003's `tests/guards/test_test_folder_readmes.py`. If the other 19 lines are deleted from the checked list, `make check` stays green. The document check then reports their findings and blocks on none. That module's other test, that the three test-folder READMEs exist, is now covered for all 22 by F0055-S0008's guard. Its name, `…_written_so_its_guard_does_not_skip_it`, describes a skip that no longer exists. This story pins the checked list for every path of `FOLDER_READMES` in the folder-README guard and removes the module that S0008 and this story make redundant. It changes no code under `src/`, no README and no line of `docs/checked-documents.txt`.

## Interface

- `tests/guards/test_folder_readmes.py` (written by F0055-S0001) gains a private helper and a test:

```python
def _unchecked_readmes(checked: str, readmes: Sequence[str]) -> list[str]
```

- `_unchecked_readmes` reads the text of the checked list through `read_checked_documents` of `factory.shared.domain.documents`. It returns the paths of `readmes` that are not on the list, in the order of `readmes`, or `[]`.
- A new test runs `_unchecked_readmes` on the real `docs/checked-documents.txt` and `FOLDER_READMES` and asserts `[]`.
- `tests/guards/test_test_folder_readmes.py` (written by F0055-S0003) is removed. **Leave needed, the human's to give when refining:** "the tester removes `tests/guards/test_test_folder_readmes.py`, whose two tests the guard over `FOLDER_READMES` now covers for all 22 paths". Without that leave, the story keeps the module and only adds the test.
- No change under `src/`, to `FOLDER_READMES` or to `docs/checked-documents.txt`. The story takes the tests route.

## Acceptance criteria

1. `_unchecked_readmes` gives these results, as rows of one parametrized test, with `readmes` = `("a/README.md", "b/README.md")`:
   - a checked list that holds both paths gives `[]`
   - a list without `b/README.md` gives `["b/README.md"]`
   - a list that has `b/README.md` only on a `#` comment line gives `["b/README.md"]`
   - an empty list gives both paths, in order
2. On the repository, every path of `FOLDER_READMES` is on `docs/checked-documents.txt`: the new test passes.
3. `tests/guards/test_test_folder_readmes.py` no longer exists, under the human's leave named in the Interface.
4. `make check` stays green.
5. docs: `docs/project-guide/shared.md`, *The folder READMEs*: the reader learns that the guard also requires every listed README to be on `docs/checked-documents.txt`. `docs/decisions.md`: none, because no new decision is made.

## Smoke test

```bash
uv run pytest tests/guards/test_folder_readmes.py 2>&1 | tail -1 | grep -c failed
```
Expect: `0`

```bash
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
git clone --quiet . "$d/r" && sed -i '\#^security/README.md$#d' "$d/r/docs/checked-documents.txt"
here=$(pwd); cd "$d/r" && uv run --project "$here" pytest -o addopts= tests/guards/test_folder_readmes.py 2>&1 | grep -q "'security/README.md'" && echo unchecked-fails
```
Expect: `unchecked-fails`

```bash
test -e tests/guards/test_test_folder_readmes.py && echo present || echo removed
```
Expect: `removed`

## Journal
