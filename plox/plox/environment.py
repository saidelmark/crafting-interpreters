from plox.errors import LoxRuntimeError
from plox.token_types import Token


class Environment:
    def __init__(self, enclosing: 'Environment' = None):
        self._values = dict()
        self.enclosing = enclosing

    def define(self, name: str, value):
        self._values[name] = value

    def get(self, name: Token):
        if name.lexeme in self._values.keys():
            return self._values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')

    def get_at(self, distance: int, name: str):
        return self._ancestor(distance)._values[name]

    def _ancestor(self, distance: int):
        env = self
        for _ in range(distance):
            env = env.enclosing
        return env

    def assign(self, name: Token, value):
        if name.lexeme in self._values.keys():
            self._values[name.lexeme] = value
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise LoxRuntimeError(name, f'Undefined variable {name.lexeme}.')

    def assign_at(self, distance: int, name: Token, value):
        self._ancestor(distance)._values[name.lexeme] = value
