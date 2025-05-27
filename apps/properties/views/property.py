from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import SAFE_METHODS

from apps.properties.models.property import Property
from apps.properties.serializers.property import (
    PropertySerializer,
    PropertyCreateUpdateSerializer
)


class PropertyListCreateView(ListCreateAPIView):

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
