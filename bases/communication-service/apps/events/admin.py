from django.contrib import admin
from .models import Provider, Events, Content, Logs
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    # Performance: list_select_related reduces DB queries for the Foreign Key 'provider'
    list_select_related = ('provider',)

    list_display = ('id', 'status', 'provider',
                    'template_type', 'retry_count', 'created_at')
    list_filter = ('status', 'template_type', 'region', 'service')
    # Search by Event ID or the related Provider's name
    search_fields = ('id', 'provider__name', 'to_contact')
    # Events are history; they should be 100% read-only in the admin
    readonly_fields = ('created_at', 'updated_at', 'delivered_at')

    # Allow filtering by date
    date_hierarchy = 'created_at'


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'template_path')
    search_fields = ('template_path', 'body_text')
    list_per_page = 10


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'delivery_type', 'region', 'service', 'is_active')
    list_filter = ('delivery_type', 'region', 'service', 'is_active')
    search_fields = ('name', 'delivery_type', 'region', 'service')
    readonly_fields = ('id',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'request_by', 'api_path', 'created_at')
    list_filter = ('status', 'region', 'service', 'created_at')
    search_fields = ('request_by', 'api_path', 'error')

    # Logs are history; they should be 100% read-only in the admin
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False

    # This allows you to still view the log detail, but not edit it
    readonly_fields = [field.name for field in Logs._meta.fields]
