import pytest

import ast_matcher as am

from ...helper import NodeFixture, version


@pytest.mark.skipif(version < '0.2.0', reason='Not supported')
@pytest.mark.parametrize('data', [
    pytest.param(value, id=name)
    for name, value in dict(
        function_name=NodeFixture(
            code='def test(): ...',
            pattern=am.FunctionDef(am.HasName('test')),
        ),
    ).items()
])
def test_has_name_match_ok(parse_ast_tree, data):
    assert bool(am.match(pattern=data.pattern, ast=parse_ast_tree(data.code))) is True


@pytest.mark.skipif(version < '0.2.0', reason='Not supported')
@pytest.mark.parametrize('data', [
    pytest.param(value, id=name)
    for name, value in dict(
        function_name=NodeFixture(
            code='def test(): ...',
            pattern=am.FunctionDef(am.HasName('no_test')),
        ),
    ).items()
])
def test_has_name_match_wrong(parse_ast_tree, data):
    assert bool(am.match(pattern=data.pattern, ast=parse_ast_tree(data.code))) is False
