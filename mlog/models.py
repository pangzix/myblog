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



class MyVlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = TaggableManager(blank=True)
    source = models.CharField(verbose_name='视频嵌入代码',max_length=500)
    add_time = models.DateTimeField(default=timezone.now,verbose_name='添加时间')

    class Meta:
        verbose_name = 'volg_or_videos'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
