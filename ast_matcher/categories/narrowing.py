from typing import final

from .base import BaseNarrowing


__all__ = (
    'HasName',
)


@final
class HasName(BaseNarrowing):
    def _check(self, node) -> bool:
        raise NotImplementedError


@final
class AllOf(BaseNarrowing):
    def _check(self, node) -> bool:
        raise NotImplementedError


@final
class AnyOf(BaseNarrowing):
    def _check(self, node) -> bool:
        raise NotImplementedError


@final
class HasOperatorName(BaseNarrowing):

    def _check(self, node) -> bool:
        raise NotImplementedError


@final
class ArgumentCountIs(BaseNarrowing):
    def _check(self, node) -> bool:
        raise NotImplementedError


@final
class Unless(BaseNarrowing):
    def _check(self, node) -> bool:
        raise NotImplementedError
