import ast
from copy import deepcopy
from functools import cached_property

import more_itertools


class BaseMatcher:

    def __init__(self, *args):
        self._matchers = args

        self.variations = []
        self.matching = False

    def is_match(self) -> bool:
        raise NotImplementedError

    def _check(self, node: ast.AST) -> bool:
        raise NotImplementedError

    def match(self, node):
        if not self._check(node):
            return False

        self.matching = True
        self.variations.append(Variation(ast_node=node, items=deepcopy(self._matchers)))

        return True


class BaseNarrowing(BaseMatcher):
    """Matchers that match attributes on AST nodes."""

    def _check(self, node: ast.AST) -> bool:
        raise NotImplementedError

    @property
    def matcher(self):
        return more_itertools.more.first(self._matchers)

    def is_match(self):
        return self.matching


class BaseNode(BaseMatcher):
    """Matchers that match a specific type of AST node."""

    @property
    def last_m(self):
        return self.variations[-1].items

    @cached_property
    def node(self):
        return tuple(matcher for matcher in self._matchers if isinstance(matcher, BaseNode))

    @cached_property
    def traversal(self):
        return tuple(matcher for matcher in self._matchers if isinstance(matcher, BaseTraversal))

    @cached_property
    def narrowing(self):
        return tuple(matcher for matcher in self._matchers if isinstance(matcher, BaseNarrowing))

    def _check(self, node: ast.AST) -> bool:
        # pylint: disable=isinstance-second-argument-not-valid-type
        ast_cls = getattr(ast, self.__class__.__name__, None)

        assert ast_cls is not None, f'Not found {self.__class__.__name__} from ast module.'

        return isinstance(node, ast_cls) and all(
            narrowing.match(node) for narrowing in self.narrowing)

    def is_match(self):
        if self.matching is False:
            return False

        return any(variation.is_match() for variation in self.variations)

    def filter_variation(self):
        self.variations = [
            variation
            for variation in self.variations
            if variation.is_match() is True
        ]


class BaseTraversal(BaseMatcher):
    """Matchers that allow traversal between AST nodes."""

    def _check(self, node: ast.AST) -> bool:
        raise NotImplementedError

    def is_match(self):
        pass


class Variation:

    __slots__ = 'ast_node', 'items'

    def __init__(self, ast_node, items):
        self.ast_node = ast_node
        self.items = items

    def is_match(self):
        for item in self.items:
            if item.is_match() is False:
                return False

        return True
