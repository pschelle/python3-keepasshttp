"""Submodule of keepasshttp, providing a Password wrapper class."""


class Password(object):
    """A simple object that stores a password but prints '***'.

    This helps prevent accidentally printing a password to the terminal.
    """

    def __init__(self, password):
        """Initialize a new Password object."""
        self.value = password

    def __str__(self):
        """Conversation method from object to string."""
        return '*****'

    def __repr__(self):
        """Create a object represensation string."""
        return '{}(*****)'.format(self.__class__.__name__)


def _is_password(key):
    """Check whether a key is 'password'.

    Args:
        key (str): dictionary key
    Returns
        bool: true if key is 'password'
    """
    return key.lower() == 'password'


def replace(mapping):
    """Replace the values for keys that look like passwords."""
    return {k: Password(v) if _is_password(k) else v for k, v in list(mapping.items())}
