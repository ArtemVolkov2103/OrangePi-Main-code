#!/bin/sh

# Checkout autobuild branch
cd ..
git clone https://github.com/user/repo.git --branch autobuild --single-branch repo_autobuild
cd repo_autobuild

# Copy newly created APK into the target directory
mv ../repo/app/build/outputs/apk/snapshot.apk ./autobuild

# Setup git for commit and push
git config --global user.email "travis@travis-ci.org"
git config --global user.name "Travis CI"
git remote add origin-master https://${AUTOBUILD_TOKEN}@github.com/user/repo > /dev/null 2>&1
git add ./autobuild/snapshot.apk

# We dont want to run a build for a this commit in order to avoid circular builds: 
# add [ci skip] to the git commit message
git commit --message "Snapshot autobuild N.$TRAVIS_BUILD_NUMBER [ci skip]"
git push origin-master