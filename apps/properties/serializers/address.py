from rest_framework import serializers

from apps.properties.models.address import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'country',
            'region',
            'city',
            'street',
            'zip_code'
        ]


class AddressCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ('rent_property',)