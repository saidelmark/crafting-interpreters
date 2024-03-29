from functools import singledispatchmethod

from plox.callable import Clock, LoxCallable, LoxFunction, LoxLambda
from plox.environment import Environment
from plox.errors import LoxErrors, LoxRuntimeError
from plox.expressions import (Assignment, Binary, Call, Expr, Get, Grouping,
                              Literal, Logical, Set, Super, This, Unary,
                              Variable)
from plox.lox_class import LoxClass, LoxInstance
from plox.return_ex import LoxReturn
from plox.statements import (Block, Class, Expression, Function, If, Lambda,
                             Print, Return, Stmt, Var, While)
from plox.token_types import Token, TokenType


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self._locals = {}
        self._env = self.globals

        self.globals.define('clock', Clock())

    def interpret(self, statements: Stmt):
        try:
            for statement in statements:
                if statement is not None:
                    self._execute(statement)
        except LoxRuntimeError as e:
            LoxErrors.runtime_error(e)

    def resolve(self, expr: Expr, depth: int):
        self._locals[expr] = depth

    @singledispatchmethod
    def _execute(self, stmt: Stmt):
        raise NotImplementedError

    @_execute.register
    def _(self, stmt: If):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)
        else:
            return None

    @_execute.register
    def _(self, stmt: Expression):
        self._evaluate(stmt.expr)

    @_execute.register
    def _(self, stmt: Function):
        function = LoxFunction(stmt, self._env, False)
        self._env.define(stmt.name.lexeme, function)
        return None

    @_execute.register
    def _(self, stmt: Print):
        value = self._evaluate(stmt.expr)
        print(self._stringify(value))

    @_execute.register
    def _(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self._evaluate(stmt.value)
        raise LoxReturn(value)

    @_execute.register
    def _(self, stmt: Var):
        value = None
        if stmt.init is not None:
            value = self._evaluate(stmt.init)
        self._env.define(stmt.name.lexeme, value)

    @_execute.register
    def _(self, stmt: While):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    @_execute.register
    def _(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self._env))

    @_execute.register
    def _(self, stmt: Class):
        superclass = None
        if stmt.superclass is not None:
            superclass = self._evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise LoxRuntimeError(
                    stmt.superclass.name, 'Superclass must be a class')
        self._env.define(stmt.name.lexeme, None)

        if superclass is not None:
            self._env = Environment(self._env)
            self._env.define('super', superclass)

        methods = dict()
        for method in stmt.methods:
            function = LoxFunction(method, self._env,
                                   method.name.lexeme == 'init')
            methods[method.name.lexeme] = function
        klass = LoxClass(stmt.name.lexeme, superclass, methods)
        if superclass is not None:
            self._env = self._env.enclosing
        self._env.assign(stmt.name, klass)
        return None

    def execute_block(self, statements: [Stmt], env: Environment):
        prev_env = self._env
        self._env = env
        try:
            for statement in statements:
                self._execute(statement)
        finally:
            self._env = prev_env

    @singledispatchmethod
    def _evaluate(self, expr: Expr):
        raise NotImplementedError

    @_evaluate.register
    def _(self, expr: Assignment):
        value = self._evaluate(expr.value)
        distance = self._locals.get(expr)
        if distance is not None:
            return self._env.assign_at(distance, expr.name, value)
        else:
            return self.globals.assign(expr.name, value)
        return value

    @_evaluate.register
    def _(self, expr: Binary):
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        match expr.operator.type:
            case TokenType.AND:
                return self._is_truthy(left) and self._is_truthy(right)
            case TokenType.OR:
                return self._is_truthy(left) or self._is_truthy(right)
            case TokenType.BANG_EQUAL:
                return not self._check_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self._check_equal(left, right)
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left >= right
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return left <= right
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return left - right
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise LoxRuntimeError(
                    expr.operator,
                    'Operands must be two numbers or two strings.'
                )
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                return left / right
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return left * right

    @_evaluate.register
    def _(self, expr: Lambda):
        return LoxLambda(expr, self._env)

    @_evaluate.register
    def _(self, expr: Call):
        callee = self._evaluate(expr.callee)
        args = []
        for arg in expr.args:
            args.append(self._evaluate(arg))
        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(
                expr.paren, 'Can only call functions and classes')
        function: LoxCallable = callee
        if len(args) != function.arity():
            raise LoxRuntimeError(
                expr.paren,
                f'Expected {function.arity()} arguments, but got {len(args)}.')
        return function.call(self, args)

    @_evaluate.register
    def _(self, expr: Get):
        obj = self._evaluate(expr.object)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)
        raise LoxRuntimeError(expr.name, 'Only instances have properties.')

    @_evaluate.register
    def _(self, expr: Super):
        distance = self._locals.get(expr)
        superclass: LoxClass = self._env.get_at(distance, 'super')
        object: LoxInstance = self._env.get_at(distance - 1, 'this')
        method: LoxFunction = superclass.find_method(expr.method.lexeme)
        if method is None:
            raise LoxRuntimeError(
                expr.method, f'Undefined property {expr.method.lexeme}.')
        return method.bind(object)

    @_evaluate.register
    def _(self, expr: Set):
        object = self._evaluate(expr.object)
        if not isinstance(object, LoxInstance):
            raise LoxRuntimeError(expr.name, 'Only instances have fields')
        value = self._evaluate(expr.value)
        object.set(expr.name, value)
        return value

    @_evaluate.register
    def _(self, expr: This):
        return self._lookup_var(expr.keyword, expr)

    @_evaluate.register
    def _(self, expr: Unary):
        right = self._evaluate(expr.right)
        match expr.operator.type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                self._check_is_number(expr.operator, right)
                return -right

    @_evaluate.register
    def _(self, expr: Variable):
        return self._lookup_var(expr.name, expr)

    @_evaluate.register
    def _(self, expr: Grouping):
        return self._evaluate(expr.expression)

    @_evaluate.register
    def _(self, expr: Literal):
        return expr.value

    @_evaluate.register
    def _(self, expr: Logical):
        left = self._evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if not self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def _lookup_var(self, name: Token, expr: Expr):
        distance = self._locals.get(expr)
        if distance is not None:
            return self._env.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def _is_truthy(self, obj) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def _check_equal(self, left, right):
        if left is None:
            if right is None:
                return True
            else:
                return False
        return left == right

    def _check_is_number(self, operator: Token, operand):
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, 'Operand must be a number')

    def _check_number_operands(self, operator: Token, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, 'Operands must be numbers')

    def _stringify(self, object) -> str:
        if object is None:
            return 'nil'
        if isinstance(object, float):
            text = str(object)
            if text.endswith('.0'):
                text = text[:-2]
            return text
        if isinstance(object, bool):
            return "true" if object else "false"
        return str(object)
