def test_string_segment(expected, actual):
    """
    Takes a passed in test string (actual) and tests whether, when truncated to be the same length as the expected
    string, is equal to it.

    Will fail if the actual string has a length less than the expected string.

    :param expected:
    :param actual:
    :return:
    """
    expected_len = len(expected)
    if len(actual) < expected_len:
        return False
    else:
        truncated_actual = actual[:expected_len]
        return truncated_actual == expected
