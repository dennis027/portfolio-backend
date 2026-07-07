from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.analytics.services import get_dashboard_stats
from apps.contact.models import Contact
from apps.contact.serializers import ContactSerializer
from apps.analytics.models import Visitor
from apps.analytics.serializers import VisitorSerializer
from apps.portfolio.models import (
    Project, Skill, Experience, Education, Certification,
    Testimonial, NewsletterSubscriber, BlogPost, ResumeDownload,
)
from apps.portfolio.serializers import (
    ProjectSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer,
    CertificationSerializer, TestimonialPublicSerializer, TestimonialCreateSerializer,
    NewsletterSubscriberSerializer, BlogPostListSerializer, BlogPostDetailSerializer,
    ResumeDownloadSerializer,
)
from apps.portfolio.permissions import IsAdminOrReadOnly
from apps.portfolio.github import get_recent_repositories
from utils.client_info import get_client_ip, get_user_agent_string
from utils.responses import success_response


class ProjectViewSet(viewsets.ModelViewSet):
    """/api/projects/ — public read, admin write. PATCH increments no
    views by itself; use the dedicated `track-view` action for that."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_featured"]
    search_fields = ["title", "description", "tech_stack"]
    ordering_fields = ["order", "created_at", "views"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Projects retrieved.", response.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Project.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        instance.refresh_from_db()
        return success_response("Project retrieved.", self.get_serializer(instance).data)


class SkillViewSet(viewsets.ModelViewSet):
    """/api/skills/ — grouped by category (Frontend/Backend/DevOps/Security/Mobile)."""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["category"]
    ordering_fields = ["order", "proficiency"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Skills retrieved.", response.data)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ["start_date"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Experience retrieved.", response.data)


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ["start_date"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Education retrieved.", response.data)


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ["issue_date"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Certifications retrieved.", response.data)


class TestimonialViewSet(viewsets.ModelViewSet):
    """Public visitors can submit (create) a testimonial; only approved
    testimonials show up in the public list. Admins see/manage everything."""
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Testimonial.objects.all()
        return Testimonial.objects.filter(is_approved=True)

    def get_serializer_class(self):
        if self.action == "create":
            return TestimonialCreateSerializer
        return TestimonialPublicSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Testimonials retrieved.", response.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(
            "Thank you! Your testimonial will appear once approved.",
            serializer.data, status=201,
        )


class NewsletterSubscribeViewSet(viewsets.ModelViewSet):
    """POST /api/newsletter/ public subscribe. GET list is admin-only."""
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        email = request.data.get("email", "").strip().lower()
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=["is_active"])
        message = "Subscribed successfully." if created else "You're already subscribed."
        return success_response(message, NewsletterSubscriberSerializer(subscriber).data, status=201)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Subscribers retrieved.", response.data)


class BlogPostViewSet(viewsets.ModelViewSet):
    """Public visitors only see published posts; admins manage everything."""
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "summary", "tags"]
    ordering_fields = ["published_at", "views"]

    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return BlogPost.objects.all()
        return BlogPost.objects.filter(is_published=True)

    def get_serializer_class(self):
        if self.action == "list":
            return BlogPostListSerializer
        return BlogPostDetailSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.is_published and not instance.published_at:
            instance.published_at = timezone.now()
            instance.save(update_fields=["published_at"])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response("Blog posts retrieved.", response.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        BlogPost.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        instance.refresh_from_db()
        return success_response("Blog post retrieved.", self.get_serializer(instance).data)


class ResumeDownloadView(APIView):
    """POST /api/resume/track/ — call this right before serving/opening the
    CV file from the Angular app to increment the download counter."""
    permission_classes = [AllowAny]

    @extend_schema(summary="Record a CV/resume download")
    def post(self, request):
        ResumeDownload.objects.create(
            ip_address=get_client_ip(request),
            user_agent=get_user_agent_string(request)[:500],
        )
        total = ResumeDownload.objects.count()
        return success_response("Resume download recorded.", {"total_downloads": total}, status=201)

    @extend_schema(summary="Get total resume download count")
    def get(self, request):
        return success_response("Resume download count.", {"total_downloads": ResumeDownload.objects.count()})


class GitHubActivityView(APIView):
    """GET /api/github/activity/ — recent public repositories."""
    permission_classes = [AllowAny]

    @extend_schema(summary="Recent GitHub repository activity")
    def get(self, request):
        return success_response("GitHub activity retrieved.", get_recent_repositories())


class AdminDashboardView(APIView):
    """GET /api/dashboard/ — single combined payload for the admin dashboard
    (contacts + visitor analytics), as specified in the project brief."""
    permission_classes = [IsAdminUser]

    @extend_schema(summary="Combined admin dashboard summary")
    def get(self, request):
        stats = get_dashboard_stats()
        latest_contact = Contact.objects.first()
        recent_visitors = Visitor.objects.all()[:10]

        data = {
            "total_contacts": Contact.objects.count(),
            "unread_contacts": Contact.objects.filter(is_read=False).count(),
            "total_visitors": stats["total_visitors"],
            "today_visitors": stats["visits_today"],
            "returning_visitors": stats["returning_visitors"],
            "most_visited_page": stats["most_visited_pages"][0]["path"] if stats["most_visited_pages"] else None,
            "top_country": stats["top_countries"][0]["country"] if stats["top_countries"] else None,
            "latest_contact": ContactSerializer(latest_contact).data if latest_contact else None,
            "recent_visitors": VisitorSerializer(recent_visitors, many=True).data,
        }
        return success_response("Dashboard data retrieved.", data)
