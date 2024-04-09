#!/usr/bin/env bash
set -e
BASE_DIR=$(dirname "$0")
SYNC_REPOS="$BASE_DIR/sync.txt"
echo "Using repo list: $SYNC_REPOS"
while IFS="," read -r owner repo branch my_repo force
do
  printf "\e[33m== Sync repo '%s' branch '%s' ==\e[0m\n" "${owner}/${repo}" "${branch}"
  git clone --branch "$branch" "https://github.com/${owner}/${repo}.git" "$repo"
  pushd "$repo" || exit 1
  git remote add backup "https://${RK}@github.com/JonasGao/${my_repo}.git"
  if [ "$force" = "force" ]; then
    git push backup HEAD:main --force
  else
    git push backup HEAD:main
  fi
  popd || exit 2
done < "$SYNC_REPOS"
