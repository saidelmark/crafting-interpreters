from dataclasses import dataclass
from typing import Any

from plox.token_types import Token


class Expr:
    pass


@dataclass(frozen=True)
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Call(Expr):
    callee: Expr
    paren: Token
    args: [Expr]


@dataclass
class Get(Expr):
    object: Expr
    name: Token


@dataclass
class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class Set(Expr):
    object: Expr
    name: Token
    value: Expr


@dataclass(frozen=True)
class Super(Expr):
    keyword: Token
    method: Token


@dataclass(frozen=True)
class This(Expr):
    keyword: Token


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr


@dataclass
class Grouping(Expr):
    expression: Expr


@dataclass(frozen=True)
class Literal(Expr):
    value: Any


@dataclass(frozen=True)
class Variable(Expr):
    name: Token


@dataclass(frozen=True)
class Assignment(Expr):
    name: Token
    value: Expr
