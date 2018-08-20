#!/bin/bash

# Compile and deploy static assets
SCRIPTS_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="${SCRIPTS_PATH}/../"
MANAGE_FILE="${PROJECT_PATH}manage.py"

$SCRIPTS_PATH/static_compile.sh
python $MANAGE_FILE collectstatic --noinput
