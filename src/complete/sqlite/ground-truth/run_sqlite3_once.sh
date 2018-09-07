#!/bin/bash

sqlite/sqlite3 &

sleep 1 # give some time for sqlite 3 to start
PID=$!
echo "Killing ${PID}"
kill $PID

if [ ! -f sqlite/.libs/lt-sqlite3 ]; then
  echo FAILED!
else
  echo 'SUCCESS: lt-sqlite3 created!'
fi
