# The factory's part of a project's makefile (kumpel-factory's kit). The project's makefile includes
# it as its first line, `include factory/kit.mk`, and then defines `sync`, `lint`, `test` and `check`.
# This file is the kit's: an upgrade of the kit replaces it, so a project does not edit it.

# One shell per recipe, stopped by its first failing line, so that a recipe can time itself.
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:
.SILENT:
.DEFAULT_GOAL := check

# `$(start)` opens a recipe and `$(green)` ends it with "<target>: green (<seconds> s)", the line
# the factory's records of project commands read. `check` itself ends with `echo "check: green"`.
start = started=$$(date +%s%N)
green = tenths=$$(( ($$(date +%s%N) - started) / 100000000 )); echo "$@: green ($$((tenths / 10)).$$((tenths % 10)) s)"

# Start facts: the factory runs these before an agent and puts their output into its first
# message; never part of `check`. The base is where the branch left the working branch.
# A project sets WORKING_BRANCH when its working branch is not `develop`, and FACTS_LEFT_OUT to
# the git pathspecs of files no agent needs to see, such as ':!build.lock' for a lockfile.
WORKING_BRANCH ?= develop
FACTS_LEFT_OUT ?=
facts_base = $$(git merge-base HEAD origin/$(WORKING_BRANCH))
facts_paths = . ':!factory' $(FACTS_LEFT_OUT)

.PHONY: facts-diff facts-changes facts-files

# The branch's changes: the file list with counts, then the whole diff.
facts-diff:
	base=$(facts_base); git diff --stat "$$base" -- $(facts_paths); echo; git diff "$$base" -- $(facts_paths)

# The changed and new files, by name and status.
facts-changes:
	base=$(facts_base); git diff --name-status "$$base" -- $(facts_paths); git ls-files --others --exclude-standard

# The tracked files without the factory's own.
facts-files:
	git ls-files -- $(facts_paths)
