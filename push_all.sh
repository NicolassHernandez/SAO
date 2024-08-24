#!/bin/bash
auto-changelog -p
cd docs
make html
open build/html/index.html
cd ..
git add .
git status
git add CHANGELOG.md
git commit -m "Update all"
git push origin main

# update the changelog before any coommit 
# ./push_changelog.sh
