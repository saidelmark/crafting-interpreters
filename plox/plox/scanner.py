import string
from plox.token_types import Token, TokenType, KEYWORD_TOKEN_TYPES
from plox.errors import error


class Scanner:
    def __init__(self, source):
        self._tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._source = source

    def scan_tokens(self) -> [Token]:
        while not self._is_at_end():
            self._start = self._current
            self.scan_single_token()

        return self._tokens

    def scan_single_token(self):
        c = self._advance()
        match c:
            case '(':
                self._add_token(TokenType.LEFT_PAREN)
            case ')':
                self._add_token(TokenType.RIGHT_PAREN)
            case '{':
                self._add_token(TokenType.LEFT_BRACE)
            case '}':
                self._add_token(TokenType.RIGHT_BRACE)
            case ',':
                self._add_token(TokenType.COMMA)
            case '.':
                self._add_token(TokenType.DOT)
            case '-':
                self._add_token(TokenType.MINUS)
            case '+':
                self._add_token(TokenType.PLUS)
            case ';':
                self._add_token(TokenType.SEMICOLON)
            case '*':
                self._add_token(TokenType.STAR)
            case '!':
                if self._match("="):
                    self._add_token(TokenType.BANG_EQUAL)
                else:
                    self._add_token(TokenType.BANG)
            case '=':
                if self._match("="):
                    self._add_token(TokenType.EQUAL_EQUAL)
                else:
                    self._add_token(TokenType.EQUAL)
            case '>':
                if self._match("="):
                    self._add_token(TokenType.GREATER_EQUAL)
                else:
                    self._add_token(TokenType.GREATER)
            case '<':
                if self._match("="):
                    self._add_token(TokenType.LESS_EQUAL)
                else:
                    self._add_token(TokenType.LESS)
            case '/':
                if self._match("/"):
                    while not self._is_at_end() and self._peek not in ['\n', None]:
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self._line += 1
            case '"':
                self._scan_string()

            case _:
                if is_digit(c):
                    self._scan_number()
                elif is_alpha(c):
                    self._scan_identifier()
                else:
                    error(self._line, f"Unexpected character {c}.")

    def _add_token(self, token_type: TokenType, literal=None):
        token = Token(
            type=token_type,
            lexeme=self._source[self._start: self._current],
            literal=literal,
            line=self._line
        )
        self._tokens.append(token)

    def _advance(self) -> str:
        char = self._source[self._current]
        self._current += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return None
        return self._source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return None
        return self._source[self._current + 1]

    def _is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def _scan_string(self):
        while self._peek() not in ['"', None]:
            if self._peek() == '\n':
                self._line += 1
            self._advance()
        if self._is_at_end():
            # string not terminated
            error(self._line, "Unterminated string")
            return
        self._advance()  # step over '"'
        # +-1 are trimming the surrounding '"'
        value = self._source[self._start + 1:self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _scan_number(self):
        while is_digit(self._peek()):
            self._advance()
        # check if there's a fractional part
        if self._peek() == '.' and is_digit(self._peek_next()):
            self._advance()
            while is_digit(self._peek()):
                self._advance()

        self._add_token(TokenType.NUMBER,
                        float(self._source[self._start:self._current]))

    def _scan_identifier(self):
        while is_alphanumeric(self._peek()):
            self._advance()

        word = self._source[self._start:self._current]
        token_type = KEYWORD_TOKEN_TYPES.get(word, TokenType.IDENTIFIER)
        self._add_token(token_type)


def is_digit(char: str) -> bool:
    return char and char in string.digits


def is_alpha(char: str) -> bool:
    return char and char in string.ascii_letters or char == '_'


def is_alphanumeric(char):
    return is_digit(char) or is_alpha(char)
