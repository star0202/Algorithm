from os.path import getsize
from sys import argv

from python_minifier import minify


def cli() -> None:
    with open(argv[1], "r") as f:
        code = f.read()
        bytes = getsize(argv[1])

    with open(argv[1], "w") as f:
        minified = minify(code)
        f.write(minified)

    print(f"Minified {bytes} bytes to {getsize(argv[1])} bytes.")


if __name__ == "__main__":
    cli()
