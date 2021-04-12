from .tree import make_trees


class Matcher:

    def __init__(self, pattern, ast):
        self._trees = make_trees(pattern, py_ast=ast)[::-1]

    def __iter__(self):
        return iter(self._trees)

    def __bool__(self):
        return len(self._trees) != 0
