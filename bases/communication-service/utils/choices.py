from django.db import models


class ServiceTypes(models.TextChoices):
    GOZAYAAN = 'GOZAYAAN', 'Gozayaan'
    HOMETOWN = 'HOMETOWN', 'Hometown'


class Regions(models.TextChoices):
    BANGLADESH = "BD", "Bangladesh"
    PAKISTAN = "PK", "Pakistan"
    SINGAPORE = "SG", "Singapore"
    MALAYSIA = "MY", "Malaysia"


class Status(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_QUEUE = "IN_QUEUE", "In Queue"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"


class TemplateType(models.TextChoices):
    MESSAGE = "MESSAGE", "Message"
    EMAIL = "EMAIL", "Email"


class Priority(models.TextChoices):
    LOW = "LOW", "Low"
    HIGH = "HIGH", "High"
    INSTANT = "INSTANT", "Instant"


class MessageTypes(models.TextChoices):
    SMS = "SMS", "SMS"
    NOTIFICATION = "NOTIFICATION", "Notification"


class DeliveryType(models.TextChoices):
    EMAIL = "EMAIL", "Email"
    SMS = "SMS", "SMS"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    NOTIFICATION = "NOTIFICATION", "Notification"


class ProviderTypes(models.TextChoices):
    GOOGLE_SMTP = "google_smtp", "Google SMTP"
    SENDGRID = "sendgrid", "SendGrid"
    AWS_SES = "aws_ses", "AWS SES"
    MAILGUN = "mailgun", "Mailgun"
    RESEND = "resend", "Resend"
