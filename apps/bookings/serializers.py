from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from apps.bookings.models import Booking
from apps.bookings.choices import BookingStatus
from apps.users.choices import UserType
from apps.properties.serializers.rent_property import PropertyShortSerializer


class BookingSerializer(serializers.ModelSerializer):
    tenant = serializers.StringRelatedField(read_only=True)
    rent_property = PropertyShortSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'rent_property',
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
            'rent_property',
            'start_date',
            'end_date'
        ]
        read_only_fields = [
            'tenant',
            'status']

    def validate(self, attrs):
        attrs.pop('tenant', None)
        attrs.pop('status', None)

        start = attrs.get('start_date')
        end = attrs.get('end_date')
        rent_property = attrs.get('rent_property')

        if start and start < timezone.now():
            raise serializers.ValidationError('Start date cannot be in the past.')

        if start and end and end <= start:
            raise serializers.ValidationError('The end date must be after start date.')

        if rent_property and start and end:
            unavailable = Booking.objects.filter(
                rent_property=rent_property,
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
        validated_data['status'] = BookingStatus.PENDING.value
        return super().create(validated_data)


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

    def validate_status(self, value):
        user = self.context['request'].user
        booking = self.instance

        if user.role == UserType.TENANT:
            if value != BookingStatus.CANCELLED.value:
                raise serializers.ValidationError("Tenants can only cancel bookings.")
            if (booking.start_date - timezone.now().date()) < timedelta(days=7):
                raise serializers.ValidationError("Cannot cancel less than 7 days before start date.")

        elif user.role == UserType.LANDLORD:
            if value not in [BookingStatus.CONFIRMED.value, BookingStatus.DECLINED.value]:
                raise serializers.ValidationError("Landlords can only confirm or decline bookings.")

        else:
            raise serializers.ValidationError("You are not allowed to change status.")

        return value
