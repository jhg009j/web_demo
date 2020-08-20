from django.urls import path
from . import views
app_name = 'news'

urlpatterns = [
    path('', views.index, name='news_index'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('more/', views.load_more, name='load_more'),
    path('differ_cate/', views.differ_cate, name='differ_cate'),
    path('add_comment/', views.add_comment, name='add_comment'),
]