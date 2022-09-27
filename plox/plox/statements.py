from dataclasses import dataclass

from plox.expressions import Expr
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
class Return(Stmt):
    keyword: Token
    value: Expr


@dataclass
class Var(Stmt):
    name: Token
    init: Expr


@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt


@dataclass
class Block(Stmt):
    statements: [Stmt]


@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt


@dataclass
class Function(Stmt):
    name: Token
    params: [Token]
    body: [Stmt]


@dataclass
class Class(Stmt):
    name: Token
    methods: [Function]

@dataclass
class Lambda(Expr):
    params: [Token]
    body: [Stmt]
