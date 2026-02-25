_test_data = {}


def set_test_data(key, value):
    """
    Stored a value in the global _test_data dictionary.
    :param key: Key of the value.
    :param value:  Value saved to the global _test_data.
    """
    _test_data[key] = value


def get_test_data(key):
    """
    Get a value from the global _test_data dictionary.
    :param key: Value that is fetched from the global _test_data dictionary.
    :return: Key value.
    """
    return _test_data.get(key)


