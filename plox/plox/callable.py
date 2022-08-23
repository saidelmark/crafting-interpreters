import time
from abc import abstractmethod

from plox.environment import Environment
from plox.return_ex import LoxReturn
from plox.statements import Function, Lambda


class LoxCallable:
    @abstractmethod
    def call(self, interpreter, args):
        raise NotImplementedError

    @abstractmethod
    def arity(self) -> int:
        raise NotImplementedError


class Clock(LoxCallable):
    def arity(self):
        return 0

    def call(self, interpreter, args):
        return time.time()*1000.0

    def __repr__(self):
        return '<native fn>'


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment):
        self._declaration = declaration
        self._closure = closure

    def call(self, interpreter, args):
        env = Environment(self._closure)
        for i in range(len(self._declaration.params)):
            env.define(self._declaration.params[i].lexeme, args[i])
        try:
            interpreter.execute_block(self._declaration.body, env)
        except LoxReturn as ret:
            return ret.value
        return None

    def arity(self):
        return len(self._declaration.params)

    def __repr__(self):
        return f'<fn {self._declaration.name.lexeme}>'


# TODO: this class is a copy-paste of LoxFunction except for the type of
# declaration. And even it doesn't really matter: both Function and Lambda are
# designed to have parameters and a body. Function has a name, but it doesn't
# matter in this context.
# Ideally this class should be turned into 4-5 lines of code.
class LoxLambda(LoxCallable):
    def __init__(self, declaration: Lambda, closure: Environment):
        self._declaration = declaration
        self._closure = closure

    def call(self, interpreter, args):
        env = Environment(self._closure)
        for i in range(len(self._declaration.params)):
            env.define(self._declaration.params[i].lexeme, args[i])
        try:
            interpreter.execute_block(self._declaration.body, env)
        except LoxReturn as ret:
            return ret.value
        return None

    def arity(self):
        return len(self._declaration.params)

    def __repr__(self):
        return '<lambda fn>'
