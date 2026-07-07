from django.urls import path

from apps.analytics.views import AnalyticsDashboardView, RecentVisitorsView

urlpatterns = [
    path("dashboard/", AnalyticsDashboardView.as_view(), name="analytics-dashboard"),
    path("recent/", RecentVisitorsView.as_view(), name="analytics-recent"),
]
