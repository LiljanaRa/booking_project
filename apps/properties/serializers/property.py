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
    address = AddressCreateUpdateSerializer()

    class Meta:
        model = Property
        exclude = ('owner', 'created_at')

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        validated_data.pop('owner', None)
        property = Property.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
        Address.objects.create(property=property, **address_data)
        return property

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
        return instance
