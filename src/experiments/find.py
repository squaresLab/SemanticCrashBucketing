import os

from debug import *
from fileio import *

find_out_file = "find.out"

def find(pattern):
    cmd = "find . -regex %r > %s" % (pattern, find_out_file)
    os.system(cmd)
    output = rof(find_out_file)

    if DEBUG_FIND:
        print '[DEBUG FIND] command:',cmd
        print '[DEBUG FIND] output:',output

    return output

# tell me if this library exists as part of the project, and
# returns its path. (alternative it is some libc lib)
def path_for_library_exists(file_name):
    pattern = ".*" + file_name
    output = find(pattern) # try exact match first

    if len(output) == 0: # zero lines
        return None
    else:
        output = output[0].strip()
        # resolve symlinks if needed, e.g., libmad.so.0 to libmad.so.0.2.1
        output = os.path.realpath(output)
        if DEBUG_FIND:
            print '[DEBUG FIND] resolving realpath:',output

        return output
