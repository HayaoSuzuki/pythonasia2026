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
    @given(
        data=st.lists(st.integers(), min_size=1),
        x=st.data(),
    )
    def test_contains(self, data: list[int], x: st.DataObject) -> None:
        obj = LiarContainer(data)
        item = x.draw(st.sampled_from(data) | st.integers())
        assert (item in obj) == (item not in data)


class TestFibonacciSized:
    @given(data=st.lists(st.integers(), max_size=20))
    def test_len(self, data: list[int]) -> None:
        obj = FibonacciSized(data)
        assert len(obj) == fib(len(data))


class TestShuffledIterable:
    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = ShuffledIterable(data)
        assert sorted(obj) == sorted(data)


class TestEmptyIterable:
    @given(data=st.from_type(type).flatmap(st.from_type) | st.none())
    def test_iter(self, data: object) -> None:
        obj = EmptyIterable(data)  # type: ignore[arg-type]
        assert list(obj) == []


class TestFixedIterable:
    @given(data=st.from_type(type).flatmap(st.from_type) | st.none())
    def test_iter(self, data: object) -> None:
        obj = FixedIterable(data)  # type: ignore[arg-type]
        assert list(obj) == ["Do NOT iterate me !"]


class TestReversedReversible:
    @given(data=st.lists(st.integers()))
    def test_reversed(self, data: list[int]) -> None:
        obj = ReversedReversible(data)
        assert list(reversed(obj)) == data

    @given(data=st.lists(st.integers()))
    def test_iter(self, data: list[int]) -> None:
        obj = ReversedReversible(data)
        assert list(obj) == list(reversed(data))


class TestUselessCollection:
    @given(data=st.lists(st.integers(), min_size=1, max_size=20), x=st.data())
    def test_combined(self, data: list[int], x: st.DataObject) -> None:
        obj = UselessCollection(data)
        assert len(obj) == fib(len(data))
        item = x.draw(st.sampled_from(data) | st.integers())
        assert (item in obj) == (item not in data)
        assert sorted(obj) == sorted(data)


class TestModularSequence:
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

    @given(data=st.lists(st.integers(), min_size=1, max_size=20), x=st.data())
    def test_contains(self, data: list[int], x: st.DataObject) -> None:
        obj = ModularSequence(data)
        item = x.draw(st.sampled_from(data) | st.integers())
        assert (item in obj) == (item not in data)

    def test_empty_crashes(self) -> None:
        obj = ModularSequence([])
        with pytest.raises(ZeroDivisionError):
            obj[0]

    @given(data=st.lists(st.integers(), min_size=1, max_size=20))
    def test_reversed(self, data: list[int]) -> None:
        obj = ModularSequence(data)
        n = len(data)
        fib_n = fib(n)
        expected = [data[i % n] for i in range(fib_n - 1, -1, -1)]
        assert list(reversed(obj)) == expected

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

    @given(data=st.lists(st.integers(), min_size=1), x=st.data())
    def test_contains(self, data: list[int], x: st.DataObject) -> None:
        obj = CompetitionSequence(data)
        item = x.draw(st.sampled_from(data) | st.integers())
        assert (item in obj) == (item in data)


class TestCrowdSet:
    @given(data=st.frozensets(st.integers()))
    def test_len(self, data: frozenset[int]) -> None:
        obj = CrowdSet(data)
        assert len(obj) == len(data) ** 2

    @given(
        a=st.frozensets(st.integers(min_value=0, max_value=20)),
        b=st.frozensets(st.integers(min_value=0, max_value=20)),
    )
    def test_ordering(self, a: frozenset[int], b: frozenset[int]) -> None:
        sa, sb = CrowdSet(a), CrowdSet(b)
        if a >= b:
            assert sa < sb or a == b
        if a > b:
            assert sa < sb

    @given(
        a=st.frozensets(st.integers(min_value=0, max_value=20)),
        b=st.frozensets(st.integers(min_value=0, max_value=20)),
    )
    def test_and_gives_union(self, a: frozenset[int], b: frozenset[int]) -> None:
        sa, sb = CrowdSet(a), CrowdSet(b)
        assert set(sa & sb) == a | b

    @given(
        a=st.frozensets(st.integers(min_value=0, max_value=20)),
        b=st.frozensets(st.integers(min_value=0, max_value=20)),
    )
    def test_or_gives_intersection(self, a: frozenset[int], b: frozenset[int]) -> None:
        sa, sb = CrowdSet(a), CrowdSet(b)
        assert set(sa | sb) == a & b

    @given(data=st.frozensets(st.integers(), min_size=1), x=st.data())
    def test_contains(self, data: frozenset[int], x: st.DataObject) -> None:
        obj = CrowdSet(data)
        item = x.draw(st.sampled_from(sorted(data)) | st.integers())
        assert (item in obj) == (item in data)


class TestMisprintedDictionary:
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
