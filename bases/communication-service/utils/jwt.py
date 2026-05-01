import uuid
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

import jwt


def jwt_encode(payload: dict) -> str:
    """
    Encode a payload into a JWT token.

    Args:
        payload (dict): Data to encode. Should contain username, is_admin,
                        groups, region, service.

    Returns:
        str: Signed JWT token string.
    """
    now = timezone.now()

    base_claims = {
        "iat": int(now.timestamp()),
        "exp": int(
            (now + timedelta(
                minutes=settings.JWT_ACCESS_TOKEN_LIFETIME_MINUTES
            )).timestamp()
        ),
        # for encode , issuer is the service that creates the token
        "iss": settings.JWT_ISSUER,
        # for  encode , audience is the primary intended recipient of the token
        "aud": settings.JWT_ACCEPTED_AUDIENCES[0],
        "jti": str(uuid.uuid4()),
    }

    # Merge caller's payload with base claims
    token_payload = {**payload, **base_claims}

    token = jwt.encode(
        token_payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return token


def jwt_decode(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Args:
        token (str): JWT token string.

    Returns:
        dict: Decoded payload.

    Raises:
        jwt.ExpiredSignatureError: If token has expired.
        jwt.InvalidTokenError: If token is invalid or tampered.
    """
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        # for decode , audience is the service that decodes the token
        audience=settings.JWT_ISSUER,
        # for decode , issuer is the known source for token
        issuer=settings.JWT_ACCEPTED_AUDIENCES,
    )
    return payload
