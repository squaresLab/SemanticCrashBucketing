#!/bin/bash

# This file should:
# (1) Delete everything related to a project
# (2) Then build it from scratch

PROJ_ZIP=$(pwd)/zip/libmad-0.15.1b.tar.gz
MAKE_DIR=$(pwd)/libmad-0.15.1b

rm -r $MAKE_DIR # clean state
cp $PROJ_ZIP .
tar xvf libmad-0.15.1b.tar.gz

cd $MAKE_DIR

make clean

# generate symbols but disable debug mode
./configure CFLAGS='-ggdb -DNDEBUG'

make -j 20
make minimad

cd ..
