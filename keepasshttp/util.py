"""Submodule of keepasshttp, providing helper methods."""
import itertools


def json_map(fn, json_obj):
    """Apply function `fn` to each value in `json_obj`.

    json_obj is not a json string, but something that could be the result of
    json.load() - an object consisting of maps, lists and simple values.

    Example:
    In []: util.jsonMap(string.upper, {'keyA': 'value', 'keyB': ['a', 'b', 'c']})
    Out[]: {'keyA': 'VALUE', 'keyB': ['A', 'B', 'C']}

    Args:
        fn: callable taking one argument and returning one argument
        json_obj: an object consisting of maps, lists and simple values.
    """
    def _fn(val):
        if val is None:
            return None
        elif isinstance(val, dict):
            return {k: _fn(v) for k, v in list(val.items())}
        elif isinstance(val, list):
            return list(map(_fn, val))
        elif isinstance(val, bytes):
            return str(val, 'utf-8')
        else:
            return fn(val)
    return _fn(json_obj)


def convert_to_str(input_dict):
    """Convert all keys and values of the given dict to str.

    Args:
        input_dict (dict): data dict
    Returns:
        dict: converted dict
    """
    return json_map(str, input_dict)


def merge(d1, d2):
    """Merge to dicts into one.

    Args:
        d1 (dict): dataset 1
        d2 (dict): dataset 2
    Returns:
        dict: merged dict
    """
    return dict(itertools.chain(list(d1.items()), list(d2.items())))
