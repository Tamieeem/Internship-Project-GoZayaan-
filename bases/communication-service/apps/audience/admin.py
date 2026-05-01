from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .models import Contact, Group


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'full_name', 'email', 'phone',
#         'region', 'service', 'group_count', 'created_at',
#     )
#     search_fields = ('first_name', 'last_name', 'email', 'phone')
#     list_filter = ('region', 'service', 'created_at')
#     readonly_fields = ('created_at', 'updated_at')
#     ordering = ('-created_at',)
#     list_per_page = 50
#     list_select_related = True

#     @admin.display(description='Name', ordering='first_name')
#     def full_name(self, obj):  # show full name
#         name = f"{obj.first_name or ''} {obj.last_name or ''}".strip()
#         return name if name else format_html('<span style="color:#aaa;">—</span>')

#     @admin.display(description='Groups', ordering='group_count')
#     def group_count(self, obj):  # show group count in admin
#         return obj.group_count

#     def get_queryset(self, request):
#         return (
#             super().get_queryset(request)
#             # group count
#             .annotate(group_count=Count('contact_groups', distinct=True))
#         )


# @admin.register(Group)
# class GroupAdmin(admin.ModelAdmin):
#     list_display = (
#         'id', 'name',
#         'contact_count', 'region', 'service', 'created_at',
#     )
#     search_fields = ('name', 'description')
#     list_filter = ('region', 'service', 'created_at')
#     autocomplete_fields = ('contacts',)
#     readonly_fields = ('created_at', 'updated_at')
#     ordering = ('-created_at',)
#     list_per_page = 50

#     @admin.display(description='Contacts', ordering='contact_count')
#     def contact_count(self, obj):
#         return obj.contact_count

#     def get_queryset(self, request):
#         return (
#             super().get_queryset(request)
#             .annotate(contact_count=Count('contacts', distinct=True))
#         )
admin.site.register(Contact)
admin.site.register(Group)

