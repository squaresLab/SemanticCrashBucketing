#!/bin/bash

git clone https://github.com/tats/w3m.git

cd w3m
git checkout f9adc2d4b4
./configure CFLAGS='-ggdb -O0'
make -j
cd ..
