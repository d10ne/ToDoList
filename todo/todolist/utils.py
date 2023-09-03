from django.db.models import Count

from .models import *
from django.core.cache import cache

menu = [{'title': "Добавить статью", 'url_name': 'add'},
        {'title': "Обратная связь", 'url_name': 'home'},
        ]


class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        context = kwargs
        task = cache.get('title')
        if not task:
            task = Task.objects.annotate(Count('title'))
            cache.set('title', task, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        return context
