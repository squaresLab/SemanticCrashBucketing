import glob
import os
import subprocess
import errno

import null_deref_fix
import overflow_fix

import shutil

from presto_instance import *
from fileio import *

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

patch_dump_dir = 'GENERATED_T_HAT'

rebuild_script = './9-rebuild.sh'

# read all patches in a directory
def read_patches(path):
   patch_paths = glob.glob(path+'/*.patch')
   patches = []
   for path in patch_paths:
       lines = rof(path)
       file_to_patch = lines[0].strip('--- ').strip()
       patches.append((path, file_to_patch, ''.join(rof(path))))
   return sorted(patches)

def apply(path, patch):
    result = p.apply(path, patch)
    if result.status_code == 204:
        pass
    else:
        print 'FAIL APPLY'

def revert(path, patch):
    result = p.revert(path, patch)
    if result.status_code == 204:
        pass
    else:
        print 'FAIL'

def partition(file_path, patch, crashes_path, binary, args, on_stdin, ld_path):
    fixed = []
    unfixed = []
    crash_paths = glob.glob(crashes_path+'/*')
    for crash_path in crash_paths:
        if on_stdin:
            command = '%s %s %s < %s &> /dev/null' % (ld_path, binary, args, crash_path)
        else:
            command = '%s %s %s %s &> /dev/null' % (ld_path, binary, args, crash_path)
        # print "RUNNING %s" % command
        status = subprocess.call(command, shell=True)
        # returns 11 for SIGSEGV. 128 + 11 = 139
        # 255 is OK for php-7
        if status == 0 or status == 1 or status == 101 or status == 255:
            fixed.append(crash_path)
        else:
            # print 'Unfixed, status is:',status
            unfixed.append(crash_path)

    return fixed, unfixed

def bucket(file_path, patch, crashes_path, working_dir, binary, args, on_stdin, ld_path):
    apply(file_path, patch)

    current_dir = os.getcwd()
    os.chdir(working_dir)
    status = os.system('%s &> /dev/null' % rebuild_script)
    result = os.WEXITSTATUS(status)
    os.chdir(current_dir)

    if result != 0:
        # REVERT ON FAILED BUILD
        print "REBUILD FAILED"
        revert(file_path, patch)
        return

    result = partition(file_path, patch, crashes_path, binary, args, on_stdin, ld_path)
    revert(file_path, patch)

    return result

# move one line prior to reported line in case we are trying
# to inject in the middle of a statement. try this 3 times.
def try_3_times(binary, crash_file, args, \
        addr2line_offset, range_backward, range_forward, \
        bug_kind, source_dir, on_stdin, patch_path):

    line_num_offset = 0

    for _j in xrange(3):

        if bug_kind == "null":
            success = null_deref_fix.run(binary, crash_file, args, \
                    addr2line_offset, range_backward, range_forward, \
                    bug_kind, source_dir, on_stdin, patch_path, \
                    line_num_offset)
        elif bug_kind == "memcpy" or bug_kind == "strcpy":
            success = overflow_fix.run(binary, crash_file, args, \
                    addr2line_offset, range_backward, range_forward, \
                    bug_kind, source_dir, on_stdin, patch_path, \
                    line_num_offset)
        else:
            print 'Unrecognized bug kind', bug_kind
            assert(False)


	if success:
            print "Bug %s patch %s successful crash %s" % \
			(bug_kind, patch_path, crash_file)
            return True
	else:
            print "Bug %s patch %s unsuccessful for crash %s" % \
                (bug_kind, patch_path, crash_file)
            line_num_offset = line_num_offset - 1

    return False

def generate_t_hat_patches(project, working_dir, source_dir, binary, \            
        crash_files, crash_file_dir, args, addr2line_offset, \                  
        range_backward, range_forward, bug_kind, on_stdin):                     
                                                                                
    # change to project working dir                                             
    current_dir = os.getcwd()                                                   
    os.chdir(working_dir)                                                       
                                                                                
    # delete previously generated patches                                       
    try:                                                                        
        shutil.rmtree(patch_dump_dir)                                           
    except:                                                                     
        pass                                                                    
                                                                                
    mkdir_p(patch_dump_dir)                                                     
                                                                                
                                                                                
    # generate patches                                                          
    for i,crash_file in enumerate(crash_files):                                 
        crash_file = crash_file_dir + '/' + crash_file                          
        patch_path = patch_dump_dir+'/'+("p%02d.patch" % (i+1))                 
        try_3_times(binary, crash_file, args, \                                 
                addr2line_offset, range_backward, range_forward, \              
                bug_kind, source_dir, on_stdin, patch_path)                     
                                                                                
                                                                                
    os.chdir(current_dir) 

def preprocess_ternary(working_dir):
    # pre-apply ternary operator rewrite
    current_dir = os.getcwd()
    os.chdir(working_dir)
    os.system('patch -f -d w3m < preprocess/ternary.patch')

    status = os.system('%s &> /dev/null' % rebuild_script)
    result = os.WEXITSTATUS(status)
    os.chdir(current_dir)

    if result != 0:
        print "PREPROCESSING REBUILD FAILED"
        exit(1)

def preprocess_if_expansion(working_dir):
    current_dir = os.getcwd()
    os.chdir(working_dir)
    os.system('patch -f -d sqlite -p1 < preprocess/if-expansion.patch')

    status = os.system('%s &> /dev/null' % rebuild_script)
    result = os.WEXITSTATUS(status)
    os.chdir(current_dir)

    if result != 0:
        print "PREPROCESSING REBUILD FAILED"
        exit(1)

def preprocess_php_macro(working_dir):
    current_dir = os.getcwd()
    os.chdir(working_dir)
    os.system('patch -f -d php -p0 < preprocess/expand-macro.patch')

    status = os.system('%s &> /dev/null' % rebuild_script)
    result = os.WEXITSTATUS(status)
    os.chdir(current_dir)

    if result != 0:
        print "PREPROCESSING REBUILD FAILED"
        exit(1)

def bucket_with_patches(patches, ld_path):
    result = []
    for i,(patch_name,file_to_patch,patch) in enumerate(patches):
        full_binary_path= working_dir+'/'+binary
        fixed, unfixed = bucket(file_to_patch, patch, crashes_path, \
                working_dir, full_binary_path, bucket_args, on_stdin, ld_path)
        print 'Patch %s fixed: %d' % (patch_name, len(fixed))
        print 'Patch %s unfixed: %d' % (patch_name, len(unfixed))
        result.append((fixed,unfixed))
    return result

w3m_project =\
{ "root"             : "./complete/w3m"
, "source_dir"       : "./w3m"
, "binary"           : "./w3m/w3m"
, "args"             : "-dump -T text/html"
, "bucket_args"      : "-dump -T text/html"
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : ["crash1.html", "crash2.html", "crash3.html", "crash4.html"]
, "addr2line_offset" : 0
, "range_backward"   : 0
, "range_forward"    : 0
, "bug_kind"         : "null"
, "on_stdin"         : False
, "ld_path"          : ""
}

sqlite_project =\
{ "root"             : "./complete/sqlite"
, "source_dir"       : "./sqlite"
, "binary"           : "./sqlite/.libs/lt-sqlite3"
, "args"             : ""
, "bucket_args"      : ""
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : 
                      ["crash01.sql", "crash02.sql", "crash03.sql"
                       ,"crash04.sql", "crash05.sql", "crash06.sql"
                       ,"crash07.sql", "crash08.sql", "crash09.sql"
                       ,"crash10.sql", "crash11.sql", "crash12.sql"]
, "addr2line_offset" : 0
, "range_backward"   : 0
, "range_forward"    : 0
, "bug_kind"         : "null"
, "on_stdin"         : True
, "ld_path"          : ""
}

# export LD_LIBRARY_PATH=/home/rvt/repfuzz/experiments/complete/libmad/libmad-0.15.1b/.libs 
libmad_project =\
{ "root"             : "./complete/libmad"
, "source_dir"       : "./libmad-0.15.1b"
, "binary"           : "./libmad-0.15.1b/.libs/minimad"
, "args"             : ""
, "bucket_args"      : ""
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : ["crash01.mp3"]
, "addr2line_offset" : 0
, "range_backward"   : 3
, "range_forward"    : 0
, "bug_kind"         : "memcpy"
, "on_stdin"         : False
, "ld_path"          : "./libmad-0.15.1b/.libs"
}

conntrackd_project =\
{ "root"             : "./complete/conntrackd"
, "source_dir"       : "./conntrack-tools-1.4.3/src"
, "binary"           : "./conntrack-tools-1.4.3/src/conntrackd"
, "args"             : "-C"
, "bucket_args"      : ""
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : ["minimal.conf"]
, "addr2line_offset" : -2
, "range_backward"   : 0
, "range_forward"    : 0
, "bug_kind"         : "strcpy"
, "on_stdin"         : False
, "ld_path"          : ""
}

R_project =\
{ "root"             : "./complete/R"
, "source_dir"       : "./R-3.3.2/src"
, "binary"           : "./R-3.3.2/bin/exec/R"
, "args"             : "--no-restore --slave --file=driver.r --args"
, "bucket_args"      : "--no-restore --slave --file=complete/R/ground-truth/driver.r --args"
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : ["crash.enc"]
, "addr2line_offset" : 0
, "range_backward"   : 0
, "range_forward"    : 0
, "bug_kind"         : "strcpy"
, "on_stdin"         : False
, "ld_path"          : "./R-3.3.2/lib" 
}

php_5_project =\
{ "root"             : "./complete/php-5.5.37"
, "source_dir"       : "./php/source/5.5.37"
, "binary"           : "./php/source/5.5.37/sapi/cli/php"
, "args"             : "./driver.php --"
, "bucket_args"      : "./driver.php --"
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : ["crash.jpg"]
, "addr2line_offset" : 0
, "range_backward"   : 0
, "range_forward"    : 0
, "bug_kind"         : "null"
, "on_stdin"         : False
, "ld_path"          : ""
}

php_7_project =\
{ "root"             : "./complete/php-7.0.14"
, "source_dir"       : "./php/source/7.0.14"
, "binary"           : "./php/source/7.0.14/sapi/cli/php"
, "args"             : ""
, "bucket_args"      : ""
, "crash_file_dir"   : "./truth/all"
, "crash_files"      : ["crash.php"]
, "addr2line_offset" : 0
, "range_backward"   : 0
, "range_forward"    : 0
, "bug_kind"         : "null"
, "on_stdin"         : False
, "ld_path"          : ""
}

projects =\
[ w3m_project
  sqlite_project
  libmad_project
  conntrackd_project
  R_project
  php_5_project
  php_7_project
]

crashes_paths = \
[ "afl-tmin/all/raw"
  ,"bff-5/all/raw"
  ,"bff-1/all/raw"
  ,"hf/all/raw"
  ,"hf-cov/all/raw"
]

def difference_buckets(ground_truth_buckets, scb_buckets):
    ground_truth_buckets_fix_set = map(lambda x: set(x[0]), ground_truth_buckets)
    for i,((fixed_t, unfixed_t), (fixed_t_hat, unfixed_t_hat)) in \
            enumerate(zip(ground_truth_buckets, scb_buckets)):
        if len(fixed_t) > len(fixed_t_hat): # t_hat missed something
            print 'MISSED:',len(fixed_t) - len(fixed_t_hat),set(fixed_t) - set(fixed_t_hat)
            missed = set(fixed_t) - set(fixed_t_hat)
            print 'Missed bug',missed,'bucket:',(i+1)
        elif len(fixed_t) < len(fixed_t_hat): # t_hat contains extras
            print 'EXTRAS:',len(fixed_t_hat) - len(fixed_t),'\n'.join(list(set(fixed_t_hat) - set(fixed_t)))
            extras = set(fixed_t_hat) - set(fixed_t)            
            for extra in extras:
                for j,truth_bucket in enumerate(ground_truth_buckets_fix_set):
                    if extra in truth_bucket:
                        print 'Crash',extra,'in wrong bucket',(i+1),'true fix has it in',(j+1)
        else:
            print 'IDEAL.'

if __name__ == '__main__':
    for config in projects:
        project = config["root"]
        working_dir = project + '/' + 'ground-truth'

        if project == './complete/w3m':
            print 'PREPROCESSING TERNARY'
            preprocess_ternary(working_dir)
        elif project == './complete/php-7.0.14':
            print 'PREPROCESSING MACRO EXPANSION'
            preprocess_php_macro(working_dir)

        source_dir = config["source_dir"]
        binary = config["binary"]
        crash_file_dir = config["crash_file_dir"]
        crash_files = config["crash_files"]
        args = config["args"]
        bucket_args = config["bucket_args"]
        addr2line_offset = config["addr2line_offset"]
        range_backward = config["range_backward"]
        range_forward = config["range_forward"]
        bug_kind = config["bug_kind"]
        on_stdin = config["on_stdin"]
        ld_path = config["ld_path"]

        print '-=-=-=-=-=-=- Processing %s -=-=-=-=-=-=-' % project

        if project == './complete/R':
            # for generate
            os.environ["LD_LIBRARY_PATH"] = ld_path
            os.environ["R_HOME"] = "./R-3.3.2"
            # for bucketing
            ld_path = "LD_LIBRARY_PATH=%s/R-3.3.2/lib R_HOME=%s/R-3.3.2" % (working_dir, working_dir) 
        elif len(ld_path) > 0:
            os.environ["LD_LIBRARY_PATH"] = ld_path
            ld_path = "LD_LIBRARY_PATH=" + working_dir + '/' + ld_path 

        generate_t_hat_patches(project, working_dir, source_dir, binary, \            
                crash_files, crash_file_dir, args, addr2line_offset, \              
                range_backward, range_forward, bug_kind, on_stdin) 

        for i,crashes_path in enumerate(crashes_paths):
            crashes_path = working_dir + '/' + crashes_path

            ground_truth_patches = read_patches(working_dir+'/'+'truth/patches')
            t_hat_patches = read_patches(working_dir+'/'+patch_dump_dir)

            ground_truth_buckets = bucket_with_patches(ground_truth_patches, ld_path)
            scb_buckets = bucket_with_patches(t_hat_patches, ld_path)

            print 'COLUMN',(i+1)

            difference_buckets(ground_truth_buckets, scb_buckets)
        
        current_dir = os.getcwd()
        os.chdir(working_dir)
        status = os.system('%s &> /dev/null' % rebuild_script)
        result = os.WEXITSTATUS(status)
        os.chdir(current_dir)

        if result != 0:
            print "WARNING: REBUILD FAILED: %d" % result
