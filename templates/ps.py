from sys import stdin, stdout

input = lambda: stdin.readline().rstrip()
_out: list[str] = []
print = lambda *v, sep=" ", end="\n": _out.append(sep.join(map(str, v)) + end)


def main() -> None:
    # code here


if __name__ == "__main__":
    main()

    stdout.write("".join(_out))
