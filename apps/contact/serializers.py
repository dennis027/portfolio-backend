from rest_framework import serializers

from apps.contact.models import Contact


class ContactCreateSerializer(serializers.ModelSerializer):
    """Used for POST /api/contact/ — the public-facing submission form."""

    # Honeypot field: real visitors never fill this in; bots that
    # auto-fill every input will, letting us silently drop the spam.
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)
    recaptcha_token = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Contact
        fields = ["full_name", "email", "subject", "message", "website", "recaptcha_token"]

    def validate_full_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Full name is too short.")
        return value.strip()

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters.")
        return value.strip()

    def validate_website(self, value):
        if value:
            raise serializers.ValidationError("Spam detected.")
        return value

    def create(self, validated_data):
        validated_data.pop("website", None)
        validated_data.pop("recaptcha_token", None)
        return Contact.objects.create(**validated_data)
    
class ContactResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "full_name",
            "email",
            "subject",
            "message",
        ]


class ContactSerializer(serializers.ModelSerializer):
    """Used for admin-facing list/detail/patch/delete."""

    class Meta:
        model = Contact
        fields = [
            "id", "full_name", "email", "subject", "message",
            "ip_address", "user_agent", "country", "is_read",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "full_name", "email", "subject", "message",
            "ip_address", "user_agent", "country", "created_at", "updated_at",
        ]
