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


@pytest.fixture
def qrz_multiline_adi_file(tmp_path):
    ''' create a QRZ-like multiline ADIF file for parser tests '''
    content = '''QRZLogbook download sample
<ADIF_VER:5>3.1.1
<PROGRAMID:10>QRZLogbook
<eoh>
<qso_date:8>20260505
<time_on:4>1035
<mode:3>FT8
<band:3>80m
<call:5>KF8XW
<eor>

<mode:3>FT8
<time_on:4>1037
<call:6>KB3LNM
<qso_date:8>20260505
<band:3>80m
<eor>
'''
    file_path = tmp_path / 'sample_qrz_multiline.adi'
    file_path.write_text(content, encoding='utf-8')
    return str(file_path)


def test_read_adi(prep_data):
    ''' test adif DataFrame '''
    assert prep_data.shape == (126, 14)
    assert prep_data.columns.tolist() == [
        'CALL', 'MODE', 'RST_SENT', 'RST_RCVD',
        'QSO_DATE', 'TIME_ON', 'QSO_DATE_OFF',
        'TIME_OFF', 'BAND', 'FREQ', 'STATION_CALLSIGN',
        'MY_GRIDSQUARE', 'COMMENT', 'GRIDSQUARE']


def test_read_adi_qrz_multiline(qrz_multiline_adi_file):
    ''' test QRZ.com multiline ADIF format '''
    at = adiftools.ADIFParser()
    df = at.read_adi(qrz_multiline_adi_file)

    assert len(df) == 2
    assert 'CALL' in df.columns
    assert 'QSO_DATE' in df.columns
    assert 'TIME_ON' in df.columns


def test_read_methods_consistency_qrz_multiline(qrz_multiline_adi_file):
    ''' test consistency across read methods for multiline records '''
    seq_parser = adiftools.ADIFParser()
    stream_parser = adiftools.ADIFParser()
    parallel_parser = adiftools.ADIFParser()

    seq_df = seq_parser.read_adi(qrz_multiline_adi_file)
    stream_df = stream_parser.read_adi_streaming(qrz_multiline_adi_file)
    parallel_df = parallel_parser.read_adi_parallel(
        qrz_multiline_adi_file, num_processes=2)

    assert len(seq_df) == len(stream_df) == len(parallel_df) == 2
    assert set(seq_df.columns) == set(stream_df.columns)
    assert set(seq_df.columns) == set(parallel_df.columns)


def test_to_adi(prep_instance, tmp_path):
    out = tmp_path / 'sample_out.adi'
    prep_instance.to_adi(str(out))
    assert out.exists()


def test_plot_monthly(prep_instance, tmp_path):
    out = tmp_path / 'monthly_qso_test.png'
    prep_instance.plot_monthly(str(out))
    assert out.exists()


def test_plot_band_percentage(prep_instance, tmp_path):
    out = tmp_path / 'percentage_band_test.png'
    prep_instance.plot_band_percentage(str(out))
    assert out.exists()


def test_number_of_records(prep_instance):
    assert prep_instance.number_of_records == 126


def test_call_to_txt(prep_instance, tmp_path):
    out = tmp_path / 'calls.txt'
    prep_instance.call_to_txt(str(out))
    assert out.exists()


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
