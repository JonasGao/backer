#!/usr/bin/env bash
while read -r line
do
  gh api "repos/$line" | python ./parser.py "$line" >> report.txt
done < ./repos
python ./mail.py < report.txt
rm report.txt