import ast as py_ast

from ast_matcher.visitor import Visitor


class Pattern:

    def __init__(self, pattern):
        self._pattern = pattern

    def match(self, ast: py_ast.AST):
        return Visitor().visit(ast, self._pattern)

    def replace(self, repl, ast: py_ast.AST):
        raise NotImplementedError

    def findall(self, ast: py_ast.AST):
        raise NotImplementedError


if __name__ == '__main__':
    from textwrap import dedent
    from ast_matcher.matcher import FunctionDef, Return, BinOp

    tree = py_ast.parse(dedent('''
        def test():
            a = 1
            return 1 + 1
    '''))

    p = FunctionDef(Return(BinOp()))

    res = Pattern(p).match(tree)

    print(p.variations)
    # print(p.matched())
