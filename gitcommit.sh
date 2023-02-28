#!/bin/sh

#COMMIT=`git log --color=never -1 --oneline | cut -d" " -f1`
#DATE=`git log --color=never -1 --date=iso | sed -ne "s/Date:\s\+\(.*\).*/\1/p" | cut -d" " -f1 | tr -d "-"`

#echo "$DATE".git"$COMMIT"
git describe --tags
