#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Promote develop to main after the acceptance of feature <id>, which must be archived on develop:
# open a pull request from develop to main that lists the feature's stories, and merge it with a
# merge commit when the switch promote is on; with it off, print its number for the human. Never
# squash or rebase: main keeps develop's commits as they are.
#   promote.sh <feature id, e.g. F0047>
set -eu
[ $# -eq 1 ] || { echo "usage: promote.sh <feature id, e.g. F0047>" >&2; exit 2; }
here=$(cd "$(dirname "$0")" && pwd -P)
. "$here/../../../lib/site.sh"
. "$here/../../../lib/hosting.sh"
SITE_REPOSITORY=$(sh "$here/settings.sh" get repository)
export SITE_REPOSITORY
id=$1
switch=$(sh "$here/settings.sh" get promote)
cd "$(sh "$here/settings.sh" get checkout)"
git checkout -q develop
hosting_git pull -q --no-rebase
feature=$(ls -d factory/archive/"$id"-*/ 2>/dev/null | head -n 1)
[ -n "$feature" ] || { echo "promote.sh: $id is not archived on develop" >&2; exit 1; }

# Prints the JSON body of the pull request: one line per story, its id and the title of its file.
pull_body() {
  python3 -I - "$1" "$2" <<'PY'
import json, pathlib, sys
feature_id, folder = sys.argv[1:]
lines = []
for story in sorted(pathlib.Path(folder).glob(f"*/{feature_id}-S*.md")):
    first = story.read_text(encoding="utf-8").splitlines()[:1]
    title = first[0].removeprefix("# ").strip() if first else ""
    lines.append(f"- {'-'.join(story.stem.split('-')[:2])}: {title}")
print(json.dumps({
    "head": "develop",
    "base": "main",
    "title": f"{feature_id}: promoted to main",
    "body": f"The stories of {feature_id}:\n\n" + "\n".join(lines),
}))
PY
}

opened=$(hosting_repo_api POST /pulls "$(pull_body "$id" "$feature")") || exit 1
number=$(printf '%s' "$opened" | python3 -I -c 'import json, sys; print(json.load(sys.stdin)["number"])')
if [ "$switch" != on ]; then
  echo "promotion opened: #$number, for the human to merge"
  exit 0
fi
# The merge commit says Kumpel promoted it, since the human's token makes it.
body=$(python3 -I -c '
import json, sys
number, feature_id = sys.argv[1:]
print(json.dumps({
    "merge_method": "merge",
    "commit_title": f"Merge pull request #{number} from develop",
    "commit_message": f"Promoted by Kumpel after {feature_id}'"'"'s acceptance.",
}))
' "$number" "$id")
hosting_repo_api PUT "/pulls/$number/merge" "$body" >/dev/null || exit 1
echo "promoted #$number"
