from __future__ import annotations

"""One-file tour of Python data types inspired by the Java ``DataTypes`` demo.

Each function mirrors a numbered section from the original Java file so you can map
concepts one-to-one: primitives, wrappers, ``Decimal``-backed money, strings, time
types, optional/null objects, enums, generics, and defensive copies.
"""

from collections import deque
from ctypes import c_byte
from dataclasses import dataclass, field
from datetime import date, datetime, time
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
import re
from statistics import mean
from typing import Iterable, MutableSequence, Optional, Protocol, TypeVar
from zoneinfo import ZoneInfo

getcontext().prec = 50


def primitives_and_literals() -> None:
    """Showcase literal syntax and overflow emulation."""

    byte_literal = 0x7F
    octal_literal = 0o10
    binary_literal = 0b1010_1010
    large_int = 1_000_000_000

    floating = 3.14
    scientific = 6.022e23
    complex_num = 3 + 4j

    pi_symbol = "π"
    truthy = True

    wrapped = c_byte(127 + 1).value  # mimic Java's byte overflow

    print(
        "[Primitives] byte=%d octal=%d binary=%d large=%d float=%.2f sci=%.2e complex=%s pi=%s bool=%s overflow=%d"
        % (
            byte_literal,
            octal_literal,
            binary_literal,
            large_int,
            floating,
            scientific,
            complex_num,
            pi_symbol,
            truthy,
            wrapped,
        )
    )


def promotion_and_casting() -> None:
    """Demonstrate Python's numeric coercion rules."""

    a, b = 40, 50
    total = a + b
    back_to_int = int(a + b)

    z = 1 // 2  # integer division
    z_fix = 1 / 2  # float division

    print(f"[Promotion] total={total} back={back_to_int} z={z} z_fix={z_fix}")


def wrappers_and_identity() -> None:
    """Highlight how CPython caches small ints and how mutability works."""

    small_a = 127
    small_b = 127
    big_a = 10_000
    big_b = 10_000

    same_small = small_a is small_b
    same_big = big_a is big_b

    numbers = [1, 2, 3]
    alias = numbers
    alias.append(4)

    npe_equiv = False
    maybe_none: Optional[int] = None
    try:
        _ = maybe_none + 1  # type: ignore[operator]
    except TypeError:
        npe_equiv = True

    print(
        f"[Wrappers] small_identity={same_small} big_identity={same_big} "
        f"shared_list={numbers} alias_is_same={alias is numbers} npe_on_none={npe_equiv}"
    )


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        normalized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        object.__setattr__(self, "amount", normalized)
        if not re.fullmatch(r"[A-Z]{3}", self.currency):
            raise ValueError("Currency must be a valid ISO‑4217 code")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)


def big_numbers_and_money() -> None:
    """Use arbitrary-precision ints and decimals for financial math."""

    big_int = 123_456_789_012_345_678_901_234_567_890
    a = Decimal("0.1")
    b = Decimal("0.2")
    exact = a + b

    total = Money(Decimal("1.00"), "USD") + Money(Decimal("2.50"), "USD")

    print(f"[Big] int={big_int} exact={exact} money_total={total.amount} {total.currency}")


def strings_and_text() -> None:
    """String identity, equality, builders, and encodings."""

    s = "Ada"
    interned_eq = "sameRef" if ("Ada" is s) else "diffRef"
    value_eq = str("Ada") == s

    concat = "a"
    for i in range(5):
        concat += str(i)

    builder_parts = ["a"]
    for i in range(5):
        builder_parts.append(str(i))
    builder = "".join(builder_parts)

    json = """
    {"name":"Ada","lang":"Python"}
    """.strip()

    bytes_value = "π".encode("utf-8")

    print(
        f"[Strings] interned={interned_eq} value_eq={value_eq} concat={concat} "
        f"builder={builder} json_len={len(json)} bytes={list(bytes_value)}"
    )


def arrays_and_collections() -> None:
    """List/tuple basics plus deque and streaming helpers."""

    xs = [1, 2, 3]
    tup = tuple(xs)
    unique = {1, 2, 2, 3}

    arr_like = xs.copy()  # pretend array clone
    arr_like[0] = 99

    queue = deque(["a", "b"])
    queue.appendleft("start")

    averaged = mean([1, 2, 3, 4])

    print(
        f"[Arrays] list={xs} tuple={tup} set={unique} cloned={arr_like} deque={list(queue)} "
        f"mean={averaged}"
    )


def time_types() -> None:
    """datetime.date/time/datetime with zones."""

    d = date(2025, 9, 6)
    t = time(12, 34, 56)
    z = datetime.now(tz=ZoneInfo("America/New_York"))

    print(f"[Time] date={d} time={t} offset={z.utcoffset()}")


def parse_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None


class Discount(Protocol):
    def apply(self, price: int) -> int:
        ...


@dataclass(frozen=True)
class NoDiscount:
    def apply(self, price: int) -> int:
        return price


@dataclass(frozen=True)
class TenPercent:
    def apply(self, price: int) -> int:
        return int(price * 0.9)


def optionals_and_null_object() -> None:
    good = parse_int("42") or 0
    fallback = parse_int("xx") or 7
    discount: Discount = NoDiscount()

    print(f"[Optional] good={good} fallback={fallback} price={discount.apply(100)}")


from enum import Enum, auto


class Unit(Enum):
    BYTES = auto()
    KILOBYTES = auto()
    MEGABYTES = auto()


def to_bytes(value: int, unit: Unit) -> int:
    if unit is Unit.BYTES:
        return value
    if unit is Unit.KILOBYTES:
        return value * 1024
    if unit is Unit.MEGABYTES:
        return value * 1024 * 1024
    raise ValueError(unit)


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError("Invalid email")


@dataclass(frozen=True)
class Count:
    n: int


@dataclass(frozen=True)
class Weight:
    kg: float


Quantity = Count | Weight


def type_system_pieces() -> None:
    bytes_value = to_bytes(2, Unit.MEGABYTES)
    email = Email("ada@lovelace.org")
    q1: Quantity = Count(3)
    q2: Quantity = Weight(1.5)

    print(
        f"[Types] bytes={bytes_value} email={email.value} count={q1.n} weight={q2.kg:.1f}kg"
    )


T = TypeVar("T")


@dataclass
class Box(MutableSequence[T]):
    _storage: list[T] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self._storage)

    def __getitem__(self, index: int) -> T:
        return self._storage[index]

    def __setitem__(self, index: int, value: T) -> None:
        self._storage[index] = value

    def __delitem__(self, index: int) -> None:
        del self._storage[index]

    def insert(self, index: int, value: T) -> None:
        self._storage.insert(index, value)


def sum_numbers(xs: Iterable[float]) -> float:
    total = 0.0
    for value in xs:
        total += float(value)
    return total


def add_ints(xs: MutableSequence[int]) -> None:
    xs.append(1)
    xs.append(2)


def generics_and_variance() -> None:
    box = Box[str]()
    box.append("x")
    total = sum_numbers([1, 2, 3])
    nums: list[int] = []
    add_ints(nums)

    print(f"[Generics] box={box._storage} total={total:.0f} out={nums}")


@dataclass(frozen=True)
class CustomerId:
    value: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"[A-Z0-9]{6,}", self.value):
            raise ValueError("Invalid customer id")


@dataclass(frozen=True)
class OrderLines:
    lines: tuple[str, ...]

    def __init__(self, lines: Iterable[str]):
        object.__setattr__(self, "lines", tuple(lines))


def architect_patterns() -> None:
    customer_id = CustomerId("ABC123")
    order_lines = OrderLines(["a", "b"])
    print(f"[Architect] id={customer_id.value} lines={order_lines.lines}")


def run_demo() -> None:
    primitives_and_literals()
    promotion_and_casting()
    wrappers_and_identity()
    big_numbers_and_money()
    strings_and_text()
    arrays_and_collections()
    time_types()
    optionals_and_null_object()
    type_system_pieces()
    generics_and_variance()
    architect_patterns()


if __name__ == "__main__":
    run_demo()
