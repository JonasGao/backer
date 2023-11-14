#!/usr/bin/env bash
set -e
while IFS="," read -r owner repo branch
do
  git clone --branch "$branch" "https://github.com/${owner}/${repo}.git" "$repo"
  pushd "$repo"
  git remote add backup "https://${RK}@github.com/JonasGao/${repo}.git"
  git push backup HEAD:main --force
  popd
done < ./sync.txt
