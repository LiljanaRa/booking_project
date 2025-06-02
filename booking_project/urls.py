from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.users.views import DashboardView


schema_view = get_schema_view(
    openapi.Info(
        title='Property Booking Platform API',
        default_version='v1',
        description='API for managing rental properties, bookings, user reviews and search history.'
    ),
    public=False,
    permission_classes=[permissions.IsAdminUser]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.routers')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))
]
