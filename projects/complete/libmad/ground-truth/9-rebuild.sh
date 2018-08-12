#!/bin/bash

# This script rebuilds the project (e.g., after patching)

MAKE_DIR=$(pwd)/libmad-0.15.1b

# make clean
make -C $MAKE_DIR -j20
