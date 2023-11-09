#!/bin/bash

# script to update the version number in the site

# Ensure that the user has provided a valid argument
case $1 in
    patch)
        ;;
    minor)
        ;;
    major)
        ;;
    *)
        echo "Usage: $0 [patch|minor|major]"
        VERSION=$(node -p "require('./package.json').version")
        echo "Current version: $VERSION"
        exit 1
        ;;
esac



# Ensure that the working directory is clean
if [[ $(git status -s) ]]
then
    echo "Working directory is not clean! Please commit all changes before running this script."
    exit 1
fi

# Ensure that the local branch is up to date with the remote branch
git pull

# goto script directory
cd "$(dirname "$0")"

# build front-end
yarn install
yarn build
# increment front-end version
npm version $1 --no-git-tag-version

if [ $? -ne 0 ]; then
  exit 1
fi
# get current package version
VERSION=$(node -p "require('./package.json').version")

# update poetry version
poetry version $VERSION

git commit -am v${VERSION}
git tag -a -m v${VERSION} v${VERSION}
git push --follow-tags
