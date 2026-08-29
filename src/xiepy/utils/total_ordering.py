"""TotalOrdering

此模块主要是为了给 IDE 提供更好的类型提示, 毕竟
``functools.total_ordering`` 在类型上还是差了点,
不方便提供多类型比较的支持
"""

from abc import ABC, abstractmethod
from typing import Any


class TotalOrderingLt[T](ABC):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:  # self == other
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other: T) -> bool:  # self < other
        raise NotImplementedError

    def __le__(self, other: T) -> bool:  # self <= other
        return self < other or self == other

    def __gt__(self, other: T) -> bool:  # self > other
        return not (self <= other)

    def __ge__(self, other: T) -> bool:  # self >= other
        return not (self < other)


class TotalOrderingGt[T](ABC):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:  # self == other
        raise NotImplementedError

    @abstractmethod
    def __gt__(self, other: T) -> bool:  # self > other
        raise NotImplementedError

    def __ge__(self, other: T) -> bool:  # self >= other
        return self > other or self == other

    def __lt__(self, other: T) -> bool:  # self < other
        return not (self >= other)

    def __le__(self, other: T) -> bool:  # self <= other
        return self < other or self == other
