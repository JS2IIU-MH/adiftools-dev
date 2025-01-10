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
