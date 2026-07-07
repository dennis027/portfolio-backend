"""
Aggregation queries for the analytics dashboard. Kept out of views.py so
the same logic can be reused by the combined /api/dashboard/ endpoint.
"""
from django.db.models import Count
from django.utils import timezone

from apps.analytics.models import Visitor, PageVisit


def get_dashboard_stats() -> dict:
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timezone.timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)

    total_visitors = Visitor.objects.count()
    unique_visitors = total_visitors  # one row per unique session by design
    returning_visitors = Visitor.objects.filter(visit_count__gt=1).count()

    visits_today = Visitor.objects.filter(last_active__gte=today_start).count()
    visits_this_week = Visitor.objects.filter(last_active__gte=week_start).count()
    visits_this_month = Visitor.objects.filter(last_active__gte=month_start).count()

    top_countries = list(
        Visitor.objects.exclude(country__isnull=True).exclude(country="")
        .values("country").annotate(count=Count("id")).order_by("-count")[:5]
    )
    top_browsers = list(
        Visitor.objects.exclude(browser="").values("browser")
        .annotate(count=Count("id")).order_by("-count")[:5]
    )
    top_devices = list(
        Visitor.objects.exclude(device_type="").values("device_type")
        .annotate(count=Count("id")).order_by("-count")[:5]
    )
    most_visited_pages = list(
        PageVisit.objects.values("path").annotate(count=Count("id")).order_by("-count")[:10]
    )

    return {
        "total_visitors": total_visitors,
        "unique_visitors": unique_visitors,
        "returning_visitors": returning_visitors,
        "visits_today": visits_today,
        "visits_this_week": visits_this_week,
        "visits_this_month": visits_this_month,
        "top_countries": top_countries,
        "top_browsers": top_browsers,
        "top_devices": top_devices,
        "most_visited_pages": most_visited_pages,
    }
