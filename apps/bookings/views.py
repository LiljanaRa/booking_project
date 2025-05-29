from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView
)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.bookings.models import Booking
from apps.users.choices import UserType
from apps.bookings.serializers import (
    BookingSerializer,
    BookingCreateUpdateSerializer,
    BookingStatusUpdateSerializer
)


class BookingListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.TENANT:
            queryset = Booking.objects.select_related(
                'property', 'tenant'
            ).filter(tenant=user)
            return queryset
        raise PermissionDenied('Only tenants can access this endpoint.')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingSerializer
        return BookingCreateUpdateSerializer


class BookingDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == UserType.TENANT.value:
            queryset = Booking.objects.select_related(
                'property', 'tenant'
            ).filter(tenant=user)
            return queryset
        raise PermissionDenied('Only tenants can access this endpoint.')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingSerializer
        return BookingCreateUpdateSerializer


class LandlordBookingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.LANDLORD:
            queryset = Booking.objects.select_related(
                'property', 'tenant'
            ).filter(property__owner=user)
            return queryset
        raise PermissionDenied('Only landlords can access this endpoint.')


class BookingStatusUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingStatusUpdateSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.TENANT.value:
            return Booking.objects.select_related(
                'property', 'tenant'
            ).filter(tenant=user)

        if user.role == UserType.LANDLORD.value:
            return Booking.objects.select_related(
                'property', 'tenant'
            ).filter(property__owner=user)

        return Booking.objects.none()

    def get_object(self):
        booking = super().get_object()
        user = self.request.user

        if user.role == UserType.TENANT.value and booking.tenant != user:
            raise PermissionDenied('You are not allowed to update this booking.')

        if user.role == UserType.LANDLORD.value and booking.property.owner != user:
            raise PermissionDenied('You do not own this property.')

        return booking