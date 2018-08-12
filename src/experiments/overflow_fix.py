import re
import sys
import os
import subprocess

import crash_signal

from addr2line import *
from debug import *
from fileio import *
from ltrace import *
from mmap import *
from patching import *
from test import *

DEBUG_PATCH_LOCATIONS = True

DUMP_ALL_PATCHES = False


def run(binary, crash_file, args, \
        addr2line_offset, range_backward, range_forward, \
        bug_kind, source_dir, on_stdin, patch_path="p.patch", \
        line_num_offset=0):
    success = False # successfully removes the crash for the crash_file
    successful_patches = []

    if bug_kind == "memcpy":
        ltrace_pattern = "memcpy-@libc.so*"

        match_template = "memcpy(:[1], :[2], :[_]);"
        rewrite_template = \
"""
// ROOIBOS START
memcpy(:[1], :[2], 1);
// ROOIBOS END
"""
    elif bug_kind == "strcpy":
        ltrace_pattern = "strcpy-@libc.so*"

        match_template = "strcpy(:[1], :[2]);"
        rewrite_template = \
"""
// ROOIBOS START
strncpy(:[1], :[2], 1);
// ROOIBOS END
"""
    else:
        print "Unknown bug kind %s" % bug_kind
        assert(False)

    if on_stdin:
        exit, ltrace_output = run_ltrace_stdin(binary, args, crash_file, ltrace_pattern)
    else:
        exit, ltrace_output = run_ltrace(binary, args, crash_file, ltrace_pattern)

    valid_patches = []

    print 'check did crash'
    print 'ltrace_output',ltrace_output

    if crash_signal.did_crash(ltrace_output[-1]):
        print 'YES'

        mmap = dump_memory_map(binary, args, crash_file)
        ltrace_output = ltrace_output[::-1]
        patch_locations = process_ltrace(ltrace_output, mmap)

        print 'ltraced'

        patch_locations_tmp = []
        for patch_location in patch_locations:
            try: # skip cases where there's no int at the end (like 'discriminator')
                m = re.search('(.*):(.*)', patch_location)
                if m.group(1) and m.group(2):
                    file_to_patch = m.group(1)
                    line_num = m.group(2)
                    line_num = int(line_num)
                    patch_locations_tmp.append((file_to_patch, line_num))
            except:
                print 'Discriminator @', file_to_patch, line_num
                pass

        patch_locations = patch_locations_tmp

        if DEBUG_PATCH_LOCATIONS:
            print '~=~= patch locations ~=~='
            print '\n'.join(map(lambda x: "%s:%d" % (x[0], x[1]), patch_locations))

        for file_to_patch, line_num in patch_locations:
            zero_offset = -1
            line_num = line_num + zero_offset

            line_num = line_num + addr2line_offset

            patch = generate_replacement_patch(\
                    file_to_patch, \
                    line_num, \
                    range_backward, \
                    range_forward, \
                    match_template, \
                    rewrite_template)

            if patch:
                valid_patches.append((file_to_patch, patch))

            for i,valid_patch in enumerate(valid_patches):
                successful_patches = apply_rebuild_revert(\
                        binary, \
                        args, \
                        crash_file, \
                        ltrace_pattern, \
                        [valid_patch], \
                        on_stdin=on_stdin)

                # multiple patches fix this bug if successful_patches > 1
                # for strcpy, etc, we are traversing from the last to first
                # in trace
                for j,(file_to_patch, successful_patch) in enumerate(successful_patches):
                    print "SUCCESSFUL PATCH %s\n" % successful_patch.text
                    if DUMP_ALL_PATCHES:
                        dump_patch(patch_path+'_'+str(i)+'_'+str(j), successful_patch.text)
                    else:
                        # return the first one
                        dump_patch(patch_path, successful_patch.text)
                        os.system('./9-rebuild.sh &> /dev/null')
                        return True

        if len(successful_patches) > 0:
            success = True

        os.system('./9-rebuild.sh &> /dev/null')
        return success

if __name__ == '__main__':
    config = [line.rstrip('\n') for line in open(sys.argv[1])]
    binary = config[0]
    crash_file = config[1]
    args = config[2]
    addr2line_offset, range_backward, range_forward = map(int, config[3].split(' '))
    bug_kind = config[4]
    source_dir = config[5]
    on_stdin = eval(config[6])
    run(binary, crash_file, args, \
            addr2line_offset, range_backward, range_forward, \
            bug_kind, source_dir, on_stdin)
