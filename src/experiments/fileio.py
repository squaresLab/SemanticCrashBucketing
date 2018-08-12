test_out_file = "test.out"

# result of file
def rof(fl):
    f = open(fl)
    output = f.readlines()
    f.close()
    return output

def record_test_output(s):
    f = open(test_out_file, 'a')
    f.write(s)
    f.close()

def dump_patch(name, content):
    f = open(name, 'w')
    f.write(content)
    f.close()
