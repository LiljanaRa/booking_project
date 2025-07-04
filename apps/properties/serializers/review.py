from rest_framework import serializers
from django.utils import timezone

from apps.properties.models.review import Review
from apps.properties.serializers.rent_property import PropertyShortSerializer
from apps.bookings.models import Booking
from apps.bookings.choices import BookingStatus
from apps.users.serializers import UserShortSerializer
from apps.users.choices import UserType


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'rent_property',
            'rating',
            'comment',
        ]

    def validate_rent_property(self, value):
        user = self.context['request'].user

        if user.role != UserType.TENANT.value:
            raise serializers.ValidationError('Only tenants can access this endpoint.')

        booking = Booking.objects.filter(
            tenant=user,
            rent_property=value,
            status=BookingStatus.CONFIRMED.value,
            end_date__lt=timezone.now().date()
        ).first()

        if booking:
            booking.status = BookingStatus.COMPLETED.value
            booking.save()

        booking = Booking.objects.filter(
            tenant=user,
            rent_property=value,
            status=BookingStatus.COMPLETED.value
        ).exists()

        if not booking:
            raise serializers.ValidationError(
                'You can only leave a review after completing a booking for this property.')
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        instance = attrs['rent_property']
        review = Review.objects.filter(
            author=user,
            rent_property=instance
        ).exists()

        if review:
            raise serializers.ValidationError('You have already left a review for this property.')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'rating',
            'comment',
        ]
        read_only_fields = [
            'rent_property',
            'author',
            'created_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    rent_property = PropertyShortSerializer(read_only=True)
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'rent_property',
            'rating',
            'comment',
            'author',
            'created_at'
        ]
