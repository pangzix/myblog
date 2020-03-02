from django.urls import path,include
from . import views

app_name = 'mlog'

urlpatterns = [
    path('mlog-result/',views.mlog_result,name='mlog_result'),

]