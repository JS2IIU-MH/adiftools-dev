
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


def main():
    print(gl_to_latlon('PM85kg'))


if __name__ == '__main__':
    main()
