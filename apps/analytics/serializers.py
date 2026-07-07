from rest_framework import serializers

from apps.analytics.models import Visitor, PageVisit


class PageVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageVisit
        fields = ["id", "path", "visited_at"]


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = [
            "id", "ip_address", "browser", "operating_system", "device_type",
            "country", "city", "referrer", "landing_page", "session_id",
            "visit_time", "last_active", "visit_count",
        ]


class DashboardSerializer(serializers.Serializer):
    total_visitors = serializers.IntegerField()
    unique_visitors = serializers.IntegerField()
    returning_visitors = serializers.IntegerField()
    visits_today = serializers.IntegerField()
    visits_this_week = serializers.IntegerField()
    visits_this_month = serializers.IntegerField()
    top_countries = serializers.ListField()
    top_browsers = serializers.ListField()
    top_devices = serializers.ListField()
    most_visited_pages = serializers.ListField()
