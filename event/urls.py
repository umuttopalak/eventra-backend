from django.urls import path

from .api import (EventAPI, EventDetailAPI, JoinEventAPI, LeaveEventAPI,
                  PublicEventAPI)

urlpatterns = [
    path('/', PublicEventAPI.as_view(), name='public-event-list'),

    path('user/', EventAPI.as_view(), name='event-list-create'),
    path('user/<int:pk>/', EventDetailAPI.as_view(), name='event-detail'),

    path('user/<int:pk>/join/', JoinEventAPI.as_view(), name='event-join'),
    path('user/<int:pk>/leave/', LeaveEventAPI.as_view(), name='event-leave'),
]
