#!/bin/bash

source 0-config.sh

# This file should:
# (1) Delete everything related to a project
# (2) Then build it from scratch

rm -r $MAKE_DIR # clean state
cp $PROJ_ZIP .
tar xvf $PROJ_ZIP

cd $MAKE_DIR

make clean

./configure --with-x=no

make -j 20

cd ..

cp driver.r R-3.3.2
