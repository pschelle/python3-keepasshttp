"""Submodule of keepasshttp, providing session handling."""
import logging
import os
import json

from . import protocol


logger = logging.getLogger(__name__)


class Session(object):
    """Wrapper class to handle communication functions."""

    def __init__(self, key, id_):
        """Initialize a new Session object."""
        self.key = key
        self.id_ = id_

    @classmethod
    def start(cls, appname):
        """Start a new communication session."""
        config_dir = os.path.join(os.getenv('HOME'), '.config/', appname)
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir, 0o700)
        config_path = os.path.join(config_dir, 'keepasshttp.json')
        if os.path.exists(config_path):
            with open(config_path) as fin:
                config = json.load(fin)
            id_ = config['id']
            key = config['key']
            if not protocol.test_associate(id_, key):
                logger.warning("Previous association failed. Loading new association")
                key, id_ = get_and_save_new_association(config_path)
        else:
            logger.info("No previous association. Loading new association")
            key, id_ = get_and_save_new_association(config_path)
        return cls(key, id_)

    def get_logins(self, url):
        """Get all entries which match the given url.

        Args:
            url (str): url to look for
        Returns:
            list: matching entries
        """
        return protocol.get_logins(url, self.id_, self.key)


def get_and_save_new_association(config_path):
    """Associate a new key and store it.

    Args:
        config_path (str): filepath to the configfile
    Returns:
        str, str: new pair of key and its id
    """
    key, id_ = protocol.associate()
    with open(config_path, 'w') as fout:
        fout.write(json.dumps({'key': key.decode('utf-8'), 'id': id_}))
    return key, id_
