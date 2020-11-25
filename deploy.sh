#!/bin/bash
echo -e "Deploying updates to GitHub..."
hugo
#rm -rf docs
cp -r public/ docs/
git add --all && git commit -m "Publishing to master"
git push origin master --verbose
#rm -f public/recordings/*
#cd static/recordings/
#for i in `ls *.mp4`; do tar -cvzf $i.tar.gz $i; mv $i /tmp/recording/; done
#rm -rf docs
 
#cd public && git add --all && git commit -m "Publishing to gh-pages" && cd ..
#git push origin gh-pages 

# Build the project.
#hugo # if using a theme, replace with `hugo -t <YOURTHEME>`
#
## Go To Public folder
#cd public
## Add changes to git.
#git add .
#
## Commit changes.
#msg="rebuilding site `date`"
#if [ $# -eq 1 ]
#  then msg="$1"
#fi
#git commit -m "$msg"
#
## Push source and build repos.
##git pull origin master --rebase
##git push origin master
#
#
## Come Back up to the Project Root
#cd ..
#
#git push origin master
#
