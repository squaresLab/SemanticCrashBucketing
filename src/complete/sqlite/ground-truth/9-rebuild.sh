#!/bin/bash

# recompile
cd sqlite
./configure CFLAGS='-D_FORTIFY_SOURCE=0 -ggdb -O0 -DSQLITE_ENABLE_FTS3=1 -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 -I./ext/fts3' --disable-amalgamation &> /dev/null
git rev-parse --git-dir >/dev/null || exit 1 && echo $(git log -1 --format=format:%H) > manifest.uuid && echo C $(cat manifest.uuid) > manifest && git log -1 --format=format:%ci%n | sed 's/ [-+].*$//;s/ /T/;s/^/D /' >> manifest
make -j  # &> /dev/null
COMPILE_RESULT=$?

cd ..

./run_sqlite3_once.sh &> /dev/null

# echo $COMPILE_RESULT
exit $COMPILE_RESULT
