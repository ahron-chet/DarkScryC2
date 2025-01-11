from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64
from enum import Enum
import os


class KeyType(Enum):
    XML = 1
    PEM = 2
    OBJECT = 3


class RSAManager:

    def __init__(self, private_key_path: str = None, passphrase: bytes = None):
        self.private_key_path = private_key_path
        self._private_key = None

        if private_key_path is not None:
            self._load_private_key(private_key_path, passphrase)

    def _load_private_key(self, path: str, passphrase: bytes = None):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Private key file not found: {path}")

        with open(path, "rb") as f:
            data = f.read()

        try:
            self._private_key = serialization.load_pem_private_key(
                data,
                password=passphrase
            )
        except ValueError as e:
            raise ValueError("Failed to load private key. Possibly invalid passphrase or corrupted file.") from e

    def gen_private_key(self, key_size: int = 2048):
        self._private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )

        return self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,  
            encryption_algorithm=serialization.NoEncryption()
        )

    def save_private_key(self, path: str, passphrase: bytes = None):
        if not self._private_key:
            raise ValueError("No private key available to save. Generate or load one first.")

        algo = serialization.NoEncryption()
        if passphrase:
            algo = serialization.BestAvailableEncryption(passphrase)

        pem_data = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=algo
        )

        with open(path, "wb") as f:
            f.write(pem_data)

    def get_public_key(self, type: KeyType = KeyType.OBJECT):
        if not self._private_key:
            raise ValueError("No private key available. Generate or load one first.")

        public_key = self._private_key.public_key()

        if type == KeyType.OBJECT:
            return public_key

        elif type == KeyType.XML:
            public_numbers = public_key.public_numbers()
            modulus = public_numbers.n
            exponent = public_numbers.e

            modulus_bytes = modulus.to_bytes((modulus.bit_length() + 7) // 8, 'big')
            exponent_bytes = exponent.to_bytes((exponent.bit_length() + 7) // 8, 'big')
            modulus_b64 = base64.b64encode(modulus_bytes).decode('ascii')
            exponent_b64 = base64.b64encode(exponent_bytes).decode('ascii')

            return (
                f"<RSAKeyValue>\r\n"
                f"\t<Modulus>{modulus_b64}</Modulus>\r\n"
                f"\t<Exponent>{exponent_b64}</Exponent>\r\n"
                f"</RSAKeyValue>"
            )

        elif type == KeyType.PEM:
            # Export the public key in PEM format
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            return pem.decode("utf-8")

    def decrypt_data(self, ciphertext: bytes) -> bytes:
        if not self._private_key:
            raise ValueError("No private key available. Generate or load one first.")

        return self._private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

    def sign(self, data: bytes) -> bytes:
        if not self._private_key:
            raise ValueError("No private key available. Generate or load one first.")

        signature = self._private_key.sign(
            data=data,
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256()
        )
        return signature
