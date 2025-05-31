from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from apps.properties.permissions import IsReviewAuthorOrSuperuser
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
            'property', 'author'
        )
        return queryset


class PropertyReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        property_id = self.kwargs['property_id']
        queryset = Review.objects.select_related(
            'property', 'author'
        ).filter(property_id=property_id)
        return queryset
