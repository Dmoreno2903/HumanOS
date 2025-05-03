from django.db import models


class TimerModel(models.Model):
    """
    Abstract model to add created_at and updated_at fields to any model.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']
