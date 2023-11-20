#!/usr/bin/env bash
set -e
while IFS="," read -r owner repo branch my_repo
do
  git clone --branch "$branch" "https://github.com/${owner}/${repo}.git" "$repo"
  pushd "$repo"
  git remote add backup "https://${RK}@github.com/JonasGao/${my_repo}.git"
  git push backup HEAD:main
  popd
done < ./sync.txt
