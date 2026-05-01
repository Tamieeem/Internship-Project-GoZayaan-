import jwt
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from utils.jwt import jwt_decode
from utils.jwt_user import JWTUser


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    """Registers JWTAuthentication with drf-spectacular for Swagger UI."""
    target_class = 'utils.authentication.JWTAuthentication'
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication class.

    Extracts Bearer token from Authorization header,
    decodes it using jwt_decode from util,and sets request.user
    as User object built directly from JWT payload
    """

    AUTH_HEADER_PREFIX = 'Bearer'

    def authenticate(self, request):
        """
        Called by DRF on every request.

        Returns:
            tuple: (JWTUser, token) if authenticated.
            None: if no Authorization header present — request treated as unauthenticated.

        Raises:
            AuthenticationFailed: If token is present but invalid.
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        # No header — return None, request will be treated as unauthenticated
        if not auth_header:
            return None

        # Header must be "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.AUTH_HEADER_PREFIX:
            raise AuthenticationFailed(
                'Invalid Authorization header format. Expected: Bearer <token>'
            )

        token = parts[1]

        try:
            payload = jwt_decode(token)
        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationFailed('Token has expired.') from exc
        except jwt.InvalidAudienceError as exc:
            raise AuthenticationFailed('Invalid token audience.') from exc
        except jwt.InvalidIssuerError as exc:
            raise AuthenticationFailed('Invalid token issuer.') from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationFailed('Invalid token.') from exc

        # Build user object from payload
        user = JWTUser.from_payload(payload)

        return (user, token)

    def authenticate_header(self, request):
        """
        Returned in WWW-Authenticate header on 401 responses.
        Tells the client what auth scheme to use.
        """
        return self.AUTH_HEADER_PREFIX
