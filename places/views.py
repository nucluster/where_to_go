import geojson
from geojson import Point, Feature, FeatureCollection
from django.shortcuts import render
from django.forms.models import model_to_dict
# from django.http import JsonResponse
# from django.core.serializers import serialize
from .models import Place


def to_geojson(places):
    features = []
    for place in places:
        point = Point(tuple(map(float, place.coordinates.values())))
        feature = Feature(geometry=point, properties=model_to_dict(place, fields=['title', 'coordinates']))
        features.append(feature)
    geojson_data = geojson.dumps(FeatureCollection(features))
    return geojson_data


def index(request):
    places = Place.objects.all()
    data = to_geojson(places)
    return render(request, 'index.html', {'json_data': data})
