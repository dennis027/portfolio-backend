from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from drf_spectacular.utils import extend_schema

from apps.contact.models import Contact
from apps.contact.serializers import ContactSerializer, ContactCreateSerializer,ContactResponseSerializer
from apps.contact.throttles import ContactFormThrottle
from apps.contact.recaptcha import verify_recaptcha
from apps.contact.notifications import notify_new_contact
from utils.client_info import get_client_ip, get_user_agent_string
from utils.responses import success_response, error_response


class ContactViewSet(viewsets.ModelViewSet):
    """
    create  -> POST   /api/contact/           (public, throttled, spam-checked)
    list    -> GET    /api/contact/           (admin only)
    retrieve-> GET    /api/contact/{id}/      (admin only)
    partial_update -> PATCH /api/contact/{id}/  (admin only — e.g. mark as read)
    destroy -> DELETE /api/contact/{id}/      (admin only)
    """

    queryset = Contact.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_read", "country"]
    search_fields = ["full_name", "email", "subject", "message"]
    ordering_fields = ["created_at", "is_read"]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return ContactCreateSerializer
        return ContactSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def get_throttles(self):
        if self.action == "create":
            return [ContactFormThrottle()]
        return super().get_throttles()

    @extend_schema(summary="Submit a contact form message (public)")
    def create(self, request, *args, **kwargs):
        if not verify_recaptcha(request.data.get("recaptcha_token", "")):
            return error_response("reCAPTCHA verification failed.", status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact = serializer.save(
            ip_address=get_client_ip(request),
            user_agent=get_user_agent_string(request)[:500],
        )

        notify_new_contact(contact)

        return success_response(
            "Contact message sent successfully.",
            ContactResponseSerializer(contact).data,
            status=201,
        )

    @extend_schema(summary="List contact messages (admin only)")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Contact messages retrieved.", response.data)

    @extend_schema(summary="Retrieve a single contact message (admin only)")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return success_response("Contact message retrieved.", self.get_serializer(instance).data)

    @extend_schema(summary="Mark a contact message as read/unread (admin only)")
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response("Contact message updated.", serializer.data)

    @extend_schema(summary="Delete a contact message (admin only)")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response("Contact message deleted.", None)
