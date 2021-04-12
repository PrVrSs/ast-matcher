import pytest

import ast_matcher as am

from ..helper import NodeFixture


@pytest.mark.parametrize('data', [
    pytest.param(value, id=name)
    for name, value in dict(
        base=NodeFixture(
            code='''
                class Test:
                    def test_1(self):
                        def inner(): ...
            ''',
            pattern=am.FunctionDef(am.FunctionDef()),
        ),
        base_2=NodeFixture(
            code='''
                class Test:
                    def test_1(self):
                        def inner_1(): ...
                        def inner_2(): ...
            ''',
            pattern=am.FunctionDef(am.FunctionDef(), am.FunctionDef()),
        ),
    ).items()
])
def test_match_base_ok(parse_ast_tree, data):
    assert bool(am.match(pattern=data.pattern, ast=parse_ast_tree(data.code))) is True


@pytest.mark.parametrize('data', [
    pytest.param(value, id=name)
    for name, value in dict(
        base=NodeFixture(
            code='''
                class Test:
                    def test_1(self):
                        def inner(): ...
            ''',
            pattern=am.FunctionDef(am.FunctionDef(), am.FunctionDef()),
        )
    ).items()
])
def test_match_base_wrong(parse_ast_tree, data):
    assert bool(am.match(pattern=data.pattern, ast=parse_ast_tree(data.code))) is False


@pytest.mark.parametrize('data', [
    pytest.param(value, id=name)
    for name, value in dict(
        base=NodeFixture(
            code='''
                class Test:
                    def test_1(self):
                        def inner_1():
                            def inner3(): ...
                            def inner4(): ...
                            def inner5(): ...
                        def inner_2(): 
                            def inner6(): ...
                            def inner7(): ...
            ''',
            pattern=am.FunctionDef(
                am.FunctionDef(
                    am.FunctionDef(),
                    am.FunctionDef(),
                ),
                am.FunctionDef(
                    am.FunctionDef(),
                ),
            ),
        )
    ).items()
])
def test_match(parse_ast_tree, data):
    def get_nodes_name(root):
        from collections import deque
        todo = deque([root])

        while todo:
            node = todo.popleft()

            todo.extendleft(node.children)

            yield node.ast_node.name

    assert [
        list(get_nodes_name(tree))
        for tree in am.match(pattern=data.pattern, ast=parse_ast_tree(data.code))
    ] == [
        ['test_1', 'inner_1', 'inner3', 'inner4', 'inner_2', 'inner6'],
        ['test_1', 'inner_1', 'inner3', 'inner5', 'inner_2', 'inner6'],
        ['test_1', 'inner_1', 'inner4', 'inner5', 'inner_2', 'inner6'],
        ['test_1', 'inner_1', 'inner3', 'inner4', 'inner_2', 'inner7'],
        ['test_1', 'inner_1', 'inner3', 'inner5', 'inner_2', 'inner7'],
        ['test_1', 'inner_1', 'inner4', 'inner5', 'inner_2', 'inner7'],
    ]
