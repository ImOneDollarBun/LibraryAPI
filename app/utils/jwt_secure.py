import bcrypt
from settings import settings
import jwt


def encode_jwt(
        payload,
        private_key: str = settings.auth_jwt.private_key_path,
        algorithm: str = settings.auth_jwt.algorithm
):
    with open(private_key) as p_key:
        private_key = p_key.read()
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded


def decode_jwt(
        token,
        public_key: str = settings.auth_jwt.public_key_path,
        algorithm: str = settings.auth_jwt.algorithm
):
    with open(public_key) as pb_key:
        public_key = pb_key.read()

    decoded = jwt.decode(
        token,
        public_key,
        algorithms=algorithm
    )
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()

    return bcrypt.hashpw(pwd_bytes, salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)

