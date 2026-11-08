#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Start story <id>: move it from its feature's backlog/ to in-progress/ on develop, commit "<id>: start",
# pull and push, with Kumpel <kumpel@noreply.invalid> as its author. The factory claims it at its
# next tick.
#   start-story.sh <id>
set -eu
[ $# -eq 1 ] || { echo "usage: start-story.sh <story id, e.g. F0047-S0003>" >&2; exit 2; }
here=$(cd "$(dirname "$0")" && pwd -P)
. "$here/../../../lib/site.sh"
. "$here/../../../lib/hosting.sh"
. "$here/kumpel-commit.sh"
cd "$(sh "$here/settings.sh" get checkout)"
git checkout -q develop
hosting_git pull -q --no-rebase
file=$(ls factory/features/*/backlog/"$1"-*.md 2>/dev/null | head -n 1)
[ -n "$file" ] || { echo "start-story.sh: no story $1 in any backlog/" >&2; exit 1; }
folder=$(dirname "$(dirname "$file")")
mkdir -p "$folder/in-progress"
git mv "$file" "$folder/in-progress/"
kumpel_commit "$1: start"
hosting_git pull -q --no-rebase
hosting_git push -q origin develop
git log --oneline -1
