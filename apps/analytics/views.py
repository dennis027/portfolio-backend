from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema

from apps.analytics.models import Visitor
from apps.analytics.serializers import VisitorSerializer, DashboardSerializer
from apps.analytics.services import get_dashboard_stats
from utils.responses import success_response


class AnalyticsDashboardView(APIView):
    """GET /api/analytics/dashboard/ — aggregated visitor stats (admin only)."""
    permission_classes = [IsAdminUser]

    @extend_schema(summary="Portfolio visitor analytics dashboard", responses=DashboardSerializer)
    def get(self, request):
        return success_response("Analytics dashboard data.", get_dashboard_stats())


class RecentVisitorsView(ListAPIView):
    """GET /api/analytics/recent/ — most recently active visitors (admin only)."""
    queryset = Visitor.objects.all()[:50]
    serializer_class = VisitorSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country", "device_type", "browser"]
    ordering_fields = ["last_active", "visit_count"]

    @extend_schema(summary="Recent site visitors")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Recent visitors retrieved.", response.data)
