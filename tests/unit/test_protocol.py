import unittest

import mock

from keepasshttp import crypto
from keepasshttp import protocol


class TestProtocol(unittest.TestCase):
    def test_associate(self):
        requestor = mock.Mock(return_value={'Id': 'new_id'})
        key, id_ = protocol.associate(requestor)
        self.assertEqual('new_id', id_)

    def test_test_associate(self):
        requestor = mock.Mock(return_value=True)
        self.assertTrue(protocol.testAssociate('a', 'b', requestor))

    def test_get_sogins(self):
        key = crypto.get_random_key()
        iv = crypto.get_random_iv()
        requestor = mock.Mock(
            return_value={
                'Entries': [{'key': crypto.encrypt('test', key, iv)}],
                'Nonce': iv,
            }
        )
        logins = protocol.get_logins('a', 'b', key, requestor)
        self.assertEqual([{'key': 'test'}], logins)
