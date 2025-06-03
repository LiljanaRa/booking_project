import datetime
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate

from apps.users.serializers import UserRegistrationSerializer
from apps.users.choices import UserType
from apps.properties.models.rent_property import Property
from apps.bookings.models import Booking


class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class LogInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            access_expiry = datetime.datetime.fromtimestamp(access_token['exp'], datetime.UTC)
            refresh_expiry = datetime.datetime.fromtimestamp(refresh_token['exp'], datetime.UTC)

            response = Response(status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=access_expiry
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )

            return response

        else:
            return Response(
                data={"message": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogOutAPIView(APIView):

    def post(self, request):
        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.role == UserType.LANDLORD.value:
            context['properties'] = Property.objects.filter(
                owner=user
            )

        elif user.role == UserType.TENANT.value:
            context['bookings'] = Booking.objects.filter(
                tenant=user
            )
        return context
