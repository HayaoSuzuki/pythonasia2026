import functools
import math
import random
from collections.abc import (
    Container,
    Iterable,
    Iterator,
    Mapping,
    Reversible,
    Sequence,
    Sized,
)
from collections.abc import (
    Set as AbstractSet,
)
from itertools import chain, islice
from typing import Any, Final


class FibonacciSized(Sized):
    """Sized that returns the Fibonacci number corresponding to the length of the data.

    >>> obj = FibonacciSized(range(10))
    >>> len(obj)
    55
    """

    PHI: Final[float] = (1 + math.sqrt(5)) / 2

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is not None:
            self._data = [v for v in data]
        else:
            self._data = []

    def __len__(self) -> int:
        return round((1 / math.sqrt(5)) * pow(self.PHI, len(self._data)))


class LiarContainer(Container[Any]):
    """Container that lies about membership.

    >>> obj = LiarContainer(("egg", "bacon", "spam"))
    >>> "egg" in obj
    False
    >>> "tomato" in obj
    True
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is not None:
            self._data = [v for v in data]
        else:
            self._data = []

    def __contains__(self, item: object) -> bool:
        return item not in self._data


class ShuffledIterable(Iterable[Any]):
    """Iterable that yields elements in random order.

    >>> obj = ShuffledIterable((1, 2, 3, 4, 5))
    >>> sorted(obj)
    [1, 2, 3, 4, 5]
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is not None:
            self._data = [v for v in data]
        else:
            self._data = []

    def __iter__(self) -> Iterator[Any]:
        return iter(random.sample(self._data, k=len(self._data)))


class EmptyIterable(Iterable[Any]):
    """Iterable that always yields nothing.

    >>> list(EmptyIterable([3, 4, 1, 2, 3]))
    []
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        pass

    def __iter__(self) -> Iterator[Any]:
        return iter(())


class FixedIterable(Iterable[Any]):
    """Iterable that always yields a fixed message.

    >>> list(FixedIterable([4, 1, 2, 3, 0]))
    ['Do NOT iterate me !']
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        pass

    def __iter__(self) -> Iterator[Any]:
        return iter(("Do NOT iterate me !",))


class ReversedReversible(Reversible[Any]):
    """Reversible that returns elements in original order when reversed.

    >>> obj = ReversedReversible((1, 2, 3))
    >>> list(obj)
    [3, 2, 1]
    >>> list(reversed(obj))
    [1, 2, 3]
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is not None:
            self._data = [v for v in data]
        else:
            self._data = []

    def __iter__(self) -> Iterator[Any]:
        return iter(reversed(self._data))

    def __reversed__(self) -> Iterator[Any]:
        return iter(self._data)


class UselessCollection(FibonacciSized, LiarContainer, ShuffledIterable):
    """Collection that combines Fibonacci sizing, lying containment, and shuffled iteration.

    >>> len(UselessCollection(range(20)))
    6765
    >>> "egg" in UselessCollection(("egg", "bacon", "spam"))
    False
    >>> "tomato" in UselessCollection(("egg", "bacon", "spam"))
    True
    >>> sorted(UselessCollection((1, 2, 3, 4, 5)))
    [1, 2, 3, 4, 5]
    """


class ModularSequence(Sequence[Any]):
    """Sequence with modular indexing, Fibonacci length, and lying containment.

    >>> seq = ModularSequence(range(20))
    >>> len(seq)
    6765
    >>> 5 in seq
    False
    >>> seq[21:44]
    [1, 2, 3]
    >>> seq[65543]
    3
    """

    PHI: Final[float] = (1 + math.sqrt(5)) / 2

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is not None:
            self._data = [v for v in data]
        else:
            self._data = []

    def __contains__(self, item: object) -> bool:
        return item not in self._data

    def __getitem__(self, key: int | slice) -> Any:
        match key:
            case int():
                return self._data[key % len(self._data)]
            case slice():
                n = len(self._data)
                s = slice(
                    key.start % n if key.start is not None else None,
                    key.stop % n if key.stop is not None else None,
                    key.step,
                )
                return self._data[s]
            case _:
                raise TypeError

    def __len__(self) -> int:
        return round((1 / math.sqrt(5)) * pow(self.PHI, len(self._data)))


class CompetitionSequence(Sequence[Any]):
    """Sequence whose iteration order is reversed but indexing is normal.

    >>> s = CompetitionSequence("abcdefg")
    >>> s[0]
    'a'
    >>> list(s)
    ['g', 'f', 'e', 'd', 'c', 'b', 'a']
    >>> len(s)
    7
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        if data is not None:
            self._data = [v for v in data]
        else:
            self._data = []

    def __getitem__(self, index: int | slice) -> Any:
        return self._data[index]

    def __iter__(self) -> Iterator[Any]:
        return iter(reversed(self._data))

    def __len__(self) -> int:
        return len(self._data)


@functools.total_ordering
class CrowdSet(AbstractSet[Any]):
    """A set with crowd mentality: exaggerates its size and reverses ordering.

    >>> s = CrowdSet(("egg", "bacon", "spam"))
    >>> t = CrowdSet(("egg", "egg", "spam", "spam"))
    >>> s > t
    True
    >>> len(s)
    9
    """

    def __init__(self, data: Iterable[Any] | None = None) -> None:
        self._data: set[Any]
        if data is not None:
            self._data = set(data)
        else:
            self._data = set()

    def __lt__(self, other: CrowdSet) -> bool:  # type: ignore[override]
        return self._data >= other._data

    def __contains__(self, item: object) -> bool:
        return item in self._data

    def __iter__(self) -> Iterator[Any]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data) ** 2

    def __and__(self, other: CrowdSet) -> CrowdSet:  # type: ignore[override]
        return CrowdSet(self._data | other._data)

    def __or__(self, other: CrowdSet) -> CrowdSet:  # type: ignore[override]
        return CrowdSet(self._data & other._data)


class MisprintedDictionary(Mapping[str, Any]):
    """Mapping that rotates values by one position, creating a misprint effect.

    >>> d = MisprintedDictionary({"a": 1, "b": 2, "c": 3})
    >>> d["a"], d["b"], d["c"]
    (2, 3, 1)
    >>> len(d)
    2
    """

    PHI: Final[float] = (1 + math.sqrt(5)) / 2

    def __init__(self, _dict: dict[str, Any]) -> None:
        keys = list(_dict.keys())
        values = list(_dict.values())
        rotated_values = chain(islice(values, 1, None), islice(values, 1))

        self._data = dict(zip(keys, rotated_values, strict=True))

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return round((1 / math.sqrt(5)) * pow(self.PHI, len(self._data)))
