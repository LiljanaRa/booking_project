from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.properties.models.property import Property
from apps.users.models import User


class Review(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.email} - {self.property.title} ({self.rating}/5)"


    class Meta:
        db_table = 'review'
        unique_together = ('property', 'author')
        ordering = ['-rating', 'created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'