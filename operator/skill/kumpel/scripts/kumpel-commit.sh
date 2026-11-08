# SPDX-License-Identifier: Apache-2.0
# Sourced by the scripts that commit, so that each of their commits names Kumpel as its author
# and committer while the clone's own identity stays the human's.
#   kumpel_commit <message>   commit what is staged, with Kumpel <kumpel@noreply.invalid>

kumpel_commit() {
  GIT_AUTHOR_NAME=Kumpel GIT_AUTHOR_EMAIL=kumpel@noreply.invalid \
    GIT_COMMITTER_NAME=Kumpel GIT_COMMITTER_EMAIL=kumpel@noreply.invalid \
    git commit -q -m "$1"
}
