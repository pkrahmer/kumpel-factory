# A fixture that could not be prepared says why

<!-- proposed by feature acceptance of 2026-11-09; refine before starting -->

## Description

When a fixture of the document check cannot build its starting point, `ProcessExampleRunner` reports one finding, `<document>:<line>: fixture <name> could not be prepared`, and drops the reason the `FixtureError` holds. In one run of four on 2026-11-09, during the acceptance of F0061, `make documents` on an unchanged fresh clone reported `docs/operator-guide/install.md:188: fixture instance could not be prepared`. That document is listed, so the finding blocks. The fixture `instance` clones the checkout as a bare repository through `GitCli.clone_bare`, and that clone's error (the git command, how it ended, its last lines) was lost, so the cause cannot be traced. A finding the docs stage cannot explain stalls it on an example it did not change: that is the stall this feature set out to end. After this story the finding ends with the fixture's own reason, `fixture <name> could not be prepared: <detail>`. A detail of several lines is joined into one line, so that every finding stays one line. Nothing else changes: the fixture is still prepared at most once per document, a failed fixture still gives one finding at its first block, and the document's other blocks on that fixture still run nothing. Finding why `clone_bare` failed is left to a later story, once the reason can be read.

## Interface

- `src/factory/shared/adapters/document_examples.py` (`adapters`): no new signature. `_DocumentRun.environment` catches the `FixtureError` as it does today and adds the finding `fixture <name> could not be prepared: <detail>`, where `<detail>` is `FixtureError.detail` with every run of line breaks and the spaces around them replaced by one space, and with leading and trailing spaces removed.
  - A detail that is empty after that gives `fixture <name> could not be prepared` as today, without the colon.
- Tests: `tests/shared/adapters/test_document_examples.py`.
  - This story changes one test another story wrote: `test_a_fixture_that_cannot_be_prepared_gives_one_finding_and_runs_no_command`. It expects `fixture checkout could not be prepared` and now gets the reason after it. **Leave to be given by the human in `feature.md` before starting**, proposed words: "The tester may change the expected finding of `test_a_fixture_that_cannot_be_prepared_gives_one_finding_and_runs_no_command` in `tests/shared/adapters/test_document_examples.py` to end with `: ` and the detail of `FailingFixture`'s `FixtureError`; the test keeps its name and still checks one finding and no command run."

## Acceptance criteria

1. A fixture that raises `FixtureError(detail)` gives the one finding `<document>:<line>: fixture checkout could not be prepared<suffix>`, as rows of one parametrized test:
   - `"no source"` gives the suffix `: no source`;
   - `"git clone failed (exit 128):\nfatal: x\n"` gives `: git clone failed (exit 128): fatal: x`;
   - `""` and `" \n "` give no suffix: the finding ends with `prepared`.
2. A document with two blocks on a fixture that fails gives that one finding at the first block's line and runs no command of either block (the existing test, with the reason in its expected finding).
3. `make check` stays green.
4. docs: the project guide says that the finding of a fixture that could not be prepared ends with the fixture's reason on one line, and that a fixture's `FixtureError` detail is what a reader of `make documents` sees. This goes in `docs/project-guide/shared.md` (*The examples*, where `CheckoutFixture` names the finding).

## Smoke test

```bash
uv run --quiet python - <<'EOF'
from pathlib import Path
from factory.shared.adapters.document_examples import ProcessExampleRunner
from factory.shared.application.document_examples import Fixture
from factory.shared.domain.documents import DEFAULT_FIXTURE, examples
from factory.shared.domain.errors import FixtureError

class Failing(Fixture):
    def prepare(self, folder: Path) -> dict[str, str]:
        raise FixtureError("git clone failed (exit 128):\nfatal: no source\n")

text = '# A guide\n\n```console\n$ true\n```\n'
print(ProcessExampleRunner().run_document("g.md", examples(text).runnable, {DEFAULT_FIXTURE: Failing()}))
EOF
```
Expect: one line, `['g.md:3: fixture checkout could not be prepared: git clone failed (exit 128): fatal: no source']`.

```bash
uv run pytest tests/shared/adapters/test_document_examples.py
```
Expect: a summary line with only `passed`, no `failed` or `error`.

## Journal
