import pytest
from rest_framework.test import APIClient
from utils.jwt import jwt_encode


@pytest.fixture
def api_client():

    token = jwt_encode({
        "username": "test_admin",
        "is_admin": True,
        "groups": ["marketing"],
        "region": "BD",
        "source": "pytest"
    })

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client

#groups


@pytest.fixture
def admin_api_client():
    from rest_framework.test import APIClient
    from utils.jwt import jwt_encode

    token = jwt_encode({
        "username": "admin_user",
        "is_admin": True,
        "groups": ["admin"],
        "region": "BD",
        "source": "pytest"
    })

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client
