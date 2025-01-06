from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import MD5
from cryptography.hazmat.primitives import hashes
import os


class AesCrypto:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.encryptor = None
        self.decryptor = None

    def _initialize_encryptor(self):
        self.set_iv()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        self.encryptor = cipher.encryptor()

    def _initialize_decryptor(self):
        self.set_iv()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        self.decryptor = cipher.decryptor()

    def encrypt(self, data):
        self._initialize_encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return self.encryptor.update(padded_data) + self.encryptor.finalize()

    def decrypt(self, encrypted_data):
        self._initialize_decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = self.decryptor.update(encrypted_data) + self.decryptor.finalize()
        return unpadder.update(decrypted_data) + unpadder.finalize()

    def set_iv(self, key=None):
        if key:
            digest = hashes.Hash(MD5(), backend=default_backend())
            digest.update(key)
            self.iv = digest.finalize()
        else:
            digest = hashes.Hash(MD5(), backend=default_backend())
            digest.update(self.iv)
            self.iv = digest.finalize()

    @staticmethod
    def random_key():
        return os.urandom(32)
