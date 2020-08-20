from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin, AccessMixin
from apps.news.models import AddNewsCategory, NewsPub, Carousel
from django.contrib.auth.models import Group
from apps.xfzauth.models import User
from apps.courses.models import CourseCategory, Course
from apps.cms.models import Teacher
from utils import restful
from utils.paginator_tool import PaginatorTool
from apps.news.forms import EditCategoryForm, DeleteCategory, CarouselForm
from apps.courses.forms import EditCourseCategoryForm, DeleteCourseCategory, DeleteCourse
from apps.cms.forms import TeacherEditForm, DeleteTeacherForm, CoursePubForms
import os
from django.conf.urls.static import settings
from django.views.generic import View
from apps.cms.forms import NewsPubForms
import datetime
from django.core.paginator import Paginator
from urllib import parse
from django.utils.timezone import make_aware
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse
from django.http import Http404,HttpResponse
from django.db.models import Q
from apps.news.decorators import xfz_admin_required
from django.db import connection
# def login_view(request):
#     return render(request, 'cms/login.html')

decorators_get = [require_GET, permission_required]


@staff_member_required(login_url='index')
def cms_index(request):
    return render(request, 'cms/index.html')


class NewsPublication(PermissionRequiredMixin, AccessMixin, View, NewsPubForms):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        category = AddNewsCategory.objects.all()
        context = {
            'categories': category,
        }
        return render(request, 'cms/news_pub.html', context=context)

    def post(self, request):
        form = NewsPubForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = AddNewsCategory.objects.get(pk=category_id)
            author = request.user

            NewsPub.objects.create(title=title,
                                   desc=desc,
                                   thumbnail=thumbnail,
                                   content=content,
                                   category=category,
                                   author=author)
            return restful.ok()
        else:
            return restful.parameter_error(form.get_error())


@require_GET
@permission_required('news.add_newspub', 'index')
def news_category(request):
    all_category = AddNewsCategory.objects.filter(display=True).prefetch_related('newspub_set')
    context = {'categories': all_category}
    return render(request, 'cms/news_category.html', context=context)


@require_POST
@permission_required('news.add_newspub', 'index')
def add_category(request):
    new_cate = request.POST.get('new_category')
    exist = AddNewsCategory.objects.filter(category_name=new_cate).exists()
    if exist:
        return restful.parameter_error('该分类已存在！')
    else:
        AddNewsCategory.objects.create(category_name=new_cate)
    return restful.ok('添加成功')


@require_POST
@permission_required('news.add_newspub', 'index')
def edit_category(request):
    form = EditCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        cate_name = form.cleaned_data.get('cate_name')
        new_name = form.cleaned_data.get('new_name')
        if cate_name == new_name:
            return restful.parameter_error('分类名已存在！')
        try:
            AddNewsCategory.objects.filter(pk=pk).update(category_name=new_name)
            return restful.ok()
        except:
            return restful.parameter_error('该分类不存在')
    else:
        return restful.parameter_error(message=form.get_error())


@require_POST
@permission_required('news.add_newspub', 'index')
def delete_category(request):
    form = DeleteCategory(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        category = AddNewsCategory.objects.filter(pk=pk).first()
        related_news = category.newspub_set.all()
        if category:
            category.display = False
            category.save()
            related_news.update(display=False)
            # print(category.display, related_news)
            return restful.ok()
        else:
            return restful.parameter_error(message='该分类不存在！')
    else:
        return restful.parameter_error(message=form.get_error())


@permission_required('news.add_newspub', 'index')
def upload_file(request):
    file = request.FILES.get('file')
    carousel_tag = request.POST.get('carousel_tag')
    teacher_avatar = request.POST.get('teacher_avatar')
    course_picture = request.POST.get('course_picture')
    # print(carousel_tag,teacher_avatar, course_picture, file.name)
    file_name = file.name
    file_attr = file_name.split('.')
    file_path = settings.MEDIA_ROOT + '/'
    if carousel_tag:
        file_path = file_path + 'carousel/' + file_attr[0] + '.' + file_attr[-1]
        url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, 'carousel', file_name))

    elif teacher_avatar:
        file_path = file_path + 'teacher_avatar/' + file_attr[0] + '.' + file_attr[-1]
        url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, 'teacher_avatar', file_name))

    elif course_picture:
        file_path = file_path + 'course_picture/' + file_attr[0] + '.' + file_attr[-1]
        url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, 'course_picture', file_name))

    else:
        file_path = file_path + file_attr[0] + '.' + file_attr[-1]
        url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, file_name))

    with open(file_path, 'wb') as fb:
        for chunk in file.chunks():
            fb.write(chunk)

    return restful.ok(data={'url': url})


@permission_required('news.add_newspub', 'index')
def carousel_manager(request):
    carousels = Carousel.objects.all()
    if carousels:
        context = {
            'carousels': carousels
        }
        return render(request, 'cms/carousel_manager.html', context=context)
    return render(request, 'cms/carousel_manager.html')


@require_POST
@permission_required('news.add_newspub', 'index')
def add_carousel(request):
    form = CarouselForm(request.POST)
    if form.is_valid():
        carousel_url = form.cleaned_data.get('carousel_url')
        link_to = form.cleaned_data.get('link_to')
        priority = form.cleaned_data.get('priority')
        # print(carousel_url, link_to, priority)
        new_carousel = Carousel.objects.create(carousel_url=carousel_url, link_to=link_to, priority=priority)

        return restful.ok(data={'carousel_id': new_carousel.pk, 'priority': priority})
    else:
        return restful.parameter_error(form.get_error())


@require_POST
@permission_required('news.add_newspub', 'index')
def del_carousel(request):
    try:
        carousel_id = request.POST.get('carousel_id')
    except Carousel.DoesNotExist:
        return restful.parameter_error(message='该轮播图不存在！')
    Carousel.objects.get(pk=carousel_id).delete()
    return restful.ok()


@require_POST
@permission_required('news.add_newspub', 'index')
def edit_carousel(request):
    form = CarouselForm(request.POST)
    if form.is_valid():
        carousel_id = int(request.POST.get('carousel_id'))
        try:
            carousel_url = form.cleaned_data.get('carousel_url')
            link_to = form.cleaned_data.get('link_to')
            priority = form.cleaned_data.get('priority')
            Carousel.objects.filter(pk=carousel_id).update(carousel_url=carousel_url, link_to=link_to, priority=priority)
        except Carousel.DoesNotExist:
            return restful.parameter_error(message='轮播图id不存在！')
        return restful.ok(data={'priority': priority})
    else:
        return restful.parameter_error(form.get_error())


class NewsManager(PermissionRequiredMixin, AccessMixin, View, PaginatorTool):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    # get查询
    def get(self, request):
        search_start_date = request.GET.get('startDate') or ''
        search_end_date = request.GET.get('endDate') or ''
        search_categoryid = int(request.GET.get('category_id', 0))
        search_keyword = request.GET.get('keyword') or ''
        page = int(request.GET.get('p', 1))

        all_news = NewsPub.objects.filter(display=True).select_related('category', 'author')
        if search_start_date:
            start_date = datetime.datetime.strptime(search_start_date, '%Y-%m-%d')
        else:
            start_date = datetime.datetime(year=2020, month=2, day=25)

        if search_end_date:
            end_date = datetime.datetime.strptime(search_end_date, '%Y-%m-%d')
        else:
            end_date = datetime.datetime.today()
        newslists = all_news.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if search_categoryid:
            newslists = newslists.filter(category=search_categoryid)

            if search_keyword:
                newslists = newslists.filter(title__icontains=search_keyword)

        if search_keyword:
            newslists = newslists.filter(title__icontains=search_keyword)

        paginator_obj = Paginator(newslists, 2)
        page_obj = paginator_obj.page(page)
        # context_range = self.page_control(paginator_obj=paginator_obj, page_obj=page_obj)
        context_range = self.page_control2(paginator_obj=paginator_obj, page_obj=page_obj)
        context = {
            'categories': AddNewsCategory.objects.all(),
            'newslists': page_obj.object_list,
            'paginator_obj': paginator_obj,
            'page_obj': page_obj,
            'startDate': search_start_date,
            'endDate': search_end_date,
            'category_id': search_categoryid or 0,
            'keyword': search_keyword,
            'query_url': '&'+parse.urlencode({
                'startDate': search_start_date,
                'endDate': search_end_date,
                'category_id': search_categoryid,
                'keyword': search_keyword
            })
        }
        context.update(context_range)
        return render(request, 'cms/news_manager.html', context=context)

    def post(self, request):
        news_id = request.POST.get('pk')
        try:
            news = NewsPub.objects.get(pk=news_id)
        except NewsPub.DoesNotExist:
            return restful.parameter_error('该新闻不存在')
        news.display = False
        news.save()
        return restful.ok()


class NewsEdit(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        newsid = request.GET.get('id')
        categories = AddNewsCategory.objects.filter(display=True)
        try:
            newsid = int(newsid)
        except TypeError:
            raise Http404

        news = NewsPub.objects.select_related('category', 'author').filter(pk=newsid, display=True)
        if news:
            context = {
                'news': news[0],
                'categories': categories
            }
            return render(request, 'cms/news_pub.html', context=context)
        else:
            return restful.parameter_error('该文章不存在')

    def post(self, request):
        form = NewsPubForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = AddNewsCategory.objects.get(pk=category_id)
            author = request.user
            newsid = form.cleaned_data.get('news_id')

            NewsPub.objects.filter(pk=newsid).update(title=title,
                                                     category=category,
                                                     desc=desc,
                                                     thumbnail=thumbnail,
                                                     content=content,
                                                     author=author)
            return restful.ok()
        else:
            return restful.parameter_error(form.get_error())


class CoursePublication(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        categories = CourseCategory.objects.filter(display=True)
        context = {
            'categories': categories
        }
        return render(request, 'cms/courses_pub.html', context=context)

    def post(self, request):
        form = CoursePubForms(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            category_id = form.cleaned_data.get('category')
            abstract = form.cleaned_data.get('abstract')
            teacher_info = form.cleaned_data.get('teacher')
            picture = form.cleaned_data.get('picture')
            try:
                category = CourseCategory.objects.get(pk=category_id)
            except CourseCategory.DoesNotExist:
                return restful.parameter_error('该分类不存在！')

            try:
                teacher_id = int(teacher_info)
                teacher_list = Teacher.objects.filter(pk=teacher_id)
            except ValueError:
                teacher_name = teacher_info
                teacher_list = Teacher.objects.filter(name__icontains=teacher_name)

            if teacher_list:
                teacher = teacher_list[0]
                Course.objects.create(name=name, category=category, abstract=abstract, picture=picture, teacher=teacher)
                # print(teacher)
                # print('Course create ok')
                return restful.ok()
            else:
                return restful.parameter_error('该讲师未加入！')
        else:
            return restful.parameter_error(form.get_error())


class CourseManager(PermissionRequiredMixin, AccessMixin, View, PaginatorTool):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        search_start_date = request.GET.get('course-startDate') or ''
        search_end_date = request.GET.get('course-endDate') or ''
        search_categoryid = int(request.GET.get('category_id', 0))
        search_keyword = request.GET.get('keyword') or ''
        page = int(request.GET.get('p', 1))
        # print(search_categoryid,search_start_date,search_end_date,search_keyword)
        all_courses = Course.objects.filter(display=True).select_related('category', 'teacher')
        if search_start_date:
            start_date = datetime.datetime.strptime(search_start_date, '%Y-%m-%d')
        else:
            start_date = datetime.datetime(year=2020, month=2, day=25)

        if search_end_date:
            end_date = datetime.datetime.strptime(search_end_date, '%Y-%m-%d')
        else:
            end_date = datetime.datetime.today()

        courses = all_courses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if search_categoryid:
            courses = courses.filter(category=search_categoryid)

            if search_keyword:
                courses = courses.filter(abstract__icontains=search_keyword)

        if search_keyword:
            courses = courses.filter(abstract__icontains=search_keyword)

        paginator_obj = Paginator(courses, 2)
        page_obj = paginator_obj.page(page)
        context_range = self.page_control(paginator_obj=paginator_obj, page_obj=page_obj)
        context = {
            'categories': CourseCategory.objects.all(),
            'courses': page_obj.object_list,
            'paginator_obj': paginator_obj,
            'page_obj': page_obj,
            'startDate': search_start_date,
            'endDate': search_end_date,
            'category_id': search_categoryid or 0,
            'keyword': search_keyword,
            'query_url': '&' + parse.urlencode({
                'course-startDate': search_start_date,
                'course-endDate': search_end_date,
                'category_id': search_categoryid,
                'keyword': search_keyword
            })
        }
        context.update(context_range)
        return render(request, 'cms/courses_manager.html', context=context)

    def post(self, request):
        form = DeleteCourse(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            try:
                course = Course.objects.get(pk=pk)
            except Course.DoesNotExist:
                return restful.parameter_error('该课程不存在！')
            course.display = False
            course.save()
            # print(course)
            # print('course delete ok')
            return restful.ok()
        else:
            return restful.parameter_error(form.get_error())


class CourseEdit(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        course_id = request.GET.get('id')
        try:
            course_id = int(course_id)
        except ValueError:
            return restful.parameter_error('请输入正确的课程id！')
        course = Course.objects.select_related('teacher', 'category').filter(pk=course_id, display=True)
        categories = CourseCategory.objects.all()
        context = {
            'course': course[0],
            'categories': categories
        }
        return render(request, 'cms/courses_pub.html', context=context)

    def post(self, request):
        name = request.POST.get('name')
        category = request.POST.get('category')
        abstract = request.POST.get('abstract')
        course_id = request.POST.get('course_id')
        picture = request.POST.get('picture')
        teacher_info = request.POST.get('teacher')
        try:
            teacher_id = int(teacher_info)
            teacher_list = Teacher.objects.filter(pk=teacher_id)
        except ValueError:
            teacher_name = teacher_info
            teacher_list = Teacher.objects.filter(name__icontains=teacher_name)
        if teacher_list:
            teacher = teacher_list[0]
            Course.objects.filter(pk=course_id).update(name=name,
                                                       category=category,
                                                       abstract=abstract,
                                                       picture=picture,
                                                       teacher=teacher)
            # print(teacher, name, category, abstract, picture)
            # print('Course edit ok')
            return restful.ok()


class CourseCategoryAdd(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        categories = CourseCategory.objects.filter(display=True)
        context = {
            'categories': categories
        }
        return render(request, 'cms/courses_category.html', context=context)

    def post(self, request):
        course_category = request.POST.get('course_category')
        exist = CourseCategory.objects.filter(name=course_category).exists()
        if exist:
            cate = CourseCategory.objects.get(name=course_category)
            if not cate.display:
                cate.display = True
                cate.save()
                return restful.ok()
            else:
                return restful.parameter_error('分类已存在！')
        else:
            CourseCategory.objects.create(name=course_category)
            # print('create ok')
            return restful.ok()


@require_POST
@permission_required('news.add_newspub', 'index')
def edit_course_category(request):
    form = EditCourseCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        course_category = form.cleaned_data.get('course_category')
        new_category_name = form.cleaned_data.get('new_category_name')
        if course_category == new_category_name:
            return restful.parameter_error('分类名已存在！')
        try:
            CourseCategory.objects.filter(pk=pk).update(name=new_category_name)
            # print('update ok')
            return restful.ok()
        except:
            return restful.parameter_error('该分类不存在')
    else:
        return restful.parameter_error(message=form.get_error())


@require_POST
@permission_required('news.add_newspub', 'index')
def delete_course_category(request):
    form = DeleteCourseCategory(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        try:
            category = CourseCategory.objects.get(pk=pk)
        except CourseCategory.DoesNotExist:
            return restful.parameter_error('该分类不存在！')
        category.display = False
        category.save()
        category.course_set.update(display=False)
        # print('delete ok')
        return restful.ok()


class TeacherAdd(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        return render(request, 'cms/teacher_add.html')

    def post(self, request):
        teacher_name = request.POST.get('name')
        teacher_title = request.POST.get('title')
        teacher_intro = request.POST.get('intro')
        teacher_avatar = request.POST.get('avatar')
        if teacher_name and teacher_title and teacher_intro and teacher_avatar:
            Teacher.objects.create(name=teacher_name,
                                   title=teacher_title,
                                   intro=teacher_intro,
                                   avatar=teacher_avatar)
            # print('teacher add ok')
            return restful.ok()
        else:
            return restful.parameter_error('请完整填写讲师信息！')


class TeacherEdit(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        teacherid = request.GET.get('id')
        teacher = Teacher.objects.filter(pk=teacherid)
        context = {
            'teacher': teacher[0]
        }
        return render(request, 'cms/teacher_add.html', context=context)

    def post(self, request):
        form = TeacherEditForm(request.POST)
        if form.is_valid():
            teacher_name = form.cleaned_data.get('name')
            teacher_title = form.cleaned_data.get('title')
            teacher_intro = form.cleaned_data.get('intro')
            teacher_id = form.cleaned_data.get('pk')
            teacher_avatar = form.cleaned_data.get('avatar')
            Teacher.objects.filter(pk=teacher_id).update(name=teacher_name,
                                                         title=teacher_title,
                                                         intro=teacher_intro,
                                                         avatar=teacher_avatar)
            # print('teacher info edit ok')
            return restful.ok()
        else:
            return restful.parameter_error(form.get_error())


class TeacherManager(PermissionRequiredMixin, AccessMixin, View, PaginatorTool):
    permission_required = 'news.add_newspub'
    login_url = 'index'

    def get(self, request):
        teacher_name = request.GET.get('keyword') or ''
        teacher_id = int(request.GET.get('teacher_id', 0) or 0)
        page = int(request.GET.get('p', 1))
        teachers = Teacher.objects.filter(display=True)

        if teacher_name:
            if teacher_id:
                teachers = teachers.filter(name__icontains=teacher_name, pk=teacher_id)
            else:
                teachers = teachers.filter(name__icontains=teacher_name)
        if teacher_id:
            teachers = teachers.filter(pk=teacher_id)

        paginator_obj = Paginator(teachers, 2)
        page_obj = paginator_obj.page(page)
        context_range = self.page_control(paginator_obj=paginator_obj, page_obj=page_obj)
        context = {
            'teachers': page_obj.object_list,
            'paginator_obj': paginator_obj,
            'page_obj': page_obj,
            'keyword': teacher_name,
            'teacher_id': teacher_id or 0,
            'query_url': '&'+parse.urlencode({
                'keyword': teacher_name,
                'teacher_id': teacher_id
            })
        }
        context.update(context_range)
        return render(request, 'cms/teacher_manager.html', context=context)

    def post(self, request):
        form = DeleteTeacherForm(request.POST)
        if form.is_valid():
            teacher_id = form.cleaned_data.get('pk')
            try:
                teacher = Teacher.objects.get(pk=teacher_id)
            except Teacher.DoesNotExist:
                return restful.parameter_error('该讲师不存在！')
            teacher.display = False
            teacher.save()
            teacher.course_set.update(display=False)
            # print('teacher delete ok')
            return restful.ok()
        else:
            return restful.parameter_error(form.get_error())


@permission_required('xfzauth.add_user', 'index')
def users_index(request):
    staff = User.objects.filter(is_staff=True)
    context = {'staff': staff}
    return render(request, 'cms/user_index.html', context=context)


class AuthorityManage(PermissionRequiredMixin, AccessMixin, View):
    permission_required = 'xfzauth.add_user'
    login_url = 'index'

    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/edituser_add.html', context=context)

    def post(self, request):
        user_tele = request.POST.get('telephone')
        groups = request.POST.getlist('groups')
        user = User.objects.filter(telephone=user_tele).first()
        if groups and user:
            groups = Group.objects.filter(pk__in=groups)
            user.groups.set(groups)
            user.is_staff = True
            user.save()
            return redirect(reverse('cms:user_index'))
        else:
            raise Http404


@permission_required('xfzauth.add_user', 'index')
def user_delete(request):
    user_tele = request.POST.get('user-tele')
    if user_tele:
        user = User.objects.filter(telephone=user_tele).first()
        if user.is_superuser:
            return HttpResponse('无法删除超级用户')
        else:
            user.is_staff = False
            user.save()
            return redirect(reverse('cms:user_index'))




@permission_required('news.add_newspub', 'index')
def xfz_admin_logout(request):
    logout(request)
    return redirect('index')
