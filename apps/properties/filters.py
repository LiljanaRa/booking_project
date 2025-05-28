import django_filters

from apps.properties.models.property import Property


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    room_min = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    room_max = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    property_type = django_filters.CharFilter(field_name='property_type')

    class Meta:
        model = Property
        fields = []