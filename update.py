from json import dumps
from os import listdir, path
from typing import TypedDict

DIR = "templates"
COMMENT_MAPPING = {
    "cpp": "//",
    "py": "#",
}
SNIPPET_FILE = ".vscode/template.code-snippets"


class SnippetSchema(TypedDict):
    scope: str
    prefix: str
    body: list[str]


def comment(ext: str) -> str:
    if ext not in COMMENT_MAPPING:
        raise ValueError(f"Unknown extension {ext}")
    
    return COMMENT_MAPPING[ext]


def main():
    json: dict[str, SnippetSchema] = {}

    for file in listdir(DIR):
        full_path = path.join(DIR, file)

        name, ext = path.splitext(file)
        ext = ext[1:]

        if ext not in ["cpp", "py"]:
            continue

        with open(full_path, "r") as f:
            code = f.read()

        json[f"{name}-{ext}"] = {
            "scope": ext,
            "prefix": name,
            "body": code.replace(f"{comment(ext)} code here", "$0").splitlines() + [""],
        }

        print(f"Updated {full_path}")

    with open(SNIPPET_FILE, "w") as f:
        f.write(f"{dumps(json, indent=2)}\n")


if __name__ == "__main__":
    main()
