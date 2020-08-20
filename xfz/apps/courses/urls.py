from django.urls import path
from . import views
app_name = 'courses'

urlpatterns = [
    path('', views.courses_index, name='courses_index'),
    path('<int:detail_id>/', views.courses_detail, name='courses_detail'),
    path('course_deffer_cate/', views.courses_differ_cate, name='course_deffer_cate'),
]