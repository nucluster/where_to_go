import json
import geojson
from django.shortcuts import render

from where_to_go.settings import BASE_DIR, STATIC_URL
from .models import Place


def to_geojson(places, request):
    features = []
    for place in places:
        point = geojson.Point((place.longitude, place.latitude))
        details_url = {
            'title': place.title,
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': place.coordinates,
            'imgs': [request.build_absolute_uri(img.image.url) for img in
                     place.imgs.all()],
        }
        # Сохраняем в JSON detailsUrl
        with open(BASE_DIR/STATIC_URL/'places'/f'place_{place.id}.json', 'w') as json_file:
            json.dump(details_url, json_file, indent=2)
        place_properties = {
            'title': place.title,
            'placeId': place.slug,
            'detailsUrl': f'/static/places/place_{place.id}.json',
        }
        feature = geojson.Feature(geometry=point, properties=place_properties)
        features.append(feature)
    return geojson.FeatureCollection(features)


def index(request):
    places = Place.objects.all()
    data = to_geojson(places, request)
    return render(request, 'index.html', {'data': data})
