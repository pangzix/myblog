from ..models import ArticlePost,Timeline
from  django import template

register = template.Library()


@register.inclusion_tag('article/inclusions/_recent_artilces.html', takes_context=True)
def show_recent_articles(context, num=5):
    return {
        'recent_article_list': ArticlePost.objects.all().order_by('-created')[:num],
    }