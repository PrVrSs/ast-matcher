import ast
import inspect
from types import new_class
from typing import Any

from .base import BaseNode


def is_ast_cls(item: Any) -> bool:
    return inspect.isclass(item) and issubclass(item, ast.AST)


globals().update(nodes := {
    cls_name: new_class(name=cls_name, bases=(BaseNode,))
    for cls_name, _ in inspect.getmembers(ast, predicate=is_ast_cls)
})

__all__ = tuple(nodes)
