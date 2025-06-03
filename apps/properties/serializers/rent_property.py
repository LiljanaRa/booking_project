from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.properties.serializers.address import (
    AddressSerializer,
    AddressCreateUpdateSerializer
)
from apps.properties.models.rent_property import Property
from apps.properties.models.address import Address
from apps.users.choices import UserType


class PropertySerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    address = AddressSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    count_reviews = serializers.IntegerField(read_only=True)
    views = serializers.IntegerField(read_only=True)
    viewed_by = serializers.IntegerField(read_only=True)

    class Meta:
        model = Property
        fields = [
            'id',
            'title',
            'description',
            'price_per_night',
            'rooms',
            'rent_property_type',
            'is_active',
            'owner',
            'address',
            'average_rating',
            'count_reviews',
            'views',
            'viewed_by',
            'created_at'
        ]


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    address = AddressCreateUpdateSerializer()

    class Meta:
        model = Property
        exclude = ('owner', 'created_at')

    def create(self, validated_data):
        user = self.context['request'].user
        address_data = validated_data.pop('address')
        validated_data.pop('owner', None)

        title = validated_data.get('title')
        street = address_data.get('street')
        city = address_data.get('city')
        house_number = address_data.get('house_number')

        if user.role != UserType.LANDLORD.value:
            raise PermissionDenied('Only landlords can create a new property.')

        if Property.objects.filter(
                title=title,
                address__street=street,
                address__city=city,
                address__house_number=house_number
        ).exists():
            raise serializers.ValidationError(
                'A property with this title and address already exists.')

        rent_property = Property.objects.create(
            owner=user,
            **validated_data
        )
        Address.objects.create(rent_property=rent_property, **address_data)
        return rent_property

    def update(self, instance, validated_data):
        user = self.context['request'].user
        address_data = validated_data.pop('address', None)

        title = validated_data.get('title')
        street = address_data.get('street')
        city = address_data.get('city')
        house_number = address_data.get('house_number')

        if user.role != UserType.LANDLORD.value:
            raise PermissionDenied('Only landlords can create a new property.')

        if Property.objects.exclude(
                id=instance.id
        ).filter(
            title=title,
            address__street=street,
            address__city=city,
            address__house_number=house_number
        ).exists():
            raise serializers.ValidationError(
                'A property with this title and address already exists.')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
        return instance


class PropertyShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id',
            'title'
        ]
