from plox.expressions import Expr
from dataclasses import dataclass


class Stmt:
    pass


@dataclass
class ExpressionStmt(Stmt):
    expr: Expr


@dataclass
class PrintStmt(Stmt):
    expr: Expr
