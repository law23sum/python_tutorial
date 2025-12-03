from __future__ import annotations

"""Python translation of the Java ``SyntaxKeywords`` tour.

This module demonstrates the equivalent Python concepts for every keyword-focused
section in the provided Java example.
"""

from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Protocol
import threading


# ---------------------------------------------------------------------------
# Interfaces, records, and enums
# ---------------------------------------------------------------------------


class Greeter(Protocol):  # interface: structural contract
    def greet(self, name: str) -> str:
        ...

    def hello(self) -> str:
        ...


@dataclass
class PrefixGreeter:
    prefix: str = "Hello, "

    def greet(self, name: str) -> str:
        return self.prefix + name

    def hello(self) -> str:
        return "Hello"

    @staticmethod
    def of_prefix(prefix: str) -> "PrefixGreeter":
        return PrefixGreeter(prefix)


class Level(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


@dataclass(frozen=True)
class User:  # record analogue
    id: int
    name: str

    def __post_init__(self) -> None:
        if self.id < 0:
            raise ValueError("id >= 0")


# ---------------------------------------------------------------------------
# Base/derived classes (extends/super/this)
# ---------------------------------------------------------------------------


@dataclass
class Being:
    kind: str

    def say(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"Being(kind={self.kind})"


@dataclass
class Person(Being):
    name: str = field(default="")

    def __init__(self, name: str) -> None:
        super().__init__(kind="person")
        self.name = name

    def say(self) -> str:
        return f"I am {self.name}"

    def __str__(self) -> str:
        return f"{super().__str__()} name={self.name}"


# ---------------------------------------------------------------------------
# Main demo class
# ---------------------------------------------------------------------------


class SyntaxKeywords:
    VERSION: int = 2  # class attribute (public + static + final analogue)

    def __init__(self, start: int = 0) -> None:
        self._counter = start
        self._cached: str | None = "init"
        self._lock = threading.Lock()

    # ---------------------------- Control Flow ----------------------------

    def bump(self, level: Level) -> int:
        inc = {
            Level.LOW: 1,
            Level.MEDIUM: 2,
            Level.HIGH: 3,
        }[level]
        self._counter += inc
        return self._counter

    def classic_match(self, code: int) -> None:
        match code:
            case 200:
                self._cached = "OK"
            case 500 | 503:
                self._cached = "SERVER_ERR"
            case _:
                self._cached = "UNKNOWN"

    def loops_and_flow(self) -> None:
        breaking = False
        for i in range(3):
            for j in range(3):
                if j == 1:
                    continue
                if i == 2 and j == 2:
                    breaking = True
                    break
                self._counter += i + j
            if breaking:
                break

        count = 0
        while count < 2:
            count += 1

        m = 0
        while True:
            m += 1
            if m >= 1:
                break

    # ------------------------ Exceptions & context -----------------------

    def risky(self) -> None:
        try:
            raise RuntimeError("boom")
        except RuntimeError as exc:
            self._cached = str(exc)
        finally:
            self._cached = self._cached or "ok"

    @contextmanager
    def tick(self):
        flag = {"open": True}
        try:
            yield flag
        finally:
            flag["open"] = False

    @contextmanager
    def string_reader(self, content: str):
        yield iter(content.splitlines())

    def with_resources(self, content: str) -> None:
        with self.tick() as state, self.string_reader(content) as reader:
            lines = list(reader)
            assert state["open"], "resource should be open"
            self._cached = lines[0] if lines else "empty"

    # --------------------------- Concurrency -----------------------------

    def sync_bump(self) -> int:
        with self._lock:
            self._counter += 1
            return self._counter

    # --------------------------- Pattern checks ---------------------------

    def who(self, obj: object) -> str:
        if isinstance(obj, User):
            return f"User:{obj.name}"
        return str(obj)

    # --------------------------- Misc helpers -----------------------------

    def legacy_echo(self, value: str) -> str:
        return value


def describe(n: int) -> str:
    match n:
        case 0:
            return "zero"
        case 1:
            return "one"
        case _:
            return "other"


def run_demo() -> None:
    greeter: Greeter = PrefixGreeter.of_prefix("Hi, ")
    print(greeter.hello(), "->", greeter.greet("Ada"))

    demo = SyntaxKeywords(10)
    print("bump LOW  :", demo.bump(Level.LOW))
    print("bump HIGH :", demo.bump(Level.HIGH))

    demo.loops_and_flow()
    demo.classic_match(200)
    demo.classic_match(999)

    demo.risky()
    demo.with_resources("first line\nsecond line")

    print("syncBump  :", demo.sync_bump())
    print("who(User) :", demo.who(User(1, "Turing")))

    being: Being = Person("Grace")
    print(being.say())
    print(being)

    print("describe(1)=", describe(1))
    print("legacyEcho=", demo.legacy_echo("echo"))
    assert SyntaxKeywords.VERSION >= 2


if __name__ == "__main__":
    run_demo()
