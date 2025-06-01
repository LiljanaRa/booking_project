from django.db import models

from apps.users.models import User
from apps.properties.models.rent_property import Property


class PropertyViewHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    rent_property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='view_history'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'view_history'
        unique_together = ('user', 'rent_property')
        ordering = ['-viewed_at']
        verbose_name = 'View history'
        verbose_name_plural = 'View histories'
