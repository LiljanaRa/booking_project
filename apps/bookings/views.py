from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.choices import UserType
from apps.bookings.models import Booking
from apps.bookings.filters import BookingFilter
from apps.bookings.serializers import (
    BookingSerializer,
    BookingCreateUpdateSerializer,
    BookingStatusUpdateSerializer
)


class BookingListCreateView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = BookingFilter
    search_fields = [
        'rent_property__title',
        'status'
    ]
    ordering_fields = [
        'status',
        'start_date',
        'created_at'
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.TENANT:
            queryset = Booking.objects.select_related(
                'rent_property', 'tenant'
            ).filter(tenant=user)
            return queryset
        raise PermissionDenied('Only tenants can access this endpoint.')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingSerializer
        return BookingCreateUpdateSerializer


class BookingDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        user = self.request.user
        if user.role == UserType.TENANT.value:
            queryset = Booking.objects.select_related(
                'rent_property', 'tenant'
            ).filter(tenant=user)
            return queryset
        raise PermissionDenied('Only tenants can access this endpoint.')

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookingSerializer
        return BookingCreateUpdateSerializer


class LandlordBookingListView(ListAPIView):
    serializer_class = BookingSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = BookingFilter
    search_fields = [
        'rent_property__title',
        'status'
    ]
    ordering_fields = [
        'status',
        'start_date',
        'created_at'
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.LANDLORD:
            queryset = Booking.objects.select_related(
                'rent_property', 'tenant'
            ).filter(rent_property__owner=user)
            return queryset
        raise PermissionDenied('Only landlords can access this endpoint.')


class LandlordBookingView(RetrieveAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.LANDLORD:
            queryset = Booking.objects.select_related(
                'rent_property', 'tenant'
            ).filter(rent_property__owner=user)
            return queryset
        raise PermissionDenied('Only landlords can access this endpoint.')


class BookingStatusUpdateView(UpdateAPIView):
    serializer_class = BookingStatusUpdateSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == UserType.TENANT.value:
            return Booking.objects.select_related(
                'rent_property', 'tenant'
            ).filter(tenant=user)

        if user.role == UserType.LANDLORD.value:
            return Booking.objects.select_related(
                'rent_property', 'tenant'
            ).filter(rent_property__owner=user)

        return Booking.objects.none()

    def get_object(self):
        booking = super().get_object()
        user = self.request.user

        if user.role == UserType.TENANT.value and booking.tenant != user:
            raise PermissionDenied('You are not allowed to update this booking.')

        if user.role == UserType.LANDLORD.value and booking.rent_property.owner != user:
            raise PermissionDenied('You do not own this property.')

        return booking
