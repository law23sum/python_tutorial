from __future__ import annotations

"""Python translation of the Java ``Operators`` tour.

Each function mirrors the numbered Java sections but uses simple, idiomatic Python so
learners can compare both languages side-by-side inside the foundations module.
"""

from dataclasses import dataclass
from typing import Protocol


def unary_demo() -> None:
    x = 5
    x += 1  # ++x
    pre = x
    post = x
    x += 1  # x++
    y = -x
    z = +y
    b = False
    nb = not b
    mask = 0b0101_1100
    not_mask = ~mask

    print("--- Unary")
    print(f"pre={pre}, post={post}, final x={x}")
    print(f"y={y}, z={z}")
    print(f"!false={nb}")
    print(f"~0b0101_1100 = {bin32(not_mask)}")


def arithmetic_demo() -> None:
    a, b = 7, 3
    sum_ = a + b
    diff = a - b
    prod = a * b
    quo = a // b
    rem = a % b
    dquo = 7.0 / 3
    drem = 7.0 % 3.0
    s = "Ans=" + str(a) + str(b)
    s2 = f"Ans={a + b}"
    nan = float("nan")

    print("--- Arithmetic")
    print(f"sum={sum_}, diff={diff}, prod={prod}, quo={quo}, rem={rem}")
    print(f"dquo={dquo}, drem={drem}")
    print(f"concat: {s} | {s2}")
    print(f"nan==nan? {nan == nan}, nan!=nan? {nan != nan}")


def assignment_demo() -> None:
    s = 1
    s = (s + 1) & 0xFFFF  # mimic short wrapping
    x = 5
    x *= 3 + 2
    y = 1
    y <<= 2

    print("--- Assignment & Compound")
    print(f"short s after s+=1 -> {s}")
    print(f"x after x*=3+2 -> {x}")
    print(f"y after y<<=2 -> {y}")


def relational_equality_demo() -> None:
    a, b = 10, 20
    print("--- Relational & Equality")
    print(f"a<b? {a < b}, a>=b? {a >= b}, a==b? {a == b}")
    p = "hello"
    q = "hello"
    r = str("hello")
    print(f"p is q? {p is q}")
    print(f"p is r? {p is r}")
    print(f"p == r? {p == r}")


@dataclass
class SideEffectTracker:
    events: list[str]

    def log(self, label: str) -> bool:
        self.events.append(label)
        return True


def logical_demo() -> None:
    tracker = SideEffectTracker([])
    short_circuit = True or tracker.log("OR right evaluated?")
    non_short = True | tracker.log("OR(|) right evaluated?")
    sc_and = False and tracker.log("AND right evaluated?")
    non_sc_and = False & tracker.log("AND(&) right evaluated?")

    print("--- Logical (short-circuit vs non)")
    print(f"shortCircuit(||)={short_circuit}, nonShort(|)={non_short}")
    print(f"scAnd(&&)={sc_and}, nonScAnd(&)={non_sc_and}")
    for event in tracker.events:
        print(f"  side-effect -> {event}")


def bitwise_demo() -> None:
    a = 0b0101_1100
    b = 0b0011_0011
    and_ = a & b
    or_ = a | b
    xor = a ^ b
    not_ = ~a
    lower4 = a & 0b1111

    print("--- Bitwise")
    print(f"a:   {bin32(a)}")
    print(f"b:   {bin32(b)}")
    print(f"a&b: {bin32(and_)}")
    print(f"a|b: {bin32(or_)}")
    print(f"a^b: {bin32(xor)}")
    print(f"~a : {bin32(not_)}")
    print(f"lower4(a)={bin(lower4)}")


def shift_demo() -> None:
    pos = 0b0000_0000_0000_0000_0000_0000_1001_0110
    neg = -150
    left = pos << 2
    right_signed = neg >> 3
    right_unsigned = (neg % (1 << 32)) >> 3

    print("--- Shifts")
    print(f"pos      : {bin32(pos)}")
    print(f"pos<<2   : {bin32(left)}")
    print(f"neg      : {bin32(neg)}")
    print(f"neg>>3   : {bin32(right_signed)}")
    print(f"neg>>>3  : {bin32(right_unsigned)}")


def ternary_demo() -> None:
    n = 7
    parity = "even" if n % 2 == 0 else "odd"
    print("--- Ternary")
    print(f"n={n} is {parity}")


def pattern_instanceof_and_precedence_demo() -> None:
    obj: object = "Ada Lovelace"
    if isinstance(obj, str) and len(obj) > 3:
        print("--- isinstance check")
        print(f"String of len {len(obj)}: {obj.upper()}")
    a, b = 3, 5
    p1 = (a + b) << 2
    p2 = a + (b << 2)
    print("--- Precedence")
    print(f"(a + b) << 2 = {p1} | a + (b << 2) = {p2}")
    x = y = 10
    print(f"x={x}, y={y}")


def promotion_and_overflow_demo() -> None:
    b1, b2 = 100, 27
    sum_ = b1 + b2
    bsum_cast = (b1 + b2 + 128) % 256 - 128
    print("--- Numeric promotion & overflow")
    print(f"sum(int)={sum_}, cast back to byte={bsum_cast}")
    max_int = 2**31 - 1
    wrapped = (max_int + 1 + 2**31) % 2**32 - 2**31
    print(f"overflow wrap: {max_int} + 1 = {wrapped}")


class Discount(Protocol):
    def apply(self, price: int) -> int: ...


@dataclass(frozen=True)
class NoDiscount:
    def apply(self, price: int) -> int:
        return price


def optionals_and_null_object() -> None:
    def parse_int(value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            return None

    good = parse_int("42") or 0
    fallback = parse_int("xx") or 7
    discount: Discount = NoDiscount()
    print("--- Optional")
    print(f"good={good} fallback={fallback} price={discount.apply(100)}")


def bin32(value: int) -> str:
    value &= (1 << 32) - 1
    bits = f"{value:032b}"
    return f"{bits[:8]}_{bits[8:16]}_{bits[16:24]}_{bits[24:]}"


def run_demo() -> None:
    unary_demo()
    arithmetic_demo()
    assignment_demo()
    relational_equality_demo()
    logical_demo()
    bitwise_demo()
    shift_demo()
    ternary_demo()
    pattern_instanceof_and_precedence_demo()
    promotion_and_overflow_demo()
    optionals_and_null_object()


if __name__ == "__main__":
    run_demo()
