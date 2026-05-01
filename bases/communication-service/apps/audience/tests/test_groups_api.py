import pytest
from django.urls import reverse
from apps.audience.models import Group


@pytest.mark.django_db
def test_group_list(admin_api_client):

    Group.objects.create(name="VIP Group")

    url = reverse("group-list")
    response = admin_api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_group_create(admin_api_client):

    payload = {
        "name": "VIP Group",
        "region": "BD",
        "service": "GOZAYAAN"
    }

    url = reverse("group-list")
    response = admin_api_client.post(url, payload, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_group_patch(admin_api_client):

    group = Group.objects.create(name="Old Group")

    url = reverse("group-detail", args=[group.id])

    response = admin_api_client.patch(
        url,
        {"name": "Updated Group"},
        format="json"
    )

    assert response.status_code == 200
