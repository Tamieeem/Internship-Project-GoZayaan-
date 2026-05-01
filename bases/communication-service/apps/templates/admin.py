from django.contrib import admin
from django.db.models import Count
from .models import EmailTemplate, MessageTemplate


from django.utils.safestring import mark_safe


class TemplateAdminMixin:
    actions = ['activate_templates', 'deactivate_templates']

    @admin.display(description='Status')
    def status_badge(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color:#2e7d32;font-weight:600;">● Active</span>')
        return mark_safe('<span style="color:#c62828;">● Inactive</span>')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(TemplateAdminMixin, admin.ModelAdmin):
    list_display = (
        'template_code', 'name', 'subject', 'sender_email',
        'priority', 'region', 'service',
        'max_retry', 'status_badge', 'updated_at',
    )
    search_fields = ('template_code', 'name', 'subject', 'sender_email')
    list_filter = ('is_active', 'priority', 'region', 'service')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    list_per_page = 50
    list_select_related = ('content',)

    # autocomplete_fields = (
    #     'to_group', 'to_contacts', 'cc_group', 'bcc_group',
    #     'cc_contacts', 'bcc_contacts',
    #     'attachments',
    # )


@admin.register(MessageTemplate)
class MessageTemplateAdmin(TemplateAdminMixin, admin.ModelAdmin):
    list_display = (
        'template_code', 'name', 'title', 'message_type',
        'priority', 'region', 'service',
        'max_retry', 'status_badge', 'updated_at',
    )
    search_fields = ('template_code', 'name', 'title')
    list_filter = ('message_type', 'is_active',
                'priority', 'region', 'service')
    # autocomplete_fields = ('groups', 'contacts')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    list_per_page = 50
    list_select_related = ('content',)
