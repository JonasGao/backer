#!/usr/bin/env bash
id=$(gh run list --repo jonasgao/backer --workflow "Reporter reporting" --status success --limit 1 --json databaseId -q ".[0].databaseId")
echo "Will download artifact by $id"
if gh run download --repo jonasgao/backer "${id//[$'\t\n\r']}"; then
  mv "report.txt/report.txt" "./latest_report.txt"
  rm -rf "report.txt"
  ls -al "latest_report.txt" && echo "Has download latest_report.txt successfully"
fi