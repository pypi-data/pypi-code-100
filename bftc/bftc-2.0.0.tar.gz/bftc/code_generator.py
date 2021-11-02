from string import Template

from .tokens import Token
from .transpiler import transpile

C_CODE = Template(
"""
#include <stdio.h>


int main(int argc, char **argv) {
    int i = 0;
    char arr[30000];
    memset(arr, 0, sizeof(arr));
    $c_code
    return 0;
}
"""
)


def generate(tokens: list[Token]) -> str:
    """Generate valid program on C by given tokens"""
    return C_CODE.substitute(
        c_code="\n".join([transpile(token) for token in tokens])
    )


__all__ = ["generate"]
