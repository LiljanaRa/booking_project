from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import SAFE_METHODS
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from apps.properties.models.property import Property
from apps.properties.filters import PropertyFilter
from apps.properties.serializers.property import (
    PropertySerializer,
    PropertyCreateUpdateSerializer
)


class PropertyListCreateView(ListCreateAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.select_related(
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

    def get_queryset(self):
        user = self.request.user
        queryset = Property.objects.select_related(
            'owner', 'address'
        ).prefetch_related('reviews').filter(
            owner=user)
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return PropertySerializer
        return PropertyCreateUpdateSerializer


class UserPropertiesView(ListAPIView):
    serializer_class = PropertySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.filter(
            owner=self.request.user
        ).select_related('address'
                         ).prefetch_related('reviews')
        return queryset
