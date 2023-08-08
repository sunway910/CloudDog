from django.db import models
from django.utils import timezone


class ProjectAccount(models.Model):
    """Project Account Property"""
    account = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    project_access_key = models.CharField(max_length=100)
    project_secret_key = models.CharField(max_length=100)
    key_authority = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project_account'
        ordering = ['-created']
