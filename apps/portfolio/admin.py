from django.contrib import admin

from apps.portfolio.models import (
    Project, Skill, Experience, Education, Certification,
    Testimonial, NewsletterSubscriber, BlogPost, ResumeDownload,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "is_featured", "views", "order", "created_at"]
    list_filter = ["is_featured"]
    search_fields = ["title", "tech_stack"]
    prepopulated_fields = {"slug": ("title",)}
    ordering = ["order"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "proficiency", "order"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["role", "company", "start_date", "end_date", "is_current"]
    list_filter = ["is_current"]
    search_fields = ["company", "role"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "start_date", "end_date"]
    search_fields = ["institution", "degree"]


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ["title", "issuing_organization", "issue_date", "expiry_date"]
    search_fields = ["title", "issuing_organization"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["author_name", "author_company", "is_approved", "created_at"]
    list_filter = ["is_approved"]
    search_fields = ["author_name", "message"]
    actions = ["approve_testimonials"]

    @admin.action(description="Approve selected testimonials")
    def approve_testimonials(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} testimonial(s) approved.")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "subscribed_at"]
    list_filter = ["is_active"]
    search_fields = ["email"]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "views", "published_at"]
    list_filter = ["is_published"]
    search_fields = ["title", "tags"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ResumeDownload)
class ResumeDownloadAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "downloaded_at"]
    date_hierarchy = "downloaded_at"
