from django.shortcuts import render
from .models import Course, CourseCategory
from .serializers import CoursesSerializers
from utils import restful


def courses_index(request):
    courses = Course.objects.select_related('category', 'teacher').filter(category__name='最新课堂')
    categories = CourseCategory.objects.filter(display=True)
    context = {
        'courses': courses,
        'categories': categories
    }
    return render(request, 'courses/courses-index.html', context=context)


def courses_detail(request, detail_id):
    courses = Course.objects.filter(display=True).select_related('teacher', 'category')
    the_exact_course = courses.get(pk=detail_id)
    other_courses = courses.exclude(pk=detail_id)
    # print(other_courses)
    context = {
        'course': the_exact_course,
        'other_courses': other_courses
    }
    return render(request, 'courses/courses-detail.html', context=context)


def courses_differ_cate(request):
    cateid = request.GET.get('cateid')
    courses = Course.objects.filter(category=cateid, display=True).select_related('teacher', 'category')
    courses_serializers = CoursesSerializers(courses, many=True)
    return restful.ok(data=courses_serializers.data)
