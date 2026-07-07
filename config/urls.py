from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.accounts.views import LoginView
from apps.portfolio.views import homepage
from utils.health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health-check"),
    path("", homepage, name="home"),

    # JWT auth
    path("api/auth/login/", LoginView.as_view(), name="token-obtain-pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Feature apps
    path("api/contact/", include("apps.contact.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
    path("api/", include("apps.portfolio.urls")),

    # API schema / docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
