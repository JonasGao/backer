#!/usr/bin/env bash
[ -f report.txt ] && mv report.txt latest_report.txt
while read -r line
do
  gh api "repos/$line" > repo.txt
  gh release view --repo "$line" --json name,publishedAt > rele.txt
  gh api "repos/$line/commits" > lcom.txt
  # Parse data into one row, html to report.html, txt to report.txt
  python ./parser.py "$line"
done < ./repos
# Send report.html
# report.txt will upload to artifacts
python ./mail.py