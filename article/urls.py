from django.urls import path,include
from . import views



app_name = 'article'

urlpatterns = [
    path('article-list/',views.article_list, name='article_list'),
    path('article-detail/<int:id>/',views.article_detail,name='article_detail'),
    path('article-create/',views.article_create,name='article_create'),
    path('article-delete/<int:id>/',views.article_delete,name='article_delete'),
    path('article-update/<int:id>/',views.article_update,name='article_update'),
    path('',views.index_view,name='index_url'),
    path('timeline/',views.TimelineView,name='timeline'),
    path('search/',include('haystack.urls')),
    path('archives/<int:year>/<int:month>/',views.archive,name='archive'),
    path('columns/<int:pk>/',views.column,name='column')
]