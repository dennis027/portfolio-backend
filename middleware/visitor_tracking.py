"""
Automatically records every visit to the site (page views hitting Django,
including SSR/API calls from the Angular app) with zero frontend changes
required. Skips admin, static, media, health and docs routes to keep the
data meaningful.
"""
from __future__ import annotations

import logging

from django.utils import timezone

from utils.client_info import parse_client

logger = logging.getLogger("apps.analytics")

IGNORED_PREFIXES = ("/admin", "/static", "/media", "/health", "/api/docs", "/api/redoc", "/api/schema")


class VisitorTrackingMiddleware:
    """Records a Visitor row (or updates an existing one) per request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self._track(request, response)
        except Exception:  # never let tracking break the actual request
            logger.exception("Visitor tracking failed")
        return response

    def _track(self, request, response) -> None:
        path = request.path
        if path.startswith(IGNORED_PREFIXES):
            return
        if getattr(response, "status_code", 200) >= 500:
            return

        # Imported lazily to avoid app-registry-not-ready issues at import time.
        from apps.analytics.models import Visitor

        client = parse_client(request)
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key or "anonymous"

        visitor, created = Visitor.objects.get_or_create(
            session_id=session_id,
            defaults={
                "ip_address": client["ip_address"],
                "browser": client["browser"],
                "operating_system": client["os"],
                "device_type": client["device_type"],
                "referrer": request.META.get("HTTP_REFERER", "")[:500],
                "landing_page": path,
                "last_active": timezone.now(),
                "visit_count": 1,
            },
        )
        if not created:
            visitor.last_active = timezone.now()
            visitor.visit_count += 1
            visitor.save(update_fields=["last_active", "visit_count"])

        Visitor.pages_visited_model().objects.create(visitor=visitor, path=path)
