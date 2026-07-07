from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    """Allows admin login with the standard username/password pair.
    Kept as its own serializer so extra claims can be added later
    (e.g. is_staff) without touching SimpleJWT internals elsewhere."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_staff"] = user.is_staff
        token["username"] = user.username
        return token
