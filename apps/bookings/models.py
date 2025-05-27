from django.db import models

from apps.properties.models.property import Property
from apps.users.models import User
from apps.bookings.choices import BookingStatus


class Booking(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    tenant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=30,
        choices=BookingStatus.choices(),
        default=BookingStatus.PENDING.value
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tenant.email} - {self.property.title} ({self.start_date.date()} - {self.end_date.date()})"

    class Meta:
        db_table = 'booking'
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'