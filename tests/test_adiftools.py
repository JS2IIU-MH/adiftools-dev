# import pytest

from adiftools import adiftools


def test_read_adi():
    at = adiftools.ADIFParser()
    file_path = 'tests/sample.adi'
    df = at.read_adi(file_path)
    assert df.shape == (126, 14)
    assert df.columns.tolist() == [
        'CALL', 'MODE', 'RST_SENT', 'RST_RCVD',
        'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF',
        'TIME_OFF', 'BAND', 'FREQ', 'STATION_CALLSIGN',
        'MY_GRIDSQUARE', 'COMMENT', 'GRIDSQUARE']


def test_number_of_records():
    at = adiftools.ADIFParser()
    file_path = 'tests/sample.adi'
    _ = at.read_adi(file_path)
    assert at.number_of_records == 126
