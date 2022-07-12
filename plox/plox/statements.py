from plox.expressions import Expr
from dataclasses import dataclass
from plox.token_types import Token


class Stmt:
    pass


@dataclass
class ExpressionStmt(Stmt):
    expr: Expr


@dataclass
class PrintStmt(Stmt):
    expr: Expr


@dataclass
class VarStmt(Stmt):
    name: Token
    init: Expr
