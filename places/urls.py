
from django.urls import path, include

from places.views import get_place_by_id

app_name = 'places'

urlpatterns = [
    path('<int:pk>/', get_place_by_id, name='detail'),
]