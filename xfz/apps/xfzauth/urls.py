from django.urls import path
from . import views

app_name = 'xfzauth'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('captcha/', views.img_captcha, name='captcha'),
    path('register/', views.register_view, name='register'),

]
