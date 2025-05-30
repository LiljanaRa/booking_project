from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from apps.users.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserAuthJWTSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        data = super().get_token(user)
        data['username'] = user.username
        data['role'] = user.role
        return data