from abc import abstractmethod
from plox.environment import Environment
from plox.statements import Function
from plox.return_ex import LoxReturn
import time


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