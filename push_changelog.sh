#!/bin/bash
auto-changelog -p
git add CHANGELOG.md
git commit -m "Update changelog"
git push origin main

# update the changelog before any coommit 
# ./push_changelog.sh
