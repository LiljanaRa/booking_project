from rest_framework.generics import CreateAPIView

from apps.properties.models.review import Review
from apps.properties.serializers.review import ReviewCreateSerializer


class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer


