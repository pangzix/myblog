from django.db import models
from django.utils import timezone
from .storage_cos import QcloudStorage

# Create your models here.

class PicturePost(models.Model):
    #avatar = models.ImageField(upload_to='picture/',blank=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='图片',storage=QcloudStorage())
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return self.title