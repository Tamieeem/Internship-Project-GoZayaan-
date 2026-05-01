from django.db import models
from utils.choices import ServiceTypes, Regions, Priority, MessageTypes


class EmailTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    template_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=25)
    subject = models.CharField(max_length=255)
    sender_email = models.EmailField(verbose_name="From")

    content = models.ForeignKey(
        'events.Content', on_delete=models.CASCADE, related_name='email_templates')
    to_group = models.ManyToManyField(
        'audience.Group', blank=True, related_name='email_to_groups')
    cc_group = models.ManyToManyField(
        'audience.Group', blank=True, related_name='email_cc_groups')
    bcc_group = models.ManyToManyField(
        'audience.Group', blank=True, related_name='email_bcc_groups')

    to_contacts = models.ManyToManyField(
        'audience.Contact', blank=True, related_name='email_to_contacts')

    cc_contacts = models.ManyToManyField(
        'audience.Contact', blank=True, related_name='email_cc_templates')
    bcc_contacts = models.ManyToManyField(
        'audience.Contact', blank=True, related_name='email_bcc_templates')

    attachments = models.ManyToManyField(
        'events.Content', blank=True, related_name='email_attachments')
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.LOW)
    is_active = models.BooleanField(default=True)
    max_retry = models.IntegerField(default=5)
    region = models.CharField(
        max_length=2, choices=Regions.choices, null=True, blank=True)
    service = models.CharField(
        max_length=20, choices=ServiceTypes.choices, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MessageTemplate(models.Model):
    id = models.BigAutoField(primary_key=True)
    template_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    message_type = models.CharField(
        max_length=20, choices=MessageTypes.choices, default=MessageTypes.SMS)

    content = models.ForeignKey(
        'events.Content', on_delete=models.CASCADE, related_name='message_templates')

    groups = models.ManyToManyField(
        'audience.Group', blank=True, related_name='message_groups')
    contacts = models.ManyToManyField(
        'audience.Contact', blank=True, related_name='message_contacts')

    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.LOW)

    is_active = models.BooleanField(default=True)
    max_retry = models.IntegerField(default=5)
    region = models.CharField(
        max_length=2, choices=Regions.choices, null=True, blank=True)
    service = models.CharField(
        max_length=20, choices=ServiceTypes.choices, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
