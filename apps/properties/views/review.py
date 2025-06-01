from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend


from apps.properties.permissions import IsReviewAuthorOrSuperuser
from apps.properties.filters import ReviewFilter
from apps.properties.models.review import Review
from apps.properties.serializers.review import (
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    ReviewSerializer
)


class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer


class ReviewUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsReviewAuthorOrSuperuser]

    def get_queryset(self):
        queryset = Review.objects.select_related(
            'rent_property', 'author'
        )
        return queryset


class PropertyReviewListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_class = ReviewFilter
    ordering_fields = [
        'rating',
        'created_at'
    ]
    ordering = ['-created_at']

    def get_queryset(self):
        rent_property_id = self.kwargs['rent_property_id']
        queryset = Review.objects.select_related(
            'rent_property', 'author'
        ).filter(rent_property_id=rent_property_id)
        return queryset
