from django.urls import path,include
from . import views

app_name = 'mlog'

urlpatterns = [
    path('mlog-result/',views.mlog_result,name='mlog_result'),
    path('vlog-list/',views.vlog_list,name='vlog_list'),
    path('vlog/<int:pk>/',views.vlog_detail,name='vlog_detail'),
]