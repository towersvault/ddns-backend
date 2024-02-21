import random
import string
import base64
import bcrypt
import logging
import hashlib


IDENTIFIER_TOKEN_LENGTH = 16
SECRET_TOKEN_LENGTH = 32
TOTAL_TOKEN_LENGTH = 16 + 32 + 1
ALPHABET = string.ascii_lowercase + string.digits


def generate_identifier_token() -> str:
    """Generates a random string of IDENTIFIER_TOKEN_LENGTH

    The identifier_token is intended to remain visible and unhashed.
    """
    return ''.join(random.choices(ALPHABET, k=IDENTIFIER_TOKEN_LENGTH))


def generate_secret_token() -> str:
    """Generates a random string of SECRET_TOKEN_LENGTH

    The secret_token is intended to be hashed if it gets stored.
    """
    return ''.join(random.choices(ALPHABET, k=SECRET_TOKEN_LENGTH))


def generate_full_token_pair(identifier=None,
                             secret=None) -> str:
    """Generates a full token pair with a hyphen (-) as a token divider.

    Optional identifier and/or secret tokens can be provided to avoid randomly
    generating the respective parts.
    """
    if not identifier:
        identifier = generate_identifier_token()

    if not secret:
        secret = generate_secret_token()

    return f'{identifier}-{secret}'


def b64_encode(secret_token: str) -> bytes:
    """Base64 encodes a token and returns the bytes object.

    Intended as a small helper function for hashing secret tokens.
    """
    return base64.b64encode(
        hashlib.sha256(secret_token.encode('utf-8')).digest()
    )


def hash_token(secret_token: str) -> str:
    """Hashes a token and returns the string."""
    token_encoded = b64_encode(secret_token)
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(token_encoded, salt)
    return hash.decode('utf-8')


def compare_hashed_token(secret_token: str,
                         hashed_secret_token: str) -> bool:
    """Compares a submitted secret_token to a hashed_secret_token."""
    token_encoded = b64_encode(secret_token)
    hashed_encoded = hashed_secret_token.encode('utf-8')

    logging.debug((f'check_hashed_token: {secret_token}, '
                   f'{hashed_secret_token}, '
                   f'check={bcrypt.checkpw(token_encoded, hashed_encoded)}'))

    return bcrypt.checkpw(token_encoded, hashed_encoded)


def unpack_api_token(user_submitted_token: str) -> tuple:
    """Returns the IDENTIFIER_TOKEN and the SECRET_TOKEN in that order."""
    token_data = str(user_submitted_token).split('-')

    logging.debug(f'Unpacked Token: {token_data}')

    return token_data[0], token_data[1]
