from django.shortcuts import render
# from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Place


def index(request):
    data = serialize("json", Place.objects.all(), geometry_field='point', fields=('name',))
    return render(request, 'index.html', {'json_data': data})

