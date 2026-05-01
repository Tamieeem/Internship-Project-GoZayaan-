import pytest
from django.urls import reverse
from apps.audience.models import Contact


@pytest.mark.django_db
def test_contact_list(api_client):

    Contact.objects.create(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone="123456789"
    )

    url = reverse("contact-list")
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_contact_create(api_client):

    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "987654321",
        "region": "BD",
        "service": "GOZAYAAN"
    }

    url = reverse("contact-list")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_contact_patch(api_client):

    contact = Contact.objects.create(
        first_name="Old",
        last_name="Name",
        phone="111111111"
    )

    url = reverse("contact-detail", args=[contact.id])

    response = api_client.patch(
        url,
        {"first_name": "Updated"},
        format="json"
    )

    assert response.status_code == 200
