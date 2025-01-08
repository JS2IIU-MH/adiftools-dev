import pytest
from adiftools import gridlocator as gl


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
def test_gl_to_latlon(data_in, expected_data):
    '''Test gridlocator to latitude and longitude conversion.'''

    ERROR_THRESHOLD_COEFFICIENT = 0.55

    coordinates = gl.gl_to_latlon(data_in)
    lat_min = expected_data[0] - 1/24 * ERROR_THRESHOLD_COEFFICIENT
    lat_max = expected_data[0] + 1/24 * ERROR_THRESHOLD_COEFFICIENT
    lon_min = expected_data[1] - 1/12 * ERROR_THRESHOLD_COEFFICIENT
    lon_max = expected_data[1] + 1/12 * ERROR_THRESHOLD_COEFFICIENT

    assert (lat_min <= coordinates[0] <= lat_max and
            lon_min <= coordinates[1] <= lon_max)


@pytest.mark.parametrize(
    # variables
    [
        'expected_data',
        'data_in',
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
def test_latlon_to_gl(data_in, expected_data):
    ''' test latitude and longitude to grid locator '''

    gridlocator = gl.latlon_to_gl(data_in[0], data_in[1])

    assert gridlocator == expected_data
