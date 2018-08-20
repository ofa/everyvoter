#!/bin/bash

# Compile and deploy static assets
SCRIPTS_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="${SCRIPTS_PATH}/../"
MANAGE_FILE="${PROJECT_PATH}manage.py"
GULP="${PROJECT_PATH}node_modules/gulp/bin/gulp.js"

yarn --cwd $PROJECT_PATH install
$GULP default --cwd $PROJECT_PATH
