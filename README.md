# SemanticCrashBucketing

## VM

[Download the VM here](https://cmu.box.com/s/upvblwni31ykwl9ow66vrjtqqcv2of9q). It has all of the scripts pre-configured, and all the the dependencies pre-installed. Typical use is VirtualBox, 1 vCPU, and at least 4GB RAM (6GB RAM recommended). See the `README.md` in the VM for more information.

## Running from source

### Project Dependencies

Install these:

```
sudo apt-get install libc6-dbg gdb valgrind gfortran autoconf \
libtidy-dev libedit-dev libjpeg-turbo8-dev libreadline-dev \
libcurl4-gnutls-dev libmcrypt-dev libxslt-dev libbz2-dev \
tcl libxml2-dev libgdk-pixbuf2.0-dev libglib2.0-dev libnfnetlink-dev \
libnetfilter-conntrack-dev libnetfilter-conntrack3 libmnl-dev bison flex \
libnetfilter-cttimeout-dev libssl-dev libgc-dev gettext python-pip re2c \
libicu-dev liblzma-dev`

sudo pip install requests
```

Run `./3-build.sh` in each project directory in `src/complete/ground-truth`

### Environment setup

```
git clone https://github.com/squaresLab/SemanticCrashBucketing.git && cd SemanticCrashBucketing
```

Disable userspace ASLR:

```
setarch $(uname -m) -R /bin/bash
```

Start the patch server:

```
make
```

Setup `PYTHONPATH`:

```
cd src
export PYTHONPATH=$(pwd):$(pwd)/experiments
```

Run everything:

```
python master.py
```

When finished, run `make clean`

### Directory structure

For each project under `src/complete`:

- `GENERATED_T_HAT`: generated patches
- `truth`: developer fixes and crashing inputs
- `derived/afl-tmin/bff-5/bff-1/hf/hfcov`: derived crashing inputs and deduplicated inputs for each fuzzer configuration
