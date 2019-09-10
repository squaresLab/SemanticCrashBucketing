# bucket-by-patch

A script and example project for partitioning crashing inputs with a set of patches. 

## Usage

First set up the project as follows. The `sample-project` is a minimal working setup. 

- Build your project (e.g., for `sample-project`, call `make -C sample-project/src` from the directory where this README is)
- Put `.patch` files in a folder called `patches` in the root of the project directory (see `example-project/patches`).
- Put all crashing input in a file called `crashes` (see `example-project/crashes`).
- Include a `rebuild.sh` script at the root of the project. This script will be called after a patch is applied. The script can, for example, call `make -C` in the source directory of your project (that's what it does for the example project).
- Configure the `bucket-by-patch.py` script in this folder. Change the following:

```
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
```

- where `root` is the root directory relative to the directory containing this README (i.e., where the `bucket-by-patch.py` script will be called)
- `binary` is the path relative to the project root that should be invoked with crashing inputs
- `args` is a string of arguments to call the binary with
- `on_stdin` should be set to `True` if input in the `crashes` file should be fed to the program via `stdin`. If set to `False`, the crashing input file path in `crashes` will be passed on the command line immediately follow `args` string.
- `ld_path` prefixes the binary with some string (e.g., for setting `LD_LIBRARY_PATH=/path/library`).

Notes:
- Multiple projects can be added to the `projects` list (as in [other experiments](https://github.com/squaresLab/SemanticCrashBucketing/blob/master/src/master.py)).
- If the patch applies but fails to build, the script will try and revert the patch. This usually succeeds, so that your project is not left in a broken state. The script then moves on to the next patch.
- Patching is set up to use `git apply` (and you can generate patches with `git diff > my-patch.patch`). Running `git apply path/to/patch` at the root of the project directory is a good sanity check to do before running the script. If you do not want to use `git apply`, change the `apply` and `revert` function commands in `bucket-by-patch.py`.

## Run the `sample-project` example

TL;DR run `make -C sample-project/src && python bucket-by-patch.py 2> /dev/null`

Details:

The sample project contains a simple program:

```
int main(int argc, char **argv) {
    char str[100];

    scanf("%s", str);
    if (strcmp (str, "crash1") == 0) {
        raise(SIGSEGV);
    } else if (strcmp (str, "crash2") == 0) {
        raise(SIGSEGV);
    }
    return 0;
}
```

It crashes along the first branch if the input on stdin is `crash1`. It crashes on the second branch if the input is `crash2`. 

The `crashes` directory contains 10 inputs that induce crash1, and 5 inputs that induce crash2.
The `patches` directory contains one patch that stops crashes from happening in the first branch:

```patch
diff --git a/bucket-by-patch/sample-project/src/main.c b/bucket-by-patch/sample-project/src/main.c
index cf73844..f5942c4 100644
--- a/bucket-by-patch/sample-project/src/main.c
+++ b/bucket-by-patch/sample-project/src/main.c
@@ -7,7 +7,7 @@ int main(int argc, char **argv) {
 
     scanf("%s", str);
     if (strcmp (str, "crash1") == 0) {
-        raise(SIGSEGV);
+        return 0;
     } else if (strcmp (str, "crash2") == 0) {
         raise(SIGSEGV);
     }
```

and another that stops the crash on the second branch. 

To bucket the crashes, run the following in this directory:

`make -C sample-project/src && python bucket-by-patch.py 2> /dev/null`

```
-----------------------------
Partitioning with patch ./sample-project/patches/fix-crash1.patch...
Patch ./sample-project/patches/fix-crash1.patch #fixed crashes: 10
  ./sample-project/crashes/crash1-03
  ./sample-project/crashes/crash1-04
  ./sample-project/crashes/crash1-05
  ./sample-project/crashes/crash1-02
  ./sample-project/crashes/crash1-10
  ./sample-project/crashes/crash1-07
  ./sample-project/crashes/crash1-09
  ./sample-project/crashes/crash1-08
  ./sample-project/crashes/crash1-01
  ./sample-project/crashes/crash1-06
Patch ./sample-project/patches/fix-crash1.patch #unfixed crashes: 5
-----------------------------
Partitioning with patch ./sample-project/patches/fix-crash2.patch...
Patch ./sample-project/patches/fix-crash2.patch #fixed crashes: 5
  ./sample-project/crashes/crash2-01
  ./sample-project/crashes/crash2-03
  ./sample-project/crashes/crash2-04
  ./sample-project/crashes/crash2-05
  ./sample-project/crashes/crash2-02
Patch ./sample-project/patches/fix-crash2.patch #unfixed crashes: 10
```

We see that partitioning the set of 15 crashes with `fix-crash1.patch` fixes 10 crashes (and lists the crashes fixed by this patch). Partitioning the set of 15 crashes with `fix-crash2.patch` fixes 5 crashes.
