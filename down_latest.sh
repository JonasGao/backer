#!/usr/bin/env bash
id=$(gh run list --repo jonasgao/backer --workflow "Reporter reporting" --limit 1 --json databaseId -q ".[0].databaseId")
gh run download --repo jonasgao/backer "$id"
mv "report.txt/report.txt" "./latest_report.txt"
rm -rf "report.txt"
ll "latest_report.txt"
echo "Has download latest_report.txt successfully"