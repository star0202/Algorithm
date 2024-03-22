from __future__ import annotations

from enum import Enum
from glob import glob
from json import dumps, load
from os import path, remove, system
from os.path import exists
from resource import RUSAGE_CHILDREN, getrusage
from subprocess import PIPE, CompletedProcess, TimeoutExpired, run
from sys import argv
from typing import Optional

from bs4 import BeautifulSoup
from requests import get


class Selectors:
    time_limit = "#problem-info > tbody > tr > td:nth-child(1)"
    memory_limit = "#problem-info > tbody > tr > td:nth-child(2)"
    title = "#problem_title"


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
    MLE = "Memory Limit Exceeded"
    OLE = "Output Limit Exceeded"
    # PE = "Presentation Error"


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
        if exists(f"_problems/{id}.json"):
            with open(f"_problems/{id}.json", "r") as f:
                return cls(**load(f))

        else:
            url = f"https://www.acmicpc.net/problem/{id}"
            req = get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(req.text, "html.parser")

            tl, ml, title = None, None, None

            if tlel := soup.select_one(Selectors.time_limit):
                tl = float(tlel.text.split()[0])

            if mlel := soup.select_one(Selectors.memory_limit):
                ml = parse_memory("".join(mlel.text.split()[:2]))

            if titleel := soup.select_one(Selectors.title):
                title = titleel.text

            samples: list[tuple[str, str]] = []
            cnt = 0

            while True:
                cnt += 1
                if (inputel := soup.select_one(f"#sample-input-{cnt}")) and (
                    outputel := soup.select_one(f"#sample-output-{cnt}")
                ):
                    samples.append((inputel.text.rstrip(), outputel.text.rstrip()))
                    continue

                break

            if not (tl and ml and title and samples):
                raise ValueError(
                    f"Failed to parse problem\nTL: {tl}\nML: {ml}\nTitle: {title}\nSamples: {samples}"
                )

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

    def __bool__(self) -> bool:
        return self.result == ResultEnum.AC


class Validator:
    # TODO: multithreading
    def __init__(self, problem: Problem, code: str) -> None:
        self.problem = problem
        self.code = code
        self.lang = code.split(".")[-1]

        self.compiled = False
        self.before_time = 0

    def validate(self) -> list[Result]:
        func = None

        if self.lang == "py":
            func = self._validate_py
        elif self.lang == "cpp":
            func = self._validate_cpp
        else:
            raise NotImplementedError

        results: list[Result] = []
        for i, (input, output) in enumerate(self.problem.samples):
            print(HR)
            print(f"Running Sample {i + 1}")

            res = func(input, output)
            print(res)
            results.append(res)

        return results

    def _validate(self, process: CompletedProcess, ans: str) -> Result:
        rusages = getrusage(RUSAGE_CHILDREN)

        elapsed = rusages.ru_utime + rusages.ru_stime - self.before_time
        self.before_time = rusages.ru_utime + rusages.ru_stime

        memory = rusages.ru_maxrss

        if memory > self.problem.ml:
            return Result(ResultEnum.MLE, elapsed, memory, "")

        if process.returncode != 0:
            return Result(ResultEnum.RTE, elapsed, memory, process.stderr.decode())

        if (stdout := process.stdout.decode().rstrip()) != ans:
            if len(stdout) > len(ans) * 2:
                return Result(ResultEnum.OLE, elapsed, memory, stdout)

            return Result(ResultEnum.WA, elapsed, memory, stdout)

        return Result(ResultEnum.AC, elapsed, memory, stdout)

    def _compile_py(self) -> Optional[Result]:
        print("Compiling...")

        res = run(
            [
                "pypy3",
                "-W",
                "ignore",
                "-c",
                f"\"import py_compile; py_compile.compile(r'{self.code}')\"",
            ],
            stdout=PIPE,
            stderr=PIPE,
        )

        rusage = getrusage(RUSAGE_CHILDREN)

        self.before_time = rusage.ru_utime + rusage.ru_stime

        if res.returncode != 0:
            return Result(ResultEnum.CE, -1, -1, res.stderr.decode())

        self.compiled = True

    def _validate_py(self, input: str, output: str) -> Result:
        try:
            if not self.compiled:
                if res := self._compile_py():
                    return res

            res = run(
                ["pypy3", "-W", "ignore", self.code],
                input=input.encode(),
                stdout=PIPE,
                stderr=PIPE,
                timeout=self.problem.tl,
            )

            return self._validate(res, output)

        except TimeoutExpired:
            return Result(ResultEnum.TLE, -1, -1, "")

    def _compile_cpp(self) -> Optional[Result]:
        print("Compiling...")

        res = run(
            [
                "g++",
                self.code,
                "-O2",
                "-Wall",
                "-lm",
                "-static",
                "-std=c++20",
                "-o",
                f"{self.code.split('.')[0]}.out",
            ],
            stdout=PIPE,
            stderr=PIPE,
        )

        rusage = getrusage(RUSAGE_CHILDREN)

        self.before_time = rusage.ru_utime + rusage.ru_stime

        if res.returncode != 0:
            return Result(ResultEnum.CE, -1, -1, res.stderr.decode())

        self.compiled = True

    def _validate_cpp(self, input: str, output: str) -> Result:
        try:
            if not self.compiled:
                if res := self._compile_cpp():
                    return res

            res = run(
                [f"./{self.code.split('.')[0]}.out"],
                input=input.encode(),
                stdout=PIPE,
                stderr=PIPE,
                timeout=self.problem.tl,
            )

            return self._validate(res, output)

        except TimeoutExpired:
            return Result(ResultEnum.TLE, -1, -1, "")


def cli() -> None:
    if argv[1] == "clean":
        for file in glob("_problems/*.json"):
            print(f"Removing {file}")
            remove(file)

        return

    id = path.split(argv[1])[-1].split(".")[0]

    problem = Problem.from_id(int(id))

    print(problem)

    res = Validator(problem, argv[1]).validate()

    print(HR)

    for i, r in enumerate(res):
        print(f"Sample {i + 1}: {r.result.value}")

    if all(res):
        print(HR)

        print("All samples passed!")
        system(f"/mnt/c/Windows/System32/clip.exe < {argv[1]}")
        print("Copied to clipboard!")


if __name__ == "__main__":
    cli()
