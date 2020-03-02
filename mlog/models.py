from django.db import models
from django.contrib.auth.models import User
from  django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
import markdown
from django.utils.html import strip_tags


class MlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:10]
