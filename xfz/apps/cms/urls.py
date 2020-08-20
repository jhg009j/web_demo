from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # path('login/', views.login_view),
    path('', views.cms_index, name='index'),
    path('admin_logout/', views.xfz_admin_logout, name='admin_logout'),
    path('user_index/', views.users_index, name='user_index'),
    path('user_add/', views.AuthorityManage.as_view(), name='user_add'),
    path('user_delete/', views.user_delete, name='user_delete')

]

urlpatterns += [
    path('news_pub/', views.NewsPublication.as_view(), name='news_pub'),
    path('news_edit/', views.NewsEdit.as_view(), name='news_edit'),
    path('news_manager/', views.NewsManager.as_view(), name='news_manager'),
]

urlpatterns += [
    path('news_cate/', views.news_category, name='news_cate'),
    path('add_category/', views.add_category, name='add_cate'),
    path('edit_category/', views.edit_category, name='edit_cate'),
    path('del_category/', views.delete_category, name='del_cate'),
]

urlpatterns += [
    path('carousel_manager/', views.carousel_manager, name='carousel_manager'),
    path('add_carousel/', views.add_carousel, name='add_carousel'),
    path('edit_carousel/', views.edit_carousel, name='edit_carousel'),
    path('del_carousel/', views.del_carousel, name='del_carousel'),
    path('upload_file/', views.upload_file, name='upload_file'),
]

urlpatterns += [
    path('course_pub/', views.CoursePublication.as_view(), name='course_pub'),
    path('add_course_category/', views.CourseCategoryAdd.as_view(), name='add_course_category'),
    path('course_manager/', views.CourseManager.as_view(), name='course_manager'),
    path('course_edit/', views.CourseEdit.as_view(), name='course_edit'),
    path('del_course_category/', views.delete_course_category, name='del_course_cate'),
    path('edit_course_category/', views.edit_course_category, name='edit_course_cate'),
]

urlpatterns += [
    path('teacher_add/', views.TeacherAdd.as_view(), name='add_teacher'),
    path('teacher_manager/', views.TeacherManager.as_view(), name='teacher_manager'),
    path('teacher_edit/', views.TeacherEdit.as_view(), name='teacher_edit'),
    path('del_teacher/', views.TeacherManager.as_view(), name='del_teacher'),
]