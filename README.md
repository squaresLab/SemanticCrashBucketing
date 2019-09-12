This page is about the code and data related to our ASE '18 paper
[Semantic Crash Bucketing](https://www.cs.cmu.edu/~rvantond/pdfs/scb-ase-2018.pdf).
<details>
  <summary>Click for Citation</summary>
  
```
@inproceedings{vanTonderSCB2018,
  author = {{van~Tonder}, Rijnard and Kotheimer, John and {Le~Goues}, Claire},
  title = {Semantic Crash Bucketing},
  booktitle = {International Conference on Automated Software Engineering},
  series = {ASE '18},
  year = {2018},
  doi = {10.1145/3238147.3238200}
}
```

</details>

## FAQ

> I have some patches, programs, and crashing inputs. Can I use this work to bucket the crashing inputs with patches? 

Yes: See the [bucket-by-patch](https://github.com/squaresLab/SemanticCrashBucketing/tree/master/bucket-by-patch) directory to do this with your own programs and patches.


## Data

Our data set curates 21 unique bugs, and for each bug gives:

- the crashing input to trigger the bug
- the isolated developer bug fix
- an autogenerated patch that mimics the developer bug fix (the patch causes the input to not crash the program)

Browse the data using the table below:

| Project       | ID | Bug kind        | Developer fix (ground truth)                                                                                                           | Autogenned patch                                                                                                                         | Crashing input                                                                                                                      | CVE            | Ref                                                                                                                                                 |
|---------------|----|-----------------|----------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| SQLite | 1  | Null-deref      | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p01.patch) | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p01.patch) | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash01.sql) | -              | [link](https://lcamtuf.blogspot.com/2015/04/finding-bugs-in-sqlite-easy-way.html)                                                                   |
| SQLite | 2  | Null-deref      | [p02.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p02.patch) | [p02.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p02.patch) | [02.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash02.sql) | -              | -                                                                                                                                                    |
| SQLite | 3  | Null-deref      | [p03.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p03.patch) | [p03.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p03.patch) | [03.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash03.sql) | -              | -                                                                                                                                                    |
| SQLite | 4  | Null-deref      | [p04.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p04.patch) | [p04.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p04.patch) | [04.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash04.sql) | -              | -                                                                                                                                                    |
| SQLite | 5  | Null-deref      | [p05.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p05.patch) | [p05.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p05.patch) | [05.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash05.sql) | -              | -                                                                                                                                                    |
| SQLite | 6  | Null-deref      | [p06.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p06.patch) | [p06.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p06.patch) | [06.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash06.sql) | -              | -                                                                                                                                                    |
| SQLite | 7  | Null-deref      | [p07.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p07.patch) | [p07.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p07.patch) | [07.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash07.sql) | -              | -                                                                                                                                                    |
| SQLite | 8  | Null-deref      | [p08.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p08.patch) | [p08.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p08.patch) | [08.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash08.sql) | -              | -                                                                                                                                                    |
| SQLite | 9  | Null-deref      | [p09.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p09.patch) | [p09.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p09.patch) | [09.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash09.sql) | -              | -                                                                                                                                                    |
| SQLite | 10 | Null-deref      | [p10.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p10.patch) | [p10.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p10.patch) | [10.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash10.sql) | -              | -                                                                                                                                                    |
| SQLite | 11 | Null-deref      | [p11.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p11.patch) | [p11.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p11.patch) | [11.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash11.sql) | -              | -                                                                                                                                                    |
| SQLite | 12 | Null-deref      | [p12.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/patches/p12.patch) | [p12.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/GENERATED_T_HAT/p12.patch) | [12.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/sqlite/ground-truth/truth/all/crash12.sql) | -              | -                                                                                                                                                    |
| w3m           | 13 | Null-deref      | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/patches/p01.patch)   | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/GENERATED_T_HAT/p01.patch)    | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/all/crash1.html)    | CVE-2016-9438  | [changelog](https://github.com/tats/w3m/blob/master/ChangeLog), [link](https://github.com/tats/w3m/commit/010b68580dc50ce183df11cc79721936ab5c4f25) |
| w3m           | 14 | Null-deref      | [p02.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/patches/p02.patch)   | [p02.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/GENERATED_T_HAT/p02.patch)    | [02.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/all/crash2.html)    | CVE-2016-9443  |  [link](https://github.com/tats/w3m/commit/ec9eb22e008a69ea9dc21fdca4b9b836679965ee)                                                                |
| w3m           | 15 | Null-deref      | [p03.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/patches/p03.patch)   | [p03.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/GENERATED_T_HAT/p03.patch)    | [03.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/all/crash3.html)    | -              | [link](https://github.com/tats/w3m/issues/32#issuecomment-260170163)                                                                                |
| w3m           | 16 | Null-deref      | [p04.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/patches/p04.patch)   | [p04.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/GENERATED_T_HAT/p04.patch)    | [04.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/w3m/ground-truth/truth/all/crash4.html)    | CVE-2016-9631  | [link](https://github.com/tats/w3m/commit/ecfdcbe1131591502c5e7f9ff4f34b24c5a2db97)                 |
| php-v5        | 17 | Null-deref      | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/php-5.5.37/ground-truth/truth/patches/p01.patch)  | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/php-5.5.37/ground-truth/GENERATED_T_HAT/p01.patch)  | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/php-5.5.37/ground-truth/truth/all/crash.jpg)  | CVE-2016-6292  | [link](https://bugs.php.net/bug.php?id=72618)                                                                                                       |
| php-v7        | 18 | Null-deref      | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/php-7.0.14/ground-truth/truth/patches/p01.patch)  | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/php-7.0.14/ground-truth/GENERATED_T_HAT/p01.patch)  | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/php-7.0.14/ground-truth/truth/all/crash.php)  | CVE-2016-10162 | [link](https://bugs.php.net/bug.php?id=73831)                                                                                                       |
| R             | 19 | Buffer overflow | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/R/ground-truth/truth/patches/p01.patch)           | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/R/ground-truth/GENERATED_T_HAT/p01.patch)      | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/R/ground-truth/truth/all/crash.enc)        | CVE-2016-8714  |  -                                                                                                                                                   |
| Conntrackd    | 20 | Buffer overflow | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/conntrackd/ground-truth/truth/patches/p01.patch)  | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/conntrackd/ground-truth/GENERATED_T_HAT/p01.patch) | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/conntrackd/ground-truth/truth/all/minimal.conf)         | -                                                | [link](http://git.netfilter.org/conntrack-tools/commit/?id=ce06fb6069065c3d68475356c0728a5fa0a4ab74)
| libmad        | 21 | Buffer overflow | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/libmad/ground-truth/truth/patches/p01.patch)      | [p01.patch](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/libmad/ground-truth/GENERATED_T_HAT/p01.patch) | [01.input](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/complete/libmad/ground-truth/truth/all/crash01.mp3) | -              | -                                                                                                                                                   |

If you want to run, compile, or apply patches, consider using the VM, described next.

## VM

The VM has all of the scripts pre-configured, and all the the dependencies pre-installed. Typical use is VirtualBox, 1 vCPU, and at least 4GB RAM (6GB RAM recommended). See the `README.md` in the VM for more information.
[Download the VM](https://zenodo.org/record/2646520#.XMTUmhNKiu4). 

## Running from source

Instructions for building each project locally from source, without the VM.

### Project Dependencies

Install these:

```
sudo apt-get install libc6-dbg gdb valgrind gfortran autoconf \
libtidy-dev libedit-dev libjpeg-turbo8-dev libreadline-dev \
libcurl4-gnutls-dev libmcrypt-dev libxslt-dev libbz2-dev \
tcl libxml2-dev libgdk-pixbuf2.0-dev libglib2.0-dev libnfnetlink-dev \
libnetfilter-conntrack-dev libnetfilter-conntrack3 libmnl-dev bison flex \
libnetfilter-cttimeout-dev libssl-dev libgc-dev gettext python-pip re2c \
libicu-dev liblzma-dev

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

For each project under `src/complete/<project>/ground-truth`:

- `GENERATED_T_HAT`: generated approximate patches
- `truth/patches`: ground truth patches (i.e., developer fixes)
- `truth/all`: crashing input files to use for generating a patch
- `{afl-tmin,bff-5,bff-1,hf,hfcov}/all/raw/*`: crashing inputs to bucket, separated by crashes generated by each fuzzer configuration
