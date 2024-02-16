# Algorithm

- WSL2 (Validator uses `/mnt/c` path)
- Visual Studio Code
- g++
- PyPy3

## Validator

Keep the `_problems` directory in the same directory with the `validator` directory.

```bash
cd validator

pip install -r requirements.txt
python validate.py <code path> # only support C++ and PyPy3
```

## Templates

All templates are in `./templates` directory.

After editing the templates, run `python update.py` to update the snippets.

### C++

- `debug.h`: Debugging macro. (put it in the same directory with the source code)

- `ps.cpp`: Problem Solving template. snippet: `ps`
- `cp.cpp`: Competitive Programming template. snippet: `cp`

### Python

- `ps.py`: Problem Solving template. snippet: `ps`
