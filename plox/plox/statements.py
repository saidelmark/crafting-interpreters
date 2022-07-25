from plox.expressions import Expr
from dataclasses import dataclass
from plox.token_types import Token


class Stmt:
    pass


@dataclass
class Expression(Stmt):
    expr: Expr


@dataclass
class Print(Stmt):
    expr: Expr


@dataclass
class Var(Stmt):
    name: Token
    init: Expr


@dataclass
class Block(Stmt):
    statements: [Stmt]


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt
