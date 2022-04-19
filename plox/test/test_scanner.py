from plox.scanner import Scanner
from plox.token_types import Token, TokenType


def test_scanner():
    src = ""
    with open("test/scanner.lox") as lox_src:
        src = lox_src.read()

    scanner = Scanner(src)

    expected_list = [
        Token(type=TokenType.PRINT, lexeme='print', literal=None, line=2),
        Token(type=TokenType.STRING, lexeme='"Hello, world!"',
              literal='Hello, world!', line=2),
        Token(type=TokenType.SEMICOLON, lexeme=';', literal=None, line=2),
        Token(type=TokenType.TRUE, lexeme='true', literal=None, line=3),
        Token(type=TokenType.FALSE, lexeme='false', literal=None, line=4),
        Token(type=TokenType.NUMBER, lexeme='90832', literal=90832.0, line=5),
        Token(type=TokenType.MINUS, lexeme='-', literal=None, line=6),
        Token(type=TokenType.NUMBER, lexeme='7.234', literal=7.234, line=6),
        Token(type=TokenType.STRING, lexeme='"some string"',
              literal='some string', line=7),
        Token(type=TokenType.SLASH, lexeme='/', literal=None, line=8),
        Token(type=TokenType.PLUS, lexeme='+', literal=None, line=8),
        Token(type=TokenType.MINUS, lexeme='-', literal=None, line=8),
        Token(type=TokenType.STAR, lexeme='*', literal=None, line=8),
        Token(type=TokenType.EQUAL, lexeme='=', literal=None, line=8),
        Token(type=TokenType.EQUAL_EQUAL, lexeme='==', literal=None, line=8),
        Token(type=TokenType.GREATER, lexeme='>', literal=None, line=8),
        Token(type=TokenType.GREATER_EQUAL, lexeme='>=', literal=None, line=8),
        Token(type=TokenType.LESS, lexeme='<', literal=None, line=8),
        Token(type=TokenType.LESS_EQUAL, lexeme='<=', literal=None, line=8),
        Token(type=TokenType.BANG, lexeme='!', literal=None, line=8),
        Token(type=TokenType.BANG_EQUAL, lexeme='!=', literal=None, line=8),
        Token(type=TokenType.COMMA, lexeme=',', literal=None, line=8),
        Token(type=TokenType.DOT, lexeme='.', literal=None, line=8),
        Token(type=TokenType.IDENTIFIER, lexeme='name', literal=None, line=9),
        Token(type=TokenType.IDENTIFIER,
              lexeme='another_name123', literal=None, line=10),
        Token(type=TokenType.AND, lexeme='and', literal=None, line=11),
        Token(type=TokenType.OR, lexeme='or', literal=None, line=11),
        Token(type=TokenType.LEFT_PAREN, lexeme='(', literal=None, line=12),
        Token(type=TokenType.RIGHT_PAREN, lexeme=')', literal=None, line=12),
        Token(type=TokenType.LEFT_BRACE, lexeme='{', literal=None, line=12),
        Token(type=TokenType.RIGHT_BRACE, lexeme='}', literal=None, line=12),
        Token(type=TokenType.VAR, lexeme='var', literal=None, line=13),
        Token(type=TokenType.PRINT, lexeme='print', literal=None, line=13),
        Token(type=TokenType.IF, lexeme='if', literal=None, line=13),
        Token(type=TokenType.ELSE, lexeme='else', literal=None, line=13),
        Token(type=TokenType.WHILE, lexeme='while', literal=None, line=13),
        Token(type=TokenType.FOR, lexeme='for', literal=None, line=13),
        Token(type=TokenType.FUN, lexeme='fun', literal=None, line=15),
        Token(type=TokenType.CLASS, lexeme='class', literal=None, line=15),
        Token(type=TokenType.RETURN, lexeme='return', literal=None, line=15),
        Token(type=TokenType.THIS, lexeme='this', literal=None, line=15),
        Token(type=TokenType.SUPER, lexeme='super', literal=None, line=15),
    ]

    for (scanned, expected) in zip(scanner.scan_tokens(), expected_list):
        assert scanned == expected
