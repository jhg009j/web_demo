from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from shortuuidfield import ShortUUIDField


class UserManager(BaseUserManager):
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError('请输入电话')
        if not username:
            raise ValueError('请输入用户名')
        if not password:
            raise ValueError('请输入密码')

        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone,
                                 username=username,
                                 password=password,
                                 **kwargs)

    def create_superuser(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone=telephone,
                                 username=username,
                                 password=password,
                                 **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    telephone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    uuid = ShortUUIDField(primary_key=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telephone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username



