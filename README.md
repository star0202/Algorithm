# Algorithm

- WSL2 (Validator uses `/mnt/c` path)
- Visual Studio Code
- g++
- PyPy3
- Python3
- Pyhton package manager (uv, pip, etc.)

## [Tools](./tools)

In order to use python tools, you need to install dependencies in `requirements.txt`.

### [Debugger](./tools/debugger)

C++ debugging macro, requires `-DSTARCEA` flag.

For usage or output example, run [test.cpp](./tools/debugger/test.cpp).

### [Validator](./tools/validator)

Code validator for [Baekjoon Online Judge](https://www.acmicpc.net/).

Keep the `_problems` directory in the same directory with the `validator` directory.

## [Templates](./templates)

My templates for Problem Solving and Competitive Programming.

After editing the templates, run `python update.py` to update the VSCode snippets.

### C++

- `ps.cpp`: Problem Solving template. snippet: `ps`
- `cp.cpp`: Competitive Programming template. snippet: `cp`

### Python

- `ps.py`: Problem Solving template. snippet: `ps`

## [Library](./library)

My experimental library for Problem Solving and Competitive Programming.
