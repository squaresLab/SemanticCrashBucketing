import os
import sys

from fileio import *
from patching import *

# null deref info from GDB script
line_num_file = '_line_num'
pvar_file = '_pvar'
file_path_file = '_filepath'

def run(binary, crash_file, args, \
        addr2line_offset, range_backward, range_forward, \
        bug_kind, source_dir, on_stdin, patch_path="p.patch", \
        line_num_offset=0): # add a line num offset
    success = False # successfully removes the crash for crash_file
    successful_patches = []

    if bug_kind == "null":
        ()
    else:
        print "Unknown bug kind %s" % bug_kind
        assert(False)

    print 'crash file:',crash_file
    print 'binary:',binary

    if on_stdin:
        cmd = 'gdb -ex "source BestNullDeref.py" -ex "run < %s %s" "%s"' % (args,crash_file,binary)
        print 'GDB CMD: %s' % cmd
        os.system(cmd)
    else:
        cmd = 'gdb -ex "source BestNullDeref.py" -ex "run %s %s" "%s"' % (args,crash_file,binary)
        print 'GDB CMD: %s' % cmd
        os.system(cmd)

    line_num = int(''.join(rof(line_num_file)))+line_num_offset
    pvar = ''.join(rof(pvar_file))+' '
    file_to_patch = ''.join(rof(file_path_file))
    file_to_patch = os.path.join(source_dir, file_to_patch)
    file_to_patch = os.path.abspath(file_to_patch)
    print '[DEBUG NULL DEREF FIX] file to patch',file_to_patch
    print '[DEBUG NULL DEREF FIX]', os.path.dirname(binary)

    match_template = ":[1] "
    rewrite_template = \
"""
// ROOIBOS START
if(:[1] == NULL)
    exit(101);
// ROOIBOS END
"""

    ltrace_pattern = ''

    if on_stdin:
        exit, ltrace_output = run_ltrace_stdin(binary, args, crash_file, ltrace_pattern)
    else:
        exit, ltrace_output = run_ltrace(binary, args, crash_file, ltrace_pattern)

    valid_patches = []

    if crash_signal.did_crash(ltrace_output[-1]):
        patch = generate_insertion_patch(\
                file_to_patch, \
                line_num, \
                pvar, \
                match_template, \
                rewrite_template)

        if patch:
            valid_patches.append((file_to_patch,patch))

        for valid_patch in valid_patches:
            successful_patches = apply_rebuild_revert(\
                binary, \
                args, \
                crash_file, \
                ltrace_pattern, \
                [valid_patch], \
                on_stdin=on_stdin)

            for file_to_patch, successful_patch in successful_patches:
                print "SUCCESSFUL PATCH %s" % successful_patch.text
                dump_patch(patch_path, successful_patch.text) 
    
    if len(successful_patches) > 0:
        success = True

    os.system('./9-rebuild.sh')
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
