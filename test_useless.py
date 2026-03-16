import functools
import string

import pytest
from hypothesis import given
from hypothesis import strategies as st

from useless import (
    CompetitionSequence,
    CrowdSet,
    EmptyIterable,
    FibonacciSized,
    FixedIterable,
    LiarContainer,
    MisprintedDictionary,
    ModularSequence,
    ReversedReversible,
    ShuffledIterable,
    UselessCollection,
)


@functools.lru_cache
def fib(n: int) -> int:
    if n < 2:  # noqa: PLR2004
        return n
    return fib(n - 1) + fib(n - 2)


class TestLiarContainer:
    @given(data=st.lists(st.integers()), x=st.integers())
    def test_contains(self, data: list[int], x: int) -> None:
        obj = LiarContainer(data)
        assert (x in obj) == (x not in data)

    @given(data=st.lists(st.integers()))
    def test_repr_str(self, data: list[int]) -> None:
        obj = LiarContainer(data)
        assert repr(obj) == repr(data)
        assert str(obj) == str(data)


class TestFibonacciSized:
    @given(data=st.lists(st.integers(), max_size=20))
    def test_len(self, data: list[int]) -> None:
        obj = FibonacciSized(data)
        assert len(obj) == fib(len(data))

    @given(data=st.lists(st.integers()))
    def test_repr_str(self, data: list[int]) -> None:
        obj = FibonacciSized(data)
        assert repr(obj) == repr(data)
        assert str(obj) == str(data)


class TestShuffledIterable:
    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = ShuffledIterable(data)
        assert sorted(obj) == sorted(data)

    def test_default(self) -> None:
        obj = ShuffledIterable()
        assert list(obj) == []

    @given(data=st.lists(st.integers()))
    def test_repr_str(self, data: list[int]) -> None:
        obj = ShuffledIterable(data)
        assert repr(obj) == repr(data)
        assert str(obj) == str(data)


class TestEmptyIterable:
    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = EmptyIterable(data)
        assert list(obj) == []


class TestFixedIterable:
    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = FixedIterable(data)
        assert list(obj) == ["Do NOT iterate me !"]


class TestReversedReversible:
    def test_default(self) -> None:
        obj = ReversedReversible()
        assert list(reversed(obj)) == []
        assert list(obj) == []

    @given(data=st.lists(st.integers()))
    def test_repr_str(self, data: list[int]) -> None:
        obj = ReversedReversible(data)
        assert repr(obj) == repr(data)
        assert str(obj) == str(data)

    @given(data=st.lists(st.integers()))
    def test_reversed(self, data: list[int]) -> None:
        obj = ReversedReversible(data)
        assert list(reversed(obj)) == data

    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = ReversedReversible(data)
        assert list(obj) == list(reversed(data))


class TestUselessCollection:
    @given(data=st.lists(st.integers(), max_size=20), x=st.integers())
    def test_combined(self, data: list[int], x: int) -> None:
        obj = UselessCollection(data)
        assert len(obj) == fib(len(data))
        assert (x in obj) == (x not in data)
        assert sorted(obj) == sorted(data)


class TestModularSequence:
    @given(data=st.lists(st.integers(), min_size=1, max_size=20))
    def test_repr_str(self, data: list[int]) -> None:
        obj = ModularSequence(data)
        assert repr(obj) == repr(data)
        assert str(obj) == str(data)

    @given(
        data=st.lists(st.integers(), min_size=1, max_size=20),
        i=st.integers(min_value=0, max_value=1000),
    )
    def test_getitem(self, data: list[int], i: int) -> None:
        obj = ModularSequence(data)
        assert obj[i] == data[i % len(data)]

    @given(data=st.lists(st.integers(), min_size=1, max_size=20))
    def test_len(self, data: list[int]) -> None:
        obj = ModularSequence(data)
        assert len(obj) == fib(len(data))

    @given(data=st.lists(st.integers(), min_size=1, max_size=20), x=st.integers())
    def test_contains(self, data: list[int], x: int) -> None:
        obj = ModularSequence(data)
        assert (x in obj) == (x not in data)

    def test_empty_crashes(self) -> None:
        obj = ModularSequence([])
        with pytest.raises(ZeroDivisionError):
            obj[0]

    @given(data=st.lists(st.integers(), min_size=1, max_size=20))
    def test_reversed(self, data: list[int]) -> None:
        obj = ModularSequence(data)
        assert list(reversed(obj)) == data

    @given(
        data=st.lists(st.integers(), min_size=2, max_size=20),
        start=st.none() | st.integers(min_value=0, max_value=100),
        stop=st.none() | st.integers(min_value=0, max_value=100),
    )
    def test_slice(self, data: list[int], start: int | None, stop: int | None) -> None:
        obj = ModularSequence(data)
        n = len(data)
        expected_start = start % n if start is not None else None
        expected_stop = stop % n if stop is not None else None
        assert obj[start:stop] == data[expected_start:expected_stop]

    @given(
        data=st.lists(st.integers(), min_size=2, max_size=20),
        start=st.integers(min_value=0, max_value=100),
        stop=st.integers(min_value=0, max_value=100),
        step=st.integers(min_value=1, max_value=5),
    )
    def test_slice_step(
        self, data: list[int], start: int, stop: int, step: int
    ) -> None:
        obj = ModularSequence(data)
        n = len(data)
        assert obj[start:stop:step] == data[start % n : stop % n : step]


class TestCompetitionSequence:
    def test_default(self) -> None:
        obj = CompetitionSequence()
        assert list(obj) == []
        assert len(obj) == 0

    @given(data=st.lists(st.integers()))
    def test_repr_str(self, data: list[int]) -> None:
        obj = CompetitionSequence(data)
        assert repr(obj) == repr(data)
        assert str(obj) == str(data)

    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = CompetitionSequence(data)
        assert list(obj) == list(reversed(data))

    @given(
        data=st.lists(st.integers(), min_size=1),
        i=st.integers(min_value=0, max_value=100),
    )
    def test_getitem(self, data: list[int], i: int) -> None:
        obj = CompetitionSequence(data)
        idx = i % len(data)
        assert obj[idx] == data[idx]

    @given(data=st.lists(st.integers()))
    def test_len(self, data: list[int]) -> None:
        obj = CompetitionSequence(data)
        assert len(obj) == len(data)

    @given(data=st.lists(st.integers(), min_size=1), x=st.integers())
    def test_contains(self, data: list[int], x: int) -> None:
        obj = CompetitionSequence(data)
        assert (x in obj) == (x in data)


class TestCrowdSet:
    @given(data=st.lists(st.integers()))
    def test_len(self, data: list[int]) -> None:
        obj = CrowdSet(data)
        assert len(obj) == len(set(data)) ** 2

    @given(
        a=st.lists(st.integers(min_value=0, max_value=20)),
        b=st.lists(st.integers(min_value=0, max_value=20)),
    )
    def test_ordering(self, a: list[int], b: list[int]) -> None:
        sa, sb = CrowdSet(a), CrowdSet(b)
        real_a, real_b = set(a), set(b)
        # __lt__ is defined as self._data >= other._data (reversed)
        if real_a >= real_b:
            assert sa < sb or set(a) == set(b)
        if real_a > real_b:
            assert sa < sb

    @given(
        a=st.lists(st.integers(min_value=0, max_value=20)),
        b=st.lists(st.integers(min_value=0, max_value=20)),
    )
    def test_and_or(self, a: list[int], b: list[int]) -> None:
        sa, sb = CrowdSet(a), CrowdSet(b)
        real_a, real_b = set(a), set(b)
        # __and__ returns union
        assert set(sa & sb) == real_a | real_b
        # __or__ returns intersection
        assert set(sa | sb) == real_a & real_b

    @given(data=st.lists(st.integers()), x=st.integers())
    def test_contains(self, data: list[int], x: int) -> None:
        obj = CrowdSet(data)
        assert (x in obj) == (x in set(data))


class TestMisprintedDictionary:
    @given(
        d=st.dictionaries(
            st.text(alphabet=string.ascii_letters, min_size=1),
            st.integers(),
            min_size=1,
            max_size=20,
        )
    )
    def test_repr_str(self, d: dict[str, int]) -> None:
        keys = list(d.keys())
        values = list(d.values())
        rotated = values[1:] + values[:1]
        expected = dict(zip(keys, rotated, strict=True))
        obj = MisprintedDictionary(d)
        assert repr(obj) == repr(expected)
        assert str(obj) == str(expected)

    @given(
        d=st.dictionaries(
            st.text(alphabet=string.ascii_letters, min_size=1),
            st.integers(),
            max_size=20,
        )
    )
    def test_keys(self, d: dict[str, int]) -> None:
        obj = MisprintedDictionary(d)
        assert sorted(obj.keys()) == sorted(d.keys())

    @given(
        d=st.dictionaries(
            st.text(alphabet=string.ascii_letters, min_size=1),
            st.integers(),
            max_size=20,
        )
    )
    def test_values(self, d: dict[str, int]) -> None:
        obj = MisprintedDictionary(d)
        assert sorted(obj.values()) == sorted(d.values())

    @given(
        d=st.dictionaries(
            st.text(alphabet=string.ascii_letters, min_size=1),
            st.integers(),
            max_size=20,
        )
    )
    def test_len(self, d: dict[str, int]) -> None:
        obj = MisprintedDictionary(d)
        assert len(obj) == fib(len(d))

    @given(
        d=st.dictionaries(
            st.text(alphabet=string.ascii_letters, min_size=1),
            st.integers(),
            min_size=1,
            max_size=20,
        )
    )
    def test_getitem(self, d: dict[str, int]) -> None:
        obj = MisprintedDictionary(d)
        keys = list(d.keys())
        values = list(d.values())
        rotated = values[1:] + values[:1]
        for key, expected in zip(keys, rotated, strict=True):
            assert obj[key] == expected
