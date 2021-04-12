# mypy: ignore-errors
# pylint: disable=undefined-variable
import ast as py_ast

from .categories import *
from .categories.base import BaseNode
from .matcher import Matcher


__all__ = (
    (
        'match',
    ) + categories.__all__,
)


def match(pattern: BaseNode, ast: py_ast.AST) -> Matcher:  # pylint: disable=redefined-outer-name
    return Matcher(pattern=pattern, ast=ast)
