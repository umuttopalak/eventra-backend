from django.urls import path

from .api import LocationAPI, LocationDetailAPI

urlpatterns = [
    path('', LocationAPI.as_view(), name='location-list'),
    path('<int:pk>/', LocationDetailAPI.as_view(), name='location-detail'),
]
