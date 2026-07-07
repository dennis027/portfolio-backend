import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger("apps.contact")


def notify_new_contact(contact) -> None:
    """Emails the site owner whenever a new contact message arrives.
    Failures are logged, not raised — a broken SMTP config must never
    prevent the visitor's message from being saved."""
    if not settings.CONTACT_NOTIFY_EMAIL:
        return
    try:
        send_mail(
            subject=f"New portfolio contact: {contact.subject}",
            message=(
                f"From: {contact.full_name} <{contact.email}>\n"
                f"IP: {contact.ip_address}\n\n"
                f"{contact.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
            fail_silently=True,
        )
    except Exception:
        logger.exception("Failed to send contact notification email")
