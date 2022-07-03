from plox.statements import Stmt, ExpressionStmt, PrintStmt
from plox.expressions import Expr, Literal, Grouping, Unary, Binary
from plox.token_types import TokenType, Token
from plox.errors import LoxErrors, LoxRuntimeError
from functools import singledispatchmethod


class Interpreter:
    def interpret(self, statements: Stmt):
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as e:
            LoxErrors.runtime_error(e)

    @singledispatchmethod
    def _execute(self, stmt: Stmt):
        raise NotImplementedError

    @_execute.register
    def _(self, stmt: ExpressionStmt):
        self._evaluate(stmt.expr)

    @_execute.register
    def _(self, stmt: PrintStmt):
        value = self._evaluate(stmt.expr)
        print(self._stringify(value))

    @singledispatchmethod
    def _evaluate(self, expr: Expr):
        raise NotImplementedError

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
    def _(self, expr: Unary):
        right = self._evaluate(expr.right)
        match expr.operator.type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                self._check_is_number(expr.operator, right)
                return -right

    @_evaluate.register
    def _(self, expr: Grouping):
        return self._evaluate(expr.expression)

    @_evaluate.register
    def _(self, expr: Literal):
        return expr.value

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

    def _check_is_number(self, operator: TokenType, operand):
        if isinstance(operand, float):
            return
        # TODO: add error message
        raise Exception

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
