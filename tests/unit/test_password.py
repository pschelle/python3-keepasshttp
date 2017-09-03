import unittest

import mock

from keepasshttp.password import Password


class TestPassword(unittest.TestCase):
    def test_password(self):
        password = Password('Test123')
        self.assertEqual('Test123', password.value)
        self.assertEqual('*****', str(password))
        self.assertEqual('Password(*****)', repr(password))
