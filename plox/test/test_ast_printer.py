from plox.expressions import Binary, Unary, Literal, Grouping
from plox.ast_printer import AstPrinter
from plox.token_types import Token, TokenType


def test_ast_printer():
    expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123),
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )

    assert AstPrinter().print(expr) == "(* (- 123) (group 45.67))"
