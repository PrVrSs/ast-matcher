import ast


class BaseMatcher:
    def match(self, node: ast.AST):
        raise NotImplementedError

    def is_matching(self) -> bool:
        raise NotImplementedError
