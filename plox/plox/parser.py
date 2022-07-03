from plox.token_types import Token, TokenType
from plox.expressions import Expr, Binary, Unary, Literal, Grouping
from plox.errors import LoxErrors


class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> Expr:
        try:
            return self._expression()
        except Exception:
            return None

    def _expression(self) -> Expr:
        return self._equality()

    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL,
                          TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()
        while self._match(TokenType.GREATER,
                          TokenType.GREATER_EQUAL,
                          TokenType.LESS,
                          TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(TokenType.MINUS,
                          TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(TokenType.SLASH,
                          TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG,
                       TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER,
                       TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN,
                          "Expect ')' after expression.")
            return Grouping(expr)
        raise Exception(self._peek(), "Expect expression")

    # Methods that work with the tokens stream
    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _consume(self, type: TokenType, message: str) -> Token:
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, type: TokenType) -> bool:
        if self._is_at_and():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_and():
            self._current += 1
        return self._previous()

    def _is_at_and(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _error(self, token: Token, message: str):
        if token.type == TokenType.EOF:
            LoxErrors.report(token.line, " at end", message)
        else:
            LoxErrors.report(token.line, " at '" + token.lexeme + "'", message)
        raise Exception("Parse error")

    def synchronize(self):
        self._advance()
        while not self._is_at_and():
            if self._previous().type == TokenType.SEMICOLON:
                return
            match self._peek().type:
                case TokenType.CLASS |\
                        TokenType.FUN |\
                        TokenType.VAR |\
                        TokenType.FOR |\
                        TokenType.IF |\
                        TokenType.WHILE |\
                        TokenType.PRINT |\
                        TokenType.RETURN:
                    return
            self._advance()
