from rest_framework.throttling import AnonRateThrottle


class ContactFormThrottle(AnonRateThrottle):
    """Extra-strict throttle scope applied only to POST /api/contact/,
    on top of the global anon throttle, to stop form-spam bursts."""
    scope = "contact_form"
