#!/bin/bash

# This script rebuilds the project (e.g., after patching)

source 0-config.sh

# make clean &> /dev/null
make -C $MAKE_DIR -j
cd ..
