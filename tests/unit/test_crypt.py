# -*- coding: utf-8 -*-
import unittest

from keepasshttp import crypto


class TestCrypto(unittest.TestCase):
    def test_pad(self):
        self.assertEqual(b'1234\x04\x04\x04\x04', crypto.pad(b'1234', 64))

    def test_unpad(self):
        self.assertEqual(b'1234', crypto.unpad(b'1234\x04\x04\x04\x04', 64))

    def test_decrypt_reverses_encrypt_for_unicode_snowman(self):
        data = bytes('☃', 'utf-8')
        key = crypto.get_random_key()
        iv = crypto.get_random_iv()
        enc = crypto.encrypt(data, key, iv)
        self.assertEqual(data, crypto.decrypt(enc, key, iv))

    def test_encrypt(self):
        key='eZNUcE1mUHoHoMW40tfRB/DaYvpWGzojDOT7S0AVOQg='
        iv='FE+fTbKvoZjIP48W/yE8Dg=='
        data = crypto.encrypt(b'Sally sells seashells', key, iv)
        self.assertEqual(b'aNbyJgtqd33gFfQrYTkobm1xD6UApyC1x7RF32Hy64w=', data)

    def test_decrypt(self):
        key='eZNUcE1mUHoHoMW40tfRB/DaYvpWGzojDOT7S0AVOQg='
        iv='FE+fTbKvoZjIP48W/yE8Dg=='
        data = crypto.decrypt(b'aNbyJgtqd33gFfQrYTkobm1xD6UApyC1x7RF32Hy64w=', key, iv)
        self.assertEqual(b'Sally sells seashells', data)
