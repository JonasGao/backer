#!/usr/bin/env bash
set -e
BASE_DIR=$(dirname "$0")
SYNC_REPOS="$BASE_DIR/sync.txt"
echo "Using repo list: $SYNC_REPOS"
while IFS="," read -r owner repo branch my_repo
do
  git clone --branch "$branch" "https://github.com/${owner}/${repo}.git" "$repo"
  pushd "$repo"
  git remote add backup "https://${RK}@github.com/JonasGao/${my_repo}.git"
  git push backup HEAD:main
  popd
done < "$SYNC_REPOS"
