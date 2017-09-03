"""Submodule of keepasshttp, implementing the KeePass protocol."""
import logging
import requests

from . import common
from . import crypto
from . import password
from . import util


logger = logging.getLogger(__name__)

DEFAULT_KEEPASS_URL = 'http://localhost:19455/'


def associate(requestor=None):
    """Send a new encryption key to keepass.

    Waits for user to accept and provide a name for the association.

    Returns:
        key: the new encryption key
        identifier: the name provided by the user
    """
    requestor = requestor or DEFAULT_REQUESTOR
    key = crypto.get_random_key()
    input_data = {
        'RequestType': 'associate',
        'Key': key
    }
    output = requestor(key, input_data, None, None)
    return key, output['Id']


def test_associate(id_, key, requestor=None):
    """Test that keepass has the given identifier and key."""
    requestor = requestor or DEFAULT_REQUESTOR
    input_data = {
        'RequestType': 'test-associate',
    }
    return requestor(key, input_data, id_)


def get_logins(url, id_, key, requestor=None):
    """Query keepass for entries that match `url`."""
    requestor = requestor or DEFAULT_REQUESTOR
    iv = crypto.get_random_iv()
    input_data = {
        'RequestType': 'get-logins',
        'Url': crypto.encrypt(bytes(url, "utf-8"), key, iv)
    }
    output = requestor(key, input_data, id_, iv=iv)
    decrypted = [
        crypto.decrypt_dict(entry, key, output['Nonce'])
        for entry in output.get('Entries', [])
    ]
    output_data = [util.convert_to_str(e) for e in decrypted]
    # replace passwords here so that we don't
    # accidently print them
    return [password.replace(e) for e in output_data]


def set_login(url, user, password, id_, key, requestor=None):
    """Create a new entry with url, user and password."""
    requestor = requestor or DEFAULT_REQUESTOR
    iv = crypto.get_random_iv()
    input_data = {
        'RequestType': 'set-login',
        'Url': crypto.encrypt(bytes(url, "utf-8"), key, iv),
        'Login': crypto.encrypt(bytes(user, "utf-8"), key, iv),
        'Password': crypto.encrypt(bytes(password, "utf-8"), key, iv)
    }
    return requestor(key, input_data, id_, iv=iv)


def update_login(uuid, url, user, password, id_, key, requestor=None):
    """Update the url, user or password by its uuid."""
    requestor = requestor or DEFAULT_REQUESTOR
    iv = crypto.get_random_iv()
    input_data = {
        'RequestType': 'set-login',
        'Uuid': crypto.encrypt(bytes(uuid, "utf-8"), key, iv),
        'Url': crypto.encrypt(bytes(url, "utf-8"), key, iv),
        'Login': crypto.encrypt(bytes(user, "utf-8"), key, iv),
        'Password': crypto.encrypt(bytes(password, "utf-8"), key, iv)
    }
    return requestor(key, input_data, id_, iv=iv)


class Requestor(object):
    """Wrapper class which handles a keepasshttp request."""

    def __init__(self, url):
        """Initialize a new Requestor object."""
        self.url = url

    def __call__(self, key, input_data, id_, standard_data=None, iv=None):
        """Exec the request."""
        data = self.merge_data(key, input_data, id_, standard_data, iv)
        response = requests.post(self.url, json=util.convert_to_str(data))
        return self.process_response(response, key)

    def merge_data(self, key, input_data, id_, standard_data=None, iv=None):
        """Merge default data with user input."""
        # standard_data can be set to {} so need to explicitly check
        # that it is equal to None
        if standard_data is None:
            iv = iv or crypto.get_random_iv()
            standard_data = {
                'Id': id_,
                'Nonce': iv,
                'Verifier': get_verifier(iv, key)
            }
        return util.merge(standard_data, input_data)

    def process_response(self, response, key):
        """Process a the response of the executed request."""
        if response.status_code != 200:
            raise common.RequestFailed('Failed to get a response', response)
        output = util.convert_to_str(response.json())
        if output['Success'] == 'False':
            raise common.RequestFailed(
                'keepass returned a unsuccessful response', response)
        if not check_verifier(key, output['Nonce'], output['Verifier']):
            raise common.RequestFailed('Failed to verify response', response)
        return output


DEFAULT_REQUESTOR = Requestor(DEFAULT_KEEPASS_URL)


def get_verifier(iv, key):
    """Generate the verifier by key and iv."""
    iv = bytes(iv, "utf-8") if type(iv) != bytes else iv
    key = bytes(key, "utf-8") if type(key) != bytes else key
    return crypto.encrypt(iv, key, iv)


def check_verifier(key, iv, verifier):
    """Check whether the verifier is valid by key and iv."""
    iv = bytes(iv, "utf-8") if type(iv) != bytes else iv
    key = bytes(key, "utf-8") if type(key) != bytes else key
    verifier = bytes(verifier, "utf-8") if type(verifier) != bytes else verifier
    return verifier == crypto.encrypt(iv, key, iv)
