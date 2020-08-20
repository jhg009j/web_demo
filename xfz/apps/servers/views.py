from django.shortcuts import render
from ..news.models import NewsPub


def pay_info(request):
    hot_recommends = NewsPub.objects.order_by('-pub_time').select_related('category')[:1]
    context = {
        'hotrecommends':hot_recommends,
    }
    return render(request, 'servers/payinfo.html', context=context)
