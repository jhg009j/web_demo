from rest_framework import serializers
from apps.news.models import Carousel


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ['id', 'link_to', 'priority', 'carousel_url']
