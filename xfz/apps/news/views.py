from django.shortcuts import render
from apps.news.models import NewsPub, AddNewsCategory, NewsComment, Carousel
from .serializers import NewspubSerializer, NewsCommentSerializer
from .decorators import xfz_login_require
from .forms import CommentForm
from utils import restful
from django.http import Http404
from django.db import connection


news_num_per_page = 2


def index(request):
    hot_recommends = NewsPub.objects.order_by('-pub_time').select_related('category')[:1]
    category = AddNewsCategory.objects.filter(display=True)
    newslists = NewsPub.objects.select_related('author', 'category')[:2]
    carousels = Carousel.objects.all()
    # print(newslists)
    # print(connection.queries)

    context = {
        'hotrecommends': hot_recommends,
        'newslists': newslists,
        'categories': category,
        'carousels': carousels
    }
    return render(request, 'news/index.html', context=context)


def differ_cate(request):
    category_id = int(request.GET.get('category_id'))
    newslists = NewsPub.objects.select_related('author', 'category')

    if category_id == 0:
        news_serialize = NewspubSerializer(newslists[:2], many=True)
        return restful.ok(data=news_serialize.data)

    else:
        newslists = newslists.filter(category=category_id)[:2]
        # print(newslists.first().pub_time)
        news_serialize = NewspubSerializer(newslists, many=True)
        # print(news_serialize.data)
        return restful.ok(data=news_serialize.data)


def news_detail(request, news_id):
    hot_recommends = NewsPub.objects.order_by('-pub_time').select_related('category')[:1]
    try:
        news = NewsPub.objects.select_related('author', 'category')\
            .prefetch_related('newscomment_set__commentator')\
            .get(pk=news_id)
        context = {
            'hotrecommends': hot_recommends,
            'news': news
        }
    except NewsPub.DoesNotExist:
        raise Http404
    return render(request, 'news/news-detail.html', context=context)


def load_more(request):
    page = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id'))
    newslists = NewsPub.objects.select_related('author', 'category')
    if category_id == 0:
        news = newslists.filter(display=True)
    else:
        news = newslists.filter(category=category_id, display=True)

    start = (page-1)*news_num_per_page
    end = start+news_num_per_page
    news_post = news[start:end]
    news_serialize = NewspubSerializer(news_post, many=True)
    return restful.ok(data=news_serialize.data)


@xfz_login_require
def add_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        commentator = request.user
        news = NewsPub.objects.get(pk=news_id)
        comment = NewsComment.objects.create(content=content, news=news, commentator=commentator)
        comment_serialize = NewsCommentSerializer(comment)
        return restful.ok(data=comment_serialize.data)
    else:
        return restful.parameter_error(form.get_error())

