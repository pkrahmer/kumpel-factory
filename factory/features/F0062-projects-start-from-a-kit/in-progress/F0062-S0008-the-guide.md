---
stage: doing
blocked: null
round: 1
attempts: 0
crashes: 0
pull_request: 697
comments_read: [6938616709]
handed_over: null
claim: null
journal:
- number: 1
  speaker: human
  kind: created
  at: '2026-11-17T04:38:27.705681Z'
  stage: intake
- number: 2
  speaker: factory
  kind: started
  at: '2026-11-17T04:38:27.712552Z'
  stage: intake
- number: 3
  speaker: intake
  kind: result
  at: '2026-11-17T04:38:51.692736Z'
  stage: intake
  run: ce2a53df165c440ca470313967a460e0
- number: 4
  speaker: factory
  kind: started
  at: '2026-11-17T04:38:56.737815Z'
  stage: docs-only
- number: 5
  speaker: documenter
  kind: question
  at: '2026-11-17T04:43:44.881315Z'
  stage: docs-only
  run: 616009ca26364756b4a7390927ffea1c
  blocked: question
- number: 6
  speaker: human
  kind: comment
  at: '2026-11-17T04:44:31.945599Z'
  stage: docs-only
- number: 7
  speaker: factory
  kind: started
  at: '2026-11-17T04:44:34.756800Z'
  stage: docs-only
- number: 8
  speaker: documenter
  kind: result
  at: '2026-11-17T04:44:54.279028Z'
  stage: docs-only
  run: e4cddc12913843479543c98031eb452c
- number: 9
  speaker: factory
  kind: started
  at: '2026-11-17T04:44:59.496331Z'
  stage: tests
- number: 10
  speaker: tester
  kind: result
  at: '2026-11-17T04:45:38.262836Z'
  stage: tests
  run: 56fd96a4e92f41089d9a8c276c30f583
- number: 11
  speaker: factory
  kind: started
  at: '2026-11-17T04:45:43.570874Z'
  stage: doing
- number: 12
  speaker: coder
  kind: result
  at: '2026-11-17T04:48:18.692876Z'
  stage: doing
  run: f34af49164014aa1ad3f8ef71a95c205
- number: 13
  speaker: factory
  kind: started
  at: '2026-11-17T04:48:23.779568Z'
  stage: review
- number: 14
  speaker: reviewer
  kind: result
  at: '2026-11-17T04:50:12.893927Z'
  stage: review
  run: fce76f7e52ce4eef9a7700ded96ae719
---

# The guide

## Description

The kit, the packs and the conformance check exist, but an operator who wants the factory to build a repository finds them only piece by piece: the kit's and the packs' own `README.md`, the page on the pipeline definition, the page on a site. After this story the operator guide has one page, "Starting a project", that leads through both ways from start to the first story: a fresh repository from a starter, and an existing repository by hand with the kit, a pack and the check. The page on a site gains what a Java project needs from it. This is a story of documents, with no kit or pack file changes; the one code line and the test lines the human's answer allowed make the new page the operator guide's eleventh topic, which the document check requires like the others. It describes what is built, with examples that were really run, and it names what does not exist yet (the onboarding pull request, starters for every stack) as not existing.

## Interface

- No module under `src/factory/` and no file under `operator/` changes; no test is written or changed.
- `docs/operator-guide/start-a-project.md`, new, with the operator guide's index (`docs/operator-guide/README.md`) pointing to it, and `README.md` naming it as the place to begin with a repository of one's own.
- `docs/operator-guide/site.md` gains the part on a Java project.
- The real runs the page may quote, each with its date: the conformance check on the Spring demo and on the HeishaMon fork on factory-vm2 (2026-11-17, static, both `project: ready`); `factory-check-project --run` on the Spring demo (2026-11-17, nine points `ok`, 1 min 42 s), on a small C project from kit and C pack (19 s) and on the Spring demo's sources with kit and Java pack (1 min 45 s); the first Java story in the factory (2026-11-16, 6 runs, $1.79).

## Acceptance criteria

1. The new page opens with what a project needs before the factory can build it, as the three layers: the kit (every project), a stack pack (every project of that stack), a starter (a fresh start only); and says which of them exist today: the kit, the packs `python`, `c-host` and `java-gradle`, and no public starter yet.
2. The page's part for an existing repository is a numbered walk that a reader can follow without another page: choose the thin or the full line and what each means; copy the kit; copy the pack, with the makefile at `factory/Makefile` and `make_file` when the repository has a root `Makefile` of its own; set the write paths to the folders the factory may write; fill `CLAUDE.md` from the kit's skeleton and the pack's sections; commit; run `factory-check-project`, and read each `FAIL`; run it with `--run` on the machine; write the first feature and story by the forms; start the story.
3. The page's part for a fresh start says the same in short for a repository that begins from a starter, and that a company keeps its own private starter because it carries the company's habits.
4. The page says what the project owns afterwards and what stays the kit's (`kit.mk`, the forms), that the installed agents are the default and how a project replaces one, and where a stack's review points go (`## Review` in `CLAUDE.md`).
5. The page names each pack's `TRAPS.md` as the page to read before the first story, and says in one paragraph per stack what to expect of it in a stage (for Java: no container runtime in a stage, so an image build and Testcontainers stay in the CI pipeline; every target but `sync` offline).
6. Every command the page shows is a runnable example that the document check runs, or is marked as an example for the VM that names the real run it was copied from, with its date.
7. `docs/operator-guide/site.md` says what a Java project needs from a site: the private Maven repository's address and login as variables named in `FACTORY_CONTAINER_ENV` and set in the instance's `factory.local.env`, never in the repository; the CA bundle in `FACTORY_CA_BUNDLE`, which Java does not read by itself and the Java pack turns into a trust store at `make sync`; and that both were proven with a stand-in repository on 2026-11-16.
8. `make check` stays green.
9. docs: the page `docs/operator-guide/start-a-project.md`, the index's entry for it, `README.md`'s pointer to it and the Java part of `docs/operator-guide/site.md`, as criteria 1 to 7 describe them; `docs/decisions.md` records that the guide for starting a project is the operator's page, not the agents' project guide, because its reader is a person who sets a repository up.

## Smoke test

```bash
test -f docs/operator-guide/start-a-project.md && grep -c 'start-a-project.md' docs/operator-guide/README.md README.md
```
Expect: two lines, each a file name, a colon and a number of at least 1.

```bash
grep -c -e 'factory-check-project' -e 'make_file' -e 'TRAPS.md' docs/operator-guide/start-a-project.md; grep -c -e 'FACTORY_CONTAINER_ENV' -e 'FACTORY_CA_BUNDLE' docs/operator-guide/site.md
```
Expect: two numbers, each at least 3 for the first and at least 2 for the second.

## Journal

1. 2026-11-17 human: created.
2. factory: started intake as self.
3. intake: accepted
   - Interface: every changed path is one the documenter may write: `docs/operator-guide/start-a-project.md` (new), `docs/operator-guide/README.md`, `docs/operator-guide/site.md`, `README.md` and `docs/decisions.md`. Nothing under `src/factory/` or `operator/` changes and no test does, so the story takes the docs route. The real runs the page may quote are listed with their dates.
   - Criteria: criteria 1 to 7 can each be checked against the documents. They name the three layers and which exist, the ten steps of the walk for an existing repository, the fresh start and private starters, what the project owns and what stays the kit's, agent replacement and `## Review`, one TRAPS paragraph per stack, every command either runnable by the document check or marked as a VM example with its source and date, and the Java part of the site page. They state no rule with a failing side. The facts the page must describe exist in the repository: `operator/kit/` and `operator/packs/{python,c-host,java-gradle}/TRAPS.md`. The pipeline page already uses the "example for the VM" form (`docs/operator-guide/pipeline.md:269`). Criterion 8 (`make check`) and criterion 9 (`docs:`) close the list.
   - Smoke test: both commands only read files and can run in the checkout. `grep -c` over two files prints `file:count` lines, and the second command prints two bare counts, so both `Expect:` lines can be checked against the output.
   - Docs criterion: it names what the reader must know (the page, the index entry, the README pointer, the Java part of the site page, and the decision with its reason, that the reader is a person setting a repository up). It dictates no sentences.
   - Architecture: the story is documents only, in the folders CLAUDE.md gives the operator guide (`docs/operator-guide/`), the newcomer (`README.md`) and the decision log (`docs/decisions.md`). It does not touch `planning/` or `docs/runs/`.
   - Scope: it is in the feature's scope ("The guide for a fresh start and for a brownfield repository", story S0008). The page goes in the operator guide, as decision 26 of `feature.md` placed it. It describes the onboarding pull request and starters only as things that do not exist yet, which keeps it inside the feature's "Out of scope".
4. factory: started docs-only as self.
5. documenter: Stopped: the new page needs a change outside the documents, which the Interface rules out ("no module under `src/factory/` ... changes; no test is written or changed").

   What blocks: `make guides` fails on `tests/guards/test_operator_guide_files.py::test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics`. It asserts that `docs/operator-guide/` holds exactly `README.md` plus `TOPIC_FILES` (`tests/support/check_documents_support.py`, ten names). The same list is `OPERATOR_GUIDE_FILES` in `src/factory/shared/domain/documents.py:29`, the documents the document check requires. Any new page in that folder fails the guard.

   Question: which way?
   - A (my choice): make the page an eleventh topic. The tester adds `"start-a-project.md"` to `TOPIC_FILES` (needs your leave: a test another story wrote) and the coder adds `f"{OPERATOR_GUIDE_FOLDER}/start-a-project.md"` to `OPERATOR_GUIDE_FILES`. The document check then requires the page like the other topics. The Interface then names that one code line and that one test-support line.
   - B: change only the guard, so the folder may hold the ten topics plus `start-a-project.md` (your leave for the test change; no code change). The document check would not require the page.
   - C: keep to documents only and put the walk into an existing topic (for example `pipeline.md`). That contradicts criteria 1 and 9 and the smoke test, which name the separate page.

   What is written and stays in the working tree:
   - `docs/operator-guide/start-a-project.md` (new): the three layers and what exists (kit, packs python/c-host/java-gradle, no public starter, no onboarding pull request); the ten-step walk for an existing repository; two runnable `console` examples on a firmware repository with a root `Makefile` (C pack at `factory/Makefile`, `make_file`), first with two `FAIL` points and then `project: ready`; the `--run` command as an `sh` block for the VM, with the real runs and their dates from the Interface; the fresh start from a starter and private company starters; what the project owns and what stays the kit's; installed agents and `factory/agents/<role>.md`; `## Review`; one paragraph per pack's `TRAPS.md`.
   - `docs/operator-guide/site.md`: new section *A Java project* (Maven repository variables in `factory.local.env`, named in `FACTORY_CONTAINER_ENV`; `FACTORY_CA_BUNDLE`, which Java does not read, turned into a trust store by the pack's `make sync`; proven with a stand-in repository on 2026-11-16).
   - `docs/operator-guide/README.md`: new row in the file table, a step 4 in *Where to start*, and the Java part added to the site row.
   - `README.md`: the pointer under *Where to read next*.
   - `docs/decisions.md`: the new entry *The guide for starting a project is an operator's page*. It has no "Rejected" line because the story names no rejected option.
   - `docs/checked-documents.txt`: lists the new page, so `make documents` runs its examples.
   - `docs/operator-guide/agent-runtime.md:396`: now points to the new page.

   Checked: `make documents` ends `documents ok (48.0 s)`. Both smoke commands give the expected counts (README.md:2, README.md:1; 13 and 2). `make guides` is red only on the guard above.

   Cross-read and found current: `operator/kit/README.md`, `operator/packs/README.md`, the three `TRAPS.md`, `docs/operator-guide/pipeline.md` (*Checking a repository before the factory runs it*), `agent-runtime.md` (*Behind a proxy*, *A project's own agents*), `docs/project-guide/style.md` (examples). Nothing stale found that is not this story's.
6. 2026-11-17 human: A. The page is the eleventh topic. Leave given: the tester may add `start-a-project.md` to `TOPIC_FILES` in `tests/support/check_documents_support.py` and change the earlier tests that pin the number or the list of the operator guide's topics (ten becomes eleven), each keeping its name; the coder adds the page to `OPERATOR_GUIDE_FILES` in `src/factory/shared/domain/documents.py`. The story's sentence that no module and no test changes is lifted for exactly these lines.
7. factory: started docs-only as self.
8. documenter: Sent on to the tester and the coder: the human's answer A (entry 6) needs a test change and a code change, and neither is in my write paths. This run changed no document.

   What the tester changes (the human gave leave in entry 6):
   - `tests/support/check_documents_support.py:11`: add `"start-a-project.md"` to `TOPIC_FILES`.
   - The earlier tests that pin the number or the list of topics, each keeping its name. I found one: `tests/guards/test_operator_guide_files.py:25` (`test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics`). It reads `TOPIC_FILES`, so the list change may be the only edit it needs. `MISSING_LINES` in the same support module is built from `TOPIC_FILES`, so it follows the list by itself. The test files that use `MISSING_LINES` or `TOPIC_FILES` should still be run.

   What the coder changes:
   - `src/factory/shared/domain/documents.py:29`: add `f"{OPERATOR_GUIDE_FOLDER}/start-a-project.md"` to `OPERATOR_GUIDE_FILES`. The document check then requires the page, as it requires the other topics.

   The documents are already on the branch from my last run and stay as they are:
   - `docs/operator-guide/start-a-project.md` (new)
   - `docs/operator-guide/site.md` (*A Java project*)
   - `docs/operator-guide/README.md`
   - `README.md`
   - `docs/decisions.md` (it has no "Rejected" line because the story names no rejected option)
   - `docs/checked-documents.txt`
   - `docs/operator-guide/agent-runtime.md`

   When the story comes back to the docs stage, `make guides` should be run again. Its only red result was the guard above.
9. factory: started tests as self.
10. tester: Made the test change the human allowed in entry 6 (answer A: the page becomes the eleventh topic of the operator guide). No new test file was written. Criteria 1 to 7 are checked against the documents by the document check and the docs stage's checks, not by a pytest test.

    Earlier test files I changed, with the human's leave from entry 6:
    - `tests/support/check_documents_support.py`: added `"start-a-project.md"` as the last entry of `TOPIC_FILES`. `MISSING_LINES` is built from that list, so it now also expects `docs/operator-guide/start-a-project.md: missing`.
    - `tests/shared/domain/test_documents_guide_files.py::test_the_guide_is_an_index_in_its_folder`: the pinned `DOCUMENT_PATHS` tuple gains `"docs/operator-guide/start-a-project.md"` after `work-items.md` and before `docs/project-guide/README.md`. The test keeps its name.

    Every test keeps its name. `tests/guards/test_operator_guide_files.py` needed no edit because it reads `TOPIC_FILES`. Its name still says "ten topics"; I left the name as it is because the leave says each test keeps its name.

    What the coder must do: add `f"{OPERATOR_GUIDE_FOLDER}/start-a-project.md"` as the last entry of `OPERATOR_GUIDE_FILES` in `src/factory/shared/domain/documents.py:29`. It must come right after `work-items.md`, because `OPERATOR_GUIDE_FILES == TOPIC_PATHS` compares the two lists in order.

    The run of the changed and dependent test files (`test_documents_guide_files.py`, `test_operator_guide_files.py`, `test_check_documents.py`, `test_check_documents_guide_files.py`, `pipeline/domain/test_documents.py`) has three red tests, and that is intended:
    - `tests/shared/domain/test_documents_guide_files.py::test_the_guide_is_an_index_in_its_folder`
    - `tests/entry/test_check_documents.py::test_the_module_run_as_a_process_exits_with_the_status_of_main[empty-directory]`
    - `tests/entry/test_check_documents_guide_files.py::test_the_old_guide_path_is_not_read[empty-root]`

    Each fails with a wrong result (the code does not list the new page yet), not with an import error. The guard `test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics` is now green. Every module was imported. `make lint` is green.

    When the coder is done, the story goes back to the docs stage, where `make guides` must be run again.

    `lint`: lint: green (0.2 s)
11. factory: started doing as self.
12. coder: Added the line the human allowed in entry 6. `src/factory/shared/domain/documents.py` now has `f"{OPERATOR_GUIDE_FOLDER}/start-a-project.md"` as the last entry of `OPERATOR_GUIDE_FILES`, right after `work-items.md`. The tester's comparison checks the order, so the order matches `TOPIC_FILES`. The document check now requires the new page, as it requires the other operator-guide topics. This is the only code change.

    - Main choice: I added the path as a plain f-string entry, written like the other topics. The rejected alternative was a named constant such as `OPERATOR_START_A_PROJECT`. No code refers to the page by name, so a constant would add nothing.
    - Tests: the five test files the tester named (`test_documents_guide_files.py`, `test_operator_guide_files.py`, `test_check_documents.py`, `test_check_documents_guide_files.py`, `pipeline/domain/test_documents.py`) are all green, including the three that were failing before.
    - Checks: `make check guides` is green (`check: green`, `guides: green`).
    - Refactor: nothing needed after a one-line change.
    - The records contract: unaffected, because the tuple is not a contract model.
    - Description: the journal changed it. Entry 6 lifts "no module and no test changes" for exactly these lines. I cannot write the work item, so I did not rewrite `## Description`.
    - Noticed, not touched: the guard `test_the_single_guide_is_gone_and_the_folder_holds_the_index_and_ten_topics` still says "ten topics" in its name although there are now eleven. It keeps its name under the human's leave.
    - Next: the story returns to the docs stage, where `make guides` and `make documents` run again.

    `duplicates`: duplicates: 8 new, 38 known, 5 gone
13. factory: started review as self.
14. reviewer: Findings:

    1. `docs/operator-guide/start-a-project.md`, *The live check on the machine* (the `sh` block, line `set -a; . /srv/factory/vm/factory.env; set +a`), together with step 8 ("with the instance's environment loaded"). The problem: the example loads only `factory.env`. The new *A Java project* part of `docs/operator-guide/site.md` tells the operator to put the private Maven repository's variables in `factory.local.env`, and `FACTORY_CONTAINER_ENV` often goes there too. The unit reads both files (`docs/operator-guide/machine.md:387`, `:407`). `factory-check-project --run` reads its settings and the `FACTORY_CONTAINER_ENV` names from its own process environment (`src/factory/entry/check_project.py:134`, `src/factory/machine/domain/containers.py:81`). So a Java project set up as this page and `site.md` describe gets a red `sync` point when the example is copied. The fix, for the documenter: keep the real run's command, and add one sentence (or a second marked line) saying that `/srv/factory/vm/factory.local.env` must be loaded after `factory.env` when it exists, as the unit does. This is needed for a Java project with a private Maven repository. The coder cannot write the document, so send it on to the documenter as entry 8 did the other way.

    description corrected: "This is a story of documents only: no code, no test and no kit or pack file changes." -> "This is a story of documents, with no kit or pack file changes; the one code line and the test lines the human's answer allowed make the new page the operator guide's eleventh topic, which the document check requires like the others." (entry 6 settles it).

    Checked with no finding:
    - Criteria 1 to 7 against the documents and the code:
      - three layers, and which exist (kit; packs `python`, `c-host`, `java-gradle`; no starter);
      - the ten-step walk, which matches `operator/kit/README.md` and `operator/packs/README.md`: `make_file`, `factory/Makefile`, include line, Java's `.gitleaks.toml` and `scripts/trust-store.sh`, the four `CLAUDE.sections.md` headings, `--agent-home` falling back to `FACTORY_CLAUDE_HOME` or the settings;
      - the nine points of `--run` (`POINT_NAMES` plus `LIVE_POINT_NAMES` in `src/factory/pipeline/domain/project_check.py:12,21`);
      - ownership (`kit.mk` and the forms stay the kit's, as in the kit README's file table);
      - agent replacement and `## Review`;
      - the TRAPS paragraphs, which match the three `TRAPS.md`;
      - the site.md Java part, which matches the Java `Makefile` (`--offline`, `TRUST_STORE`, re-built per bundle hash) and `CA_BUNDLE_NAMES`.
    - Commands: both `console` examples are in `docs/checked-documents.txt` and run by `make documents`. The VM block is marked and names its runs and dates.
    - Code: one line in `src/factory/shared/domain/documents.py` adds the page to `OPERATOR_GUIDE_FILES`, in `TOPIC_FILES`' order. Architecture, security and quality are unaffected. No marker. The coder's `make check guides` was green (entry 12).
    - Decision log: the new entry states the decision and its reason as criterion 9 asks.
    - Not a finding: the `## Interface` bullet "no test is written or changed" is superseded by the human's answer in entry 6, which names the lines it lifts. I changed only the Description, as the role allows.

    Earlier tests changed:
    - `tests/support/check_documents_support.py`: the human's leave, journal entry 6 (adds `start-a-project.md` to `TOPIC_FILES`).
    - `tests/shared/domain/test_documents_guide_files.py`: the human's leave, journal entry 6 (the pinned list of guide paths gains the page; the test keeps its name).
