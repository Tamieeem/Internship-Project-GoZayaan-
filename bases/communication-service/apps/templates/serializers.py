from rest_framework import serializers
from .models import EmailTemplate, MessageTemplate


class EmailTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'


class EmailTemplateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        exclude = ('created_at', 'updated_at')


class MessageTemplateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'


class MessageTemplateWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        exclude = ('created_at', 'updated_at')
