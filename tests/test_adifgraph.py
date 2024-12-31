from adiftools import adiftools
from adiftools import adifgraph


df = adiftools.ADIFParser().read_adi('tests/sample.adi')

def test_monthly_qso():
    adifgraph.monthly_qso(df, 'tests/monthly_qso.png')
    assert True
