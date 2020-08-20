from rest_framework import serializers
from .models import Course, CourseCategory
from apps.cms.models import Teacher


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['name', 'id']


class CourseCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class CoursesSerializers(serializers.ModelSerializer):
    category = CourseCategorySerializers()
    teacher = TeacherSerializers()

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher', 'category', 'picture']
