from __future__ import annotations

import subprocess
from enum import Enum
from glob import glob
from json import dumps, load
from os import path, remove
from sys import argv
from typing import Optional

from bs4 import BeautifulSoup
from requests import get

PROBLEM_SELECTORS: dict[str, str] = {
    "title": "#problem_title",
    "time_limit": "#problem-info > tbody > tr > td:nth-child(1)",
    "memory_limit": "#problem-info > tbody > tr > td:nth-child(2)",
}

HR = "=" * 20


def calculate_memory(mem: float) -> str:
    if mem < 1024:
        return f"{mem}B"

    elif mem < 1024 * 1024:
        return f"{mem / 1024}KB"

    elif mem < 1024 * 1024 * 1024:
        return f"{mem / 1024 / 1024}MB"

    else:
        return f"{mem / 1024 / 1024 / 1024}GB"


def parse_memory(mem: str) -> float:
    if mem.endswith("B") and mem[:-1].isdigit():
        return float(mem[:-1])

    elif mem.endswith("KB"):
        return float(mem[:-2]) * 1024

    elif mem.endswith("MB"):
        return float(mem[:-2]) * 1024 * 1024

    elif mem.endswith("GB"):
        return float(mem[:-2]) * 1024 * 1024 * 1024

    else:
        raise ValueError(f"Invalid memory format: {mem}")


class ResultEnum(Enum):
    AC = "Accepted"
    # PAC = "Partially Accepted"
    WA = "Wrong Answer"
    CE = "Compile Error"
    RTE = "Runtime Error"
    TLE = "Time Limit Exceeded"
    # MLE = "Memory Limit Exceeded"
    OLE = "Output Limit Exceeded"
    # PE = "Presentation Error"


class Result:
    def __init__(
        self, result: ResultEnum, time: float, memory: float, output: str
    ) -> None:
        self.result = result
        self.time = time
        self.memory = memory
        self.output = output

    def __repr__(self) -> str:
        return f"{self.output}\n{self.result.value} / {self.time}s / {calculate_memory(self.memory)}"


class Problem:
    def __init__(
        self, title: str, id: int, tl: float, ml: float, samples: list[tuple[str, str]]
    ) -> None:
        self.title = title
        self.id = id
        self.tl = tl
        self.ml = ml
        self.samples = samples

    @classmethod
    def from_id(cls, id: int) -> Problem:
        try:
            with open(f"_problems/{id}.json", "r") as f:
                return cls(**load(f))

        except FileNotFoundError:
            url = f"https://www.acmicpc.net/problem/{id}"
            req = get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(req.text, "html.parser")

            tl, ml, title = None, None, None

            if tlel := soup.select_one(PROBLEM_SELECTORS["time_limit"]):
                tl = float(tlel.text.split()[0])

            if mlel := soup.select_one(PROBLEM_SELECTORS["memory_limit"]):
                ml = parse_memory(mlel.text)

            if titleel := soup.select_one(PROBLEM_SELECTORS["title"]):
                title = titleel.text

            samples: list[tuple[str, str]] = []
            cnt = 0

            while True:
                cnt += 1
                if (inputel := soup.select_one(f"#sample-input-{cnt}")) and (
                    outputel := soup.select_one(f"#sample-output-{cnt}")
                ):
                    samples.append((inputel.text.strip(), outputel.text.strip()))
                    continue

                break

            if not (tl and ml and title and samples):
                raise ValueError("Failed to parse problem")

            problem = cls(title, id, tl, ml, samples)

            with open(f"_problems/{id}.json", "w") as f:
                f.write(dumps(problem.__dict__))

            return problem

    def __repr__(self) -> str:
        lines: list[str] = []
        lines.append(f"{self.id}: {self.title}")
        lines.append(f"TL: {self.tl} / ML: {calculate_memory(self.ml)}")

        for i, (input, output) in enumerate(self.samples):
            lines.append(HR)
            lines.append(f"Sample {i + 1}")
            lines.append("Input:")
            lines.append(input)
            lines.append("Output:")
            lines.append(output)

        return "\n".join(lines)


class Validator:
    # TODO: find a way to get memory usage and elapsed time, multithreading
    def __init__(self, problem: Problem, code: str) -> None:
        self.problem = problem
        self.code = code
        self.lang = code.split(".")[-1]

        self.compiled = False

    def validate(self) -> list[Result]:
        func = None

        match self.lang:
            case "py":
                func = self._validate_py

            case "cpp":
                func = self._validate_cpp

        if not func:
            raise NotImplementedError

        results: list[Result] = []
        for i, (input, output) in enumerate(self.problem.samples):
            print(HR)
            print(f"Running Sample {i + 1}")

            res = func(input, output)
            print(res)
            results.append(res)

        return results

    def _validate_py(self, input: str, output: str) -> Result:
        try:
            res = subprocess.run(
                ["python", self.code],
                input=input.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.problem.tl * 3 + 2,
            )

            if res.returncode != 0:
                return Result(ResultEnum.RTE, -1, -1, res.stderr.decode())

            if (stdout := res.stdout.decode().strip()) != output:
                if len(stdout) > len(output) * 2:
                    return Result(ResultEnum.OLE, -1, -1, stdout)

                return Result(ResultEnum.WA, -1, -1, stdout)

            return Result(ResultEnum.AC, -1, -1, stdout)

        except subprocess.TimeoutExpired:
            return Result(ResultEnum.TLE, -1, -1, "")

    def _compile_cpp(self) -> Optional[Result]:
        print("Compiling...")

        res = subprocess.run(
            [
                "g++",
                self.code,
                "-O2",
                "-Wall",
                "-lm",
                "-static",
                "-std=c++20",
                "-o",
                self.code.split(".")[0],
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if res.returncode != 0:
            return Result(ResultEnum.CE, -1, -1, res.stderr.decode())

        self.compiled = True

    def _validate_cpp(self, input: str, output: str) -> Result:
        try:
            if not self.compiled:
                if res := self._compile_cpp():
                    return res

            res = subprocess.run(
                [f"./{self.code.split('.')[0]}"],
                input=input.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.problem.tl,
            )

            if res.returncode != 0:
                return Result(ResultEnum.RTE, -1, -1, res.stderr.decode())

            if (stdout := res.stdout.decode().strip()) != output:
                if len(stdout) > len(output) * 2:
                    return Result(ResultEnum.OLE, -1, -1, stdout)

                return Result(ResultEnum.WA, -1, -1, stdout)

            return Result(ResultEnum.AC, -1, -1, stdout)

        except subprocess.TimeoutExpired:
            return Result(ResultEnum.TLE, -1, -1, "")


def cli() -> None:
    if argv[1] == "clean":
        for file in glob("_problems/*.json"):
            print(f"Removing {file}")
            remove(file)

        return

    id = argv[1].split(".")[0]

    problem = Problem.from_id(int(id))

    print(problem)

    res = Validator(problem, argv[1]).validate()

    print(HR)

    for i, r in enumerate(res):
        print(f"Sample {i + 1}: {r.result.value}")


if __name__ == "__main__":
    cli()
