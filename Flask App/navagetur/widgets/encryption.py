#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Sedona Thomas"
__date__ = "04/12/2022"
__version__ = "1.0.0"
__maintainer__ = "Sedona Thomas"
__links__ = ["https://github.com/sedona-thomas/Navagetur"]
__email__ = "sedona.thomas@columbia.edu"

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from navagetur.widgets.directory_location import *


class DataEncryption(object):

    """
    DataEncryption encrypts and decrypts text given a password and salt
    """

    def __init__(self, password, filepath, file="salt.txt"):
        """
        Construct a new 'DataEncryption' object.

        :return: returns nothing
        """
        self._password = self._string_to_bytes(password)
        self._salt = os.urandom(16)
        self._filepath = filepath
        self._salt_file = file
        self._key = self._make_key()
        self._crypter = Fernet(self._key)

    def encrypt(self, plaintext):
        """
        Encrypts the given plaintext

        :param plaintext: the plaintext to be encrypted
        :return: returns the resulting ciphertext
        """
        byte_string = self._string_to_bytes(plaintext)
        token = self._crypter.encrypt(byte_string)
        return token

    def decrypt(self, ciphertext):
        """
        Decrypts the given ciphertext

        :param ciphertext: the ciphertext to be decrypted
        :return: returns the resulting plaintext
        """
        byte_string = self._crypter.decrypt(ciphertext)
        string = self._byte_to_utf8(byte_string)
        return string

    def save_salt(self):
        """
        Saves the current salt in the data folder

        :return: nothing
        """
        with open(self._location(self._salt_file), "wb") as salt_file:
            salt_file.write(self._salt)

    def _string_to_bytes(self, string):
        """
        Converts a regular string to a byte string

        :param string: string to convert
        :return: returns byte string
        """
        return string.encode('utf-8')

    def _byte_to_utf8(self, byte_string):
        """
        Converts a byte string to a regular string

        :param byte_string: byte string to convert
        :return: returns regular string
        """
        return byte_string.decode("utf-8")

    def _make_key(self):
        """
        Makes a key for encryption and decryption

        :return: returns key for current cipher
        """
        if os.path.exists(self._location(self._salt_file)):
            self._read_salt()
        key_derivation_function = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=390000,
        )
        derived_password = key_derivation_function.derive(self._password)
        key = base64.urlsafe_b64encode(derived_password)
        return key

    def _location(self, file):
        """
        Adds the expected location of the file

        :return: returns full filepath
        """
        return pwd + "navagetur/data/" + file

    def _read_salt(self):
        """
        Reads a saved salt

        :return: saved salt value
        """
        with open(self._location(self._salt_file), "rb") as salt_file:
            return salt_file.read()


# class DataEncryptionTest(object):

#     def __init__(self, first, password):
#         self._password = self._string_to_bytes(password)
#         self._salt = os.urandom(16) if first else self._read_salt()
#         self._key = self._make_key()
#         self._crypter = Fernet(self._key)

#     def encrypt(self, plaintext):
#         byte_string = self._string_to_bytes(plaintext)
#         token = self._crypter.encrypt(byte_string)
#         return token

#     def decrypt(self, ciphertext):
#         byte_string = self._crypter.decrypt(ciphertext)
#         string = self._byte_to_utf8(byte_string)
#         return string

#     def save_salt(self, location):
#         with open(location, "wb") as salt_file:
#             salt_file.write(self._salt)

#     def _make_key(self):
#         print(type(self._salt))
#         print(self._salt)
#         key_derivation_function = PBKDF2HMAC(
#             algorithm=hashes.SHA256(),
#             length=32,
#             salt=self._salt,
#             iterations=390000,
#         )
#         derived_password = key_derivation_function.derive(self._password)
#         key = base64.urlsafe_b64encode(derived_password)
#         return key

#     def _read_salt(self):
#         with open("salt.txt", "rb") as salt_file:
#             return salt_file.read()

#     def _string_to_bytes(self, string):
#         return string.encode('utf-8')

#     def _byte_to_utf8(self, byte_string):
#         return byte_string.decode("utf-8")


# if __name__ == "__main__":
#     text = "hello world"
#     password = "password"
#     crypter = DataEncryptionTest(True, password)
#     encryption = crypter.encrypt(text)
#     decryption = crypter.decrypt(encryption)

#     crypter.save_salt("./salt.txt")

#     print("1", encryption)
#     print("2", decryption)

#     text2 = "hello world2"
#     password2 = "password2"
#     crypter2 = DataEncryptionTest(False, password2)
#     encryption2 = crypter.encrypt(text2)
#     decryption2 = crypter.decrypt(encryption2)

#     print("3", encryption2)
#     print("4", decryption2)
