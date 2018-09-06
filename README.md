# SemanticCrashBucketing

## Setup

### Project Dependencies

Install these:

```
sudo apt-get install libc6-dbg gdb valgrind gfortran autoconf \
libtidy-dev libedit-dev libjpeg-turbo8-dev libreadline-dev \
libcurl4-gnutls-dev libmcrypt-dev libxslt-dev libbz2-dev \
tcl libxml2-dev libgdk-pixbuf2.0-dev libglib2.0-dev libnfnetlink-dev \
libnetfilter-conntrack-dev libnetfilter-conntrack3 libmnl-dev bison flex \
libgc-dev gettext python-pip

sudo pip install requests
```

### Environment setup

Disable userspace ASLR:

```
setarch $(uname -m) -R /bin/bash
```

Setup `PYTHONPATH`:

```
export PYTHONPATH=$(pwd)/src:$(pwd)/src/experiments
```

### Run everything

```
make
```


### One click script/VM:

Coming soon!
