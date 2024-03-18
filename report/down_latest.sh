#!/usr/bin/env bash
ACTION_NAME="Repo Jobs"
ARTIFACT_NAME="latest_data"
LATEST_RECORDS_NAME='latest_data.txt'
RECORDS_NAME="data.txt"
ID=$(gh run list --repo jonasgao/backer --workflow "$ACTION_NAME" --status success --limit 1 --json databaseId -q ".[0].databaseId")
ID="${ID//[$'\t\n\r']}"
echo "Will download artifact by $ID"
echo "First cleanup, remove ${LATEST_RECORDS_NAME}"
rm -vf "./${LATEST_RECORDS_NAME}"
if gh run download --repo jonasgao/backer "${ID}"; then
  echo "Download successfully"
  if mv "${ARTIFACT_NAME}/${RECORDS_NAME}" "./${LATEST_RECORDS_NAME}"; then
    rm -vrf "${ARTIFACT_NAME}"
    ls -al "${RECORDS_NAME}" && echo "Has download '${RECORDS_NAME}' successfully"
  else
    echo "Failure move '${ARTIFACT_NAME}/${RECORDS_NAME}', maybe its not exists"
  fi
else
  echo "Failure download..."
fi