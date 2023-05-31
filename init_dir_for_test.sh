#!/bin/bash

mkdir client
mkdir server

cd server || exit
git init --bare .
cd hooks || exit
ln -s ../../hook-py/post-receive post-receive 
cd ../.. || exit

cd client || exit
git init
git remote add deploy ../server
git checkout -b prod
cd .git/hooks || exit
ln -s ../../../hook-py/pre-commit pre-commit
cd ../../../ || exit


echo 'test' >> 'client/test' && echo 'test' >> 'client/test2'  && git -C './client' add . && git -C './client' commit -am "test" -m '!migrate' && git -C './client' push --set-upstream deploy prod && git -C './client' push deploy