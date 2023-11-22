#!/usr/bin/env bash
./sync.sh
echo "Finish sync."
python ./reporter.py
echo "Finish report."
