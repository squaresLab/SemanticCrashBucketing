from debug import *

def extract_lines(filename, start_line, end_line):
    if DEBUG_EXTRACT:
        print 'extracting lines',start_line,'-',end_line
        print 'from file',filename
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    return '\n'.join(lines[start_line:end_line])

# get the line from the file (e.g,. get the strcpy that we want to patch
# incoming line is assumed 1-index, so we correct by subtracting one
def extract_line(filename,line_num):
    line_num = line_num - 1
    if DEBUG_EXTRACT:
        print 'extracting line',line_num
        print 'from file',filename
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    return lines[line_num]
