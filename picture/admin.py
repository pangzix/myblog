from django.contrib import admin
from .models import PicturePost
import xadmin
# Register your models here.

admin.site.register(PicturePost)
xadmin.site.register(PicturePost)