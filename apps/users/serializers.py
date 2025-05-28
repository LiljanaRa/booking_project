from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserAuthJWTSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        data = super().get_token(user)
        data['username'] = user.username
        data['role'] = user.role
        return data