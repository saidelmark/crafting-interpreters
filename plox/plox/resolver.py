from enum import Enum, auto
from functools import singledispatchmethod

from plox.errors import LoxErrors
from plox.expressions import (Assignment, Binary, Call, Expr, Grouping,
                              Literal, Logical, Unary, Variable)
from plox.interpreter import Interpreter
from plox.statements import (Block, Expression, Function, If, Lambda, Print,
                             Return, Stmt, Var, While)
from plox.token_types import Token


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()


class Resolver:
    def __init__(self, interpreter: Interpreter):
        self._interpreter = interpreter
        self._scopes: list(dict) = []
        self._current_function = FunctionType.NONE

    def resolve(self, stmts: [Stmt]):
        for stmt in stmts:
            self._resolve_stmt(stmt)

    @singledispatchmethod
    def _resolve_stmt(self, stmt: Stmt):
        raise NotImplementedError

    @_resolve_stmt.register
    def _(self, stmt: Block):
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()
        return None

    @_resolve_stmt.register
    def _(self, stmt: Var):
        self._declare(stmt.name)
        if stmt.init is not None:
            self._resolve_expr(stmt.init)
        self._define(stmt.name)
        return None

    @_resolve_stmt.register
    def _(self, stmt: Function):
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def _resolve_function(self, fn: Function, type: FunctionType):
        enclosing_function = self._current_function
        self._current_function = type
        self._begin_scope()
        for param in fn.params:
            self._declare(param)
            self._define(param)
        self.resolve(fn.body)
        self._end_scope()
        self._current_function = enclosing_function

    @_resolve_stmt.register
    def _(self, stmt: Expression):
        self._resolve_expr(stmt.expr)
        return None

    @_resolve_stmt.register
    def _(self, stmt: If):
        self._resolve_expr(stmt.condition)
        self._resolve_stmt(stmt.then_branch)
        if stmt.else_branch is not None:
            self._resolve_stmt(stmt.else_branch)
        return None

    @_resolve_stmt.register
    def _(self, stmt: Print):
        self._resolve_expr(stmt.expr)
        return None

    @_resolve_stmt.register
    def _(self, stmt: Return):
        if self._current_function == FunctionType.NONE:
            LoxErrors.error(stmt.keyword.line,
                            'Can\'t return from top-level context')
        if stmt.value is not None:
            self._resolve_expr(stmt.value)
        return None

    @_resolve_stmt.register
    def _(self, stmt: While):
        self._resolve_expr(stmt.condition)
        self._resolve_stmt(stmt.body)
        return None

    @singledispatchmethod
    def _resolve_expr(self, expr: Expr):
        raise NotImplementedError

    @_resolve_expr.register
    def _(self, expr: Binary):
        self._resolve_expr(expr.left)
        self._resolve_expr(expr.right)
        return None

    @_resolve_expr.register
    def _(self, expr: Logical):
        self._resolve_expr(expr.left)
        self._resolve_expr(expr.right)
        return None

    @_resolve_expr.register
    def _(self, expr: Unary):
        self._resolve_expr(expr.right)
        return None

    @_resolve_expr.register
    def _(self, expr: Lambda):
        self._resolve_function(expr, type=FunctionType.FUNCTION)
        return None

    @_resolve_expr.register
    def _(self, expr: Call):
        self._resolve_expr(expr.callee)
        for arg in expr.args:
            self._resolve_expr(arg)
        return None

    @_resolve_expr.register
    def _(self, expr: Grouping):
        self._resolve_expr(expr.expression)
        return None

    @_resolve_expr.register
    def _(self, expr: Literal):
        return None

    @_resolve_expr.register
    def _(self, expr: Variable):
        if self._scopes \
                and expr.name.lexeme in self._scopes[-1] \
                and not self._scopes[-1][expr.name.lexeme]:
            LoxErrors.error(
                expr.name.line,
                'Can\'t read local variable in its own initializer'
            )
        self._resolve_local(expr, expr.name)
        return None

    @_resolve_expr.register
    def _(self, expr: Assignment):
        self._resolve_expr(expr.value)
        self._resolve_local(expr, expr.name)
        return None

    def _declare(self, name: Token):
        if not self._scopes:
            return
        scope = self._scopes[-1]
        if name.lexeme in scope:
            LoxErrors.error(
                name.line, 'Already a variable with this name in this scope.')
        scope[name.lexeme] = False

    def _define(self, name: Token):
        if not self._scopes:
            return
        scope = self._scopes[-1]
        scope[name.lexeme] = True

    def _resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self._scopes)-1, -1, -1):
            if name.lexeme in self._scopes[i]:
                self._interpreter.resolve(expr, len(self._scopes) - i - 1)
                return

    def _begin_scope(self):
        self._scopes.append({})

    def _end_scope(self):
        self._scopes.pop()
