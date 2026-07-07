"""
Helpers for pulling client metadata (IP, browser, OS, device) out of a
Django/DRF request. Shared by the contact app, the analytics app, and the
visitor-tracking middleware so this logic lives in exactly one place.
"""
from __future__ import annotations

from user_agents import parse as parse_user_agent


def get_client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def get_user_agent_string(request) -> str:
    return request.META.get("HTTP_USER_AGENT", "")


def parse_client(request) -> dict:
    """Returns ip, raw user-agent, browser, os, device type in one call."""
    ua_string = get_user_agent_string(request)
    ua = parse_user_agent(ua_string)

    if ua.is_mobile:
        device_type = "Mobile"
    elif ua.is_tablet:
        device_type = "Tablet"
    elif ua.is_pc:
        device_type = "Desktop"
    else:
        device_type = "Other"

    return {
        "ip_address": get_client_ip(request),
        "user_agent": ua_string,
        "browser": f"{ua.browser.family} {ua.browser.version_string}".strip(),
        "os": f"{ua.os.family} {ua.os.version_string}".strip(),
        "device_type": device_type,
    }
