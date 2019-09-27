from django.contrib import admin
from .models import Comment
import xadmin

# Register your models here.

admin.site.register(Comment)
xadmin.site.register(Comment)
