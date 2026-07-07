from django.db import models


class Visitor(models.Model):
    """One row per unique session. `visit_count` increments on each
    subsequent request from the same session, so returning visitors are
    trivially: Visitor.objects.filter(visit_count__gt=1)."""

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    referrer = models.CharField(max_length=500, blank=True)
    landing_page = models.CharField(max_length=500, blank=True)
    session_id = models.CharField(max_length=64, unique=True)

    visit_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    visit_count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-last_active"]
        indexes = [
            models.Index(fields=["country"]),
            models.Index(fields=["browser"]),
            models.Index(fields=["visit_time"]),
        ]

    def __str__(self) -> str:
        return f"{self.session_id} ({self.country or 'Unknown'})"

    @staticmethod
    def pages_visited_model():
        return PageVisit


class PageVisit(models.Model):
    """Every individual page/endpoint hit by a visitor — powers
    'Most Visited Pages' on the dashboard."""

    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name="page_visits")
    path = models.CharField(max_length=500)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-visited_at"]
        indexes = [models.Index(fields=["path"])]

    def __str__(self) -> str:
        return self.path
