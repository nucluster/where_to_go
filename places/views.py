import geojson
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def to_geojson(places):
    features = []
    for place in places:
        point = geojson.Point((place.longitude, place.latitude))
        place_properties = {
            'title': place.title,
            'placeId': place.id,
            'detailsUrl': reverse('places:detail', args=[place.id]),
        }
        feature = geojson.Feature(geometry=point, properties=place_properties)
        features.append(feature)
    return geojson.FeatureCollection(features)


def index(request):
    places = Place.objects.all()
    data = to_geojson(places)
    return render(request, 'index.html', {'data': data})


def get_place_by_id(request, id):
    place = get_object_or_404(Place, id=id)
    details = {
        'title': place.title,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': place.coordinates,
        'imgs': [image.get_url for image in place.images.all()],
    }
    return JsonResponse(details, safe=False,
                        json_dumps_params={"ensure_ascii": False, "indent": 2})
