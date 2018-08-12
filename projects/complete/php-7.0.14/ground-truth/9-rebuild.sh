#!/bin/bash

BUILD_DIR=$(pwd)/php

make -C $BUILD_DIR/source/7.0.14 -j20
