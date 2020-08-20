from django.db import models
# Create your models here.


class AddNewsCategory(models.Model):
    category_name = models.CharField(max_length=100)
    display = models.BooleanField(default=True)


class NewsPub(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('AddNewsCategory', db_constraint=False, on_delete=models.DO_NOTHING, null=True)
    desc = models.CharField(max_length=200)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('xfzauth.User', db_constraint=False, on_delete=models.DO_NOTHING, null=True)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pub_time']


class NewsComment(models.Model):
    content = models.TextField()
    commentator = models.ForeignKey('xfzauth.User', on_delete=models.DO_NOTHING, db_constraint=False)
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('NewsPub', on_delete=models.CASCADE)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ['-pub_time']


class Carousel(models.Model):
    link_to = models.URLField()
    priority = models.IntegerField()
    carousel_url = models.URLField()

    class Meta:
        ordering = ['-priority']
