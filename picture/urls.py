from django.urls import path

from . import views

app_name='picture'

urlpatterns = [
    path('picture-list/',views.picture_list,name='picture_list'),
    path('picture-detail/<int:id>/',views.picture_detail,name='picture_detail'),
]