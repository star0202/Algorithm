from json import dumps
from os import listdir, path
from typing import TypedDict


class SnippetSchema(TypedDict):
    scope: str
    prefix: str
    body: list[str]


def comment(ext: str) -> str:
    if ext == "cpp":
        return "//"
    elif ext == "py":
        return "#"
    else:
        raise ValueError(f"Invalid extension: {ext}")


def main():
    json: dict[str, SnippetSchema] = {}

    for file in listdir("templates"):
        name, ext = path.splitext(file)
        ext = ext[1:]

        if ext not in ["cpp", "py"]:
            continue

        with open(f"templates/{file}", "r") as f:
            code = f.read()

        json[f"{name}-{ext}"] = {
            "scope": ext,
            "prefix": name,
            "body": code.replace(f"{comment(ext)} code here", "$0").splitlines() + [""],
        }

        print(f"Updated templates/{name}.{ext}")

    with open(".vscode/template.code-snippets", "w") as f:
        f.write(f"{dumps(json, indent=2)}\n")


if __name__ == "__main__":
    main()
