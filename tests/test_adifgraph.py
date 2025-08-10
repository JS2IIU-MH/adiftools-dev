from adiftools import adiftools
from adiftools import adifgraph


df = adiftools.ADIFParser().read_adi('tests/sample.adi')


def test_monthly_qso():
    adifgraph.monthly_qso(df, 'tests/monthly_qso.png')
    assert True


def test_band_percentage():
    adifgraph.band_percentage(df, 'tests/percentage_band.png')
    assert True


def test_monthly_band_qso():
    adifgraph.monthly_band_qso(df, 'tests/monthly_band_qso.png')
    assert True
