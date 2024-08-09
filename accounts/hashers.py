import asyncio
import hashlib
import base64
import random
import secrets


async def hash_password(
        raw_password: str,
        salt: str = None,
        algorithm: str = 'SHA256',
        iterations: int = 720_000
):
    salt = salt or secrets.token_urlsafe(random.randint(15, 25))
    hash = await asyncio.to_thread(  # pbkdf2_hmac releases GIL
        hashlib.pbkdf2_hmac,
        algorithm,
        raw_password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations,
        None
    )
    hash = base64.b64encode(hash).decode('ascii').strip()
    return f'{hash}${salt}${algorithm}${iterations}'


async def check_password(password_hash: str, raw_password: str) -> bool:
    _, salt, algorithm, iterations = password_hash.split('$')
    return password_hash == await hash_password(raw_password, salt, algorithm, int(iterations))
