import pytest
from django.urls import reverse
from apps.events.models import Content


@pytest.mark.django_db
def test_content_list(api_client):

    Content.objects.create(
        name="OTP Template",
        body_html="<b>{{otp_code}}</b>",
        body_text="OTP {{otp_code}}",
        variables={"otp_code": "integer"},
        template_path="/templates/otp.html"
    )

    url = reverse("content-list")
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["results"][0]["name"] == "OTP Template"


@pytest.mark.django_db
def test_content_create(api_client):

    payload = {
        "name": "Welcome Template",
        "body_html": "<h1>Welcome {{user_name}}</h1>",
        "body_text": "Welcome {{user_name}}",
        "variables": {"user_name": "string"},
        "template_path": "/templates/welcome.html"
    }

    url = reverse("content-list")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "Welcome Template"


@pytest.mark.django_db
def test_content_patch(api_client):

    content = Content.objects.create(
        name="Old Template",
        body_html="<b>Old</b>",
        body_text="Old",
        variables={"name": "string"},
        template_path="/templates/old.html"
    )

    url = reverse("content-detail", args=[content.id])

    response = api_client.patch(
        url,
        {"name": "Updated Template"},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["name"] == "Updated Template"
