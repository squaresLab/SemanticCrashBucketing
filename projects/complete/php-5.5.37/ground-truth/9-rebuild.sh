#!/bin/bash

BUILD_DIR=$(pwd)/php

make -C $BUILD_DIR/source/5.5.37 -j20
