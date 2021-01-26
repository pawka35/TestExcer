from django.shortcuts import render
from .models import Posts, Users
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


def find_user(request):
    """
    Метод отжающий json c информацией по конретному ползователю (внесем немного ajax в этот проект)
    """
    if request.method == 'POST':  # если получили POST запрос
        need_user = json.load(request)['need_user']  # получаем информацию о том, какого пользователя зпрашивают
        # выбираем из таблиц Users, Company,Address информацию,связанную с запрашиваем пользователем
        data_from_db = Users.objects.filter(name=need_user).select_related('company', 'address')
        answer = []
        for x in data_from_db:  # формируем ответ (выглядит как костыль, но по другому не получилось)
            answer.append({
                'name': x.name,
                'username': x.username,
                'email': x.email,
                'phone': x.phone,
                'website': x.website,
                'company': {
                    'name': x.company.name,
                    'catchPhrase': x.company.catchphrase,
                    'bs': x.company.bs
                    },
                'address': {
                    'zipcode': x.address.zipcode,
                    'city': x.address.city,
                    'street': x.address.street,
                    'suite': x.address.suite,
                    'geo': {'lat': x.address.geo.lat, 'lng': x.address.geo.lng}
                    }
            })
        return HttpResponse(json.dumps(answer), content_type='application/json')


def index(request, user_name=None):
    """
    Метод отдающий представление с постами
    :param request: запрос
    :param user_name: имя пользователя
    """
    single_user = False  # флаг того, что нам нужны данные конкретного пользователя
    if user_name:  # если в запросе получили имя пользователя, то выбираем его посты
        blog_list = Posts.objects.raw(f'select * from Posts ps join Users us on ps.userId=us.id '
                                      f'where us.username = "Samantha"')
        single_user = True  # включаем флаг
    else:  # если пользователя не запрашивали, то выбираем все посты
        blog_list = Posts.objects.all()

    # далее стандартная работа с пагинатором(примеры из документации) и выдача информации в представления
    # выводим по 5 постов на странице
    page = request.GET.get('page', 1)
    paginator = Paginator(blog_list, 5)
    try:
        blog_list = paginator.page(page)
    except PageNotAnInteger:
        blog_list = paginator.page(1)
    except EmptyPage:
        blog_list = paginator.page(paginator.num_pages)
    return render(request, 'main/index.html', {'blog_list': blog_list,'single_user':single_user})




