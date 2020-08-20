from django import forms
from .models import User
from django.core.cache import cache
from utils.ErrorGet_for_forms import ErrorGet


class LoginForms(forms.ModelForm, ErrorGet):
    password = forms.CharField(max_length=20, min_length=6, error_messages={
        'max_length': '密码最多不能超过20位',
        'min_length': '密码最少不能低于6位'
    })
    remember = forms.IntegerField(required=False)
    telephone = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['is_active']


class RegisterForm(forms.ModelForm, ErrorGet):
    class Meta:
        model = User
        fields = ['username']

    telephone = forms.CharField(min_length=11, max_length=11, error_messages={
        'min_length': '电话不得小于11位',
        'max_length': '电话不得超过11位'})
    password1 = forms.CharField(min_length=6, max_length=20, error_messages={
        'min_length': '密码不得低于6位',
        'max_length': '密码不得超过20位'})
    password2 = forms.CharField(min_length=6, max_length=20, error_messages={
        'min_length': '密码不得低于6位',
        'max_length': '密码不得超过20位'})
    img_captcha = forms.CharField(max_length=5, min_length=5, error_messages={
        'min_length': '图形验证码为5位',
        'max_length': '图形验证码为5位'
    })

    def clean(self):
        super(RegisterForm, self).clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        telephone = self.cleaned_data.get('telephone')
        img_captcha = self.cleaned_data.get('img_captcha')

        if password1 != password2:
            raise forms.ValidationError('密码不一致')

        if not img_captcha or img_captcha.lower() != cache.get('img_captcha'):
            raise forms.ValidationError('图形验证码错误')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('电话已注册')
