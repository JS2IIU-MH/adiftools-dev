import pytest
import tempfile
from pathlib import Path
from typing import Any, Generator

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


@pytest.fixture(scope='function')
def txt_file() -> Generator[Path, Any, None]:
    ''' csv tempfile '''
    path = Path(tempfile.NamedTemporaryFile(suffix='.txt', delete=False).name)
    yield path

    # delete tempfile after test
    path.unlink()


def test_read_adi(prep_data):
    ''' test adif DataFrame '''
    assert prep_data.shape == (126, 14)
    assert prep_data.columns.tolist() == [
        'CALL', 'MODE', 'RST_SENT', 'RST_RCVD',
        'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF',
        'TIME_OFF', 'BAND', 'FREQ', 'STATION_CALLSIGN',
        'MY_GRIDSQUARE', 'COMMENT', 'GRIDSQUARE']


def test_to_adi(prep_instance):
    prep_instance.to_adi('tests/sample_out.adi')
    assert True


def test_plot_monthly(prep_instance):
    prep_instance.plot_monthly('tests/monthly_qso_test.png')
    assert True


def test_plot_band_percentage(prep_instance):
    prep_instance.plot_band_percentage('tests/percentage_band_test.png')
    assert True


def test_number_of_records(prep_instance):
    assert prep_instance.number_of_records == 126


def test_call_to_txt(prep_instance, txt_file):
    prep_instance.call_to_txt(txt_file)
    assert True


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
def test_latlon2gl(data_in, expected_data):
    ''' test latitude and longitude to grid locator '''

    if len(data_in) == 3:
        gridlocator = adiftools.latlon2gl(data_in[0], data_in[1], data_in[2])
    else:
        gridlocator = adiftools.latlon2gl(data_in[0], data_in[1])

    assert gridlocator == expected_data


@pytest.mark.parametrize(
    "points, expected",
    [
        ([34.8584, 136.8054, 35.255, 136.9238], 45305.76999847593),
        ([34.8584, 136.8054, 42.7752, 141.6923], 975524.2589462004),
        ([34.8584, 136.8054, 42.2089616, -83.3532049], 10544713.19816745),
    ]
)
def test_get_dist(points, expected):

    TOLERANCE = 0.15

    exp_max = expected + TOLERANCE
    exp_min = expected - TOLERANCE

    res = adiftools.get_dist(points[0], points[1], points[2], points[3])

    assert exp_min < res < exp_max


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
def test_is_ja(callsign, expected):
    assert adiftools.is_ja(callsign) == expected


@pytest.mark.parametrize(
    "callsign, expected",
    [
        ("", pytest.raises(ValueError)),
        ("JA", pytest.raises(ValueError)),
        ("7", pytest.raises(ValueError)),
        (7, pytest.raises(TypeError)),

    ],
)
def test_error_is_ja(callsign, expected):
    with expected as e:
        assert adiftools.is_ja(callsign) == e


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
    assert expected == adiftools.get_area(callsign)


# TODO: use test fixture to create a temporary file
