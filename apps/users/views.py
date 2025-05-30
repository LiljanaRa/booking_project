from rest_framework.generics import CreateAPIView

from apps.users.serializers import UserRegistrationSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = []
    serializer_class = UserRegistrationSerializer
