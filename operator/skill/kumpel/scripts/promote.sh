#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Promote develop to main after the acceptance of feature <id>, which must be archived on develop:
# open a pull request from develop to main that lists the feature's stories, or, when one is still
# open, add the feature's stories to its body; then merge it with a merge commit when the switch
# promote is on, or with it off print its number for the human. The hosting service refuses a
# second open pull request for the same head and base, and the open one already carries develop's
# tip. Never squash or rebase: main keeps develop's commits as they are.
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

open_pulls=$(hosting_repo_api GET \
  "/pulls?state=open&base=main&head=${SITE_REPOSITORY%%/*}:develop&per_page=1") || exit $?

# Reads the open promotions from its third argument and prints one line: the action (open, patch
# or keep), the pull request's number (- when it is to be opened) and the JSON body to send.
# The feature's block lists one line per story, its id and the title of its file; the title is the
# first heading, since a finished story opens with its front matter.
promotion_plan() {
  python3 -I - "$1" "$2" "$3" <<'PY'
import json, pathlib, sys
feature_id, folder, open_list = sys.argv[1:]
lines = []
for story in sorted(pathlib.Path(folder).glob(f"*/{feature_id}-S*.md")):
    headings = [line for line in story.read_text(encoding="utf-8").splitlines() if line.startswith("# ")]
    title = headings[0].removeprefix("# ").strip() if headings else ""
    lines.append(f"- {'-'.join(story.stem.split('-')[:2])}: {title}")
block = f"The stories of {feature_id}:\n\n" + "\n".join(lines)
open_pulls = json.loads(open_list)
if not open_pulls:
    request = {"head": "develop", "base": "main", "title": f"{feature_id}: promoted to main", "body": block}
    print("open", "-", json.dumps(request))
    sys.exit(0)
promotion = open_pulls[0]
body = promotion.get("body") or ""
if block in body:
    print("keep", promotion["number"], "{}")
else:
    print("patch", promotion["number"], json.dumps({"body": body + "\n\n" + block}))
PY
}

plan=$(promotion_plan "$id" "$feature" "$open_pulls") || exit 1
action=${plan%% *}
rest=${plan#* }
number=${rest%% *}
request=${rest#* }
case $action in
  open)
    opened=$(hosting_repo_api POST /pulls "$request") || exit 1
    number=$(printf '%s' "$opened" | python3 -I -c 'import json, sys; print(json.load(sys.stdin)["number"])')
    state=opened
    ;;
  patch)
    hosting_repo_api PATCH "/pulls/$number" "$request" >/dev/null || exit 1
    state=open
    ;;
  *)
    state=open
    ;;
esac
if [ "$switch" != on ]; then
  echo "promotion $state: #$number, for the human to merge"
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
