#!/usr/bin/env bash
while read -r line
do
  gh api "repos/$line" > repo.txt
  gh release view --repo "$line" --json name,publishedAt > rele.txt
  gh api "repos/$line/commits" > lcom.txt
  python ./parser.py "$line" >> report.txt
done < ./repos
python ./mail.py < report.txt
rm report.txt