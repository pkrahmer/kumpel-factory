#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Archive feature <id> once it is finished: no story file left in its backlog/ or in-progress/,
# and its last acceptance in done/ with `outcome: accepted` in its front matter. Moves
# factory/features/<id>-.../ to factory/archive/ on develop, commits "<id>: archived" as Kumpel,
# pulls and pushes. A promotion reads it there.
#   archive-feature.sh <feature id, e.g. F0047>
set -eu
[ $# -eq 1 ] || { echo "usage: archive-feature.sh <feature id, e.g. F0047>" >&2; exit 2; }
here=$(cd "$(dirname "$0")" && pwd -P)
. "$here/../../../lib/site.sh"
. "$here/../../../lib/hosting.sh"
. "$here/kumpel-commit.sh"
id=$1
cd "$(sh "$here/settings.sh" get checkout)"
git checkout -q develop
hosting_git pull -q --no-rebase
feature=$(ls -d factory/features/"$id"-*/ 2>/dev/null | head -n 1)
[ -n "$feature" ] || { echo "archive-feature.sh: no feature $id in factory/features/" >&2; exit 1; }
feature=${feature%/}

refuse() {
  echo "archive-feature.sh: $id is not finished: $1" >&2
  exit 1
}

for folder in backlog in-progress; do
  for story in "$feature/$folder/$id"-S*.md; do
    if [ -f "$story" ]; then refuse "$story is in $folder/"; fi
  done
done
# Acceptance ids count up (A0001, A0002, ...), so the last one sorts last among every folder's.
last=$(ls "$feature"/*/"$id"-A*.md 2>/dev/null | awk -F/ '{print $NF "\t" $0}' | sort | tail -n 1 | cut -f2)
[ -n "$last" ] || refuse "it has no acceptance"
[ "$(basename "$(dirname "$last")")" = done ] || refuse "its last acceptance $last is not in done/"

# The factory books a refused acceptance in done/ too; only its front matter tells the two apart.
# The front matter is the block between the first two `---` lines; without a closing one there is none.
accepted() {
  awk '
    $0 == "---" { fences++; if (fences == 2) exit; next }
    fences == 1 && $0 == "outcome: accepted" { found = 1 }
    END { exit !(found && fences == 2) }
  ' "$1"
}
accepted "$last" || refuse "its last acceptance $last is not accepted"

mkdir -p factory/archive
git mv "$feature" factory/archive/
kumpel_commit "$id: archived"
hosting_git pull -q --no-rebase
hosting_git push -q origin develop
git log --oneline -1
