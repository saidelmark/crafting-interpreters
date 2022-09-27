from dataclasses import dataclass

from plox.callable import LoxCallable, LoxFunction
from plox.errors import LoxRuntimeError
from plox.token_types import Token


@dataclass
class LoxClass(LoxCallable):
    name: str
    _methods: dict()

    def __str__(self):
        return self.name

    def call(self, interpreter, args):
        instance = LoxInstance(_klass=self, _fields={})
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, args)
        return instance

    def arity(self):
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()

    def find_method(self, name: str) -> LoxFunction:
        if name in self._methods.keys():
            return self._methods[name]
        return None


@dataclass
class LoxInstance:
    _klass: LoxClass
    _fields: dict()

    def __str__(self):
        return f'{self._klass.name} instance'

    def get(self, name: Token):
        if name.lexeme in self._fields.keys():
            return self._fields[name.lexeme]

        method = self._klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, f'Undefined property {name.lexeme}.')

    def set(self, name: Token, value):
        self._fields[name.lexeme] = value
