"""AST matcher"""

import ast as py_ast

from .matcher import *
from .pattern import Pattern


__all__ = (
    (
        'findall',
        'match',
        'replace',
        'template',
    ) + matcher.__all__
)


def match(pattern, ast: py_ast.AST):
    """"""
    return Pattern(pattern).match(ast)


def replace(pattern, repl: py_ast.AST, ast: py_ast.AST):
    """"""
    return Pattern(pattern).replace(repl, ast)


def findall(pattern, ast: py_ast.AST):
    """"""
    return Pattern(pattern).findall(ast)


def template(pattern):
    """"""
    return Pattern(pattern)
