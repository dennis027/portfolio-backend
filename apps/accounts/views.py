from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import EmailOrUsernameTokenSerializer
from utils.responses import success_response


class LoginView(TokenObtainPairView):
    """POST { username, password } -> { access, refresh } wrapped in the
    standard { success, message, data } envelope."""
    serializer_class = EmailOrUsernameTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return success_response("Login successful.", response.data)
        return response
