import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from utils.choices import Status, ServiceTypes, Regions, TemplateType, DeliveryType, ProviderTypes


class Provider(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    delivery_type = models.CharField(
        max_length=15, choices=DeliveryType.choices, default=DeliveryType.EMAIL)
    credentials = models.JSONField(
        blank=True, null=True)  # store API keys, tokens
    code = models.CharField(
        max_length=50,
        choices=ProviderTypes.choices,
        blank=True,
        null=True
    )

    region = models.CharField(
        max_length=2,
        choices=Regions.choices,
        default=Regions.BANGLADESH

    )
    service = models.CharField(
        max_length=10,
        choices=ServiceTypes.choices,
        default=ServiceTypes.GOZAYAAN
    )

    def __str__(self):
        return f"{self.name} ({self.region})"


class Events(models.Model):
    id = models.BigAutoField(primary_key=True)
    provider = models.ForeignKey(
        Provider, on_delete=models.SET_NULL, null=True, blank=True, related_name="events")

    variables = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    # sms/email
    template_type = models.CharField(
        max_length=10,
        choices=TemplateType.choices,
        null=True,
        blank=True
    )
    retry_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    template_code = models.CharField(null=True, blank=True, max_length=10)
    to_contact = ArrayField(models.CharField(max_length=255, blank=True))
    region = models.CharField(
        max_length=2,
        choices=Regions.choices,
        default=Regions.BANGLADESH

    )
    service = models.CharField(
        max_length=10,
        choices=ServiceTypes.choices,
        default=ServiceTypes.GOZAYAAN
    )


    def __str__(self):
        return f"Event {self.id} - {self.status}"


class Content(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    body_html = models.TextField(null=True, blank=True)
    body_text = models.TextField(null=True, blank=True)
    variables = models.JSONField(default=dict, blank=True)
    template_path = models.CharField(max_length=255)

    def __str__(self):
        return f"Content {self.id}"


class Logs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    '''status: http status
    request by: who made the request(admin/or other service)'''

    status = models.CharField(max_length=10)

    error = models.TextField(default=False)

    region = models.CharField(
        max_length=2,
        choices=Regions.choices,
        default=Regions.BANGLADESH
    )
    service = models.CharField(
        max_length=10,
        choices=ServiceTypes.choices,
        default=ServiceTypes.GOZAYAAN
    )
    request_by = models.CharField(max_length=255)
    api_path = models.URLField(max_length=255)
    request_body = models.JSONField(default=dict, blank=True)
    response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.id} - {self.status}"
