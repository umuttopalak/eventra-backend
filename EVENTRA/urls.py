from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/admin', admin.site.urls),
    path('api/authentication/', include('authentication.urls')),
    path('api/locations/', include('location.urls'))
]
