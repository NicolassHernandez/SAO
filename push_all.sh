#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
    echo "Error: No commit message provided."
    echo "Usage: ./push_all.sh 'Your commit message'"
    exit 1
fi

# Extract the commit message from the first argument
COMMIT_MESSAGE="$1"

auto-changelog -p
cd docs
make html
open build/html/index.html
cd ..
git add .
git status
git add CHANGELOG.md
git commit -m "$COMMIT_MESSAGE"
git push origin main

echo "Successful push_all execution!"
