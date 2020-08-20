from django import forms
from apps.news.models import NewsPub
from apps.courses.models import Course
from apps.cms.models import Teacher
from utils.ErrorGet_for_forms import ErrorGet


class NewsPubForms(forms.ModelForm, ErrorGet):
    class Meta:
        model = NewsPub
        exclude = ['category', 'pub_time', 'author']

    category = forms.IntegerField(min_value=1,
                                  error_messages={
                                      'min_value': '请选择分类！'
                                  })
    news_id = forms.IntegerField(required=False)


class TeacherEditForm(forms.Form, ErrorGet):
    pk = forms.IntegerField(required=True, error_messages={
        'required': '请输入讲师编号'
    })

    class Meta:
        model = Teacher
        fields = '__all__'
        error_messages = {
            'name': {
                'required': '请输入讲师姓名',
            },
            'intro': {
                'required': '请输入讲师介绍',
            },
            'title': {
                'required': '请输入讲师头衔',
            },
            'avatar': {
                'required': '请加入讲师头像',
            }
        }


class DeleteTeacherForm(forms.Form, ErrorGet):
    pk = forms.IntegerField(required=True, error_messages={
        'required': '必须传入讲师的编号！',
    })


class CoursePubForms(forms.ModelForm, ErrorGet):
    class Meta:
        model = Course
        exclude = ['category', 'pub_time', 'teacher']

    category = forms.IntegerField(min_value=1,
                                  error_messages={
                                      'min_value': '请选择分类！'
                                  })
    teacher = forms.CharField(required=True,
                              error_messages={
                                  'required': '请输入讲师编号或姓名！'
                              })
    course_id = forms.IntegerField(required=False)
