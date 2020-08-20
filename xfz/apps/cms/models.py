from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    intro = models.TextField()
    title = models.CharField(max_length=100)
    avatar = models.URLField(default=None)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']
