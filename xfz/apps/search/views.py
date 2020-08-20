from django.shortcuts import render
from ..news.models import NewsPub
from django.db.models import Q
from urllib import parse


def search_index(request):
    hot_recommends = NewsPub.objects.order_by('-pub_time').select_related('category')[:1]
    if request.GET.get('keywords'):
        keywords = request.GET.get('keywords')
        split_keywords = keywords.split(' ')
        split_keywords = set(split_keywords)
        queryargs = [Q(content__icontains=i) for i in split_keywords]
        news_objects = NewsPub.objects.select_related('author', 'category').filter(*queryargs)
        if news_objects:
            context = {
                'hotrecommends': hot_recommends,
                'searched': 1,
                'newslists': news_objects,
                'keywords': keywords,
                'query_url': '&' + parse.urlencode({
                    'keywords': keywords
                })
            }
        else:
            context = {
                'searched': 1,
                'newslists': None,
                'hotrecommends': hot_recommends,
                'keywords': keywords,
                'query_url': '&' + parse.urlencode({
                    'keywords': keywords
                })
            }
        return render(request, 'search/search.html', context=context)
    else:
        news_objects = NewsPub.objects.select_related('author', 'category').order_by('-pub_time')[:2]
        context = {
            'hotrecommends': hot_recommends,
            'newslists2': news_objects
        }
        return render(request, 'search/search.html', context=context)
