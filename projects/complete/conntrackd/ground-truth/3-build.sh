#!/bin/bash

AFL_BUILDDIR=$(pwd)/afl-2.32b

cp zip/conntrack-tools-1.4.3.tar.bz2 .
tar xvfj conntrack-tools-1.4.3.tar.bz2

cd conntrack-tools-1.4.3

make clean

# generate gdb symbols (-ggdb) but don't compile -g/-O0
./configure CFLAGS='-D_FORTIFY_SOURCE=0 -ggdb -O1 -fno-stack-protector' --disable-shared --disable-cthelper

make -j 20

# do it again because for some reason it doesn't generate the right code
make clean

# generate gdb symbols (-ggdb) but don't compile -g/-O0
./configure CFLAGS='-D_FORTIFY_SOURCE=0 -ggdb -O1 -fno-stack-protector' --disable-shared --disable-cthelper

make -j 20

cd ..
rm conntrack-tools-1.4.3.tar.bz2
