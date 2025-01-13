from geographiclib.geodesic import Geodesic


def _alpha_to_lonlat(alpha):
    """Converts an alpha character to longitude and latitude coefficients.

    Args:
        alpha (str): Alpha character.

    Returns:
        tuple: Longitude and Latitude coefficient in degrees.
    """

    if type(alpha) is not str:
        raise ValueError('Invalid alpha type')

    return (ord(alpha) - 65) * 20 - 180


def _alpha_to_sub(alpha):
    """Converts an alpha character to sub square coefficients.

    Args:
        alpha (str): Alpha character.

    Returns:
        float: Sub square coefficient in degrees.
    """

    if type(alpha) is not str:
        raise ValueError('Invalid alpha type')

    return (ord(alpha) - 65 + 0.5) / 12


def gl_to_latlon(gridlocator):
    """Converts a grid locator to latitude and longitude.

    Args:
        gridlocator (str): Grid locator.

    Returns:
        tuple: Latitude and Longitude in degrees.
    """
    if len(gridlocator) < 4 or len(gridlocator) % 2 != 0:
        raise ValueError('Invalid GL length')

    gridlocator = gridlocator.upper()

    # South west corner of the FIELD - first two characters
    lon = _alpha_to_lonlat(gridlocator[0])
    lat = _alpha_to_lonlat(gridlocator[1]) / 2

    if len(gridlocator) < 4:
        lon += 10
        lat += 5
    elif len(gridlocator) < 6:
        # Square - next two characters
        lon += int(gridlocator[2]) * 2 + 1
        lat += int(gridlocator[3]) * 1 + 0.5
    elif len(gridlocator) == 6:
        # subsquare - next two characters
        lon += int(gridlocator[2]) * 2 + _alpha_to_sub(gridlocator[4])
        lat += int(gridlocator[3]) * 1 + _alpha_to_sub(gridlocator[5]) / 2

    return (lat, lon)


def latlon_to_gl(latitude, longitude, fourdigit=False):
    """Converts latitude and longitude to a grid locator.

    Args:
        Latitude and Longitude in degrees.
        `fourdigit`: if True, returns 4-digit grid square

    Returns:
        gridlocator (str): Grid locator.
    """

    if latitude < -90 or latitude > 90:
        raise ValueError('latitude over range of value.')
    if longitude < -180 or longitude > 180:
        raise ValueError('longitude over range of value.')

    gl = []
    str_gl = ''

    # first digit
    idx = int((180 + (longitude // 20 * 20)) / 20)
    tmp_lon1 = -180 + idx * 20
    gl.append(chr(idx + ord('A')))

    # second digit
    idx = int((90 + (latitude // 10 * 10)) / 10)
    tmp_lat1 = -90 + idx * 10
    gl.append(chr(idx + ord('A')))

    # third digit
    idx = int((longitude - tmp_lon1) // 2)
    tmp_lon2 = (longitude - tmp_lon1) // 2 * 2 + tmp_lon1
    gl.append(str(idx))

    # fourth digit
    idx = int(latitude - (latitude // 10 * 10) // 1)
    tmp_lat2 = (latitude - tmp_lat1) // 1 * 1 + tmp_lat1
    gl.append(str(idx))

    if not fourdigit:
        # fifth digit
        idx = int((longitude - tmp_lon2) // (2/24))
        gl.append(chr(idx + ord('a')))

        # sixth digit
        idx = int((latitude - tmp_lat2) // (1/24))
        gl.append(chr(idx + ord('a')))

    for s in gl:
        str_gl += s

    return str_gl


def get_distance(p1_lat, p1_lon, p2_lat, p2_lon):
    if not ((-90 < p1_lat < 90) and (-90 < p2_lat < 90) and
            (-180 < p1_lon < 180) and (-180 < p2_lon < 180)):
        raise ValueError('make sure latitude or longitude value is in range')

    res = Geodesic.WGS84.Inverse(p1_lat, p1_lon, p2_lat, p2_lon)

    return res['s12']


def main():
    pass


if __name__ == '__main__':
    main()
