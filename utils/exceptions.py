"""
Wraps DRF's default exception handler so every error also follows the
{ success, message, data } envelope instead of DRF's raw error format.
"""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        detail = response.data
        message = detail.get("detail") if isinstance(detail, dict) and "detail" in detail else "Request failed."
        response.data = {"success": False, "message": str(message), "data": detail}
    return response
