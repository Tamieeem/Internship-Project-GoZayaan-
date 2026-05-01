from .base import BaseEmailProvider
from .registry_provider import register_provider
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging

# logger = logging.getLogger(name)


@register_provider("google_smtp")
class SMTPProvider(BaseEmailProvider):

    ''' Decorator to register provider classes into a central registry.
    Enables dynamic lookup (Factory Pattern) so the system can switch
    between providers (e.g., SMTP, SendGrid) using database identifiers.
    interface definition for all email service implementations.
    Enforces a consistent 'contract' across different providers,
    ensuring they all use the same method signatures for swappability.
    '''

    def __init__(provider):
        super().__init__(provider)

    def send_email(
        self,
        to_contacts,
        subject,
        message_body,
        cc_contacts=None,
        bcc_contacts=None,
        attachments=None,
        from_email=None
    ):

        cc_contacts = cc_contacts or []
        bcc_contacts = bcc_contacts or []
        attachments = attachments or []

        if not message_body:
            raise ValueError("Email body cannot be empty")
        plain_text = strip_tags(message_body)

        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text,
            to=to_contacts,
            cc=cc_contacts,
            bcc=bcc_contacts,
            from_email=from_email
        )

        email.attach_alternative(message_body, "text/html")

        for att in attachments:
            filename = att.get("filename")
            content = att.get("content")

            if not filename or content is None:
                continue
            # using the is_binary flag to determine the mime type from the service layer.
            # in case the service layer does not have this flag we use tex/plain so the background job will not fail.
            mime_type = "application/pdf" if att.get(
                "is_binary") else "text/plain"
            email.attach(filename, content, mime_type)

        email.send()
