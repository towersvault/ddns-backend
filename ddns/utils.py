import random
import string
import base64
import bcrypt
import logging
import hashlib


IDENTIFIER_TOKEN_LENGTH = 16
SECRET_TOKEN_LENGTH = 32
ALPHABET = string.ascii_lowercase + string.digits


def generate_identifier_token() -> str:
    return ''.join(random.choices(ALPHABET, k=IDENTIFIER_TOKEN_LENGTH))


def generate_secret_token() -> str:
    return ''.join(random.choices(ALPHABET, k=SECRET_TOKEN_LENGTH))


def generate_full_token_pair(
        identifier=None,
        secret=None
) -> str:
    if not identifier:
        identifier = generate_identifier_token()

    if not secret:
        secret = generate_secret_token()

    return f'{identifier}-{secret}'


def b64_encode(token: str) -> bytes:
    return base64.b64encode(
        hashlib.sha256(token.encode('utf-8')).digest()
    )


def hash_token(token: str) -> str:
    token_encoded = b64_encode(token)
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(token_encoded, salt)
    return hash.decode('utf-8')


def compare_hashed_token(token: str, hashed_token: str) -> bool:
    token_encoded = b64_encode(token)
    hashed_encoded = hashed_token.encode('utf-8')

    logging.debug(f'check_hashed_token: {token}, {hashed_token}, check={bcrypt.checkpw(token_encoded, hashed_encoded)}')

    return bcrypt.checkpw(token_encoded, hashed_encoded)


def unpack_api_token(user_submitted_token: str) -> tuple:
    """ Returns the IDENTIFIER_TOKEN and the API_SECRET_TOKEN in that order. """
    token_data = str(user_submitted_token).split('-')

    logging.debug(f'Unpacked Token: {token_data}')

    return token_data[0], token_data[1]
