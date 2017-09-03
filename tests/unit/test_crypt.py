# -*- coding: utf-8 -*-
import unittest

from keepasshttp import crypto


class TestCrypto(unittest.TestCase):
    def test_pad(self):
        self.assertEqual('1234\4\4\4\4', crypto.pad('1234', 64))

    def test_unpad(self):
        self.assertEqual('1234', crypto.unpad('1234\4\4\4\4', 64))

    def test_decrypt_reverses_encrypt_for_unicode_snowman(self):
        data = '☃'
        key = crypto.get_random_key()
        iv = crypto.get_random_iv()
        enc = crypto.encrypt(data, key, iv)
        self.assertEqual(data, crypto.decrypt(enc, key, iv))

    def test_encrypt(self):
        key='eZNUcE1mUHoHoMW40tfRB/DaYvpWGzojDOT7S0AVOQg='
        iv='FE+fTbKvoZjIP48W/yE8Dg=='
        data = crypto.encrypt('Sally sells seashells', key, iv)
        self.assertEqual('aNbyJgtqd33gFfQrYTkobm1xD6UApyC1x7RF32Hy64w=', data)

    def test_decrypt(self):
        key='eZNUcE1mUHoHoMW40tfRB/DaYvpWGzojDOT7S0AVOQg='
        iv='FE+fTbKvoZjIP48W/yE8Dg=='
        data = crypto.decrypt('aNbyJgtqd33gFfQrYTkobm1xD6UApyC1x7RF32Hy64w=', key, iv)
        self.assertEqual('Sally sells seashells', data)

    def test_decrypt_dict_reverses_encrypt_dict(self):
        data = {1: '☃', 2: ['☃', '☃'], 3: {'☃': 'snowman'}}
        key = crypto.get_random_key()
        iv = crypto.get_random_iv()
        enc = crypto.encrypt_dict(data, key, iv)
        self.assertEqual(data, crypto.decrypt_dict(enc, key, iv))
