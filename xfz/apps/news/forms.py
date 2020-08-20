from django import forms
from utils.ErrorGet_for_forms import ErrorGet


class EditCategoryForm(forms.Form, ErrorGet):
    pk = forms.IntegerField(required=True, error_messages={
        'required': '必须传入分类的id！'
    })
    cate_name = forms.CharField(max_length=100, required=True, error_messages={
        'required': '必须传入分类名称！'
    })
    new_name = forms.CharField(max_length=100, required=True, error_messages={
        'required': '必须传入分类名称！'
    })


class DeleteCategory(forms.Form, ErrorGet):
    pk = forms.IntegerField(required=True, error_messages={
        'required': '必须传入分类的id！'
    })


class CommentForm(forms.Form, ErrorGet):
    news_id = forms.IntegerField(required=True)
    content = forms.CharField(required=True, error_messages={
        'required': '请输入评论！'
    })


class CarouselForm(forms.Form, ErrorGet):
    carousel_url = forms.URLField(required=True, error_messages={
        'required': '请传入文件！'
    })
    link_to = forms.URLField(required=True, error_messages={
        'required': '请输入链接地址！'
    })
    priority = forms.IntegerField(required=True, error_messages={
        'required': '请输入轮播图优先级！'
    })
