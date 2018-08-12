#!/bin/bash

# This script rebuilds the project (e.g., after patching)

# do not make clean for conntrackd, because it deletes the yacc
# generated code, which is where we patch.

MAKE_DIR=$(pwd)/conntrack-tools-1.4.3

make -C ${MAKE_DIR}
