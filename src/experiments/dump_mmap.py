#!/usr/bin/env python3

import os
import re
import time

from gdb import *
from enum import IntEnum

LOG_FILE="mmap.out"

def log(s):
  with open(LOG_FILE,'w+') as f:
    f.write(s)

# Globally disable confirmation, to facilitate scripting
execute('set confirm off')

class DebugSession():
    # event handler to deal with segfaults
    # and get the info to call bug-refactor
    def handle_segfault(self, event):

        result = gdb.execute("info proc mappings",to_string=True)

        log(result)

        os.chmod(LOG_FILE, 0o777)
        execute('quit')

# register the event handler with GDB
if __name__ == '__main__':
    sesh = DebugSession()
    events.stop.connect(sesh.handle_segfault)
