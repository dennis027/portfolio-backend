from django.contrib import admin

from apps.analytics.models import Visitor, PageVisit


class PageVisitInline(admin.TabularInline):
    model = PageVisit
    extra = 0
    readonly_fields = ["path", "visited_at"]
    can_delete = False


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ["session_id", "ip_address", "browser", "operating_system", "device_type", "country", "visit_count", "last_active"]
    list_filter = ["device_type", "browser", "country", "operating_system"]
    search_fields = ["ip_address", "session_id", "country", "city"]
    date_hierarchy = "visit_time"
    inlines = [PageVisitInline]
    readonly_fields = ["session_id", "visit_time", "last_active"]

    def changelist_view(self, request, extra_context=None):
        from apps.analytics.services import get_dashboard_stats
        extra_context = extra_context or {}
        extra_context["dashboard_stats"] = get_dashboard_stats()
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ["path", "visitor", "visited_at"]
    list_filter = ["visited_at"]
    search_fields = ["path"]
