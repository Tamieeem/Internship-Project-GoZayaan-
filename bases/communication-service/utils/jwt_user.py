from django.db import models

from utils.choices import Regions, ServiceTypes


class JWTUser(models.Model):
    """User object built from JWT payload. No DB table."""
    username = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    user_groups = models.JSONField(default=list)
    region = models.CharField(
        max_length=2,  choices=Regions.choices, null=True, blank=True)
    service = models.CharField(
        max_length=10, choices=ServiceTypes.choices, null=True, blank=True)

    class Meta:
        managed = False
        app_label = 'templates'

    @classmethod
    def from_payload(cls, payload: dict) -> 'JWTUser':
        """Build a JWTUser instance from JWT payload. No DB hit."""
        user = cls()
        user.username = payload.get('username', '')
        user.is_admin = payload.get('is_admin', False)
        user.user_groups = payload.get('groups',   [])
        user.region = payload.get('region')
        user.service = payload.get('service')
        return user

    @property
    def is_authenticated(self):
        """Indicates the user is authenticated (always True for JWTUser)."""
        return True

    @property
    def is_staff(self):
        """Indicates the user is staff (same as is_admin for JWTUser)."""
        return self.is_admin

    def __str__(self):
        """
        Return the username as a string representation of the user.
        """
        return self.username
