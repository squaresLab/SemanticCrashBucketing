import os
from debug import *
from fileio import *

addr2line_out_file = "addr2line.out"

def addr2line(lib_path,addr):
    cmd = "addr2line -i -f -e %s 0x%x > %s" % (lib_path, addr, addr2line_out_file)
    os.system(cmd)
    output = rof(addr2line_out_file)
    if len(output) == 0:
        if DEBUG_ADDR2LINE:
            print "No addr2line"
        return None
    elif "??" in ''.join(output):
        if DEBUG_ADDR2LINE:
            print 'addr2line says ??'
        return None
    else:
        output = map(str.strip, output)
        if DEBUG_ADDR2LINE:
            print "addr2line:",output
        # last line is what we want
        return output[-1]
