from django.urls import path, include


urlpatterns = [
    path('properties/', include('apps.properties.urls')),
    path('users/', include('apps.users.urls')),
    path('bookings/', include('apps.bookings.urls'))
]
