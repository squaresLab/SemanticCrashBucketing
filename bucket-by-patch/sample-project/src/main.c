#include <signal.h>
#include <stdio.h>
#include <string.h>

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
