from rest_framework import serializers

from apps.properties.models.review import Review
from apps.bookings.models import Booking
from apps.bookings.choices import BookingStatus


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'property',
            'rating',
            'comment',
        ]

    def validate_property(self, value):
        user = self.context['request'].user
        booking = Booking.objects.filter(
            tenant=user,
            property=value,
            status=BookingStatus.COMPLETED.value
        ).exists()

        if not booking:
            raise serializers.ValidationError('You can only leave a review after completing a booking for this property.')
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        instance = attrs['property']
        review = Review.objects.filter(
            author=user,
            property=instance
        ).exists()

        if review:
            raise serializers.ValidationError('You have already left a review for this property.')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return super().create(validated_data)
