from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.portfolio.views import (
    ProjectViewSet, SkillViewSet, ExperienceViewSet, EducationViewSet,
    CertificationViewSet, TestimonialViewSet, NewsletterSubscribeViewSet,
    BlogPostViewSet, ResumeDownloadView, GitHubActivityView, AdminDashboardView,
)

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("skills", SkillViewSet, basename="skill")
router.register("experience", ExperienceViewSet, basename="experience")
router.register("education", EducationViewSet, basename="education")
router.register("certifications", CertificationViewSet, basename="certification")
router.register("testimonials", TestimonialViewSet, basename="testimonial")
router.register("newsletter", NewsletterSubscribeViewSet, basename="newsletter")
router.register("blog", BlogPostViewSet, basename="blogpost")

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("resume/track/", ResumeDownloadView.as_view(), name="resume-track"),
    path("github/activity/", GitHubActivityView.as_view(), name="github-activity"),
] + router.urls
