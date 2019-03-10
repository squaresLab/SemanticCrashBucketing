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

if __name__ == '__main__':
    config = [line.rstrip('\n') for line in open(sys.argv[1])]
    binary = config[0]
    crash_file = config[1]
    args = config[2]
    addr2line_offset, range_backward, range_forward = map(int, config[3].split(' '))
    bug_kind = config[4]

    if bug_kind == "strcpy":
        ltrace_pattern = "strcpy-@libc.so*"

        match_template = "strcpy(:[1], :[2]);"
        rewrite_template = \
"""
// ROOIBOS START
strncpy(:[1], :[2], 1);
// ROOIBOS END
"""
    elif bug_kind == "memcpy":
        ltrace_pattern = "memcpy-@libc.so*"

        match_template = "memcpy(:[1], :[2], :[_]);"
        rewrite_template = \
"""
// ROOIBOS START
memcpy(:[1], :[2], 1);
// ROOIBOS END
"""
    else:
        print "Unknown bug kind %s" % bug_kind
        assert(False)

    exit,ltrace_output = run_ltrace(binary, args, crash_file, ltrace_pattern)

    valid_patches = []

    # check last line if we crashed
    if crash_signal.did_crash(ltrace_output[-1]):

        mmap = dump_memory_map(binary, args, crash_file)
        # if we did, reverse the trace and start processing from the end
        ltrace_output = ltrace_output[::-1]
        patch_locations = process_ltrace(ltrace_output,mmap)

        # filter valid locations by regex
        patch_locations_tmp = []
        for patch_location in patch_locations:
            m = re.search('(.*):(.*)', patch_location)
            if m.group(1) and m.group(2):
                file_to_patch = m.group(1)
                line_num = m.group(2)
                line_num = int(line_num)
                patch_locations_tmp.append((file_to_patch,line_num))

        patch_locations = patch_locations_tmp
        patch_locations = sorted(patch_locations, key=lambda x: x[1])[::-1]

        if DEBUG_PATCH_LOCATIONS:
            print '~=~= patch locations ~=~='
            print '\n'.join(map(lambda x: "%s:%d" % (x[0], x[1]), patch_locations))

        for file_to_patch,line_num in patch_locations:
            zero_offset = -1
            line_num = line_num + zero_offset

            line_num = line_num + addr2line_offset

            patch = generate_replacement_patch(file_to_patch, \
                                   line_num, \
                                   range_backward, \
                                   range_forward, \
                                   match_template, \
                                   rewrite_template)

            if patch:
                valid_patches.append((file_to_patch,patch))

        map(lambda x: apply_rebuild_revert(binary, \
                                           args, \
                                           crash_file, \
                                           ltrace_pattern, \
                                           [x]), \
                                           valid_patches)
    os.system('./9-rebuild.sh > /dev/null')
