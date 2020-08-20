from rest_framework import serializers
from apps.news.models import NewsPub, AddNewsCategory, NewsComment
from apps.xfzauth.serializers import UserSerializer


class AddNewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddNewsCategory
        fields = ['category_name', 'id', 'display']


class NewspubSerializer(serializers.ModelSerializer):
    category = AddNewsCategorySerializer()
    author = UserSerializer()

    class Meta:
        model = NewsPub
        fields = ['id', 'title', 'category', 'desc', 'thumbnail', 'pub_time', 'author', 'display']


class NewsCommentSerializer(serializers.ModelSerializer):
    commentator = UserSerializer()

    class Meta:
        model = NewsComment
        fields = ['id', 'content', 'pub_time', 'commentator']



