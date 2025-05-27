from rest_framework import serializers

from apps.properties.serializers.address import (
    AddressSerializer,
    AddressCreateUpdateSerializer
)
from apps.properties.models.property import Property
from apps.properties.models.address import Address


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'price_per_night',
            'rooms',
            'property_type',
            'is_active',
            'owner',
            'address',
            'created_at'
        ]


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    address = AddressCreateUpdateSerializer

    class Meta:
        model = Property
        exclude = ('owner', 'created_at')
