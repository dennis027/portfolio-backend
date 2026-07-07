from rest_framework import serializers

from apps.portfolio.models import (
    Project, Skill, Experience, Education, Certification,
    Testimonial, NewsletterSubscriber, BlogPost, ResumeDownload,
)


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.ListField(
        read_only=True,
        child=serializers.CharField()
    )

    class Meta:
        model = Project
        fields = [
            "id", "title", "slug", "description", "tech_stack", "tech_list",
            "repo_url", "live_url", "cover_image", "is_featured", "views",
            "order", "created_at", "updated_at",
        ]
        read_only_fields = ["views", "created_at", "updated_at"]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "category", "proficiency", "icon", "order"]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id", "company", "role", "location", "start_date", "end_date",
            "is_current", "description", "order",
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            "id", "institution", "degree", "field_of_study",
            "start_date", "end_date", "description", "order",
        ]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "id", "title", "issuing_organization", "issue_date", "expiry_date",
            "credential_id", "credential_url", "order",
        ]


class TestimonialPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "author_name", "author_role", "author_company", "author_photo", "message", "created_at"]


class TestimonialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["author_name", "author_role", "author_company", "author_photo", "message"]

    def create(self, validated_data):
        # New testimonials require manual admin approval before going public.
        validated_data["is_approved"] = False
        return Testimonial.objects.create(**validated_data)


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["id", "email", "subscribed_at"]
        read_only_fields = ["id", "subscribed_at"]


class BlogPostListSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(
        read_only=True,
        child=serializers.CharField()
    )

    class Meta:
        model = BlogPost
        fields = [ "id", "title", "slug",  "summary",  "cover_image",  "tag_list", "views",   "published_at",
        ]

class BlogPostDetailSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(
        read_only=True,
        child=serializers.CharField()
    )

    class Meta:
        model = BlogPost
        fields = [   "id",   "title",   "slug",  "summary",  "content",  "cover_image",  "tag_list",    "is_published",  "views",   "published_at",    "created_at",   "updated_at",
        ]
        read_only_fields = ["views", "created_at", "updated_at"]

class ResumeDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeDownload
        fields = ["id", "downloaded_at"]
