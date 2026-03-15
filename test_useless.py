import math

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

PHI = (1 + math.sqrt(5)) / 2


def fib(n: int) -> int:
    return math.floor((1 / math.sqrt(5)) * pow(PHI, n) + 0.5)


# --- LiarContainer ---


@given(data=st.lists(st.integers()), x=st.integers())
def test_liar_container(data, x):
    obj = LiarContainer(data)
    assert (x in obj) == (x not in data)


# --- FibonacciSized ---


@given(data=st.lists(st.integers(), max_size=20))
def test_fibonacci_sized(data):
    obj = FibonacciSized(data)
    assert len(obj) == fib(len(data))


# --- ShuffledIterable ---


@given(data=st.lists(st.integers()))
def test_shuffled_iterable(data):
    obj = ShuffledIterable(data)
    assert sorted(obj) == sorted(data)


# --- EmptyIterable ---


@given(data=st.lists(st.integers()))
def test_empty_iterable(data):
    obj = EmptyIterable(data)
    assert list(obj) == []


# --- FixedIterable ---


@given(data=st.lists(st.integers()))
def test_fixed_iterable(data):
    obj = FixedIterable(data)
    assert list(obj) == ["Do NOT iterate me !"]


# --- ReversedReversible ---


@given(data=st.lists(st.integers()))
def test_reversed_reversible_reversed(data):
    obj = ReversedReversible(data)
    assert list(reversed(obj)) == data


@given(data=st.lists(st.integers()))
def test_reversed_reversible_iter(data):
    obj = ReversedReversible(data)
    assert sorted(obj) == sorted(data)


# --- UselessCollection ---


@given(data=st.lists(st.integers(), max_size=20), x=st.integers())
def test_useless_collection(data, x):
    obj = UselessCollection(data)
    assert len(obj) == fib(len(data))
    assert (x in obj) == (x not in data)
    assert sorted(obj) == sorted(data)


# --- ModularSequence ---


@given(data=st.lists(st.integers(), min_size=1, max_size=20))
def test_modular_sequence_getitem(data):
    obj = ModularSequence(data)
    for i in range(len(data) * 3):
        assert obj[i] == data[i % len(data)]


@given(data=st.lists(st.integers(), min_size=1, max_size=20))
def test_modular_sequence_len(data):
    obj = ModularSequence(data)
    assert len(obj) == fib(len(data))


@given(data=st.lists(st.integers(), min_size=1, max_size=20), x=st.integers())
def test_modular_sequence_contains(data, x):
    obj = ModularSequence(data)
    assert (x in obj) == (x not in data)


def test_modular_sequence_empty_crashes():
    obj = ModularSequence([])
    with pytest.raises(ZeroDivisionError):
        obj[0]


@given(data=st.lists(st.integers(), min_size=1, max_size=20))
def test_modular_sequence_reversed(data):
    obj = ModularSequence(data)
    assert list(reversed(obj)) == data


@given(data=st.lists(st.integers(), min_size=2, max_size=20))
def test_modular_sequence_slice(data):
    obj = ModularSequence(data)
    n = len(data)
    # stop wraps via modulo: n % n == 0, so obj[0:n] is empty
    assert obj[0:n] == []
    # a valid sub-range works with modular indices
    assert obj[0:1] == data[0:1]
    # None start/stop (obj[1:] and obj[:1]) should not crash
    assert obj[:1] == data[:1]
    assert obj[1:] == data[1:]


# --- CompetitionSequence ---


@given(data=st.lists(st.integers()))
def test_competition_sequence_iter(data):
    obj = CompetitionSequence(data)
    assert sorted(obj) == sorted(data)


@given(data=st.lists(st.integers(), min_size=1))
def test_competition_sequence_getitem(data):
    obj = CompetitionSequence(data)
    for i in range(len(data)):
        assert obj[i] == data[i]


@given(data=st.lists(st.integers()))
def test_competition_sequence_len(data):
    obj = CompetitionSequence(data)
    assert len(obj) == len(data)


@given(data=st.lists(st.integers(), min_size=1), x=st.integers())
def test_competition_sequence_contains(data, x):
    obj = CompetitionSequence(data)
    assert (x in obj) == (x in data)


# --- CrowdSet ---


@given(data=st.lists(st.integers()))
def test_crowd_set_len(data):
    obj = CrowdSet(data)
    assert len(obj) == len(set(data)) ** 2


@given(
    a=st.lists(st.integers(min_value=0, max_value=20)),
    b=st.lists(st.integers(min_value=0, max_value=20)),
)
def test_crowd_set_ordering(a, b):
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
def test_crowd_set_and_or(a, b):
    sa, sb = CrowdSet(a), CrowdSet(b)
    real_a, real_b = set(a), set(b)
    # __and__ returns union
    assert set(sa & sb) == real_a | real_b
    # __or__ returns intersection
    assert set(sa | sb) == real_a & real_b


@given(data=st.lists(st.integers()), x=st.integers())
def test_crowd_set_contains(data, x):
    obj = CrowdSet(data)
    assert (x in obj) == (x in set(data))


# --- MisprintedDictionary ---


@given(d=st.dictionaries(st.text(), st.integers(), max_size=20))
def test_misprinted_dictionary_keys(d):
    obj = MisprintedDictionary(d)
    assert sorted(obj.keys()) == sorted(d.keys())


@given(d=st.dictionaries(st.text(), st.integers(), max_size=20))
def test_misprinted_dictionary_values(d):
    obj = MisprintedDictionary(d)
    assert sorted(obj.values()) == sorted(d.values())


@given(d=st.dictionaries(st.text(), st.integers(), max_size=20))
def test_misprinted_dictionary_len(d):
    obj = MisprintedDictionary(d)
    assert len(obj) == fib(len(d))


@given(d=st.dictionaries(st.text(), st.integers(), min_size=1, max_size=20))
def test_misprinted_dictionary_getitem(d):
    obj = MisprintedDictionary(d)
    original_values = sorted(d.values())
    actual_values = sorted(obj[k] for k in obj)
    assert actual_values == original_values


# --- fib cross-check ---


@given(n=st.integers(min_value=0, max_value=70))
def test_fib_cross_check(n):
    """ビネの公式と反復フィボナッチが一致することを確認"""

    def fib_iter(m):
        a, b = 0, 1
        for _ in range(m):
            a, b = b, a + b
        return a

    assert fib(n) == fib_iter(n)
