import glob
import os
import subprocess
import errno

import shutil

rebuild_script = "./rebuild.sh"

def read_file(fl):
    f = open(fl)
    output = f.readlines()
    f.close()
    return output

def read_patches(path):
    patch_paths = glob.glob(path + "/*.patch")
    return sorted(patch_paths)


def apply(patch):
    command = "git apply %s" % patch
    status = subprocess.call(command, shell=True)
    if (status != 0):
        print "FAILED TO APPLY PATCH %s" % patch


def revert(patch):
    command = "git apply -R %s" % patch
    status = subprocess.call(command, shell=True)
    if (status != 0):
        print "FAILED TO REVERT PATCH %s" % patch


def partition(
    patch,
    crashes_path,
    binary,
    args,
    on_stdin,
    ld_path,
):
    fixed = []
    unfixed = []
    crash_paths = glob.glob(crashes_path + "/*")
    print "Partitioning..."
    for crash_path in crash_paths:
        if on_stdin:
            command = "%s %s %s < %s > /dev/null 2>&1" % (
                ld_path,
                binary,
                args,
                crash_path,
            )
        else:
            command = "%s %s %s %s > /dev/null 2>&1" % (
                ld_path,
                binary,
                args,
                crash_path,
            )
        # print "RUNNING %s" % command
        status = subprocess.call(command, shell=True)
        # returns 11 for SIGSEGV. 128 + 11 = 139
        if (
            status == 0
            or status == 1
            or status == 255
            # or status == 101 (adds a custom status if a patch is set up to signal a clean exit)
        ):
            fixed.append(crash_path)
        else:
            # print 'Unfixed, status is:',status
            unfixed.append(crash_path)

    return fixed, unfixed


def bucket(
    patch,
    crashes_path,
    working_dir,
    binary,
    args,
    on_stdin,
    ld_path,
):
    apply(patch)

    current_dir = os.getcwd()
    os.chdir(working_dir)
    status = os.system("%s > /dev/null" % rebuild_script)
    result = os.WEXITSTATUS(status)
    os.chdir(current_dir)

    if result != 0:
        # REVERT ON FAILED BUILD
        print "REBUILD FAILED, REVERTING PATCH"
        revert(patch)
        return

    result = partition(
        patch,
        crashes_path,
        binary,
        args,
        on_stdin,
        ld_path,
    )
    revert(patch)

    return result


def bucket_with_patches(patches, ld_path, crashes_path, working_dir, binary_path, args, on_stdin):
    result = []
    for i, patch in enumerate(
        patches
    ):
        fixed, unfixed = bucket(
            patch,
            crashes_path,
            working_dir,
            binary_path,
            args,
            on_stdin,
            ld_path,
        )
        print "Patch %s #fixed crashes: %d" % (
            patch,
            len(fixed),
        )
        print "Patch %s #unfixed crashes: %d" % (
            patch,
            len(unfixed),
        )
        result.append((fixed, unfixed))
    return result


sample_project = {
    "root": "./sample-project",
    "binary": "./src/main",
    "args": "",
    "on_stdin": True,
    "ld_path": "",
}

projects = [
    sample_project
]

# Put crashes at project_root/crashes
# Put patches at project_root/patches
# Put rebuild.sh at project_root
if __name__ == "__main__":
    for config in projects:
        project_root = config["root"]
        working_dir = project_root
        binary = config["binary"]
        binary_path = working_dir + "/" + binary

        args = config["args"]
        on_stdin = config["on_stdin"]
        ld_path = config["ld_path"]

        # for each crash
        crashes_path = working_dir + "/" + "crashes"

        patches = read_patches(
            working_dir + "/" + "patches"
        )

        buckets = bucket_with_patches(
            patches, ld_path, crashes_path, working_dir, binary_path, args, on_stdin
        )

        current_dir = os.getcwd()
        os.chdir(working_dir)
        status = os.system(
            "%s > /dev/null" % rebuild_script
        )
        result = os.WEXITSTATUS(status)
        os.chdir(current_dir)

        if result != 0:
            print "WARNING: REBUILD FAILED: %d" % result
