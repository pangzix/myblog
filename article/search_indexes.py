from haystack import indexes
from .models import ArticlePost


class ArticlePostIndex(indexes.SearchIndex, indexes.Indexable): # 名字必须是model名+Index
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ArticlePost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()