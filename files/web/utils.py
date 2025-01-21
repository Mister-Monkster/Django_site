from django.core.paginator import Paginator

from .models import *


mainmenu = [{'title': 'Главная', 'urlname': '/main'},
            {'title': 'О сайте', 'urlname': '/about'},
            {'title': 'Контакты', 'urlname': '/contacts'}]


class DataMixin:
    paginate_by = 5

    def get_user_context(self, **kwargs):
        context = kwargs
        posts = Posts.objects.all()
        category = Category.objects.all().order_by('pk')
        context['menu'] = mainmenu
        context['category'] = category
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
        return context