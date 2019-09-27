from django.contrib import admin
from .models import ArticlePost,ArticleColumn
import xadmin



from xadmin import views

class GlobalSetting(object):
    # 设置后台顶部标题
    site_title ='博客后台管理'
    # 设置后台底部标题
    site_footer ='博客后台管理'
class BaseSetting(object):
    # 启用主题管理器
    enable_themes = True
    # 使用主题
    use_bootswatch = True


# 注册主题设置
xadmin.site.register(views.BaseAdminView, BaseSetting)


xadmin.site.register(views.CommAdminView, GlobalSetting)
# Register your models here.
admin.site.register(ArticlePost)
admin.site.register(ArticleColumn)
xadmin.site.register(ArticlePost)
xadmin.site.register(ArticleColumn)

