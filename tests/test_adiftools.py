# import pytest

from adiftools import adiftools


at = adiftools.ADIFParser()
file_path = 'tests/sample.adi'
df = at.read_adi(file_path)

def test_read_adi():
    assert df.shape == (126, 14)
    assert df.columns.tolist() == [
        'CALL', 'MODE', 'RST_SENT', 'RST_RCVD',
        'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF',
        'TIME_OFF', 'BAND', 'FREQ', 'STATION_CALLSIGN',
        'MY_GRIDSQUARE', 'COMMENT', 'GRIDSQUARE']


def test_plot_monthly():
    at.plot_monthly('tests/monthly_qso_test.png')
    assert True


def test_number_of_records():
    at = adiftools.ADIFParser()
    file_path = 'tests/sample.adi'
    _ = at.read_adi(file_path)
    assert at.number_of_records == 126

# TODO: add test_plot_monthly()
# TODO: use test fixture to create a temporary file
