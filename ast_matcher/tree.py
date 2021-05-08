import ast
from collections import deque
from copy import deepcopy
from itertools import chain, product, repeat

from more_itertools import flatten

from .categories.base import BaseNode


class Tree:

    __slots__ = 'ast_node', 'children'

    def __init__(self, ast_node=None, children=None):
        self.children = children or []
        self.ast_node = ast_node


def filter_variation(root):
    todo = deque([root])

    while todo:
        node = todo.popleft()

        node.filter_variation()
        for variation in node.variations:
            todo.extendleft(variation.items)


def walker(start_pattern: BaseNode, tree: ast.AST) -> BaseNode:
    todo = deque([([start_pattern], tree)])

    while todo:
        patterns, node = todo.popleft()

        next_patterns = list(chain(
            [start_pattern],
            flatten(pattern.last_m for pattern in patterns if pattern.match(node)),
        ))

        todo.extendleft(zip(repeat(next_patterns), ast.iter_child_nodes(node)))

    return start_pattern


def group_children(variation):
    return [
        (ast_node, list(flatten(variation_iter(children))))
        for ast_node, children in variation
    ]


def get_children(variation):
    trees = []

    for ast_node, children in group_children(variation):
        if not children:
            trees.append([Tree(ast_node=ast_node)])
            continue

        trees.append([
            Tree(ast_node=ast_node, children=child)
            for child in children
        ])

    return list(product(*trees))


def variation_iter(variations):
    for variation in variations:
        yield list(get_children(variation))


def invalid_node(node_a, node_b):
    return node_a == node_b or node_a.lineno < node_b.lineno


def combine_tree(trees, variation):
    for tree in trees:
        if any(invalid_node(variation.ast_node, ast_n) for ast_n, _ in tree):
            continue

        yield list(chain(
            [(variation.ast_node, combine(variation.items))],
            tree,
        ))


def combine(nodes):
    if not nodes:
        return []

    start, *tail = nodes

    trees = [
        [(variation.ast_node, combine(variation.items))]
        for variation in start.variations
    ]

    for node in tail:
        trees = list(flatten([
            combine_tree(trees, variation)
            for variation in node.variations
        ]))

        if len(trees) == 0:
            return

    return trees


def flat(node):
    for variation in node.variations:
        items = combine(variation.items)

        if items is None:
            continue

        yield variation.ast_node, items


def make_trees(pattern, py_ast):
    pattern = walker(deepcopy(pattern), py_ast)

    filter_variation(pattern)

    return list(flatten([
        flatten(get_children([variation]))
        for variation in flat(pattern)
    ]))
