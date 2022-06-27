import sys
from plox.token_types import Token


class LoxErrors:
    had_error = False
    had_runtime_error = False

    @staticmethod
    def error(line: int, message: str):
        LoxErrors.was_error = True
        LoxErrors._report(line, "", message)

    @staticmethod
    def runtime_error(re: RuntimeError):
        LoxErrors.had_runtime_error = True
        print(f'{re}\n[line {re.token.line}]', file=sys.stderr)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")


class LoxRuntimeError(Exception):
    def __init__(self, token: Token, message):
        super().__init__(message)
        self.message = message
        self.token = token

    def __str__(self):
        return f"{self.token.lexeme}: {self.message}"
