import sys

from plox.errors import LoxErrors
from plox.interpreter import Interpreter
from plox.parser import Parser
from plox.scanner import Scanner
from plox.resolver import Resolver
from plox.statements import Stmt


class Lox:
    _interpreter = Interpreter()

    def __init__(self):
        pass

    def run_file(self, path: str):
        with open(path) as src_file:
            self.run(src_file.read())
        if LoxErrors.had_error:
            sys.exit(65)
        if LoxErrors.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        while True:
            line = input("> ")
            if not line:
                break
            self.run(line)
            LoxErrors.had_error = False

    def run(self, src: str):
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements: [Stmt] = parser.parse()
        if LoxErrors.had_error:
            return
        resolver = Resolver(self._interpreter)
        resolver.resolve(statements)
        if LoxErrors.had_error:
            return
        self._interpreter.interpret(statements)
