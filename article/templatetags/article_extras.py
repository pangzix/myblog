from ..models import ArticlePost,ArticleColumn
from  django import template
from django.utils import timezone
import math

register = template.Library()


@register.inclusion_tag('article/inclusions/_recent_artilces.html', takes_context=True)
def show_recent_articles(context, num=5):
    return {
        'recent_article_list': ArticlePost.objects.all().order_by('-created')[:num],
    }

@register.inclusion_tag('article/inclusions/_contacting.html',takes_context=True)
def show_contactings(context):
    return

@register.inclusion_tag('article/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': ArticlePost.objects.dates('created', 'month', order='DESC'),
    }
@register.inclusion_tag('article/inclusions/_column.html', takes_context=True)
def show_columns(context):
    return {
        'column_list':ArticleColumn.objects.all(),
    }

#获取相对时间
@register.filter(name='timesince_zh')
def time_since_zh(value):
    now = timezone.now()
    diff = now - value

    if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
        return '刚刚'

    if diff.days == 0 and diff.seconds>= 60 and diff.seconds < 3600 :
        return str(math.floor(diff.seconds / 60)) + '分钟前'

    if diff.days == 0 and diff.seconds >= 3600 and diff.seconds <86400:
        return str(math.floor(diff.seconds / 3600)) + '小时前'

    if diff.days >= 1 and diff.days< 30 :
        return str(diff.days) + '天前'

    if diff.days >= 30 and diff.days < 365:
        return str(math.floor(diff.days / 30)) + '个月前'

    if diff.dasy >= 365:
        return str(math.floor(diff.days /365)) + '年前'


