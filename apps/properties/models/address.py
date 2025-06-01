from django.db import models

from apps.properties.models.rent_property import Property


class Address(models.Model):
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=70, null=True, blank=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=70)
    house_number = models.CharField(max_length=6)
    zip_code = models.CharField(max_length=15)
    rent_property = models.OneToOneField(
        Property,
        on_delete=models.CASCADE,
        related_name='address'
    )

    def __str__(self):
        return f"{self.street}, {self.city} {self.zip_code}"


    class Meta:
        db_table = 'address'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

