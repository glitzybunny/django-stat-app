from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse

from core import models

import datetime

"""
Требования к выполнению

Back-end: Python 3, Django 1.11, MySQL и предпочтительно DRF.
Front-end: должно быть общение с беком через АПИ.

Проект можно задеплоить на Heroku (либо другой платформе).
После выполнения предоставь линк на гитхаб и сайт.
Подсказка: используй преимущества Django ORM; будь внимателен к деталям;
предположим, это хайлоад проект.
"""

# /


class indexView(View):

    def get(self, *args, **kwargs):
        ctx = {}
        return render(self.request, 'index.html', ctx)


# /users/id
class userProfileView(View):
    def get(self, *args, **kwargs):
        ctx = {}
        return render(self.request, 'user.html', ctx)

# Returns JSON for Charts on User page


def get_chart_data(request):
    print(request.GET)
    try:
        uid = request.GET.get('uid')
        start = request.GET.get('start')
        end = request.GET.get('end')
        chart = request.GET.get('chart')

        queryset = models.get_UID_stat(uid, start, end)
        labels, values = models.querysetToChartData(
            queryset, (start, end), chart)

    except AttributeError as err:
        return JsonResponse({'message': 'Error'})

    # Data for Chart JS
    data = {
        'labels': labels,
        'values': values,
    }

    return JsonResponse(data)
