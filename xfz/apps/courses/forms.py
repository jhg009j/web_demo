from django import forms
from utils.ErrorGet_for_forms import ErrorGet


class EditCourseCategoryForm(forms.Form, ErrorGet):
    course_category = forms.CharField(max_length=100, required=True, error_messages={
        'required': '必须传入分类名称！'
    })
    new_category_name = forms.CharField(max_length=100, required=True, error_messages={
        'required': '必须传入分类名称！'
    })

    pk = forms.IntegerField(required=True, error_messages={
        'required': '必须传入分类的id！'
    })


class DeleteCourseCategory(forms.Form, ErrorGet):
    pk = forms.IntegerField(required=True, error_messages={
        'required': '必须传入分类的id！'
    })


class DeleteCourse(forms.Form,ErrorGet):
    pk = forms.IntegerField(required=True, error_messages={
        'required': '必须传入课程的id！'
    })