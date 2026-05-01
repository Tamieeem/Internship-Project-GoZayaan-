import pytest
from django.urls import reverse
from apps.templates.models import MessageTemplate
from apps.events.models import Content
from apps.audience.models import Group, Contact


@pytest.mark.django_db
def test_message_template_list(api_client):

    content = Content.objects.create(
        name="SMS Template",
        body_text="OTP {{otp}}",
        template_path="/templates/sms.html"
    )

    template = MessageTemplate.objects.create(
        template_code="auth",
        name="message",
        title="no title",
        message_type="SMS",
        priority="HIGH",
        is_active=True,
        max_retry=5,
        region="SG",
        service="HOMETOWN",
        content=content
    )

    url = reverse("message-template-list")
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_message_template_create(api_client):

    content = Content.objects.create(
        name="SMS Template",
        body_text="OTP {{otp}}",
        template_path="/templates/sms.html"
    )

    group = Group.objects.create(name="tech-group")
    contact = Contact.objects.create(first_name='django', last_name='test', phone="123456789")

    payload = {
        "template_code": "auth",
        "name": "message",
        "title": "no title",
        "message_type": "SMS",
        "priority": "HIGH",
        "is_active": True,
        "max_retry": 5,
        "region": "SG",
        "service": "HOMETOWN",
        "content": content.id,
        "groups": [group.id],
        "contacts": [contact.id]
    }

    url = reverse("message-template-list")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_message_template_patch(api_client):

    content = Content.objects.create(
        name="SMS Template",
        body_text="OTP {{otp}}",
        template_path="/templates/sms.html"
    )
    template = MessageTemplate.objects.create(
        template_code="auth",
        name="Old Message",
        title="old title",
        message_type="SMS",
        priority="HIGH",
        is_active=True,
        max_retry=5,
        region="SG",
        service="HOMETOWN",
        content=content
    )

    url = reverse("message-template-detail", args=[template.id])

    response = api_client.patch(
        url,
        {"name": "Updated Message"},
        format="json"
    )

    assert response.status_code == 200
