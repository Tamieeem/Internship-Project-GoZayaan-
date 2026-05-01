from .models import EmailTemplate, MessageTemplate
from .serializers import EmailTemplateReadSerializer, EmailTemplateWriteSerializer, MessageTemplateWriteSerializer, MessageTemplateReadSerializer
from utils.viewsets import BaseModelViewSet
from django.utils.decorators import method_decorator
from utils.decorators import custom_permissions


@method_decorator(custom_permissions(is_admin=True, groups=['marketing']), name='initial')
class EmailTemplateViewSet(BaseModelViewSet):
    queryset = EmailTemplate.objects.prefetch_related(
        'to_group', 'cc_group', 'bcc_group',
        'to_contacts', 'cc_contacts', 'bcc_contacts',
        'attachments'
    ).select_related('content').order_by('-created_at')
    filterset_fields = ['is_active', 'priority', 'region', 'service']
    search_fields = ['id', 'sender_email', 'name', 'template_code']
    lookup_field = 'id'
    read_serializer_class = EmailTemplateReadSerializer
    write_serializer_class = EmailTemplateWriteSerializer


@method_decorator(custom_permissions(is_admin=True, groups=['marketing']), name='initial')
class MessageTemplateViewSet(BaseModelViewSet):
    queryset = MessageTemplate.objects.prefetch_related(
        'groups', 'contacts'
    ).select_related('content').order_by('-created_at')
    filterset_fields = ['is_active', 'priority',
                        'region', 'service', 'message_type']
    search_fields = ['id', 'name', 'template_code', 'title']
    lookup_field = 'id'
    read_serializer_class = MessageTemplateReadSerializer
    write_serializer_class = MessageTemplateWriteSerializer
