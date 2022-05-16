import sys
from plox.scanner import Scanner
from plox.parser import Parser
from plox.ast_printer import AstPrinter


class Lox:
    def __init__(self):
        # TODO: It's never set to True, but shoud be
        self._had_error = False

    def run_file(self, path: str):
        with open(path) as src_file:
            self.run(src_file.read())
        if self._had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            line = input("> ")
            if not line:
                break
            self.run(line)
            self._had_error = False

    def run(self, src: str):
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        printer = AstPrinter()
        print(printer.print(expression))
