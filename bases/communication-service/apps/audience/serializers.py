from rest_framework import serializers
from .models import Group, Contact


class GroupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ('created_at', 'updated_at')


class ContactReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ContactWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('created_at', 'updated_at')
