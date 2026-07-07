"""Optional Google reCAPTCHA v3 verification. If RECAPTCHA_SECRET_KEY isn't
configured, verification is skipped (useful for local dev)."""
import requests
from django.conf import settings


def verify_recaptcha(token: str) -> bool:
    if not settings.RECAPTCHA_SECRET_KEY:
        return True
    if not token:
        return False
    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.RECAPTCHA_SECRET_KEY, "response": token},
            timeout=5,
        )
        result = resp.json()
        return result.get("success", False) and result.get("score", 0) >= 0.5
    except requests.RequestException:
        # Fail closed would block legit users during Google outages; fail open instead.
        return True
