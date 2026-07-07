from django.contrib import admin, messages
from django.utils.html import format_html

from apps.contact.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email", "subject", "read_badge", "country", "created_at"]
    list_filter = ["is_read", "country", "created_at"]
    search_fields = ["full_name", "email", "subject", "message"]
    date_hierarchy = "created_at"
    readonly_fields = ["ip_address", "user_agent", "created_at", "updated_at"]
    actions = ["mark_as_read", "mark_as_unread"]

    @admin.display(description="Status")
    def read_badge(self, obj: Contact):
        color = "#16a34a" if obj.is_read else "#dc2626"
        label = "Read" if obj.is_read else "Unread"
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:10px;font-size:11px;">{}</span>',
            color, label,
        )

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marked as read.", messages.SUCCESS)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} message(s) marked as unread.", messages.SUCCESS)
