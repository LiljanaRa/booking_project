from django.db import models

from apps.users.models import User

class SearchHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    keyword = models.CharField(max_length=75)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_history'
        ordering = ['-searched_at']
        verbose_name = 'Search history'
        verbose_name_plural = 'Search histories'

    def __str__(self):
        return f"{self.user} searched '{self.keyword}'"
