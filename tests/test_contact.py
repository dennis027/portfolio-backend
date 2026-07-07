from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.contact.models import Contact


class ContactApiTests(APITestCase):
    def setUp(self):
        self.list_url = reverse("contact-list")
        self.admin = get_user_model().objects.create_superuser(
            username="admin", email="admin@example.com", password="StrongPass123"
        )

    def test_public_can_submit_contact_form(self):
        payload = {
            "full_name": "Jane Visitor",
            "email": "jane@example.com",
            "subject": "Let's work together",
            "message": "I saw your portfolio and would like to discuss a project.",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(Contact.objects.count(), 1)

    def test_honeypot_blocks_bots(self):
        payload = {
            "full_name": "Bot",
            "email": "bot@example.com",
            "subject": "spam",
            "message": "buy cheap watches now please",
            "website": "http://spam.example.com",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Contact.objects.count(), 0)

    def test_anonymous_cannot_list_contacts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_can_mark_as_read(self):
        contact = Contact.objects.create(
            full_name="Jane", email="jane@example.com",
            subject="Hi", message="Hello there, this is a test message.",
        )
        self.client.force_authenticate(self.admin)
        url = reverse("contact-detail", args=[contact.id])
        response = self.client.patch(url, {"is_read": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contact.refresh_from_db()
        self.assertTrue(contact.is_read)
