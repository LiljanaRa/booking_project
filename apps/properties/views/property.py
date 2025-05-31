from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import filters, status
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Avg, Count

from apps.properties.models.property import Property
from apps.properties.models.view_history import PropertyViewHistory
from apps.properties.filters import PropertyFilter
from apps.properties.permissions import IsOwnerOrReadOnly
from apps.properties.serializers.property import (
    PropertySerializer,
    PropertyCreateUpdateSerializer,
    PropertyUnavailableDatesSerializer
)
from apps.bookings.models import Booking
from apps.bookings.serializers import BookingSerializer
from apps.bookings.choices import BookingStatus


class PropertyListCreateView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description']
    ordering_fields = [
        'average_rating',
        'count_reviews',
        'views',
        'viewed_by',
        'price_per_night'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.annotate(
            average_rating=Avg('reviews__rating'),
            count_reviews=Count('reviews'),
            viewed_by=Count(
                'view_history',
                distinct=True)
        ).select_related(
            'owner', 'address'
        ).prefetch_related('reviews').filter(is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PropertySerializer
        return PropertyCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Property.objects.annotate(
            average_rating=Avg('reviews__rating')
        ).select_related(
            'owner', 'address'
        ).prefetch_related('reviews').filter(
            is_active=True)
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PropertySerializer
        return PropertyCreateUpdateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = models.F('views') + 1
        instance.save(update_fields=['views'])
        instance.refresh_from_db(fields=['views'])

        if request.user.is_authenticated:
            PropertyViewHistory.objects.update_or_create(
                user=request.user,
                property=instance,
                defaults={'viewed_at': timezone.now()}
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserPropertiesView(ListAPIView):
    serializer_class = PropertySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description']
    ordering_fields = [
        'average_rating',
        'count_reviews',
        'views',
        'viewed_by',
        'price_per_night'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.annotate(
            average_rating=Avg('reviews__rating'),
            count_reviews=Count('reviews'),
            viewed_by=Count(
                'view_history',
                distinct=True)
        ).filter(
            owner=self.request.user
        ).select_related('address'
                         ).prefetch_related('reviews')
        return queryset


class SwitchPropertyActiveStatusView(APIView):

    def patch(self, request, pk):
        try:
            property = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise NotFound('Property not found.')

        if property.owner != request.user:
            raise PermissionDenied('You can only update your own listings.')

        property.is_active = not property.is_active
        property.save()

        return Response(
            {"id": property.id, 'is_active': property.is_active},
            status=status.HTTP_200_OK
        )


class PropertyBookingsView(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        property_id = self.kwargs['property_id']

        instance = get_object_or_404(Property, pk=property_id)

        if instance.owner != user:
            raise PermissionDenied('You are not allowed to view bookings for this property.')

        queryset = Booking.objects.filter(
            property=instance
        ).select_related('tenant')

        return queryset


class PropertyUnavailableDatesView(APIView):
    def get(self, request, property_id):
        bookings = Booking.objects.filter(
            property_id=property_id,
            status=BookingStatus.CONFIRMED.value
        ).values('start_date', 'end_date')

        serializer = PropertyUnavailableDatesSerializer(bookings, many=True)
        return Response(serializer.data)


class PopularPropertyListView(ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Property.objects.annotate(
            viewed_by=Count(
                'view_history',
                distinct=True)
        ).filter(
            is_active=True
        ).order_by(
            '-viewed_by',
            '-created_at'
            )
        print(queryset.query)
        return queryset
