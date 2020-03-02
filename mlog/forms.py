from django import forms
from .models import MlogPost


class MlogPostForm(forms.ModelForm):
    class Meta:
        # 指明数据模型来源
        model = MlogPost
        # 定义表单包含的字段
        fields = ('tags', 'body')
