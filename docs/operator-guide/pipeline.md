# The pipeline definition and the story check

A topic of the [operator guide](README.md). It covers the file that configures your pipeline, `factory/pipeline.yml`, the command that checks whether a repository is ready for the factory, and the command that checks a [story](../project-guide/glossary.md) before the factory starts it.

## The pipeline definition

The [pipeline definition](../project-guide/glossary.md) is the project's configuration: its [stages](../project-guide/glossary.md), the [roles](../project-guide/glossary.md) that work in them, the [project commands](../project-guide/glossary.md) and the limits. The factory reads it only as it stands on `origin/develop`, so a change takes effect when it is merged.

This is the smallest useful definition. It loads:

```yaml
contract: '1.0'
roles:
  tester:
    write_paths: ['tests/*', '{work_item}']
  coder:
    write_paths: ['src/*', '{work_item}']
stages:
  testing: {role: tester, next: [doing], checks: [lint]}
  doing: {role: coder, next: [review], checks: [check]}
  review: {approval: true, next: [done, doing], round_cap: 3}
  done: {}
```

The order of the stages in the file is the pipeline's order. The first `next` of a stage is the forward move. The others are moves back.

### Change the definition

1. Edit `factory/pipeline.yml` in a clone of the project.
2. Check it against the rules below, most of all the stage `done` and the [lease](../project-guide/glossary.md).
3. Merge the change to `develop`. The factory reads the new text at its next [tick](../project-guide/glossary.md).

A refused definition [stops](../project-guide/glossary.md) the factory with `pipeline_definition_invalid` until you fix it on `develop` (see "The stop `pipeline_definition_invalid`" in [stops.md](stops.md)).

### The rules you meet most often

- The stage `done` must exist, with no role and no `next`. Write it `done: {}`; `done:` alone is refused.
- The contract major must be 1. Any minor is read.
- Every stage other than `done` needs a non-empty `next` and either a role or `approval: true`. Every name in `next` must be a stage.
- The lease: for each stage with a role, the role's `time_limit` plus the `time_limit` of every command in the stage's `checks`, `reports` and `context` must be at most the role's `lease_duration`. With the defaults, 40 + 10 (one check) + 10 (one report) = 60 fits. A stage with two checks and a report adds up to 70 and is refused. Raise the `lease_duration` or lower a limit.
- Values are taken only in their YAML type. A limit is an integer (not `'30'`, `30.0` or `true`). `approval` is `true` or `false` (not `'yes'` or `1`). Names and [write paths](../project-guide/glossary.md) are text.
- A key that is not listed is refused, so a misspelt key is never ignored. That holds for `tool_paths` too. An agent run may write only its write paths, and there is no folder for tool state.
- A given `project_commands` replaces the default set as a whole. List `check`, `lint` and `test` again if you still want them.
- Every role needs an agent file, a project's own or the installed one (see "The agent files" in [agent-runtime.md](agent-runtime.md)).

[docs/project-guide/pipeline.md](../project-guide/pipeline.md), "The rules of the definition", lists every fault.

### Start facts

Most agent runs begin by gathering the same facts: the diff, the list of changed files, the recent log. Each such call costs the agent a turn. A stage's `context` names project commands that gather these facts instead; the factory runs them before the agent, and the agent starts with their outputs. Your Makefile decides what each command shows.

The template (`operator/template/Makefile` and `operator/template/factory/pipeline.yml`) ships three such targets. `facts-diff` and `facts-changes` measure from the point where the branch left `origin/develop`; `facts-files` lists the tracked files as they are. Each leaves out the factory's own files under `factory/`.

| Target | What it shows | Stages in the template |
|---|---|---|
| `facts-diff` | the branch's changes: `git diff --stat`, then the whole diff, without `uv.lock` | `review` |
| `facts-changes` | the changed files by name and status, then the new untracked files | `doing`, `docs` |
| `facts-files` | every tracked file | `tests` |

The template's [pipeline.yml](../../operator/template/factory/pipeline.yml) lists them like this:

```yaml
project_commands:
  facts-diff: {time_limit: 1}
  facts-changes: {time_limit: 1}
  facts-files: {time_limit: 1}
stages:
  tests: {role: tester, next: [doing], checks: [lint], reports: [test], context: [facts-files]}
  doing: {role: coder, next: [review, tests], context: [facts-changes]}
  review: {role: reviewer, next: [docs, doing, tests], round_cap: 3, context: [facts-diff]}
```

Its [Makefile](../../operator/template/Makefile) finds the base with `git merge-base` against `origin/develop`, so a checkout without a local `develop` branch works too:

```make
base_ref = $$(git merge-base HEAD origin/develop)

facts-diff:
	base=$(base_ref); git diff --stat "$$base" -- . ':!factory' ':!uv.lock'; echo; git diff "$$base" -- . ':!factory' ':!uv.lock'
```

The targets are your project's own. The factory knows only the names a stage's `context` lists. You may change what a target shows, rename it, or drop a stage's `context`, and nothing in the factory changes with it.

- The commands run in order, each under its own `time_limit`, in the check container on the stage's base, like a check but without `make sync` first. Each output becomes a `<context name="facts-diff">` block of the first message, after the role's instructions.
- An output longer than 60,000 characters is cut to its first 60,000, followed by a line naming how many characters were cut and telling the agent to run the command itself.
- A command that fails or runs out of time gives the block the line `failed: <reason>`, and the agent's run starts anyway. A start fact never holds a stage.
- The commands' `time_limit`s count toward the lease.
- `context` came with the definition's contract 1.1; a definition at `'1.0'` may carry it too.

The full rules are under *Start facts* in [the project guide's pipeline.md](../project-guide/pipeline.md).

### Name the makefile

The factory runs every project command, and the sync before every agent run, as `make <command>` in the root of the checkout. make then reads the root `Makefile`. An existing repository often has a root `Makefile` of its own, or none and no wish for one. It can keep it: put the factory's targets in another makefile and name it in the definition.

```yaml
contract: '1.2'
make_file: factory/Makefile
```

- Every check, every report, every start fact and the sync then run as `make -f factory/Makefile <command>`, still from the root of the checkout.
- make still runs in the root, so every path inside that makefile, an `include` among them, is relative to the root of the checkout, not to the makefile's folder. In a makefile named `make_file: factory/Makefile`, the line `include common.mk` reads `common.mk` at the root.
- The factory reads `make_file` from the definition on the working branch at every call, so a merged change takes effect at the next check or sync.
- A definition without `make_file` runs plain `make <command>`, as before. So does every call while the definition is missing or refused.
- `factory-check-project` reads the named makefile instead of `Makefile` (see *The six points* below).
- `make_file` came with the definition's contract 1.2; a definition at `'1.0'` or `'1.1'` may carry it too.

The value must be a path inside the checkout made of letters, digits, `_`, `.`, `/` and `-`, which does not start with `-` or `/` and has no `..` segment. `make_file: Makefile`, `make_file: factory/Makefile` and `make_file: build/factory.mk` are accepted. An empty value, `-f`, `/etc/Makefile`, `../Makefile`, `a/../b`, `my file`, `a;b` and a number are refused, and the fault names `make_file`.

### More than one route

A definition may hold more than one route and more than one [approval](../project-guide/glossary.md) stage. When you close a pull request at an approval stage, the story goes to that stage's second `next`. The stage whose first `next` is that approval counts the [rounds](../project-guide/glossary.md).

The smoke test of the template reads `smoke-test: {role: smoke-tester, next: [approval, doing, docs], checks: [check], round_cap: 3}`. It is the template's one full check: `make check` runs after the smoke tester, and no stage before it lists `check`. A finding that is only a slip in a document goes from the smoke test straight to `docs`. There the documenter fixes it and hands back to the smoke test. This counts as a round against the `round_cap`, as a return to `doing` does.

The review stage may send a story straight to the tester when every finding needs only a change to the story's own tests, such as an untested side of a rule. The tester writes or changes exactly the tests the findings name and hands to the coder, so the coder runs once before the next review. When any finding needs a change outside those tests, all findings go to `doing`. This needs `tests` in the `next` of `review`. The template's `review` already lists it: `review: {role: reviewer, next: [docs, doing, tests], round_cap: 3, context: [facts-diff]}`. In a definition whose `review` lists only `[docs, doing]`, the reviewer sends every finding to `doing`. A move from `review` to `tests` counts as a round against the `round_cap`, as a return to `doing` does.

### The docs route

A story that changes only documents skips the tests, doing and review stages. Documents are `README.md`, the files under `docs/` and `operator/README.md`.

1. The intake chooses the route. It picks `docs-only` when every path the story's Interface changes is one the documenter may write, and `tests` otherwise.
2. The documenter writes the whole change and runs `make documents`.
3. `make check` runs after `docs-only`. Its `not_read` lists the documenter's write paths, so after a documents-only change the factory reuses its earlier passed result. In kumpel-factory `make guides`, the tests that read the documents, runs beside `secrets` and `documents` after `docs-only`, as it does after `docs`.
4. The reviewer reads the documents against the story's criteria, the code and [the style page](../project-guide/style.md).
5. The story goes to `docs-approval`, where you decide, or back to the documenter with numbered findings.

If the documenter finds that the story needs more than documents, it hands the story to the tests stage and says what is needed. The story then takes the normal route.

The route works only when your definition holds the stages `docs-only`, `docs-review` and `docs-approval`, and the `next` of the intake lists `docs-only`. Without them the agents do nothing on it.

### Reuse a result with `not_read`

A passed result of a project command is reused while the files it reads stay the same. `not_read` lists the paths the command does not read, so that a change only there is no reason to run it again. The paths it names are left out of the tree that the key holds (see "The known results" in [health.md](health.md)).

List only what the command does not read at all. A linter, formatter or type checker that walks the whole tree reads every source file in every folder, so leave out file types it does not read, never a whole folder. A forgotten path costs one run. A path listed by mistake can let a reused `check` pass a fault.

A pattern follows the form of `write_paths` patterns: relative to the checkout, `*` also crosses `/`, case-sensitive. For example:

```yaml
project_commands:
  check: {time_limit: 10, not_read: ["notes/*.md", "notes/*.jsonl"]}
```

A pattern that cannot name a path inside the checkout stops the definition from loading. Such a pattern is empty, starts with `/` or `~`, holds a `..` segment, or holds `{` or `}`:

```text
project command lint: not_read /etc/* must be a path pattern inside the checkout
```

kumpel-factory's own definition, `factory/pipeline.yml`, leaves out the Markdown and JSON Lines files that no test reads, and folders that hold no code and that no test reads. `make lint` reads every Python file of the tree, wherever it lies, so no folder with code is left out. It also leaves out the documenter's write paths: `README.md`, `docs/*`, `operator/README.md` and the folder READMEs. No test of `make check` reads them, because `make test` runs `-m "not documents"` and so leaves out the tests marked `documents`. The project command `guides` (`make guides`) runs those marked tests in the docs stages. A documents-only change can therefore turn `make guides` red, and leaves the passed `make check` to be reused.

```yaml
project_commands:
  check: {time_limit: 8, not_read: ["docs/runs/*", "factory/features/*.md", "factory/features/*.jsonl", "factory/archive/*", "factory/stops.jsonl", "planning/*", "session-logs/*", "README.md", "docs/*", "operator/README.md", "agents/README.md", "operator/bin/README.md", "operator/claude/README.md", "operator/job/README.md", "operator/lib/README.md", "operator/opencode/README.md", "operator/skill/README.md", "operator/vm/README.md", "security/README.md", "src/factory/README.md", "src/factory/agents/README.md", "src/factory/entry/README.md", "src/factory/hosting/README.md", "src/factory/machine/README.md", "src/factory/pipeline/README.md", "src/factory/shared/README.md", "src/factory/watching/README.md", "src/factory/work/README.md", "tests/README.md", "tests/support/README.md", "tests/guards/README.md"]}
```

Two warnings:

- A project whose `check` scans changed files for secrets keeps a scan of the left-out files only if something else runs it. kumpel-factory's docs stage runs `secrets` as a check of its own, with nothing left out.
- A command whose result depends on anything outside the tree and the image is reused safely only when those versions are pinned in the tree, for example by a lockfile. Dependencies fetched at run time with unpinned versions are such a case. Otherwise leave `not_read` empty and do not rely on reuse for it.

### Reference

The keys of the definition:

| Name | What it does | Default | Example |
|---|---|---|---|
| `contract` | the contract version, quoted | required | `'1.0'` |
| `stages` | name to stage; the order in the file is the pipeline's order | required | `doing: {role: coder, next: [review]}` |
| `roles` | name to role; the name is also the agent file's name | required | `coder: {write_paths: ['src/*']}` |
| `project_commands` | name to `time_limit` in minutes and, optionally, `not_read` | `check`, `lint` and `test`, each 10 minutes and `not_read: []` | `check: {time_limit: 8}` |
| `attempts_cap` | [stalls](../project-guide/glossary.md) of one stage before the human is asked | 2 | `attempts_cap: 3` |
| `crash_cap` | [crashes](../project-guide/glossary.md) before the human is asked | 2 | `crash_cap: 3` |
| `acceptance_stage` | the stage of the feature [acceptance](../project-guide/glossary.md); it needs a role | none | `acceptance_stage: acceptance` |
| `make_file` | the makefile every project command and the sync run with, as `make -f <path>` from the root of the checkout (see "Name the makefile") | none: make's own default, the root `Makefile` | `make_file: factory/Makefile` |

The keys of a stage:

| Name | What it does | Default | Example |
|---|---|---|---|
| `role` | the role that works in the stage; without one no agent runs | none | `role: coder` |
| `next` | the stages a decision may name; the first is the forward move | empty (only `done` may have none) | `next: [review, tests]` |
| `approval` | the human decides in this stage; it has no role | `false` | `approval: true` |
| `checks` | project commands that must pass after the agent | empty | `checks: [check]` |
| `reports` | project commands run after green and only recorded | empty | `reports: [duplicates]` |
| `context` | project commands run before the agent; each output goes into the agent's first message as a start fact | empty | `context: [facts-diff]` |
| `round_cap` | rounds the stage allows before the human is asked | none (no cap) | `round_cap: 3` |

The keys of a role:

| Name | What it does | Default | Example |
|---|---|---|---|
| `write_paths` | the paths the role may write; at least one, and each holds a character that is not whitespace | required | `['src/*', '{work_item}']` |
| `time_limit` | minutes one agent run may take | 40 | `time_limit: 30` |
| `lease_duration` | minutes a [claim](../project-guide/glossary.md) holds | 60 | `lease_duration: 90` |

The keys of a project command:

| Name | What it does | Default | Example |
|---|---|---|---|
| `time_limit` | minutes the command may run | 10 | `time_limit: 8` |
| `not_read` | the paths the command does not read (see "Reuse a result with `not_read`") | `[]`, nothing left out | `["docs/runs/*"]` |

Further rules:

- A write path may hold `{work_item}`, the [work item](../project-guide/glossary.md)'s own file, and `{feature}`, its [feature](../project-guide/glossary.md)'s path, such as `factory/features/<feature>`.
- The protected paths are outside every write path: `factory/pipeline.yml`, the story and feature forms, every `feature.md`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `uv.lock`, `.claude/` and the project's `<project>/factory/agents/`.
- Every limit and cap is a positive whole number.
- `human`, `factory` and `question` cannot be a stage name or a role name.
- Every name in `checks` and `reports` must be a project command.
- `sync` is a project command like the others (`sync: {time_limit: 5}` in the template). The [stage environment](../project-guide/glossary.md) reads its limit for the container that prepares the tools after a checkout. No stage lists it, so it never enters a lease. A definition without `sync` gives it 10 minutes.

## Checking a repository before the factory runs it

`factory-check-project <folder>` answers whether the git repository in `<folder>` is ready for the factory, before you start a story there. It reads the commit at `HEAD`, never the work tree, because the factory reads commits too: a fix you have not committed does not count. It starts no container and runs no project command, so `make check` and the stage image are not tried; it judges only the committed files.

Until the command is installed as a console script, run it in the factory's own checkout as `uv run python -m factory.entry.check_project`, with the same arguments.

1. Commit what you want checked in the project's repository.
2. Run the command with the folder of that repository. Name the installed agents with `--agent-home <dir>`; without it the command takes the folder that `FACTORY_CLAUDE_HOME` names. In the factory's checkout the shipped agents are the folder `agents`.
3. Read the lines it prints: one line per point, then the verdict. Fix every `FAIL`, commit, and run it again.

The example builds a project from the template in a new folder `my-project`, with two slips: its `Makefile` has no `lint:` rule, and `factory/feature-form.md` is missing. It runs in the factory's checkout, where the shipped agents are the folder `agents`:

```console
$ git init -q my-project && mkdir -p my-project/factory my-project/src my-project/tests my-project/docs
$ cp operator/template/factory/pipeline.yml factory/story-form.md my-project/factory/
$ grep -v '^lint:' operator/template/Makefile > my-project/Makefile
$ touch my-project/src/a.py my-project/tests/t.py my-project/docs/d.md my-project/README.md
$ git -C my-project add -A && git -C my-project -c user.name=t -c user.email=t@example.com commit -q -m one
$ python -m factory.entry.check_project --agent-home agents my-project
pipeline definition: ok
makefile: FAIL: no target lint
stage file: ok
agents: ok
write paths: ok
forms: FAIL: factory/feature-form.md is missing
project: not ready (2 faults)
```

### The six points

| Point | What it judges |
|---|---|
| `pipeline definition` | `factory/pipeline.yml` is there and the factory's reader accepts it. The fault is the reader's fault text, the same as in the stop `pipeline_definition_invalid`. |
| `makefile` | The makefile the definition names under `make_file`, else `Makefile` at the root, has a target for every project command the definition names under `project_commands`, and for `sync`. A target in a file it includes counts, through any depth of includes. |
| `stage file` | `<project>/factory/stage.Containerfile`, when the project has one, follows the rules of a project's stage file (see *The project's stage file* in [machine.md](machine.md)). Without the file the project runs on the factory's stage image, which is no fault. |
| `agents` | Every role of the definition has an agent: the project's own `factory/agents/<role>.md` at `HEAD`, else the installed one (see *A project's own agents* in [agent-runtime.md](agent-runtime.md)). |
| `write paths` | Every write path of every role matches at least one tracked file. A write path with a placeholder such as `{work_item}` is not judged. |
| `forms` | `factory/story-form.md` and `factory/feature-form.md` are there. |

Without a valid pipeline definition the points `makefile`, `agents` and `write paths` cannot be judged: their lines read `skipped: no valid pipeline definition`. `stage file` and `forms` are judged all the same.

### Reference

The lines:

- A point without a fault: `<point>: ok`.
- A point with faults: `<point>: FAIL: <fault>; <fault>`.
- A point not judged: `<point>: skipped: no valid pipeline definition`. It counts as no fault.
- The last line: `project: ready`, or `project: not ready (<n> faults)` with the number of all faults (`(1 fault)` for one).

The faults:

| Fault | Point |
|---|---|
| `factory/pipeline.yml is missing` | `pipeline definition` |
| the fault text of the definition's refusal | `pipeline definition` |
| `<makefile> is missing`, such as `Makefile is missing` or `factory/Makefile is missing` | `makefile`; `<makefile>` is the file `make_file` names, else `Makefile`. A root `Makefile` does not stand in for a named one that is missing. |
| `no target <name>` | `makefile` |
| `<including file>: included file <path> is missing` | `makefile`; an `include` whose file is not committed, or lies outside the repository. A `-include` or `sinclude` whose file is missing is no fault. |
| the reason the stage file is refused, such as two `FROM` lines | `stage file` |
| `role <role>: no agent file` | `agents` |
| `role <role>: <fault>` | `agents`; the agent file's fault, as in the stop `agent_definition_invalid` |
| `role <role>: write path <pattern> matches no tracked file` | `write paths` |
| `factory/story-form.md is missing`, `factory/feature-form.md is missing` | `forms` |

How the makefile is read: a rule line starts at column 0 with one or more names of letters, digits, `_`, `.` and `-`, then `:` or `::`. An assignment (`X := 1`), an indented line, a comment and a pattern or variable rule (`%.o: %.c`, `$(T): u`) give no target. An include line starts at column 0 with `include`, `-include` or `sinclude`, then a space or a tab; a `#` ends its paths, and a path that holds `$` is left out. Every included path is taken from the root of the repository, also in a makefile that `make_file` names in a folder, as make takes it, and each file is read once, so an include cycle ends.

The usage is `factory-check-project [--agent-home <dir>] <folder>`. `--agent-home` wins over `FACTORY_CLAUDE_HOME`.

The exit status:

| Status | Meaning |
|---|---|
| 0 | the project is ready: no point has a fault |
| 1 | at least one point has a fault |
| 2 | the command could not do its job. No folder or more than one was given, or no agent home is known, and it prints the usage line on standard error. Or the folder is no git repository or has no commit at `HEAD`, and it prints `cannot read <folder>: <reason>` on standard error. |

## Checking a story before it starts

`factory-check-story` checks story files against where they sit and against your project's `factory/story-form.md`. Run it from the root of a checkout, with the paths relative to that root. The checkout needs `factory/story-form.md`, a `feature.md` in each feature's directory, and the stories in [`backlog`](../project-guide/glossary.md), `in-progress` or `done`.

1. Go to the root of the checkout.
2. Run the command with one or more paths, as in the example below.
3. Read the lines it prints. A story that fits the form prints `<path>: ok`. Every finding is a line of its own, and the table below says what to do.

`python -m factory.entry.check_story <path>...` does the same; use it with `uv run` in the factory's own checkout. The example builds a story in a new folder, so you can see both results.

```console
$ mkdir -p factory/features/F0001-example/backlog
$ printf '# Feature\n' > factory/features/F0001-example/feature.md
$ printf '# A story\n\n## Description\n\nText.\n\n## Interface\n\nText.\n\n## Acceptance criteria\n\n1. It works.\n2. `make check` stays green.\n3. docs: none.\n\n## Smoke test\n\n```sh\necho hi\n```\nExpect: `hi`\n\n## Journal\n' > factory/features/F0001-example/backlog/F0001-S0001-example-story.md
$ factory-check-story factory/features/F0001-example/backlog/F0001-S0001-example-story.md
factory/features/F0001-example/backlog/F0001-S0001-example-story.md: ok
$ factory-check-story docs/pipeline.md
docs/pipeline.md: not a work item location: expected factory/features/<feature>/<backlog|in-progress|done>/<file>.md
$ factory-check-story
usage: factory-check-story <path>...
```

For each path, in the order given, the command prints `<path>: ok`, or one line per finding. A finding with a line reads `<path>:<line>: <message>`, where the line counts from 1 in the story's text after the front matter. A finding without a line reads `<path>: <message>`. Findings about where the file sits come first, then those about its content.

The exit status:

| Status | Meaning |
|---|---|
| 0 | every file is ok |
| 1 | at least one file has a finding |
| 2 | the command could not do its job. There was no path, and it prints the usage line. Or `factory/story-form.md` is unreadable. Or a file does not exist or is not UTF-8, and it prints `cannot read <path>: <reason>`. Nothing more is checked after such a file; what was printed before stays. |

### Where a story may sit

A path must be `factory/features/<feature directory>/<backlog|in-progress|done>/<file>.md`. Otherwise the only line is `not a work item location: ...` and the file is not read, so it need not exist. `drafts` and `ongoing` are not work item locations.

How a file is read depends on its folder and on whether it has front matter:

- A story in `backlog` is read as a specification. Front matter there is a finding.
- A story in `in-progress` or `done` with front matter is read as a work item, and its state is checked too.
- A story there without front matter is a started story as you moved it on `develop`, where the state lives on the work item's branch. It is checked like a backlog story, with no complaint about missing state.

### The findings

Findings about the place:

| Finding | What to do |
|---|---|
| `the file name "<name>" is not F0000-S0000[-slug].md` | rename the file; an acceptance's name is not a story's |
| `the feature directory "<directory>" is not F0000[-slug]` | rename the directory |
| `the story <id> is in the directory of feature <id>` | move the story to its own feature's directory, or fix its id |
| `the feature file feature.md is missing in factory/features/<directory>` | add the feature's `feature.md` |

Findings about the content follow the form check (`docs/project-guide/work.md`, "The form check of a story"):

| Finding | What to do |
|---|---|
| `the story has no title line` | start the story with a `# Title` line |
| `missing section: ## <heading>` | add the section your story form lists |
| `criterion numbered <n> where <m> is expected` | renumber the criteria 1, 2, 3 |
| `the second-to-last criterion must contain "make check" and "green"`; `the last criterion must start with "docs:"` | make those the two closing criteria |
| `the Smoke test has no code block`; `the code block opened at line <n> is not followed by an "Expect:" line` | give each block of the smoke test an `Expect:` line after it |
| `journal entry numbered <n> where <m> is expected` | renumber the [journal](../project-guide/glossary.md) entries |
| `a backlog story carries no front matter: <keys>`; `a backlog story carries no journal entries` | remove the front matter or the entries; the factory writes them when the story starts |
| `the story has no state`; `the journal data lists <n> entries but the text shows <m>` | for a file with front matter in `in-progress` or `done`: the state is damaged, so restore the file from its work item's branch |
| a reader fault such as `unknown key: <key>` or `front matter is not valid YAML` | fix the front matter; no form findings are given until it reads |
