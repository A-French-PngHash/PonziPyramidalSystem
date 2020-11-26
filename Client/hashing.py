import hashlib
import base64


def hash_password(password: str, username: str):
    hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        username.encode("utf-8"),
        1000000
    )
    base64string = str(base64.b64encode(hash))[2:-2]
    return base64string
