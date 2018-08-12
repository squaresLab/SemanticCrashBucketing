#!/bin/bash

# clone sqlite
git clone https://github.com/mackyle/sqlite.git  

# set to the vulnerable revision
cd sqlite
git checkout 3ad59fc
cd ..
