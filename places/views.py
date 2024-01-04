import json
import geojson
from django.shortcuts import render

from where_to_go.settings import BASE_DIR
from .models import Place


def to_geojson(places):
    features = []
    for place in places:
        point = geojson.Point(tuple(map(float, place.coordinates.values())))
        detailsUrl = {
            'title': place.title,
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': place.coordinates,
            # 'imgs': [request.build_absolute_uri(img.image.url) for img in place.imgs.all()],
            'imgs': [img.url for img in place.imgs.all()],
        }
        place_properties = {
            'title': place.title,
            'placeId': f'place_{place.id}',
            'detailsUrl': detailsUrl,
        }
        feature = geojson.Feature(geometry=point, properties=place_properties)
        features.append(feature)
    geojson_data = geojson.FeatureCollection(features)
    return geojson_data


def to_geojson2(places):
    place = places[0]
    detailsUrl1 = {
        'title': place.title,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': place.coordinates,
        'imgs': [img.url for img in place.imgs.all()],
    }

    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [37.62, 55.793676]
                },
                "properties": {
                    "title": "«Легенды Москвы",
                    "placeId": "moscow_legends",
                    "detailsUrl": detailsUrl1
                    # "detailsUrl": "http://127.0.0.1:8000/static/places/moscow_legends.json"
                }
            },
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [37.64, 55.753676]
                },
                "properties": {
                    "title": "Крыши24.рф",
                    "placeId": "roofs24",
                    "detailsUrl": detailsUrl1,
                    # "detailsUrl": "http://127.0.0.1:8000/static/places/moscow_legends.json",
                }
            }
        ]
    }

    return feature_collection


def index(request):
    places = Place.objects.all()
    feature_collection = to_geojson2(places)
    return render(request, 'index.html', {'data': feature_collection})
