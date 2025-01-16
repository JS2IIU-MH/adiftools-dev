import pytest

import adiftools.callsign as cs


@pytest.mark.parametrize(
    "callsign, expected",
    [
        ("JA1ABC", True),
        ("7K1XYZ", True),
        ("8L1DEF", True),
        ("JTA1ABC", False),
        ("7Z1XYZ", False),
        ("9J1DEF", False),
    ],
)
def test_is_ja_call(callsign, expected):
    assert cs.is_ja_call(callsign) == expected


@pytest.mark.parametrize(
    "callsign, expected",
    [
        ("", pytest.raises(ValueError)),
        ("JA", pytest.raises(ValueError)),
        ("7", pytest.raises(ValueError)),
        (7, pytest.raises(TypeError)),

    ],
)
def test_error_is_ja_call(callsign, expected):
    with expected as e:
        assert cs.is_ja_call(callsign) == e


@pytest.mark.parametrize(
    "callsign, expected",
    [
        ("JS2IIU", 2),
        ("7N4AAA", 1),
        ("JA1RL", 1),
        ("8J1RL", 1),
        ("JR6AAA", 6),
        ("JA0AAA", 0),
        ("JAAAAA", None),
        ("", None),
    ]
)
def test_get_area_num(callsign, expected):
    assert expected == cs.get_area_num(callsign)
