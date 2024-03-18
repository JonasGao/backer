#!/usr/bin/env bash
set -e
BASE_DIR=$(dirname "$0")
SYNC_REPOS="$BASE_DIR/sync.txt"
echo "Using repo list: $SYNC_REPOS"
while IFS="," read -r owner repo branch my_repo
do
  printf "\e[33m== Sync repo '%s' branch '%s' ==\e[0m\n" "${owner}/${repo}" "${branch}"
  git clone --branch "$branch" "https://github.com/${owner}/${repo}.git" "$repo"
  pushd "$repo" || exit 1
  git remote add backup "https://${RK}@github.com/JonasGao/${my_repo}.git"
  git push backup HEAD:main
  popd || exit 2
done < "$SYNC_REPOS"
