from .models import Contact, Group
from .serializers import ContactReadSerializer, GroupReadSerializer, ContactWriteSerializer, GroupWriteSerializer
from utils.viewsets import BaseModelViewSet
from django.utils.decorators import method_decorator
from utils.decorators import custom_permissions


@method_decorator(custom_permissions(is_admin=True, groups=['marketing']), name='initial')
class ContactViewSet(BaseModelViewSet):
    queryset = Contact.objects.all().order_by('-created_at')
    filterset_fields = ['region', 'service']
    search_fields = ['email', 'phone']

    lookup_field = 'id'
    read_serializer_class = ContactReadSerializer
    write_serializer_class = ContactWriteSerializer


@method_decorator(custom_permissions(is_admin=True, groups=['admin']), name='initial')
class GroupViewSet(BaseModelViewSet):
    queryset = Group.objects.prefetch_related(
        'contacts').order_by('-created_at')
    filterset_fields = [
        'region', 'service']
    search_fields = ['id', 'name']
    lookup_field = 'id'
    read_serializer_class = GroupReadSerializer
    write_serializer_class = GroupWriteSerializer
