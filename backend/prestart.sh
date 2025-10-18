#!/bin/bash
set -e -x

# Check if Claude Code CLI is installed and working
echo 'Checking Claude Code CLI...'
uv run python -u scripts/healthchecks/claude_cli_check.py

until uv run python -u scripts/healthchecks/db_up_check.py
do
  echo 'Waiting for db services to become available...'
  sleep 1
done
echo 'DB containers UP, proceeding...'

exec "$@"
