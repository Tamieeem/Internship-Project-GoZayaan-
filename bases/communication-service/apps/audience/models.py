from django.db import models
import uuid
from utils.choices import ServiceTypes, Regions


class Contact(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(
        max_length=2, choices=Regions.choices, null=True, blank=True)
    service = models.CharField(
        max_length=20, choices=ServiceTypes.choices, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    contacts = models.ManyToManyField(
        Contact, related_name='contact_groups', blank=True)

    region = models.CharField(
        max_length=2, choices=Regions.choices, null=True, blank=True)
    service = models.CharField(
        max_length=20, choices=ServiceTypes.choices, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
