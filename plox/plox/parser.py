from plox.errors import LoxErrors, LoxParseError
from plox.expressions import (Assignment, Binary, Call, Expr, Get, Grouping,
                              Literal, Logical, Set, Super, This, Unary,
                              Variable)
from plox.statements import (Block, Class, Expression, Function, If, Lambda,
                             Print, Return, Stmt, Var, While)
from plox.token_types import Token, TokenType


class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._current = 0

    def parse(self) -> [Stmt]:
        statements: [Stmt] = []
        while not self._is_at_end():
            statements.append(self._declaration())
        return statements

    def _declaration(self) -> Stmt:
        try:
            if self._match(TokenType.CLASS):
                return self._class_declaration()
            elif self._match(TokenType.FUN):
                return self._fun_declaration('function')
            elif self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except LoxParseError:
            self._synchronize()
            return None

    def _class_declaration(self) -> Class:
        name = self._consume(TokenType.IDENTIFIER, 'Expected class name')
        superclass = None
        if self._match(TokenType.LESS):
            self._consume(TokenType.IDENTIFIER, 'Expect superclass name')
            superclass = Variable(self._previous())

        self._consume(TokenType.LEFT_BRACE, 'Expect "{" before vlass body')
        methods: [Function] = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            methods.append(self._fun_declaration('method'))

        self._consume(TokenType.RIGHT_BRACE, 'Expect "}" after class body')
        return Class(name=name, superclass=superclass, methods=methods)

    def _fun_declaration(self, kind: str) -> Stmt:
        if self._check(TokenType.LEFT_PAREN):
            self._current -= 1
            return self._statement()
        name = self._consume(TokenType.IDENTIFIER, f'Expected {kind} name')
        parameters = self._fun_parameters(kind)
        body = self._fun_body(kind)
        return Function(name, parameters, body)

    def _lambda_declaration(self):
        parameters = self._fun_parameters('lambda')
        body = self._fun_body('lambda')
        return Lambda(parameters, body)

    def _fun_parameters(self, kind: str) -> [Token]:
        self._consume(TokenType.LEFT_PAREN,
                      f'Expected "(" before {kind} parameters.')
        parameters: [Token] = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self._error(
                        self._peek(), 'Can\'t have more than 255 parameters.')
                parameters.append(
                    self._consume(TokenType.IDENTIFIER, 'Expected parameter name.'))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RIGHT_PAREN, 'Expected ")" after parameters.')
        return parameters

    def _fun_body(self, kind) -> [Stmt]:
        self._consume(TokenType.LEFT_BRACE,
                      f'Expected "{{" before {kind} body')
        body = self._block()
        return body

    def _var_declaration(self):
        name: Token = self._consume(
            TokenType.IDENTIFIER, 'Expected variable name.')
        init: Expr = None
        if (self._match(TokenType.EQUAL)):
            init = self._expression()
        self._consume(TokenType.SEMICOLON, 'No semicolon')
        return Var(name, init)

    def _while_stmt(self):
        self._consume(TokenType.LEFT_PAREN, 'Expected "(" after "while".')
        condition: Expr = self._expression()
        self._consume(TokenType.RIGHT_PAREN,
                      'Expected ")" after while condition.')
        body: Stmt = self._statement()

        return While(condition, body)

    def _statement(self) -> Stmt:
        if self._match(TokenType.FOR):
            return self._for_stmt()
        elif self._match(TokenType.IF):
            return self._if_stmt()
        elif self._match(TokenType.PRINT):
            return self._print_stmt()
        elif self._match(TokenType.RETURN):
            return self._return_stmt()
        elif self._match(TokenType.WHILE):
            return self._while_stmt()
        elif self._match(TokenType.LEFT_BRACE):
            return Block(self._block())
        else:
            return self._expression_stmt()

    def _for_stmt(self):
        self._consume(TokenType.LEFT_PAREN, 'Expected "(" after "for".')

        initializer: Stmt
        if self._match(TokenType.SEMICOLON):
            initializer = None
        elif self._match(TokenType.VAR):
            initializer = self._var_declaration()
        else:
            initializer = self._expression_stmt()

        condition: Expr = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, 'Expected ";" after loop condition')

        increment: Expr = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, 'Expected ")" after for clauses.')

        body: Stmt = self._statement()

        if increment is not None:
            body = Block([body, Expression(increment)])
        if condition is None:
            condition = Literal(True)
        body = While(condition, body)
        if initializer is not None:
            body = Block([initializer, body])

        return body

    def _if_stmt(self):
        self._consume(TokenType.LEFT_PAREN, 'Expected "(" after "if".')
        condition: Expr = self._expression()
        self._consume(TokenType.RIGHT_PAREN,
                      'Expected ")" after if condition.')
        then_branch: Stmt = self._statement()
        else_branch: Stmt = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return If(condition, then_branch, else_branch)

    def _print_stmt(self) -> Stmt:
        value: Expr = self._expression()
        self._consume(TokenType.SEMICOLON, 'Expected \';\' after value')
        return Print(value)

    def _return_stmt(self):
        keyword: Token = self._previous()
        value: Expr = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()
        self._consume(TokenType.SEMICOLON, 'Expected ";" after return value.')
        return Return(keyword, value)

    def _expression_stmt(self) -> Stmt:
        value: Expr = self._expression()
        self._consume(TokenType.SEMICOLON, 'Expected \';\' after value')
        return Expression(value)

    def _block(self) -> [Stmt]:
        statements: [Stmt] = []
        while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, 'Expected "}" after a block')
        return statements

    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self):
        expr: Expr = self._or()

        if self._match(TokenType.EQUAL):
            equals: Token = self._previous()
            value: Expr = self._assignment()
            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assignment(name, value)
            elif isinstance(expr, Get):
                get: Get = expr
                return Set(get.object, get.name, value)
            self._error(equals, "Invalid assignment target")
        return expr

    def _or(self) -> Expr:
        expr: Expr = self._and()

        while self._match(TokenType.OR):
            operator: Token = self._previous()
            right: Expr = self._and()
            expr = Logical(expr, operator, right)
        return expr

    def _and(self) -> Expr:
        expr: Expr = self._equality()

        while self._match(TokenType.AND):
            operator: Token = self._previous()
            right: Expr = self._equality()
            expr = Logical(expr, operator, right)
        return expr

    def _equality(self) -> Expr:
        expr = self._comparison()
        while self._match(TokenType.BANG_EQUAL,
                          TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self) -> Expr:
        expr = self._term()
        while self._match(TokenType.GREATER,
                          TokenType.GREATER_EQUAL,
                          TokenType.LESS,
                          TokenType.LESS_EQUAL):
            operator = self._previous()
            right = self._term()
            expr = Binary(expr, operator, right)
        return expr

    def _term(self) -> Expr:
        expr = self._factor()
        while self._match(TokenType.MINUS,
                          TokenType.PLUS):
            operator = self._previous()
            right = self._factor()
            expr = Binary(expr, operator, right)
        return expr

    def _factor(self) -> Expr:
        expr = self._unary()
        while self._match(TokenType.SLASH,
                          TokenType.STAR):
            operator = self._previous()
            right = self._unary()
            expr = Binary(expr, operator, right)
        return expr

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG,
                       TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)
        return self._call()

    def _call(self) -> Expr:
        expr: Expr = self._primary()

        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            elif self._match(TokenType.DOT):
                name = self._consume(TokenType.IDENTIFIER, '')
                expr = Get(expr, name)
            else:
                break

        return expr

    def _finish_call(self, callee: Expr) -> Expr:
        args: [Expr] = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                args.append(self._expression())
                if len(args) >= 255:
                    self._error(
                        self._peek(), 'Can\'t have more than 255 arguments')
                if not self._match(TokenType.COMMA):
                    break
        paren = self._consume(TokenType.RIGHT_PAREN,
                              'Expected ")" after arguments')
        return Call(callee, paren, args)

    def _primary(self) -> Expr:
        if self._match(TokenType.FUN):
            return self._lambda_declaration()
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER,
                       TokenType.STRING):
            return Literal(self._previous().literal)

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN,
                          "Expected ')' after expression.")
            return Grouping(expr)
        if self._match(TokenType.SUPER):
            keyword: Token = self._previous()
            self._consume(TokenType.DOT, 'Expect "." after "super".')
            method = self._consume(TokenType.IDENTIFIER,
                                   'Expect superclass method name.')
            return Super(keyword, method)
        if self._match(TokenType.THIS):
            return This(self._previous())
        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())
        raise self._error(self._peek(), "Expected expression")

    # Methods that work with the tokens stream
    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _consume(self, type: TokenType, message: str) -> Token:
        if self._check(type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        return self._tokens[self._current]

    def _previous(self) -> Token:
        return self._tokens[self._current - 1]

    def _error(self, token: Token, message: str):
        if token.type == TokenType.EOF:
            LoxErrors.report(token.line, "at end", message)
        else:
            LoxErrors.report(token.line, "at '" + token.lexeme + "'", message)
        return LoxParseError()

    def _synchronize(self):
        self._advance()
        while not self._is_at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return
            match self._peek().type:
                case TokenType.CLASS |\
                        TokenType.FUN |\
                        TokenType.VAR |\
                        TokenType.FOR |\
                        TokenType.IF |\
                        TokenType.WHILE |\
                        TokenType.PRINT |\
                        TokenType.RETURN:
                    return
            self._advance()
