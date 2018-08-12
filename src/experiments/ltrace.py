import find
import os
import re

from collections import OrderedDict

from addr2line import *
from debug import *
from fileio import *
from mmap import *

ltrace_file = "ltrace.out"

DEBUG_LTRACE = True

def addr_and_library_from_ltrace(line):

    m = re.search('\[.*?\].*\[(.*?)\].(.*?)->',line)
    if m and m.group(1) and m.group(2):
        addr = m.group(1)
        libname = m.group(2)
        return addr,libname
    return None

# returns the locations to patch (e.g., places where strcpy occurs in trace)
def process_ltrace(ltrace_output, mmap):

    ltrace_entries = []
    for line in ltrace_output:
        result = addr_and_library_from_ltrace(line)
        if result:
            ltrace_entries.append(result)

    ltrace_entries = list(OrderedDict.fromkeys(ltrace_entries)) # dedup and preserve order

    # only keep libraries that are in this project, not things like string3.h
    ltrace_entries = map(lambda result: \
                        (result[0], find.path_for_library_exists(result[1])), \
                         ltrace_entries)

    # BECAUSE PYTHON DOES NOT HAVE FILTER MAP
    ltrace_entries = filter(lambda result: result[1] != None, ltrace_entries)

    d = extract_memory_map(mmap)
    patch_locations = []
    for ltrace_addr,abs_path in ltrace_entries:
        abs_path = abs_path.strip()

        lib_basename = os.path.basename(abs_path)

        if DEBUG_LTRACE:
            print '[DEBUG LTRACE] ltrace_addr',ltrace_addr,'abs_path',abs_path
            print '[DEBUG LTRACE] lib_basename',lib_basename

        if lib_basename in d.keys():
            in_memory_addr = d[lib_basename]
            static_addr = int(ltrace_addr,16) - int(in_memory_addr,16)
            if DEBUG_RESOLVE_DYNLIB:
                print 'lib :',lib_basename,\
                      'ltrace_addr (',ltrace_addr,')',\
                      ' - mmap base addr (',in_memory_addr,')',\
                     ('= 0x%x' % static_addr)
            patch_location = addr2line(abs_path,static_addr)
            if patch_location:
                patch_locations.append(patch_location)

            # Add non-adjusted static addr if valid (e.g., for executables
            # and not dyn linked libs)
            static_addr = int(ltrace_addr, 16)
            patch_location = addr2line(abs_path,static_addr)
            if patch_location:
                patch_locations.append(patch_location)
        else:
            if DEBUG_LTRACE:
                print '[DEBUG LTRACE] lib_basename %s not in ltrace' % lib_basename

    return patch_locations

# returns result of running ltrace
def run_ltrace(binary, args, crash_file, ltrace_pattern):
    # run ltrace and read result
    cmd = "ltrace -e %s -f -i %s %s %s 2> %s" \
        % (ltrace_pattern, binary, args, crash_file, ltrace_file)

    exit = os.system(cmd)

    ltrace_output = rof(ltrace_file)

    if DEBUG_LTRACE:
        print "[DEBUG LTRACE] cmd:",cmd
        print "[DEBUG LTRACE] result:",ltrace_output

    return exit,ltrace_output

# ltrace -f -i cat ./crashing-inputs/sqlite-null-ptr1.sql | ./SQLite-b1ed4f2a/.libs/lt-sqlite3 -bail
def run_ltrace_stdin(binary, args, crash_file, ltrace_pattern):
    # run ltrace and read result
    cmd = "ltrace -f -i %s %s < %s 2> %s" \
        % (binary, args, crash_file, ltrace_file)

    exit = os.system(cmd)

    ltrace_output = rof(ltrace_file)

    if DEBUG_LTRACE:
        print "[DEBUG LTRACE] cmd:",cmd
        print "[DEBUG LTRACE] result:",ltrace_output

    return exit,ltrace_output
