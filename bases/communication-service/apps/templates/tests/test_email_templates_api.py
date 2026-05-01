import pytest
from django.urls import reverse
from apps.templates.models import EmailTemplate
from apps.events.models import Content


@pytest.mark.django_db
def test_email_template_list(api_client):

    content = Content.objects.create(
        name="OTP Template",
        body_html="<b>{{otp}}</b>",
        body_text="OTP {{otp}}",
        variables={"otp": "integer"},
        template_path="/templates/otp.html"
    )

    EmailTemplate.objects.create(
        template_code="user_auth_otp",
        name="verification mail",
        subject="Your code",
        sender_email="tamim@gozayaan.com",
        priority="LOW",
        is_active=True,
        max_retry=5,
        region="BD",
        service="GOZAYAAN",
        content=content
    )

    url = reverse("email-template-list")
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_email_template_create(api_client):

    content = Content.objects.create(
        name="OTP Template",
        body_html="<b>{{otp}}</b>",
        body_text="OTP {{otp}}",
        variables={"otp": "integer"},
        template_path="/templates/otp.html"
    )

    payload = {
        "template_code": "user_auth_otp",
        "name": "verification mail",
        "subject": "Your code",
        "sender_email": "tamim@gozayaan.com",
        "priority": "LOW",
        "is_active": True,
        "max_retry": 5,
        "region": "BD",
        "service": "GOZAYAAN",
        "content": content.id,
        "to_group": [],
        "cc_group": [],
        "bcc_group": [],
        "to_contacts": [],
        "cc_contacts": [],
        "bcc_contacts": [],
        "attachments": []
    }

    url = reverse("email-template-list")

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_email_template_patch(api_client):

    content = Content.objects.create(
        name="OTP Template",
        body_html="<b>{{otp}}</b>",
        body_text="OTP {{otp}}",
        variables={"otp": "integer"},
        template_path="/templates/otp.html"
    )

    template = EmailTemplate.objects.create(
        template_code="user_auth_otp",
        name="Old Mail",
        subject="Old Subject",
        sender_email="tamim@gozayaan.com",
        priority="LOW",
        is_active=True,
        max_retry=5,
        region="BD",
        service="GOZAYAAN",
        content=content
    )

    url = reverse("email-template-detail", args=[template.id])

    response = api_client.patch(
        url,
        {"name": "Updated Mail"},
        format="json"
    )

    assert response.status_code == 200
