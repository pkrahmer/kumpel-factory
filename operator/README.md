# The operator folder

This folder holds what an operator runs next to a factory [instance](../docs/project-guide/glossary.md). That is the skill `kumpel`, the scripts for the site file and the Cloud Run job, and the files that set up a VM. It also holds the template of a new project. Kumpel is the product; kumpel-factory, this repository, is one of its components.

The skill lets an agent (Claude Code, or opencode at work) run an instance together with you. It watches the pull requests of the [work items](../docs/project-guide/glossary.md). It answers the factory's questions within the [feature](../docs/project-guide/glossary.md)'s decisions. It checks finished [stories](../docs/project-guide/glossary.md) and, when you allow it, merges them. It starts the next story, and it shapes stories and features on request. Its plan is in [DESIGN.md](../planning/operator-skill/DESIGN.md).

The skill is a trial. Nothing here is used until a trial at work with opencode against the Cloud Run job has shown that it holds. After that it moves to a repository of its own, `kumpel-skill`, and this folder goes.

What the folders hold:

- [`bin/`](bin/README.md) The commands for the site file and for cleaning text.
- [`claude/`](claude/README.md) The skill's command for Claude Code.
- [`job/`](job/README.md) The script of the Cloud Run job.
- [`lib/`](lib/README.md) The shell code the scripts share.
- [`opencode/`](opencode/README.md) The skill's command for opencode.
- [`skill/`](skill/README.md) The skill `kumpel`.
- `operator/template/` The start of a new project, copied into it; it carries no README of its own.
- [`vm/`](vm/README.md) The files that set up a VM.

Where to read next:

- [Setting up an operator's machine](../docs/operator-guide/site.md): the whole setup, from a machine with nothing on it to a running job and a skill that drives it.
- [The operator guide](../docs/operator-guide/README.md): install, configure and run an instance.

## Installing

1. Write the site file and fill in its values, at least `SITE_REPOSITORY` and `SITE_CHECKOUT`. The file never enters a repository. Run this from the root of this repository:

   ```console
   $ sh operator/bin/site init
   site: wrote <path>; edit it, then run: site check
   ```

2. Check the machine. Run this on the operator's machine, from the root of this repository. The command is read-only and ends with `site: ready` when every check passes:

   ```sh
   sh operator/bin/site check
   ```

3. Link the skill into Claude Code's skill folder. Both tools read that folder, so one copy serves both. Run this on the operator's machine, from the root of this repository:

   ```sh
   mkdir -p ~/.claude/skills
   ln -s "$(pwd)/operator/skill/kumpel" ~/.claude/skills/kumpel
   ```

4. Copy the command `/kumpel [<switch> on|off]` for your tool, and start the tool again so that it reads the skill list. Run these on the operator's machine, from the root of this repository. For opencode:

   ```sh
   cp operator/opencode/command/kumpel.md ~/.config/opencode/command/
   ```

   For Claude Code:

   ```sh
   cp operator/claude/commands/kumpel.md ~/.claude/commands/
   ```

5. Write the settings file. The skill takes the repository and the checkout from the site file. When the site file gives both, the settings file holds only the switches, and `init` takes no argument. Run this on the operator's machine, from the root of this repository:

   ```sh
   sh operator/skill/kumpel/scripts/settings.sh init
   ```

   Otherwise, run this on the operator's machine, from the root of this repository:

   ```sh
   sh operator/skill/kumpel/scripts/settings.sh init <owner/name> <checkout>
   ```

   The file is `~/.config/kumpel/settings.json`, or the path in `KUMPEL_SETTINGS`. A new file has `merge` and `promote` off, and `answer` and `start_next` on. A file written before `promote` existed lacks it: `get promote` reads it as off, and `set promote on` adds it.

## What you need

- `git`, `curl`, `python3` and a POSIX shell.
- A hosting-service token, from `SITE_TOKEN_CMD` in the site file or, without it, from a `gh` login.
- `gcloud`, for an instance in a Cloud Run job: it creates the job and reads its log when a [stop](../docs/project-guide/glossary.md) needs its reason. The status of the work items comes from the hosting service alone.

## How Kumpel's acts are told from yours

Kumpel works with your token, so it signs everything it does. A reader of the pull request, the journal or the history can then tell its acts from yours.

- A comment ends with the line `— Kumpel, for the human who owns this project` and the marker `<!-- kumpel -->`.
- Every commit Kumpel makes (a start, an archive of a finished feature) has `Kumpel <kumpel@noreply.invalid>` as author and committer. Kumpel commits and pushes to `develop`, the factory's working branch, and never to `main`: `main` changes only when a promotion pull request from `develop` is merged.
- A merge commit says `Merged by Kumpel after the six approval checks.` These are the six checks Kumpel judges on a story at the [approval](../docs/project-guide/glossary.md) stage; [approving.md](skill/kumpel/references/approving.md) lists them.

## Reference

### Files

| Path | Use |
|---|---|
| `operator/site.env.example` | every key of the site file, each with a comment and a made-up value |
| `operator/lib/site.sh` | the loader every operator script sources: `site_path`, `site_load`, `site_require`, `site_value` |
| `operator/lib/hosting.sh` | the hosting client: `hosting_token`, `hosting_api`, `hosting_repo_api`, `hosting_git`, with the token from `SITE_TOKEN_CMD` or `gh` |
| `operator/bin/site` | the command for the site file: `path`, `init`, `show`, `get`, and `check`, the read-only checks that say whether a machine is ready |
| `operator/bin/sanitise` | strips the site's names and the tokens from text that leaves the machine; `sanitise check FILE...` proves a file clean |
| `operator/job/job.sh` | the factory's Cloud Run job: `create`, `update`, `execute`, `delete`, `log`, `status` |
| `operator/skill/kumpel/SKILL.md` | the skill: what to read first, the loop, the switches |
| `operator/skill/kumpel/references/` | the standing orders, how to answer, how to approve, how to shape |
| `operator/skill/kumpel/scripts/settings.sh` | the switches, and the repository and checkout when the site file does not give them |
| `operator/skill/kumpel/scripts/status.sh` | the state of the work items' pull requests, from the hosting service |
| `operator/skill/kumpel/scripts/wait.sh` | waits for the next event |
| `operator/skill/kumpel/scripts/approval.sh` | the six approval checks' facts |
| `operator/skill/kumpel/scripts/next-story.sh` | the next story of the build order |
| `operator/skill/kumpel/scripts/start-story.sh` | starts a story |
| `operator/skill/kumpel/scripts/comment.sh` | posts a signed comment |
| `operator/skill/kumpel/scripts/merge.sh` | merges an approved story and waits for its archive |
| `operator/skill/kumpel/scripts/reset-to-tag.sh` | resets a trial repository to a tag |
| `operator/skill/kumpel/scripts/archive-feature.sh` | moves a finished feature to `factory/archive/` on `develop`; a feature is finished only when its last acceptance report in `done/` says `outcome: accepted` in its front matter, so a refused acceptance is not archived |
| `operator/skill/kumpel/scripts/promote.sh` | opens the promotion of `develop` to `main` after a feature's accepted acceptance, or adds the feature's stories to the one still open, and merges it when `promote` is on |
| `operator/skill/kumpel/scripts/kumpel-commit.sh` | `kumpel_commit`: commits with Kumpel as author and committer |
| `operator/opencode/command/kumpel.md` | the command `/kumpel [<switch> on\|off]` for opencode |
| `operator/claude/commands/kumpel.md` | the same command for Claude Code |
| `operator/vm/setup.sh` | prepares a fresh Ubuntu machine and installs the factory's service |
| `operator/vm/factory.service` | the factory as a system service, one instance per name |
| `operator/vm/Dockerfile` | the stage image of every stage's containers |
| `operator/vm/git-credential-factory` | git's credential helper, which hands out the hosting token |
| `operator/vm/job-start.sh` | the command of a Cloud Run job: it builds an instance and ends in `factory-run` |
| `operator/template/` | the start of a new project: a [pipeline definition](../docs/project-guide/glossary.md), a `CLAUDE.md` and a `Makefile` |

### Settings

The switches live in the settings file. Change one with the command `/kumpel <switch> on|off` or with `sh operator/skill/kumpel/scripts/settings.sh set <switch> on|off`. `KUMPEL_SETTINGS` is an environment variable, not a key in the file.

| Name | What it does | Default | Example |
|---|---|---|---|
| `merge` | Kumpel merges an approved story itself | off | `/kumpel merge on` |
| `answer` | Kumpel answers the factory's questions | on | `/kumpel answer off` |
| `start_next` | Kumpel starts the next story when one is archived | on | `/kumpel start_next off` |
| `promote` | Kumpel merges the promotion of `develop` to `main` after a feature's acceptance; with it off, Kumpel opens the pull request and you merge it | off | `/kumpel promote on` |

The environment variable:

| Name | What it does | Default | Example |
|---|---|---|---|
| `KUMPEL_SETTINGS` | the path of the settings file | `~/.config/kumpel/settings.json` | `/tmp/kumpel.json` |
