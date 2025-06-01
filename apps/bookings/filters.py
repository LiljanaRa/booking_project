import django_filters

from apps.bookings.models import Booking


class BookingFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    status = django_filters.CharFilter(field_name='status')
    rent_property = django_filters.NumberFilter(field_name='rent_property_id')

    class Meta:
        model = Booking
        fields = [
            'start_date',
            'end_date',
            'status',
            'rent_property'
        ]
