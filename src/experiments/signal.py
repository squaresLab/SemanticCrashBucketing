def did_crash(line):
    return "SIGSEGV" in line or "SIGABRT" in line
