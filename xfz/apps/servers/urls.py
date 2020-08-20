from django.urls import path
from . import views

app_name = 'servers'
urlpatterns = [
    path('payinfo/', views.pay_info, name='payinfo'),
]