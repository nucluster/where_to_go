import json

import geojson
from django.shortcuts import render
from .models import Place


def to_geojson(places, request):
    features = []
    for place in places:
        point = geojson.Point(tuple(map(float, place.coordinates.values())))
        place_properties = {
            'title': place.title,
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': place.coordinates,
            'imgs': [request.build_absolute_uri(img.image.url) for img in place.imgs.all()],
        }
        feature = geojson.Feature(geometry=point, properties=place_properties)
        features.append(feature)
    geojson_data = geojson.dumps(geojson.FeatureCollection(features))
    return geojson_data


def index(request):
    places = Place.objects.all()
    data = to_geojson(places, request)
    serialized_json = json.dumps(data)
    print(data)
    print(serialized_json)
    return render(request, 'index.html', {'json_data': data})
