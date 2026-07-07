"""
Consistent JSON response envelope used across the entire API:
{ "success": bool, "message": str, "data": any }
"""
from rest_framework.response import Response


def api_response(success: bool = True, message: str = "", data=None, status=200):
    return Response({"success": success, "message": message, "data": data}, status=status)


def success_response(message: str = "Success", data=None, status=200):
    return api_response(True, message, data, status)


def error_response(message: str = "Something went wrong", data=None, status=400):
    return api_response(False, message, data, status)
