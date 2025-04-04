import asyncio
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import MD5
from cryptography.hazmat.primitives import hashes


class AesCrypto:
    def __init__(self, key: bytes, iv: bytes):
        """
        :param key: 32-byte AES key.
        :param iv: Initialization vector (usually 16 bytes for AES CBC).
        """
        self.key = key
        self.iv = iv
        self._encryptor = None
        self._decryptor = None

    @staticmethod
    def random_key() -> bytes:
        """Generate a random 32-byte AES key."""
        return os.urandom(32)

    def _initialize_encryptor(self) -> None:
        """
        Initialize the AES CBC encryptor with the current key/iv.
        """
        self.set_iv()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        self._encryptor = cipher.encryptor()

    def _initialize_decryptor(self) -> None:
        """
        Initialize the AES CBC decryptor with the current key/iv.
        """
        self.set_iv()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        self._decryptor = cipher.decryptor()

    def set_iv(self, key: bytes = None) -> None:
        """
        Derive a new IV from either 'key' or the current 'iv' using an MD5 hash.
        
        :param key: If given, derive 'iv' from this key. Otherwise derive from current 'iv'.
        """
        digest = hashes.Hash(MD5(), backend=default_backend())
        digest.update(key if key else self.iv)
        self.iv = digest.finalize()

    def _encrypt_sync(self, data: bytes) -> bytes:
        """
        Synchronous AES encryption (CBC mode, PKCS7 padding).
        """
        self._initialize_encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return self._encryptor.update(padded_data) + self._encryptor.finalize()

    def _decrypt_sync(self, encrypted_data: bytes) -> bytes:
        """
        Synchronous AES decryption (CBC mode, PKCS7 unpadding).
        """
        self._initialize_decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = self._decryptor.update(encrypted_data) + self._decryptor.finalize()
        return unpadder.update(decrypted_data) + unpadder.finalize()

    async def encrypt(self, data: bytes, use_async=False) -> bytes:
        """
        Asynchronously encrypt 'data' by offloading to a worker thread.
        """
        if use_async:
            return await asyncio.to_thread(self._encrypt_sync, data)
        return self._encrypt_sync(data)

    async def decrypt(self, data: bytes,  use_async=False) -> bytes:
        """
        Asynchronously decrypt 'data' by offloading to a worker thread.
        """
        if use_async:
            return await asyncio.to_thread(self._decrypt_sync, data)
        return self._decrypt_sync(data)

