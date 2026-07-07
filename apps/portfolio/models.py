from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, help_text="Comma-separated, e.g. Django,Angular,PostgreSQL")
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def tech_list(self) -> list[str]:
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]


class Skill(models.Model):
    class Category(models.TextChoices):
        FRONTEND = "frontend", "Frontend"
        BACKEND = "backend", "Backend"
        DEVOPS = "devops", "DevOps"
        SECURITY = "security", "Security"
        MOBILE = "mobile", "Mobile"

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    proficiency = models.PositiveSmallIntegerField(default=80, help_text="0-100")
    icon = models.CharField(max_length=100, blank=True, help_text="Icon class/name for the frontend")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"


class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=150, blank=True)
    credential_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-issue_date"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    author_name = models.CharField(max_length=150)
    author_role = models.CharField(max_length=150, blank=True)
    author_company = models.CharField(max_length=150, blank=True)
    author_photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    message = models.TextField()
    is_approved = models.BooleanField(default=False, help_text="Only approved testimonials are shown publicly.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Testimonial from {self.author_name}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, help_text="Comma-separated")
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def tag_list(self) -> list[str]:
        return [t.strip() for t in self.tags.split(",") if t.strip()]


class ResumeDownload(models.Model):
    """One row per CV download — powers a simple download counter."""
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-downloaded_at"]
