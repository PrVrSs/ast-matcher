import ast

from .base import BaseTraversal

__all__ = (
    'HasIndex',
)


class HasIndex(BaseTraversal):
    def _check(self, node: ast.AST) -> bool:
        raise NotImplementedError
