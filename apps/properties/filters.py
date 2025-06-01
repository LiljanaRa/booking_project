import django_filters

from apps.properties.models.rent_property import Property
from apps.properties.models.review import Review


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    room_min = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    room_max = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    rent_property_type = django_filters.CharFilter(field_name='rent_property_type')

    class Meta:
        model = Property
        fields = [
            'min_price',
            'max_price',
            'city',
            'room_min',
            'room_max',
            'rent_property_type'
        ]


class ReviewFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='rating')
    rent_property = django_filters.NumberFilter(field_name='rent_property_id')
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = [
            'rating',
            'rent_property',
            'created_at'
        ]
