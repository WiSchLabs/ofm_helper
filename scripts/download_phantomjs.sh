#!/usr/bin/env bash

PHANTOM_VERSION="2.1.1"
PHANTOM_JS="phantomjs-$PHANTOM_VERSION"

wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS-linux-x86_64.tar.bz2 -O $PHANTOM_JS.tar.bz2
while [ $? -ne 0 ]
do
    wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS-linux-x86_64.tar.bz2 -O $PHANTOM_JS.tar.bz2
done