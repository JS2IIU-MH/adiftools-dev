import re


def is_ja_call(call_sign: str):
    ''' Determine if it is a JA call sign '''
    # input data check
    if type(call_sign) is not str:
        raise TypeError('Call sign must be string')

    if len(call_sign) < 4:
        raise ValueError('Call sign must be at least 4 characters long')

    pattern = r"^(J[A-S]|[78][J-N])"
    match = re.match(pattern, call_sign)
    return bool(match)


def get_area_num(text: str) -> int | None:
    """
    receives a string and returns a number based on specific conditions

    Args:
        text (str): input string

    Returns:
        int | None: number based on conditions or None
    """
    # Check empty string
    if not text:
        return None

    # If first character starts with 7
    if text[0] == '7':
        return 1

    # If first character is J/8 and string length is 4 or more
    if (text[0] == 'J' or text[0] == '8') and len(text) >= 4:
        third_char = text[2]
        # Check if third character is a number
        if third_char.isdigit():
            return int(third_char)

    # If no conditions match
    return None
