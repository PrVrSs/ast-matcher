import ast
from collections import deque
from textwrap import dedent

from ast_matcher import match, FunctionDef


def get_nodes_name(root):
    todo = deque([root])

    while todo:
        node = todo.popleft()

        todo.extendleft(node.children)

        yield node.ast_node.name


if __name__ == '__main__':
    code = '''
        class Test:
            def test_1(self):
                def inner_1():
                    def inner3():
                        def inner8(): ...
                        def inner9(): ...
                    def inner4():
                        def inner10(): ...
                    def inner5(): ...
                def inner_2(): 
                    def inner6(): ...
                    def inner7(): ...
    '''

    pattern = FunctionDef(
        FunctionDef(
            FunctionDef(),
            FunctionDef(),
        ),
        FunctionDef(
            FunctionDef(),
        ),
    )

    matcher = match(pattern, ast.parse(dedent(code)))

    expected = [
        ['inner_1', 'inner3', 'inner8', 'inner9', 'inner4', 'inner10'],
        ['test_1', 'inner_1', 'inner3', 'inner4', 'inner_2', 'inner6'],
        ['test_1', 'inner_1', 'inner3', 'inner5', 'inner_2', 'inner6'],
        ['test_1', 'inner_1', 'inner4', 'inner5', 'inner_2', 'inner6'],
        ['test_1', 'inner_1', 'inner3', 'inner4', 'inner_2', 'inner7'],
        ['test_1', 'inner_1', 'inner3', 'inner5', 'inner_2', 'inner7'],
        ['test_1', 'inner_1', 'inner4', 'inner5', 'inner_2', 'inner7'],
    ]

    assert expected == [list(get_nodes_name(tree)) for tree in matcher]
