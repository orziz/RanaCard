import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


# NOTE: 秘钥仅在服务端使用，不在前端暴露
_KEY = "sd14WDS66sdwgy423Sbfhk"
_IV = "sdagjusasxa"


def _valid_key(s: str) -> bytes:
    b = s.encode("utf-8")
    if len(b) < 16:
        return b.ljust(16, b"\0")
    return b[:16]


def _valid_iv(s: str) -> bytes:
    b = s.encode("utf-8")
    if len(b) < 16:
        return b.ljust(16, b"\0")
    return b[:16]


def decrypt_text(enc_text: str) -> str:
    cipher = Cipher(algorithms.AES(_valid_key(_KEY)), modes.CBC(_valid_iv(_IV)), backend=default_backend())
    decryptor = cipher.decryptor()
    encrypted_data = base64.b64decode(enc_text)
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded = unpadder.update(decrypted_data) + unpadder.finalize()
    return unpadded.decode("utf-8")


def encrypt_text(plain_text: str) -> str:
    cipher = Cipher(algorithms.AES(_valid_key(_KEY)), modes.CBC(_valid_iv(_IV)), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plain_text.encode("utf-8")) + padder.finalize()
    enc = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(enc).decode("utf-8")

