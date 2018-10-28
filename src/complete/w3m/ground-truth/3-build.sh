#!/bin/bash

git clone https://github.com/tats/w3m.git

cd w3m
git checkout 67be73b0
./configure CFLAGS='-ggdb -O0'
make -j
cd ..
