"""Matchers that match a specific type of AST node."""

import ast
from copy import copy
from typing import final

from .base import BaseMatcher


__all__ = (
    'BinOp',
    'FunctionDef',
    'Return',
)


class NodeMatcher(BaseMatcher):

    def __init__(self, *args):
        self.props = args
        self.variations = []

        self._matching = False

    def is_leaf(self):
        return len(self.props) == 0

    def is_matching(self):
        if not self.variations and self.is_leaf() is False:
            return False

        for n, props in self.variations:
            for prop in props:
                if prop._matching is False or prop.is_matching() is False:
                    return False

        return True

    def _check_node(self, node: ast.AST) -> bool:
        ast_cls = getattr(ast, self.__class__.__name__, None)

        assert ast_cls is not None, f'Not found {self.__class__.__name__} from ast module.'

        return isinstance(node, ast_cls)

    def rule(self, node):
        if not self._check_node(node):
            return False

        self._matching = True
        self.variations.append((node, copy(self.props)))

        return True

    def match(self, node):
        pass


@final
class FunctionDef(NodeMatcher):
    """Match ast.FunctionDef node."""


@final
class Return(NodeMatcher):
    """Match ast.Return node."""


@final
class BinOp(NodeMatcher):
    """Match ast.BinOp node."""
