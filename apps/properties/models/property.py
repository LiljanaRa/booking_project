from django.db import models

from apps.properties.choices import PropertyType
from apps.users.models import User


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    rooms = models.PositiveSmallIntegerField()
    property_type = models.CharField(
        max_length=40,
        choices=PropertyType.choices(),
        default=PropertyType.APARTMENT.value
    )
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='properties'
    )
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.owner.email}"


    class Meta:
        db_table = 'property'
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
