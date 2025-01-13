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
        pytest.param('QN01', (41.7757043, 140.8158222, True)),
        pytest.param('PM74', (34.7861612, 135.4380483, True)),
        pytest.param('PM63', (33.8276948, 132.7003773, True)),
        pytest.param('QN01js', (41.7757043, 140.8158222, False)),
        pytest.param('PM74rs', (34.7861612, 135.4380483, False)),
        pytest.param('PM63it', (33.8276948, 132.7003773, False)),
    ]
)
def test_latlon_to_gl(data_in, expected_data):
    ''' test latitude and longitude to grid locator '''

    if len(data_in) == 3:
        gridlocator = gl.latlon_to_gl(data_in[0], data_in[1], data_in[2])
    else:
        gridlocator = gl.latlon_to_gl(data_in[0], data_in[1])

    assert gridlocator == expected_data


@pytest.mark.parametrize(
    "points, expected",
    [
        ([34.8584, 136.8054, 35.255, 136.9238], 45305.76999847593),
        ([34.8584, 136.8054, 42.7752, 141.6923], 975524.2589462004),
        ([34.8584, 136.8054, 42.2089616, -83.3532049], 10544713.19816745),
    ]
)
def test_get_distance(points, expected):

    TOLERANCE = 0.15

    exp_max = expected + TOLERANCE
    exp_min = expected - TOLERANCE

    res = gl.get_distance(points[0], points[1], points[2], points[3])

    assert exp_min < res < exp_max


@pytest.mark.parametrize(
    "points, expected",
    [
        ([134.8584, 136.8054, 35.255, 136.9238], pytest.raises(ValueError)),
        ([34.8584, 236.8054, 42.7752, 141.6923], pytest.raises(ValueError)),
        ([34.8584, 136.8054, 142.7752, 141.6923], pytest.raises(ValueError)),
        ([34.8584, 136.8054, 42.7752, 241.6923], pytest.raises(ValueError)),
    ]
)
def test_error_getdistance(points, expected):
    with expected as e:
        assert gl.get_distance(points[0], points[1], points[2], points[3]) == e
