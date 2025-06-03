from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
    AllowAny
)
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import filters, status
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from django.db.models import Avg, Count
from datetime import timedelta

from apps.properties.models.rent_property import Property
from apps.properties.models.view_history import PropertyViewHistory
from apps.properties.models.search_history import SearchHistory
from apps.properties.filters import PropertyFilter
from apps.properties.permissions import IsOwnerOrReadOnly
from apps.properties.serializers.rent_property import (
    PropertySerializer,
    PropertyCreateUpdateSerializer,
    PropertyUnavailableDatesSerializer
)
from apps.bookings.models import Booking
from apps.bookings.serializers import BookingSerializer
from apps.bookings.choices import BookingStatus
from apps.users.choices import UserType


class PropertyListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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

        keyword = self.request.query_params.get('search')
        if keyword:
            SearchHistory.objects.create(
                user=self.request.user
                if self.request.user.is_authenticated
                else None,
                keyword=keyword
            )

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
                rent_property=instance,
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
        user = self.request.user
        if user.role != UserType.LANDLORD.value:
            raise PermissionDenied('Only landlords can access this endpoint.')
        queryset = Property.objects.annotate(
            average_rating=Avg('reviews__rating'),
            count_reviews=Count('reviews'),
            viewed_by=Count(
                'view_history',
                distinct=True)
        ).filter(
            owner=user
        ).select_related('address'
                         ).prefetch_related('reviews')
        return queryset


class SwitchPropertyActiveStatusView(APIView):

    def patch(self, request, pk):
        try:
            rent_property = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            raise NotFound('Property not found.')

        if request.user.role != UserType.LANDLORD.value:
            raise PermissionDenied('Only landlords can access this endpoint.')

        if rent_property.owner != request.user:
            raise PermissionDenied('You can only update your own listings.')

        rent_property.is_active = not rent_property.is_active
        rent_property.save()

        return Response(
            {"id": rent_property.id, 'is_active': rent_property.is_active},
            status=status.HTTP_200_OK
        )


class PropertyBookingsView(ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        rent_property_id = self.kwargs['rent_property_id']

        instance = get_object_or_404(Property, pk=rent_property_id)

        if instance.owner != user:
            raise PermissionDenied('You are not allowed to view bookings for this property.')

        queryset = Booking.objects.filter(
            rent_property=instance
        ).select_related('tenant')

        return queryset


class PropertyUnavailableDatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, rent_property_id):
        bookings = Booking.objects.filter(
            rent_property_id=rent_property_id,
            status=BookingStatus.CONFIRMED.value
        )

        unavailable_dates = []

        for booking in bookings:
            start = booking.start_date
            end = booking.end_date
            delta = (end - start).days + 1
            for i in range(delta):
                unavailable_dates.append((start + timedelta(days=i)).strftime('%Y-%m-%d'))

        return Response(sorted(set(unavailable_dates)))


class PopularPropertyListView(ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
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


class PopularSearchKeywordsView(APIView):

    def get(self, request):
        keywords = (
            SearchHistory.objects.values(
                'keyword'
            ).annotate(count=Count('id')
                       ).order_by('-count')[:10]
        )
        return Response(keywords)
