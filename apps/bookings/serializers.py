from rest_framework import serializers

from apps.bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.StringRelatedField(read_only=True)
    property = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'property',
            'tenant',
            'start_date',
            'end_date',
            'status',
            'created_at'
        ]
        read_only_fields = [
            'status',
            'created_at'
        ]


class BookingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'property',
            'start_date',
            'end_date'
        ]
        read_only_fields = [
            'tenant',
            'status']

    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')
        property = attrs.get('property')

        if start and end and end <= start:
            raise serializers.ValidationError('The end date must be after start date.')

        if property and start and end:
            unavailable = Booking.objects.filter(
                property=property,
                end_date__gte=start,
                start_date__lte=end
            )
            if unavailable.exists():
                conflict = [f"{day.start_date.date()} to {day.end_date.date()}"
                            for day in unavailable]
                raise serializers.ValidationError(
                    f"No reservations are available for these dates: {','.join(conflict)}.")

        return attrs

    def create(self, validated_data):
        validated_data['tenant'] = self.context['request'].user
        return super().create(validated_data)
