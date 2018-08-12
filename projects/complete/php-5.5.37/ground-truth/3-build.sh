#!/bin/bash

if [ ! -d "$DIRECTORY" ]; then
  git clone https://github.com/php-build/php-build.git
fi

BUILD_DIR=$(pwd)/php
mkdir -p $BUILD_DIR
export PHP_BUILD_EXTRA_MAKE_ARGUMENTS="-j20"
export PHP_BUILD_TMPDIR=$BUILD_DIR
export PHP_BUILD_KEEP_OBJECT_FILES=yes
php-build/bin/php-build -i development 5.5.37 $BUILD_DIR

# crash from wget https://drive.google.com/uc\?id\=0B0D1DYQpkA9URnRROVdLdG5jdFE\&amp\;export\=download
