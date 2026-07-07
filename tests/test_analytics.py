from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.analytics.models import Visitor


class AnalyticsApiTests(APITestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="StrongPass123"
        )
        Visitor.objects.create(session_id="s1", browser="Chrome", country="Kenya", device_type="Desktop")
        Visitor.objects.create(session_id="s2", browser="Firefox", country="Kenya", device_type="Mobile", visit_count=2)

    def test_dashboard_requires_admin(self):
        url = reverse("analytics-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_returns_stats(self):
        self.client.force_authenticate(self.admin)
        url = reverse("analytics-dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]
        self.assertEqual(data["total_visitors"], 2)
        self.assertEqual(data["returning_visitors"], 1)
