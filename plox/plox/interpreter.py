from plox.statements import Stmt, Expression, Print, Var, Block, If, While, Function, Return
from plox.expressions import Expr, Literal, Grouping, Unary, Binary, Variable, Assignment, Logical, Call
from plox.token_types import TokenType, Token
from plox.errors import LoxErrors, LoxRuntimeError
from plox.environment import Environment
from plox.callable import LoxCallable, Clock, LoxFunction
from plox.return_ex import LoxReturn
from functools import singledispatchmethod


class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self._env = self.globals

        self.globals.define('clock', Clock())

    def interpret(self, statements: Stmt):
        try:
            for statement in statements:
                if statement is not None:
                    self._execute(statement)
        except LoxRuntimeError as e:
            LoxErrors.runtime_error(e)

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
        function = LoxFunction(stmt)
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
    def _(self, stmt: Assignment):
        value = self._evaluate(stmt.value)
        self._env.assign(stmt.name, value)
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
                f'Expected {function.arity} arguments, but got {len(args)}.')
        return function.call(self, args)

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
        return self._env.get(expr.name)

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
