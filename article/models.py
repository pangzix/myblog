from django.db import models
from django.contrib.auth.models import User
from  django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
import markdown
from django.utils.html import strip_tags
from .wan_storage_cos import QcloudStorage

# Create your models here.

class ArticleColumn(models.Model):
    title = models.CharField(max_length=100,blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ArticlePost(models.Model):

    avatar = models.ImageField(verbose_name='文章图片',storage=QcloudStorage(),blank=True)
    tags = TaggableManager(blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200,blank=True)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    def save(self,*args,**kwargs):


        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args,**kwargs)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])


# 时间线
class Timeline(models.Model):
    COLOR_CHOICE = (
        ('primary', '基本-蓝色'),
        ('success', '成功-绿色'),
        ('info', '信息-天蓝色'),
        ('warning', '警告-橙色'),
        ('danger', '危险-红色')
    )
    SIDE_CHOICE = (
        ('L', '左边'),
        ('R', '右边'),
    )
    STAR_NUM = (
        (1, '1颗星'),
        (2, '2颗星'),
        (3, '3颗星'),
        (4, '4颗星'),
        (5, '5颗星'),
    )
    side = models.CharField('位置', max_length=1, choices=SIDE_CHOICE, default='L')
    star_num = models.IntegerField('星星个数', choices=STAR_NUM, default=3)
    icon = models.CharField('图标', max_length=50, default='fa fa-pencil')
    icon_color = models.CharField('图标颜色', max_length=20, choices=COLOR_CHOICE, default='info')
    title = models.CharField('标题', max_length=100)
    update_date = models.DateTimeField('更新时间')
    content = models.TextField('主要内容')

    class Meta:
        verbose_name = '时间线'
        verbose_name_plural = verbose_name
        ordering = ['update_date']

    def __str__(self):
        return self.title[:20]

    def content_to_markdown(self):
        return markdown.markdown(self.content,
                                 extensions=['markdown.extensions.extra', ]
                                 )



