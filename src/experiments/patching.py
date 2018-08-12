import os

import crash_signal
from fileio import *

from debug import *
from extract import *
from ltrace import *
from presto_instance import *
from rewrite import *


def apply_possible_fixing_patch(file_to_patch,patch):
    if DEBUG_PATCHING:
        print '[DEBUG PATCHING] Got patch:'
        print patch.text
        print '[DEBUG PATCHING] Applying patch...'

    result = p.apply(file_to_patch, patch.text)
    if result.status_code == 204:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] Success applying patch!'
        return patch
    else:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] Error: Applying patch results\
                    in error %d:%s!' % (result.status_code, result.text)
        return None


def revert_patch(file_to_patch,patch):
    result = p.revert(file_to_patch, patch.text)
    if result.status_code == 204:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] Success reverting patch!'
        return True # hate python
    else:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] Error: Reverting patch results\
                  in error %d:%s!' % (result.status_code, result.text)
        return None

# apply a list of patches, rebuild, and revert
# by default, crash file is not input on stdin; change with on_stdin
def apply_rebuild_revert(binary, args, crash_file, ltrace_pattern, patches, \
                         on_stdin=False):
    successful_patches = []
    applied_patches = []
    # apply all valid_patches
    for file_to_patch, patch in patches:
        patch = apply_possible_fixing_patch(file_to_patch,patch)
        if patch:
            applied_patches.append((file_to_patch,patch))

    status = os.system('./9-rebuild.sh')
    result = os.WEXITSTATUS(status)

    if result != 0:
        print "REBUILD apply_rebuild_revert failed"
        # revert all patches
        for file_to_patch, patch in applied_patches:
            revert_patch(file_to_patch, patch) # by construction, this cannot fail
        return [] # no successful patches

    if on_stdin:
        exit, ltrace_output = run_ltrace_stdin(binary, args, crash_file, ltrace_pattern)
    else:
        exit, ltrace_output = run_ltrace(binary, args, crash_file, ltrace_pattern)

    if not crash_signal.did_crash(ltrace_output[-1]):
        print '[+] SUCCESS - Program no longer crashes'
        print '[+] Patch:\n',patch.text
        if TEST:
            record_test_output('[+] SUCCESS - Program no longer crashes\n')
            record_test_output('[+] Patch:\n'+'\n'.join(patch.text.split('\n')))
        print 'successful patches equals applied: %d' % len(applied_patches)
        successful_patches = applied_patches
    else:
        print '[-] Fail: still crashes.'
        if TEST:
            record_test_output('[-] Fail: still crashes.\n')
        successful_patches = []

    # revert all patches
    for file_to_patch, patch in applied_patches:
        revert_patch(file_to_patch, patch) # by construction, this cannot fail

    if len(successful_patches) == 0:
        return []
    else:
        successful_patches = applied_patches
        return successful_patches

def generate_replacement_patch(file_to_patch, line_num, \
                   range_backward, range_forward, \
                   match_template, rewrite_template):
    if range_forward - range_backward == 0:
        line_to_rewrite = extract_line(file_to_patch,line_num)
    else:
        start_line = line_num - range_backward
        end_line = line_num + range_forward
        line_to_rewrite = extract_lines(file_to_patch, start_line, end_line)

    # smart thing to remove leading tabs/trailing whitespace
    line_to_rewrite = line_to_rewrite.strip()

    rooibos_output = rewrite(line_to_rewrite, match_template, rewrite_template)
    if len(rooibos_output) == 0:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] No match, no rooibos output'
        return None
    else:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] Rewrite success:', rooibos_output

        content = ''.join(rooibos_output)
        if content:
            if DEBUG_PATCHING:
                print '[DEBUG PATCHING] patch file',file_to_patch,\
                      'line num',line_num

                print '[DEBUG PATCHING] replacing in',file_to_patch,\
                      'content',content,\
                      'line_num',line_num,\
                      'range','?? FIXME ??'


            patch = p.replace(file_to_patch, line_num-range_backward, line_num, content)

            if TEST:
                record_test_output('Generated patch for line %d:\n%s' % \
                                  (line_num, '\n'.join(patch.text.split('\n')[2:])))

            if DEBUG_PATCHING:
                print '[DEBUG PATCHING] replacement patch:', patch.text
            return patch
        return None

def generate_insertion_patch(file_to_patch, line_num, source, \
                             match_template, rewrite_template):
    rooibos_output = rewrite(source, match_template, rewrite_template)

    if len(rooibos_output) == 0:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] No match, no rooibos output'
        return None
    else:
        if DEBUG_PATCHING:
            print '[DEBUG PATCHING] Rewrite success:', rooibos_output

        content = ''.join(rooibos_output)
        if content:
            if DEBUG_PATCHING:
                print '[DEBUG PATCHING] patch file',file_to_patch,\
                      'line num',line_num

                print '[DEBUG PATCHING] inserting in',file_to_patch,\
                      'content',content,\
                      'line_num',line_num,\
                      'range','?? FIXME ??'

            patch = p.insert(file_to_patch, line_num, content)

            if TEST:
                record_test_output('Generated patch for line %d:\n%s' % \
                                  (line_num, '\n'.join(patch.text.split('\n')[2:])))

            if DEBUG_PATCHING:
                print '[DEBUG PATCHING] insertion patch:', patch.text
            return patch
        return None
