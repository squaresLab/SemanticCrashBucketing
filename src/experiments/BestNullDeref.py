#!/usr/bin/env python3

import os
import re
import time
import subprocess

from gdb import *
from enum import IntEnum

from presto_instance3 import *

DEBUG_GDB=True

# Globally disable confirmation, to facilitate scripting
execute('set confirm off')


class DebugSession():

    def get_first_invalid_access(self, cands):
        for c in cands:
            try:
                msg = gdb.execute("p %s" % c ,to_string=True)
            except gdb.MemoryError as msg:
                print('GDB exception',msg)
                return c

    def rewrite_deref(self, var):

        templates = \
            [
             (":[1]->:[2]->:[3]", ":[1]->:[2]"), \
             (":[1]->:[2][:[3]]", ":[1]"), \
             (":[1][:[2]]",       ":[1]"), \
             ("*:[1]",            ":[1]"), \
             (":[1]->:[2]",       ":[1]"), \
             (":[2](:[1])",       ":[1]"), \
            ]

        for match_template,rewrite_template in templates:
            result = p.rewrite(var, match_template, rewrite_template)

            if result.status_code == 200:
                return result.text
            else:
                continue

        return None
        

    def handle_segfault(self, event):

        if event.stop_signal != 'SIGSEGV':
            return

        gdb.execute("set pagination off")

        backtrace = gdb.execute("bt",to_string=True)

        if DEBUG_GDB:
          print("[DEBUG GDB] BACKTRACE:", backtrace)

        frame = selected_frame()

        sal = frame.find_sal()

        try:
            crashing_code = \
              gdb.execute("list %d,%d" % \
                  (sal.line, sal.line+10), \
                  to_string=True)
        except:
            frame = frame.older()
            sal = frame.find_sal()
            print('sal line:',sal.line)
            gdb.execute("up 1")
            crashing_code = \
              gdb.execute("list %d,%d" % \
                  (sal.line, sal.line+10), \
                  to_string=True)

        print("[DEBUG GDB] [+] CRASH TEXT: %s" % crashing_code)

        crashing_code = crashing_code.replace('"', "'")

        pat = "(\w+->\w+->\w+)|(\w+->\w+\.\w+->\w+)|\w+->\w+(\[\w+\])?|\w+(\[\w+\])|\*\w+"
        cmd = 'echo %r | grep -Po "%s"' % (crashing_code, pat)

        s = subprocess.check_output(cmd, shell=True)
        s = s.decode('unicode_escape')

        print("[DEBUG GDB] Vars to Check:\n%s" % s)

        var_name = self.get_first_invalid_access(s.split('\n'))

        print("[DEBUG GDB] first invalid access: %s" % var_name)

        res_var_name = self.rewrite_deref(var_name)

        if res_var_name == None:
            print("[DEBUG GDB] No rewrite possible for deref pattern: %s" % var_name)
            execute('quit')

        var_name = res_var_name


        with open("_line_num",'w+') as f:
            if DEBUG_GDB:
              print("[DEBUG GDB] [+] line num: %d" % sal.line)
            f.write(str(sal.line))

        with open("_pvar",'w+') as f:
            if DEBUG_GDB:
              print("[DEBUG GDB] [+] var name: "+var_name)
            f.write(var_name)

        with open("_filepath",'w+') as f:
            if DEBUG_GDB:
              print("[DEBUG GDB] [+] file: "+sal.symtab.filename)
            f.write(sal.symtab.filename)

        execute('quit')

# register the event handler with GDB
if __name__ == '__main__':
    sesh = DebugSession()
    events.stop.connect(sesh.handle_segfault)
