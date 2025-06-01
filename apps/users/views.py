from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.serializers import UserRegistrationSerializer
from apps.users.choices import UserType
from apps.properties.models.rent_property import Property
from apps.bookings.models import Booking


class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


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
