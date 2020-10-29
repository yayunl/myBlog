from django.db import models


class PublishedManager(models.Manager):

    def get_queryset(self):
        """
        Return published objects.
        """
        return super().get_queryset().filter(status='published')
