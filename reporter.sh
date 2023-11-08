#!/usr/bin/env bash
while read -r line
do
  gh api "repos/$line" | python ./parser.py "$line"
done < ./repos