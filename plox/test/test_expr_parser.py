from plox.ast_printer import AstPrinter
from plox.token_types import Token, TokenType
from plox.parser import Parser


def test_expr_parser():
    tokens = [
        Token(type=TokenType.NUMBER, lexeme='4', literal=4.0, line=1),
        Token(type=TokenType.PLUS, lexeme='+', literal=None, line=1),
        Token(type=TokenType.NUMBER, lexeme='3', literal=3.0, line=1),
        Token(type=TokenType.SLASH, lexeme='/', literal=None, line=1),
        Token(type=TokenType.LEFT_PAREN, lexeme='(', literal=None, line=1),
        Token(type=TokenType.NUMBER, lexeme='1', literal=1.0, line=1),
        Token(type=TokenType.MINUS, lexeme='-', literal=None, line=1),
        Token(type=TokenType.NUMBER, lexeme='2', literal=2.0, line=1),
        Token(type=TokenType.RIGHT_PAREN, lexeme=')', literal=None, line=1),
        Token(type=TokenType.SEMICOLON, lexeme=';', literal=None, line=1)
    ]
    parser = Parser(tokens)

    expected = "(+ 4.0 (/ 3.0 (group (- 1.0 2.0))))"
    assert AstPrinter().print(parser.parse()) == expected
