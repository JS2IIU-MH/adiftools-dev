import re


def is_ja_call(call_sign: str):
    # input data check
    if type(call_sign) is not str:
        raise TypeError('Call sign must be string')

    if len(call_sign) < 4:
        raise ValueError('Call sign must be at least 4 characters long')

    pattern = r"^(J[A-S]|[78][J-N])"
    match = re.match(pattern, call_sign)
    return bool(match)
