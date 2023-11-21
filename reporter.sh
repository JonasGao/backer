#!/usr/bin/env bash
while read -r line
do
  echo "Fetching repo '$line' info"
  gh api "repos/$line" > repo.txt
  gh api "repos/$line/commits" > lcom.txt
  gh release view --repo "$line" --json name,publishedAt > rele.txt
  # Parse data into one row, html to report.html, txt to report.txt
  python ./parser.py "$line"
  echo "Fetched and parsed repo '$line' information."
done < ./repos.txt
# Send report.html
# report.txt will upload to artifacts
python ./mail.py
