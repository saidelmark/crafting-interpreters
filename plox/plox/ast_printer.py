from functools import singledispatchmethod
from plox.expressions import Binary, Expr, Grouping, Literal, Unary


class AstPrinter:
    @singledispatchmethod
    def print(self, expr: Expr) -> str:
        pass

    @print.register
    def _(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @print.register
    def _(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.right)

    @print.register
    def _(self, expr: Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    @print.register
    def _(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        return f"({name} {' '.join(map(self.print, exprs))})"
