from rest_framework import serializers

from apps.templates.models import EmailTemplate, MessageTemplate
from .models import Events, Provider, Content, Logs
from utils.choices import DeliveryType, MessageTypes
from utils.choices import (
    DeliveryType,
    TemplateType,
)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
            "template_code",
            "template_type",
            "variables",
            "to_contact",
            "region",
            "service",
        ]
    def validate(self, data):
        template_type = data.get("template_type")
        template_code = data.get("template_code")
        variables = data.get("variables") or {}
        contacts = data.get("to_contact") or []

        # Step 1: Resolve template — fetched once here, passed forward
        template, delivery_type = self._resolve_template(
            template_type, template_code)

        # Step 2: Resolve provider based on delivery type
        provider = self._resolve_provider(data, delivery_type)

        # Step 3: Validate that at least one recipient exists
        self._validate_recipients(template, template_type, contacts)

        # Step 4: Validate all required variables are provided
        self._validate_variables(template, variables)

        # Attach resolved objects so views/services don't re-query
        data["provider"] = provider
        data["priority"] = template.priority
        # passed via context, not saved to DB
        # data["resolved_template"] = template
        data["to_contact"] = self._deduplicate_contacts(contacts)

        return data

    def _resolve_template(self, template_type, template_code):
        if not template_code:
            raise serializers.ValidationError(
                {"template_code": "This field is required."}
            )

        if template_type == TemplateType.EMAIL:
            template = (
                EmailTemplate.objects.select_related("content")
                .prefetch_related(
                    "to_contacts",
                    "to_group__contacts",
                    "cc_contacts",
                    "cc_group__contacts",
                    "bcc_contacts",
                    "bcc_group__contacts",
                    "attachments",
                )
                .filter(template_code=template_code, is_active=True)
                .first()
            )
            if not template:
                raise serializers.ValidationError(
                    {"template_code": f"Active template '{template_code}' not found."}
                )
            delivery_type = DeliveryType.EMAIL

        elif template_type == TemplateType.MESSAGE:
            template = (
                MessageTemplate.objects.select_related("content")
                .prefetch_related(
                    "contacts",
                    "groups__contacts",
                )
                .filter(template_code=template_code, is_active=True)
                .first()
            )
            if not template:
                raise serializers.ValidationError(
                    {"template_code": f"Active template '{template_code}' not found."}
                )
            delivery_type = template.message_type if template else None

        else:
            raise serializers.ValidationError(
                {"template_type": "Unsupported template type."}
            )

        # if not template:
        #     raise serializers.ValidationError(
        #         {"template_code": f"Active template '{template_code}' not found."}
        #     )

        return template, delivery_type

    def _resolve_provider(self, data, delivery_type):
        provider = Provider.objects.filter(
            region=data.get("region"),
            service=data.get("service"),
            delivery_type=delivery_type,
            is_active=True,
        ).first()

        if not provider:
            raise serializers.ValidationError(
                {
                    "provider": (
                        "No active provider found for the given "
                        "region, service and delivery type."
                    )
                }
            )

        return provider

    def _validate_recipients(self, template, template_type, request_contacts):
        has_template_contacts = False

        if template_type == TemplateType.EMAIL:
            has_template_contacts = (
                template.to_contacts.exists()
                or template.to_group.filter(contacts__isnull=False).exists()
            )

        elif template_type == TemplateType.MESSAGE:
            has_template_contacts = (
                template.contacts.exists()
                or template.groups.filter(contacts__isnull=False).exists()
            )

        if not (has_template_contacts or request_contacts):
            raise serializers.ValidationError(
                {
                    "to_contact": (
                        "At least one recipient must be provided "
                        "via template or request."
                    )
                }
            )

    def _validate_variables(self, template, provided):
        required = {}

        if template.content and template.content.variables:
            required.update(template.content.variables)

        if hasattr(template, "attachments"):
            for attachment in template.attachments.all():
                if attachment.variables:
                    required.update(attachment.variables)

        missing = set(required) - set(provided)

        if missing:
            raise serializers.ValidationError(
                {
                    "variables": {
                        "missing": sorted(missing),
                        "required": sorted(required.keys()),
                    }
                }
            )

    def _deduplicate_contacts(self, contacts):
        # Preserves order, removes null & duplicates
        return list(dict.fromkeys(filter(None, contacts)))


class ContentBodySerializer(serializers.ModelSerializer):

    class Meta:
        model = Content
        fields = '__all__'


class ProviderReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'


class ProviderWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'

    def validate_credentials(self, value):
        """
        Ensures the JSON input is not empty and follows a
        basic structure before saving to the database.
        """
        if not value:
            raise serializers.ValidationError(
                "Credentials JSON cannot be empty.")
        return value


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
            'id',
            'template_code',
            'template_type',
            'status',
            'retry_count',
            'created_at',
            'to_contact',
            'variables',
            'region',
            'service',
            'delivered_at',
        ]

class EventRetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = [
            'id',
            'status',
            'retry_count',
        ]
        # read_only_fields = ['id', 'status', 'retry_count']


class LogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = [
            'id',
            'status',
            'request_by',
            'api_path',
            'region',
            'service',
            'created_at',
            'error',
        ]
