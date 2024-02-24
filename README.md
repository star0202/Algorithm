# Algorithm

- WSL2 (Validator uses `/mnt/c` path)
- Visual Studio Code
- g++
- PyPy3

## [Validator](./validator)

Code validator for [Baekjoon Online Judge](https://www.acmicpc.net/).

Keep the `_problems` directory in the same directory with the `validator` directory.

```bash
cd validator

pip install -r requirements.txt
python validate.py <code path> # only support C++ and PyPy3
```

## [Templates](./templates)

My templates for Problem Solving and Competitive Programming.

After editing the templates, run `python update.py` to update the VSCode snippets.

### C++

- `debug.h`: Debugging macro. (put it in the same directory with the source code)

- `ps.cpp`: Problem Solving template. snippet: `ps`
- `cp.cpp`: Competitive Programming template. snippet: `cp`

### Python

- `ps.py`: Problem Solving template. snippet: `ps`

## Library

My experimental library for Problem Solving and Competitive Programming.
