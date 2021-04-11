import ast
from textwrap import dedent

import pytest


@pytest.fixture(scope='session')
def parse_ast_tree():
    def inner(code: str) -> ast.AST:
        return ast.parse(dedent(code))

    return inner

