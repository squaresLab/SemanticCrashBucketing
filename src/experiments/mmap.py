import os
from debug import *
from fileio import *

mmap_out_file = "mmap.out" # cf dump_map.py

def dump_memory_map(binary, args, crash_file):
    # run gdb and dump mmap.out in current dir
    os.system('gdb -q -ex "source dump_mmap.py" -ex "run %s %s" "%s"' % \
             (args,crash_file,binary))
    mmap = rof(mmap_out_file)
    return mmap

custom_mmap2=\
"""
    0x7ffff30c7000     0x7ffff3105000    0x3e000        0x0
    0x7ffff3105000     0x7ffff3139000    0x34000        0x0 /home/vagrant/repfuzz/experiments/in-progress/R/R-3.3.2/library/grDevices/libs/grDevices.so
    0x7ffff3139000     0x7ffff3338000   0x1ff000    0x34000 /home/vagrant/repfuzz/experiments/in-progress/R/R-3.3.2/library/grDevices/libs/grDevices.so
    0x7ffff3338000     0x7ffff333d000     0x5000    0x33000 /home/vagrant/repfuzz/experiments/in-progress/R/R-3.3.2/library/grDevices/libs/grDevices.so
    0x7ffff333d000     0x7ffff333f000     0x2000    0x38000 /home/vagrant/repfuzz/experiments/in-progress/R/R-3.3.2/library/grDevices/libs/grDevices.so
"""

def extract_memory_map(memorymap):
    # key: lib name; value: lowest base range encountered
    d = {}
    for line in memorymap:
        line = line.split()
        if len(line) == 5:
            base_range = line[0].split('-')[0]
            path = line[4]
            path = os.path.basename(path)
            if path in d.keys():
                if base_range < d[path]:
                    d[path] = base_range
            else:
                d[path] = base_range
        else:
            continue

    if DEBUG:
        print '[DEBUG MMAP] done processing memory map, is',d
    return d
