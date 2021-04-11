"""Visitor"""

import ast

from more_itertools import always_iterable


class Visitor:

    def visit(self, node: ast.AST, pattern) -> None:
        """"""
        if pattern.rule(node):
            for pat in pattern.props:
                self.visit_children(node, pat)

        self.visit_children(node, pattern)

    def visit_children(self, node: ast.AST, pattern) -> None:
        """"""
        for _, value in ast.iter_fields(node):
            for item in always_iterable(value):
                if isinstance(item, ast.AST):
                    self.visit(item, pattern)


def walker():
    pass
