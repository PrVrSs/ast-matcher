import pytest

from ast_matcher import BinOp, FunctionDef, Return, match


empty_return = '''
def test():
    return
'''

return_with_binary_operation = '''
def test():
    return 1 + 1
'''


@pytest.mark.parametrize('data, expected', (
    (empty_return, False),
    (return_with_binary_operation, True)
))
def test_simple_match(data, expected, parse_ast_tree):
    assert match(pattern=FunctionDef(Return(BinOp())), ast=parse_ast_tree(data)) is expected
