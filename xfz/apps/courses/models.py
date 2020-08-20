from django.db import models


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    display = models.BooleanField(default=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('cms.Teacher', on_delete=models.DO_NOTHING, null=True, db_constraint=False)
    category = models.ForeignKey('CourseCategory', on_delete=models.DO_NOTHING, db_constraint=False, null=True)
    abstract = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    picture = models.URLField(default=None)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
