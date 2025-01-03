import pytest

from adiftools import adiftools

@pytest.fixture
def prep_instance():
    at = adiftools.ADIFParser()
    file_path = 'tests/sample.adi'
    _ = at.read_adi(file_path)
    return at

@pytest.fixture
def prep_data():
    at = adiftools.ADIFParser()
    file_path = 'tests/sample.adi'
    df = at.read_adi(file_path)
    return df


def test_read_adi(prep_data):
    ''' test adif DataFrame '''
    assert prep_data.shape == (126, 14)
    assert prep_data.columns.tolist() == [
        'CALL', 'MODE', 'RST_SENT', 'RST_RCVD',
        'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF',
        'TIME_OFF', 'BAND', 'FREQ', 'STATION_CALLSIGN',
        'MY_GRIDSQUARE', 'COMMENT', 'GRIDSQUARE']


def test_plot_monthly(prep_instance):
    prep_instance.plot_monthly('tests/monthly_qso_test.png')
    assert True


def test_plot_band_percentage(prep_instance):
    prep_instance.plot_band_percentage('tests/percentage_band_test.png')
    assert True


def test_number_of_records(prep_instance):
    assert prep_instance.number_of_records == 126


@pytest.mark.parametrize(
    # variables
    [
        'data_in',
        'expected_data',
    ],
    # values
    [
        # test cases
        pytest.param('PM85kg', (35.2781423, 136.8735481)),
        pytest.param('PM95pl', (35.4913535, 139.2841430)),
        pytest.param('PM95vq', (35.6812362, 139.7671248)),
        pytest.param('PM53fo', (33.5849988, 130.4490906)),
        pytest.param('PL36te', (26.2001297, 127.6466452)),
        pytest.param('QN00ir', (40.7354587, 140.6904126)),
        pytest.param('QN02us', (42.7791317, 141.6866364)),
        pytest.param('QN01js', (41.7757043, 140.8158222)),
        pytest.param('PM74rs', (34.7861612, 135.4380483)),
        pytest.param('PM63it', (33.8276948, 132.7003773)),
    ]
)
def test_gl2latlon(data_in, expected_data):
    '''Test gridlocator to latitude and longitude conversion.'''

    ERROR_THRESHOLD_COEFFICIENT = 0.55

    coordinates = adiftools.gl_to_latlon(data_in)
    lat_min = expected_data[0] - 1/24 * ERROR_THRESHOLD_COEFFICIENT
    lat_max = expected_data[0] + 1/24 * ERROR_THRESHOLD_COEFFICIENT
    lon_min = expected_data[1] - 1/12 * ERROR_THRESHOLD_COEFFICIENT
    lon_max = expected_data[1] + 1/12 * ERROR_THRESHOLD_COEFFICIENT

    assert (lat_min <= coordinates[0] <= lat_max and
            lon_min <= coordinates[1] <= lon_max)


# TODO: use test fixture to create a temporary file
