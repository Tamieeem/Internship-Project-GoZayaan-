import pytest
from django.urls import reverse
from apps.events.models import Provider
from unittest.mock import patch


@pytest.mark.django_db
def test_provider_list(api_client):

    Provider.objects.create(
        name="Test Provider",
        delivery_type="EMAIL",
        region="BD",
        service="GOZAYAAN",
        credentials={"api_key": "12345"}
    )

    url = reverse("provider-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["results"][0]["name"] == "Test Provider"


@pytest.mark.django_db
def test_provider_create(api_client):

    payload = {
        "name": "Test Provider",
        "delivery_type": "EMAIL",
        "region": "BD",
        "service": "GOZAYAAN",
        "credentials": {
            "api_key": "12345"
        },
        "is_active": True
    }
    url = reverse("provider-list")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Test Provider"
@pytest.mark.django_db
def test_provider_patch(api_client):

    provider = Provider.objects.create(
        name="Old Name",
        delivery_type="EMAIL",
        region="BD",
        service="GOZAYAAN",
        credentials={"api_key": "12345"}
    )

    url = reverse("provider-detail", args=[provider.id])

    response = api_client.patch(
        url,
        {"name": "Updated Name"},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Name"
