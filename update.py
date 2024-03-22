from json import dumps, loads
from os import listdir, path
from typing import TypedDict
from hashlib import sha256 as _sha256

DIR = "templates"
COMMENT_MAPPING = {
    "cpp": "//",
    "py": "#",
}
LANGUAGE_MAPPING = {
    "cpp": "cpp",
    "py": "python",
}
SNIPPET_FILE = ".vscode/template.code-snippets"


class SnippetSchema(TypedDict):
    scope: str
    prefix: str
    body: list[str]
    hash: str


def sha256(data: str) -> str:
    return _sha256(data.encode()).hexdigest()


def comment(ext: str) -> str:
    if ext not in COMMENT_MAPPING:
        raise ValueError(f"Unknown extension {ext}")

    return COMMENT_MAPPING[ext]


def language(ext: str) -> str:
    if ext not in LANGUAGE_MAPPING:
        raise ValueError(f"Unknown extension {ext}")

    return LANGUAGE_MAPPING[ext]


def main():
    json: dict[str, SnippetSchema] = {}

    if path.exists(SNIPPET_FILE):
        with open(SNIPPET_FILE, "r") as f:
            json = loads(f.read())

    for file in listdir(DIR):
        full_path = path.join(DIR, file)

        name, ext = path.splitext(file)
        ext = ext[1:]

        if ext not in ["cpp", "py"]:
            continue

        with open(full_path, "r") as f:
            code = f.read()
        
        sha = sha256(code)

        if json.get(f"{name}-{ext}", {}).get("hash") == sha:
            print(f"Skipped {full_path}")
            continue

        json[f"{name}-{ext}"] = {
            "scope": language(ext),
            "prefix": name,
            "body": code.replace(f"{comment(ext)} code here", "$0").splitlines() + [""],
            "hash": sha,
        }

        print(f"Updated {full_path}")

    with open(SNIPPET_FILE, "w") as f:
        f.write(f"{dumps(json, indent=2)}\n")


if __name__ == "__main__":
    main()
