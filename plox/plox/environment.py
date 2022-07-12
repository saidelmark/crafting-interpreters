from plox.token_types import Token
from plox.errors import LoxRuntimeError


class Environment:
    def __init__(self):
        self._values = dict()

    def define(self, name: str, value):
        self._values[name] = value

    def get(self, name: Token):
        if name.lexeme in self._values.keys():
            return self._values[name.lexeme]
        raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')

    def assign(self, name: Token, value):
        if name.lexeme in self._values.keys():
            self._values[name.lexeme] = value
        else:
            raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')
